import pandas as pd
import streamlit as st
from queries.setup_selectors import T, get_all, save_changes, to_dataframe


def setup_page_ui(model: type[T]) -> None:
    editor_key = f"editor_{model.__tablename__}"
    original_key = f"original_{model.__tablename__}"

    if original_key not in st.session_state:
        st.session_state[original_key] = to_dataframe(get_all(model))

    original_df: pd.DataFrame = st.session_state[original_key]

    edited_df: pd.DataFrame = st.data_editor(
        original_df,
        key=editor_key,
        num_rows="dynamic",
        hide_index=True,
    )

    if st.button("Save", key=f"save_{model.__tablename__}"):
        save_changes(model, original_df, edited_df)
        del st.session_state[original_key]  # force reload след запис
        st.rerun()
