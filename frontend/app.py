import streamlit as st
import requests

st.set_page_config(
    page_title="FarmProfit",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 FarmProfit")
st.write("Welcome to Farmers Expenses Tracker")

menu = st.sidebar.selectbox(
    "Choose Module",
    [
        "Dashboard",
        "Farmer Profile",
        "Fields",
        "Plowing"
    ]
)

if menu == "Farmer Profile":

    st.header("👨‍🌾 Farmer Profile")

    name = st.text_input("Name")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120
    )

    mobile = st.text_input("Mobile")

    village = st.text_input("Village")

    if st.button("Save Profile"):

        farmer_data = {
            "name": name,
            "age": age,
            "mobile": mobile,
            "village": village
        }

        response = requests.post(
            "http://127.0.0.1:8000/farmers",
            json=farmer_data
        )

        if response.status_code == 200:
            st.success("Profile Saved Successfully")
        else:
            st.error("Failed to Save Profile")

if menu == "Fields":

    st.header("🌾 Add Field")

    field_name = st.text_input("Field Name")

    area_acres = st.number_input(
        "Area (Acres)",
        min_value=0.1,
        step=0.1
    )

    if st.button("Save Field"):

        field_data = {
            "farmer_id": 1,
            "field_name": field_name,
            "area_acres": area_acres
        }

        response = requests.post(
            "http://127.0.0.1:8000/fields",
            json=field_data
        )

        if response.status_code == 200:
            st.success("Field Added Successfully")
        else:
            st.error("Failed to Add Field ")


if menu == "Plowing":

    st.header("🚜 Plowing Entry")

    # Get all fields from FastAPI
    response = requests.get(
        "http://127.0.0.1:8000/fields"
    )

    fields = response.json()

    # Create dropdown options
    field_names = []

    for field in fields:
        field_names.append(field["field_name"])

    selected_field = st.selectbox(
        "Select Field",
        field_names
    )

    hours_worked = st.number_input(
    "Hours Worked",
    min_value=0.0,
    step=0.5,
    format="%.1f")

    rate_per_hour = st.number_input(
        "Rate Per Hour",
        min_value=0,
        step=100
    )

    remarks = st.text_input(
        "Remarks"
    )

    total_cost = hours_worked * rate_per_hour

    st.info(
        f"Total Plowing Cost: ₹{total_cost}"
    )

    if st.button("Save Plowing"):

        # Find field_id of selected field
        field_id = None

        for field in fields:

            if field["field_name"] == selected_field:

                field_id = field["field_id"]

        plowing_data = {
            "field_id": field_id,
            "plowing_date" : st.date_input("Plowing Date"),
            "hours_worked": hours_worked,
            "rate_per_hour": rate_per_hour,
            "remarks": remarks
        }

        response = requests.post(
            "http://127.0.0.1:8000/plowing",
            json=plowing_data
        )

        if response.status_code == 200:

            st.success(
                "Plowing Saved Successfully ✅"
            )

        else:

            st.error(
                "Failed to Save Plowing ❌"
            )


if menu == "Dashboard":

    st.header("📊 Farm Dashboard")

    response = requests.get(
        "http://127.0.0.1:8000/farmer-dashboard/1"
    )

    data = response.json()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🌾 Total Fields",
            data["total_fields"]
        )

    with col2:
        st.metric(
            "🚜 Plowing Records",
            data["total_plowing_records"]
        )

    with col3:
        st.metric(
            "💰 Total Expense",
            f"₹{data['total_plowing_expense']}"
        )

    st.divider()

    st.subheader(
        f"👨‍🌾 Farmer: {data['farmer_name']}"
    )