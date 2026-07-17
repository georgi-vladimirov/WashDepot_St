from typing import TypeVar

import pandas as pd
from sqlalchemy import select, Sequence

from core.db import get_session
from core.models.base import BaseModel

T = TypeVar("T", bound=BaseModel)


def to_dataframe(data: Sequence) -> pd.DataFrame:
    return pd.DataFrame([item.__dict__ for item in data])


def get_all(model: type[T]):
    with get_session() as session:
        return session.scalars(select(model)).all()


def save_changes(model: type[T], original_df: pd.DataFrame, edited_df: pd.DataFrame) -> None:
    with get_session() as session:
        # UPDATE
        try:
            changed_idx = edited_df.compare(original_df).index.tolist()
            for _, row in edited_df.loc[changed_idx].iterrows():
                obj = session.get(model, int(row["id"]))
                if obj:
                    for col in edited_df.columns:
                        if col != "id":
                            setattr(obj, col, row[col])
        except ValueError:
            pass  # няма промени

        # INSERT
        new_rows = edited_df[edited_df["id"].isna()]
        for _, row in new_rows.iterrows():
            data = {k: v for k, v in row.items() if k != "id" and pd.notna(v)}
            session.add(model(**data))

        # DELETE
        deleted_ids = set(original_df["id"]) - set(edited_df["id"])
        for obj_id in deleted_ids:
            obj = session.get(model, int(obj_id))
            if obj:
                session.delete(obj)

        session.commit()
