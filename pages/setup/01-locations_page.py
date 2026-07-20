from utils.ui_elements import DataTable
from core.models.core import Location
from services.services import save_object
import streamlit as st


with st.container(horizontal_alignment="center", width = 500):
    with st.form("new_location"):
        name = st.text_input("Name")
        short_name = st.text_input("Short Name")
        submitted = st.form_submit_button("Save")

if submitted:
    location = Location(name=name, short_name=short_name)
    save_object(location)
    st.success("Location saved!")

table = DataTable(Location, width="content").display()
