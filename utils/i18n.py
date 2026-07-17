"""i18n via stdlib gettext.

- Translations live in locales/<lang>/LC_MESSAGES/messages.po (plain text).
- .po files are auto-compiled to .mo on startup (no Poedit/msgfmt needed).
- Language is stored in st.session_state["lang"]; default comes from the
  browser's Accept-Language header.

Usage:
    from utils.i18n import tr, language_selector
    _ = tr()
    st.title(_("Sales"))
"""

from __future__ import annotations

import gettext as _gettext
import re
from pathlib import Path

import streamlit as st

LOCALES_DIR = Path(__file__).resolve().parent.parent / "locales"
LANGUAGES = {"bg": "Български", "en": "English"}
DEFAULT_LANG = "bg"
DOMAIN = "messages"


def _compile() -> None:
    """Compile every .po newer than its .mo (or with a missing .mo)."""
    try:
        for po in LOCALES_DIR.glob(f"*/LC_MESSAGES/{DOMAIN}.po"):
            mo = po.with_suffix(".mo")
            if not mo.exists() or po.stat().st_mtime > mo.stat().st_mtime:
                _po_to_mo(po, mo)
    except OSError as exc:  # read-only fs etc. — keep the app running
        st.warning(f"i18n: could not compile translations: {exc}")


def _po_to_mo(po_path: Path, mo_path: Path) -> None:
    """Minimal .po -> .mo compiler (msgid/msgstr, incl. multiline strings)."""
    import struct

    catalog: dict[str, str] = {}
    msgid: list[str] | None = None
    msgstr: list[str] | None = None
    current: list[str] | None = None

    def flush() -> None:
        if msgid is not None and msgstr is not None:
            catalog["".join(msgid)] = "".join(msgstr)

    for raw in po_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("msgid "):
            flush()
            msgid = [_unquote(line[6:])]
            msgstr = None
            current = msgid
        elif line.startswith("msgstr "):
            msgstr = [_unquote(line[7:])]
            current = msgstr
        elif line.startswith('"') and current is not None:
            current.append(_unquote(line))
    flush()

    keys = sorted(catalog)
    ids = b""
    strs = b""
    offsets = []
    for k in keys:
        v = catalog[k]
        offsets.append((len(ids), len(k.encode()), len(strs), len(v.encode())))
        ids += k.encode() + b"\x00"
        strs += v.encode() + b"\x00"
    key_start = 7 * 4 + 16 * len(keys)
    val_start = key_start + len(ids)
    koffsets: list[int] = []
    voffsets: list[int] = []
    for o1, l1, o2, l2 in offsets:
        koffsets += [l1, o1 + key_start]
        voffsets += [l2, o2 + val_start]
    output = struct.pack(
        "Iiiiiii", 0x950412DE, 0, len(keys), 7 * 4, 7 * 4 + len(keys) * 8, 0, 0
    )
    output += struct.pack(f"{len(koffsets)}i", *koffsets)
    output += struct.pack(f"{len(voffsets)}i", *voffsets)
    output += ids + strs
    mo_path.write_bytes(output)


def _unquote(s: str) -> str:
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    return s.replace('\\n', '\n').replace('\\"', '"').replace("\\\\", "\\")


def _browser_lang() -> str:
    accept = st.context.headers.get("Accept-Language") or ""
    for code in re.findall(r"[a-zA-Z]{2}", accept):
        if code.lower() in LANGUAGES:
            return code.lower()
    return DEFAULT_LANG


def current_lang() -> str:
    if "lang" not in st.session_state:
        st.session_state["lang"] = _browser_lang()
    return st.session_state["lang"]


@st.cache_resource
def _translation(lang: str, mo_mtime: float) -> _gettext.NullTranslations:
    return _gettext.translation(
        DOMAIN, localedir=LOCALES_DIR, languages=[lang], fallback=True
    )


def tr():
    """Return the gettext function for the current language."""
    _compile()
    lang = current_lang()
    mo = LOCALES_DIR / lang / "LC_MESSAGES" / f"{DOMAIN}.mo"
    mtime = mo.stat().st_mtime if mo.exists() else 0.0
    return _translation(lang, mtime).gettext


def language_selector() -> None:
    """Render a language selector in the sidebar."""
    current_lang()  # ensure st.session_state["lang"] is initialized
    st.sidebar.selectbox(
        "Език / Language",
        list(LANGUAGES),
        format_func=LANGUAGES.get,
        key="lang",
    )
