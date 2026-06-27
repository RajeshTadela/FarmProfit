import streamlit as st
import time
import requests
from datetime import date
# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="FarmProfit",
    page_icon="🌾",
    layout="centered"
)

# ----------------------------------
# SESSION STATE
# ----------------------------------

if "page" not in st.session_state:
    st.session_state.page = "splash"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "farmer_id" not in st.session_state:
    st.session_state.farmer_id = None
# ----------------------------------
# SPLASH SCREEN
# ----------------------------------

if st.session_state.page == "splash":

    st.markdown(
        """
        <h1 style='text-align:center;'>
        🌾 FarmProfit
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h3 style='text-align:center;'>
        Farm Expense Management System
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown(
        """
        <p style='text-align:center;'>
        Track every rupee from seed to harvest 🚜
        </p>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    st.markdown(
    """
    <h4 style='text-align:center;'>
    LOADING...
    </h4>
    """,
    unsafe_allow_html=True
)

    progress_bar = st.progress(0)

    for i in range(100):
        time.sleep(0.02)
        progress_bar.progress(i + 1)

    st.session_state.page = "login"
    st.rerun()

# ----------------------------------
# LOGIN PAGE
# ----------------------------------

elif st.session_state.page == "login":

    # response = requests.get(
    # f"https://farmprofit.onrender.com/farmer/{st.session_state.farmer_id}")

    # farmer = response.json()
    st.title("🔐 Login")

    username = st.text_input(
    "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    st.write("")

    if st.button(
    "LOGIN",
    width="stretch"
):

        login_data = {
            "username": username,
            "password": password
        }

        response = requests.post(
            "https://farmprofit.onrender.com/login",
            json=login_data
        )

        result = response.json()

        if result["success"]:

            st.session_state.logged_in = True

            st.session_state.farmer_id = result["farmer_id"]

            st.session_state.page = "dashboard"

            st.rerun()

        else:

            st.error(
                result["message"]
            )

    st.write("")
    st.write("")
    st.write("---")

    st.markdown(
        """
        <div style='text-align:center;'>
            Don't have an account?
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Register Now",
        width="stretch"
    ):
        st.session_state.page = "register"
        st.rerun()
# ----------------------------------
# REGISTER PAGE
# ----------------------------------


elif st.session_state.page == "register":

    st.title("📝 Create Account")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button(
    "Create Account",
    width="stretch"
    ):

        # Empty username
        if username.strip() == "":
            st.error(
                "Username cannot be empty"
            )

        # Username length
        elif len(username) < 6:
            st.error(
                "Username must be at least 6 characters"
            )

        # Empty password
        elif password.strip() == "":
            st.error(
                "Password cannot be empty"
            )

        # Password mismatch
        elif password != confirm_password:
            st.error(
                "Passwords do not match"
            )

        else:

            register_data = {
                "username": username,
                "password": password
            }

            response = requests.post(
                "https://farmprofit.onrender.com/register",
                json=register_data
            )

            result = response.json()

            if result["success"]:

                st.success(
                    "✅ Account Created Successfully"
                )

                st.balloons()

            else:

                st.error(
                    result["message"]
                )

        st.write("")
        st.write("---")

    if st.button(
        "Back To Login",
        width="stretch"
    ):
        st.session_state.page = "login"
        st.rerun()

# ----------------------------------
# DASHBOARD
# ----------------------------------

elif st.session_state.page == "dashboard":

    response = requests.get(
        f"https://farmprofit.onrender.com/farmer/{st.session_state.farmer_id}"
    )

    farmer = response.json()
    land_response = requests.get(
    f"https://farmprofit.onrender.com/total-land/{st.session_state.farmer_id}")

    land_data = land_response.json()
    col1, col2 = st.columns([5,1])

    with col1:
        st.title("🌾 FarmProfit")

    with col2:

        menu = st.selectbox(
    "Menu",
    [
        "    🤵",
        "👤 Profile",
        "🚪 Logout"
    ],
    label_visibility="collapsed"
)
    if menu == "👤 Profile":

        st.session_state.page = "profile"

        st.rerun()
    if menu == "🚪 Logout":

        st.session_state.logged_in = False

        st.session_state.farmer_id = None

        st.session_state.page = "login"

        st.rerun()

    st.write("---")

    if farmer["name"] is None:

        st.warning(
            "Please Complete Your Profile"
        )

        if st.button(
            "Create Profile",
            width="stretch"
        ):
            st.session_state.page = "profile"
            st.rerun()

    else:

        st.markdown(
            f"# 👨‍🌾 Welcome, {farmer['name']}"
        )

        st.write(
            f"📍 {farmer['village']}"
        )

        st.caption(
            f"🌾 Total Land : {land_data['total_land']} Acres"
        )

        fields_response = requests.get(
    f"https://farmprofit.onrender.com/farmer-fields/{st.session_state.farmer_id}"
        )

        fields = fields_response.json()

        st.write("---")

        st.subheader("🌾 My Fields")

        table_data = []

        for index, field in enumerate(
            fields,
            start=1
        ):

            table_data.append(
                {
                    "S.No": index,
                    "Field Name": field["field_name"],
                    "Area (Acres)": f"{field['area_acres']:.2f}"
                }
            )

        if len(table_data) > 0:

            import pandas as pd

            df = pd.DataFrame(table_data)

            st.dataframe(
                df,
                hide_index=True,
                width="stretch",
                column_config={
                "S.No": st.column_config.NumberColumn(
                    "S.No",
                    width="small"
                )}
            )

        else:

            st.info(
                "No Fields Added Yet"
            )

    st.markdown("""
        <style>

        div[data-testid="stExpander"] details summary p {
            font-size: 22px !important;
            font-weight: bold !important;
        }

        div[data-testid="stExpander"] {
            border-radius: 12px;
            margin-bottom: 10px;
        }

        </style>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>

        div[data-testid="stExpander"]{
            font-size:22px;
            margin-top:10px;
            margin-bottom:10px;
            border:2px solid #dcdcdc;
            border-radius:10px;
            padding:5px;
        }

        </style>
        """, unsafe_allow_html=True)
    st.write("---")

    st.header("🌾 Farm Operations")

    with st.expander(
    "🚜 Plowing",
    expanded=False
    ):

    # Fields

        fields_response = requests.get(
            f"https://farmprofit.onrender.com/farmer-fields/{st.session_state.farmer_id}"
        )

        fields = fields_response.json()

        field_options = {
            field["field_name"]: field["field_id"]
            for field in fields
        }

        selected_field = st.selectbox(
            "Select Field",
            list(field_options.keys())
        )

        # Drivers

        drivers_response = requests.get(
            f"https://farmprofit.onrender.com/drivers/{st.session_state.farmer_id}"
        )

        drivers = drivers_response.json()

        driver_options = {
            driver["driver_name"]: driver["driver_id"]
            for driver in drivers
        }

        col1, col2 = st.columns([5,1])

        with col1:

            selected_driver = st.selectbox(
                "Select Driver",
                list(driver_options.keys())
            )

        with col2:

            st.write("")
            st.write("")

            if st.button(
                "➕",
                key="add_driver"
            ):
                st.session_state.show_driver = True

        if st.session_state.get("show_driver", False):

            st.info("Add New Driver")

            new_driver = st.text_input(
                "Driver Name"
            )

            if st.button(
                "Save Driver",
                key="save_driver"
            ):

                driver_data = {

                    "farmer_id": st.session_state.farmer_id,

                    "driver_name": new_driver,

                    "mobile": ""
                }

                response = requests.post(
                    "https://farmprofit.onrender.com/driver",
                    json=driver_data
                )

                result = response.json()

                if result["success"]:

                    st.success("Driver Added")

                    st.session_state.show_driver = False

                    st.rerun()

        plowing_date = st.date_input(
            "Plowing Date"
        )

        hours_worked = st.number_input(
            "Hours Worked",
            min_value=0.0,
            step=0.5
        )
        today_plowings = st.number_input(
            "No. of Plowings Today",
            min_value=1,
            step=1
        )
        rate_per_hour = st.number_input(
            "Rate Per Hour",
            min_value=0.0
        )

        plowing_round = st.number_input(
            "Plowing Round",
            min_value=1,
            step=1
        )

        total_amount = (
            hours_worked
            * rate_per_hour
        )

        st.info(
            f"Total Amount = ₹{total_amount}"
        )

        if st.button(
        "Save Plowing",
        use_container_width=True
    ):

            plowing_data = {

                "field_id": field_options[selected_field],

                "driver_id": driver_options[selected_driver],

                "plowing_date": str(plowing_date),

                "hours_worked": hours_worked,

                "rate_per_hour": rate_per_hour,

                "today_plowings": today_plowings,

                "plowing_round": plowing_round

            }

            response = requests.post(
    "https://farmprofit.onrender.com/plowing",
    json=plowing_data
            )

            print("Status:", response.status_code)
            print("Response:", response.text)

            result = response.json()

            if result.get("success"):
                st.success("Plowing Saved Successfully")
            else:
                st.error(result)
        
        st.write("---")

        st.subheader("💰 Driver Payment")

        drivers_response = requests.get(
            f"https://farmprofit.onrender.com/drivers/{st.session_state.farmer_id}"
        )

        drivers = drivers_response.json()

        if len(drivers) == 0:

            st.warning("No drivers available.")

        else:

            driver_options = {
                d["driver_name"]: d
                for d in drivers
            }

            selected_driver = st.selectbox(
                "Select Driver",
                list(driver_options.keys()),
                key="payment_driver_select"
            )

            driver = driver_options[selected_driver]

            st.info(
                f"💰 Total Paid : ₹{driver['total_paid']}"
            )

            if driver["balance_amount"] == 0:

                st.success("✅ No Pending Balance")

            else:

                st.error(
                    f"Pending Balance : ₹{driver['balance_amount']}"
                )

            payment_amount = st.number_input(
                "Payment Amount",
                min_value=0.0,
                step=100.0,
                key="payment_amount"
            )

            if st.button(
                "💰 Pay Driver",
                use_container_width=True
            ):

                payment_data = {

                    "driver_id": driver["driver_id"],

                    "payment_date": str(date.today()),

                    "amount_paid": payment_amount
                }

                response = requests.post(
                    "https://farmprofit.onrender.com/driver-payment",
                    json=payment_data
                )

                result = response.json()

                if result["success"]:

                    st.success("Payment Saved Successfully")

                    st.rerun()

                else:

                    st.error("Payment Failed")
            
    with st.expander("🌱 Seeding"):
        pass

    with st.expander("🧪 Fertilizer"):
        pass

    with st.expander("💧 Irrigation"):
        pass

    with st.expander("☠️ Pesticide"):
        pass

    with st.expander("🌾 Harvesting"):
        pass

    st.write("---")

    st.header("📋 Records")

    with st.expander("🚜 Plowing Records"):

        response = requests.get(
            f"https://farmprofit.onrender.com/plowing-records/{st.session_state.farmer_id}"
        )

        records = response.json()

        if len(records) == 0:

            st.info("No Plowing Records")

        else:

            import pandas as pd

            df = pd.DataFrame(records)

            df.columns = [

                "Field",

                "Area",

                "Date",

                "Hours",

                "Driver",

                "Today's Plowings",

                "Amount (₹)"

            ]

            st.dataframe(
                df,
                hide_index=True,
                use_container_width=True
            )

    with st.expander("💰 Driver Payment Records"):

        response = requests.get(
            f"https://farmprofit.onrender.com/driver-payment-records/{st.session_state.farmer_id}"
        )

        records = response.json()

        if len(records) == 0:

            st.info("No Payments")

        else:

            import pandas as pd

            df = pd.DataFrame(records)

            st.dataframe(
                pd.DataFrame(records),
                hide_index=True,
                use_container_width=True
            )
# ----------------------------------
# PROFILE PAGE
# ----------------------------------

elif st.session_state.page == "profile":

    response = requests.get(
        f"https://farmprofit.onrender.com/farmer/{st.session_state.farmer_id}"
    )

    farmer = response.json()

    st.title("👤 Farmer Profile")

    name = st.text_input(
        "Farmer Name",
        value=farmer["name"] or ""
    )

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=farmer["age"] or 1
    )

    mobile = st.text_input(
        "Mobile Number",
        value=farmer["mobile"] or ""
    )

    village = st.text_input(
        "Village",
        value=farmer["village"] or ""
    )
    
    st.write("---")

    st.subheader("🌾 My Fields")

    fields_response = requests.get(
        f"https://farmprofit.onrender.com/farmer-fields/{st.session_state.farmer_id}"
    )

    fields = fields_response.json()

    for index, field in enumerate(
    fields,
    start=1
):

        st.write("---")

        st.markdown(
            f"### Field {index}"
        )

        st.write(
            f"Name : {field['field_name']}"
        )

        st.write(
            f"Area : {field['area_acres']} Acres"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
            "✏ Edit",
            key=f"edit_{field['field_id']}"):

                st.session_state.edit_field_id = (
                    field["field_id"]
                )

                st.session_state.edit_field_name = (
                    field["field_name"]
                )

                st.session_state.edit_field_area = (
                    field["area_acres"]
                )

        with col2:

            if st.button(
                "🗑 Delete",
                key=f"delete_{field['field_id']}"
            ):

                requests.delete(
                    f"https://farmprofit.onrender.com/field/{field['field_id']}"
                )

                st.success(
                    "Field Deleted"
                )

                st.rerun()
    
    if "edit_field_id" in st.session_state:

        st.write("---")

        st.subheader("✏ Edit Field")

        updated_name = st.text_input(
            "Field Name",
            value=st.session_state.edit_field_name
        )

        updated_area = st.number_input(
            "Area (Acres)",
            min_value=0.1,
            value=float(
                st.session_state.edit_field_area
            )
        )

        if st.button(
            "Update Field"
        ):

            update_data = {

                "farmer_id":
                st.session_state.farmer_id,

                "field_name":
                updated_name,

                "area_acres":
                updated_area
            }

            response = requests.put(
                f"https://farmprofit.onrender.com/field/{st.session_state.edit_field_id}",
                json=update_data
            )

            result = response.json()

            if result["success"]:

                st.success(
                    "Field Updated Successfully"
                )

                del st.session_state.edit_field_id

                st.rerun()

        # ----------------------------------
    # ADD FIELD
    # ----------------------------------

    if st.button(
        "➕ Add Field",
        width="stretch"
    ):
        st.session_state.show_add_field = True

    if st.session_state.get(
        "show_add_field",
        False
    ):

        st.write("---")

        new_field_name = st.text_input(
            "Field Name",
            key="new_field_name"
        )

        new_area = st.number_input(
            "Area (Acres)",
            min_value=0.01,
            step=0.01,
            format="%.2f"
        )

        if st.button(
            "Save Field",
            key="save_new_field"
        ):

            field_data = {
                "farmer_id":
                st.session_state.farmer_id,

                "field_name":
                new_field_name,

                "area_acres":
                new_area
            }

            response = requests.post(
                "https://farmprofit.onrender.com/fields",
                json=field_data
            )

            if response.status_code == 200:

                st.success(
                    "Field Added Successfully"
                )

                st.session_state.show_add_field = False

                st.rerun()

            else:

                st.error(
                    "Failed To Add Field"
                )
    if st.button(
    "Save Profile",
    width="stretch"
    ):

        profile_data = {
            "farmer_id": st.session_state.farmer_id,
            "name": name,
            "age": age,
            "mobile": mobile,
            "village": village
        }

        response = requests.put(
            "https://farmprofit.onrender.com/profile",
            json=profile_data
        )

        result = response.json()

        if result["success"]:

            st.success(
                "✅ Profile Saved Successfully"
            )

        else:

            st.error(
                "Failed To Save Profile"
            )
    if st.button(
        "⬅ Back To Dashboard",
        width="stretch"
    ):

        st.session_state.page = "dashboard"

        st.rerun()

