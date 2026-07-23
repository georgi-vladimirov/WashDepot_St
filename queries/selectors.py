import pandas as pd
from sqlalchemy import inspect as sa_inspect, select
from core.db import get_session
from core.models.base import T


class Selector:
    def __init__(self, model: type[T]):
        self.model = model

    def get_dataframe(self) -> pd.DataFrame:
        columns = [attr.key for attr in sa_inspect(self.model).mapper.column_attrs]
        with get_session() as session:
            rows = session.scalars(select(self.model)).all()
            data = pd.DataFrame([
                {k: v for k, v in row.__dict__.items() if not k.startswith("_")}
                for row in rows
            ], columns=columns)
        return data