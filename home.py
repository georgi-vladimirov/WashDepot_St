from typing import Dict, List

import streamlit as st

from utils.i18n import language_selector, tr

st.set_page_config(page_title="Home", layout="wide")

_ = tr()

sales_page = st.Page("pages/01-sales_page.py", title=_("Sales"))
cashDesk_page = st.Page("pages/02-cashDesk_page.py", title=_("Cash Desk"))
expenses_page = st.Page("pages/03-expences_page.py", title=_("Expenses"))
salaries_page = st.Page("pages/04-salaries_page.py", title=_("Salaries"))
report_page = st.Page("pages/05-report_page.py", title=_("Reports"))

operations: List = [sales_page, cashDesk_page, expenses_page, salaries_page, report_page]

locations_page = st.Page("pages/setup/01-locations_page.py", title=_("Locations"))
vehicleType_page = st.Page("pages/setup/02-vehicleType_page.py", title=_("Vehicle Types"))
serviceTypes_page = st.Page("pages/setup/03-serviceTypes_page.py", title=_("Service Types"))
services_page = st.Page("pages/setup/04-services_page.py", title=_("Services"))
servicePrices_page = st.Page("pages/setup/05-servicePrices_page.py", title=_("Service Prices"))
vehicleBrands_page = st.Page("pages/setup/06-vehicleBrands_page.py", title=_("Vehicle Brands"))
employeePositions_page = st.Page("pages/setup/07-employeePositions_page.py", title=_("Employee Positions"))
employees_page = st.Page("pages/setup/08-employees_page.py", title=_("Employees"))
subscribers_page = st.Page("pages/setup/09-subscribers_page.py", title=_("Subscribers"))
calendarEvents_page = st.Page("pages/setup/10-calendarEvents_page.py", title=_("Calendar Events"))

setup: Dict = {_("Setup"): [
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

language_selector()

pg = st.navigation({"": operations, **setup}, position="top")
pg.run()
