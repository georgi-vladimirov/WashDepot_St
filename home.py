from typing import Dict, List

import streamlit as st

st.set_page_config(page_title="Home")

sales_page = st.Page("pages/01-sales_page.py", title="Sales")
cashDesk_page = st.Page("pages/02-cashDesk_page.py", title="Cash Desk")
expenses_page = st.Page("pages/03-expences_page.py", title="Expenses")
salaries_page = st.Page("pages/04-salaries_page.py", title="Salaries")
report_page = st.Page("pages/05-report_page.py", title="Reports")

operations: List = [sales_page, cashDesk_page, expenses_page, salaries_page, report_page]

locations_page = st.Page("pages/setup/01-locations_page.py", title="Locations")
vehicleType_page = st.Page("pages/setup/02-vehicleType_page.py", title="Vehicle Types")
serviceTypes_page = st.Page("pages/setup/03-serviceTypes_page.py", title="Service Types")
services_page = st.Page("pages/setup/04-services_page.py", title="Services")
servicePrices_page = st.Page("pages/setup/05-servicePrices_page.py", title="Service Prices")
vehicleBrands_page = st.Page("pages/setup/06-vehicleBrands_page.py", title="Vehicle Brands")
employeePositions_page = st.Page("pages/setup/07-employeePositions_page.py", title="Employee Positions")
employees_page = st.Page("pages/setup/08-employees_page.py", title="Employees")
subscribers_page = st.Page("pages/setup/09-subscribers_page.py", title="Subscribers")
calendarEvents_page = st.Page("pages/setup/10-calendarEvents_page.py", title="Calendar Events")

setup: Dict = {"Setup": [
    locations_page,
    vehicleType_page,
    serviceTypes_page,
    services_page,
    servicePrices_page,
    vehicleBrands_page,
    employeePositions_page,
    employees_page,
    subscribers_page,
    calendarEvents_page,
]}

pg = st.navigation({"": operations, **setup}, position="top")
pg.run()
