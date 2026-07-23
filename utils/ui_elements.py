from typing import Any
import streamlit as st
from queries.selectors import Selector
from core.models.base import T


class DataTable:
    def __init__(self, model: type[T], **kwargs):
        self.model = model
        self.data = Selector(model).get_dataframe()
        self.column_config = self._build_column_config()
        self.kwargs = kwargs

    def _build_column_config(self) -> dict[str, Any]:
        return {
            col_key: st.column_config.Column(col_info.get("label", col_key))
            for col_key, col_info in self.model.col_info().items()
        }

    def display(self) -> list:
        key = f"data_table_{self.model.__tablename__}"
        st.dataframe(
            self.data,
            key=key,
            on_select="rerun",
            selection_mode="multi-row",
            column_config=self.column_config,
            **self.kwargs,
        )
        selected_rows = st.session_state[key]["selection"]["rows"]
        selected_rows = [i for i in selected_rows if i < len(self.data)]
        selected_ids = self.data.iloc[selected_rows]["id"].tolist()
        return selected_ids
