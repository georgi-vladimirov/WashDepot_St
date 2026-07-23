import streamlit as st
from utils.ui_elements import DataTable
from core.models.core import VehicleType
from services.services import save_object, delete_by_id

with st.container(horizontal_alignment="center", width = 500):
    with st.form("new_vehicleType"):
        is_active = st.checkbox("Active", value=True)
        name = st.text_input("Name")
        submitted = st.form_submit_button("Save")

if submitted:
    vehicleType = VehicleType(is_active=is_active, name=name)
    save_object(vehicleType)
    st.success("Vehicle Type saved!")

table = DataTable(VehicleType, width="content").display()
st.button("Delete", on_click=delete_by_id, args=(VehicleType, table))