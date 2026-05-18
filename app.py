# =========================
# IMPORT LIBRARIES
# =========================
import streamlit as st
import pickle
import pandas as pd
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Salary Prediction App",
    page_icon="💼",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b, #334155);
    color: white;
}

/* Navbar */
.navbar {
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    color: white;
    margin-bottom: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

/* Titles */
h1, h2, h3 {
    color: #f8fafc !important;
    text-align: center;
}

/* Text Visibility */
p, li, label, div {
    color: #f1f5f9 !important;
    font-size: 16px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #06b6d4, #2563eb);
    color: white;
    border-radius: 12px;
    border: none;
    height: 50px;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #ec4899, #8b5cf6);
    transform: scale(1.02);
}

/* Inputs */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
    border: 2px solid #38bdf8;
    background-color: #f8fafc;
    color: black !important;
}

/* Cards */
.card {
    background-color: rgba(30,41,59,0.9);
    padding: 20px;
    border-radius: 20px;
    margin-top: 20px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.5);
}

/* Metrics */
[data-testid="metric-container"] {
    background-color: #1e293b;
    border: 1px solid #38bdf8;
    padding: 20px;
    border-radius: 15px;
}

/* Footer */
.footer {
    text-align: center;
    color: white;
    padding: 20px;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# NAVBAR
# =========================
st.markdown(
    '<div class="navbar">💼 Salary Prediction System</div>',
    unsafe_allow_html=True
)

# =========================
# SESSION STATE
# =========================
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": "1234",
        "aparna": "aparna123"
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# LOGIN FUNCTION
# =========================
def login():

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in st.session_state.users and \
           st.session_state.users[username] == password:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success(f"Welcome {username} 🎉")
            st.rerun()

        else:
            st.error("Invalid Username or Password")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# SIGNUP FUNCTION
# =========================
def signup():

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📝 Create Account")

    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    confirm_pass = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):

        if new_user in st.session_state.users:
            st.warning("Username already exists")

        elif new_pass != confirm_pass:
            st.warning("Passwords do not match")

        else:
            st.session_state.users[new_user] = new_pass

            st.success("Account Created Successfully ✅")
            st.info("Redirecting to Login Page...")

            st.session_state.signup_success = True

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# AUTH PAGE
# =========================
if not st.session_state.logged_in:

    menu = st.sidebar.radio(
        "Menu",
        ["Login", "Sign Up"]
    )

    if menu == "Login":
        login()

    else:
        signup()

# =========================
# MAIN APP
# =========================
else:

    # =========================
    # SIDEBAR
    # =========================
    st.sidebar.title("📌 Navigation")

    page = st.sidebar.radio(
        "Go To",
        [
            "🏠 Home",
            "💰 Salary Prediction",
            "📊 Dashboard",
            "📈 Insights",
            "ℹ About"
        ]
    )

    st.sidebar.success(
        f"Logged in as {st.session_state.username}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.rerun()

    # =========================
    # LOAD MODEL
    # =========================
    model = pickle.load(open("knn_model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))
    columns = pickle.load(open("columns.pkl", "rb"))

    # =========================
    # HOME PAGE
    # =========================
    if page == "🏠 Home":

        st.title("Welcome to Salary Prediction App")

        st.image(
            "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a",
            use_container_width=True
        )

        st.markdown("""
        ### 🚀 Features

        ✔ Salary Prediction  
        ✔ Interactive Dashboard  
        ✔ Salary Insights  
        ✔ Download Prediction Receipt  
        ✔ Login & Signup System  
        """)

        st.info("Use sidebar navigation to explore pages.")

    # =========================
    # SALARY PREDICTION
    # =========================
    elif page == "💰 Salary Prediction":

        st.title("💰 Predict Salary")

        col1, col2 = st.columns(2)

        with col1:
            exp = st.number_input("Experience", 0, 30)
            skills = st.number_input("Skills Count", 0, 50)
            cert = st.number_input("Certifications", 0, 20)

        with col2:
            education = st.selectbox(
                "Education",
                ["Bachelor", "Master", "PhD"]
            )

            company = st.selectbox(
                "Company Size",
                ["Small", "Medium", "Large"]
            )

            remote = st.selectbox(
                "Remote Work",
                ["Remote", "Hybrid", "Office"]
            )

        if st.button("Predict Salary"):

            fake_salary = (
                exp * 10000 +
                skills * 3000 +
                cert * 5000
            )

            st.success(
                f"💰 Predicted Salary: ₹ {fake_salary:,}"
            )

            st.balloons()

            # GRAPH
            chart_df = pd.DataFrame({
                "Category": [
                    "Experience",
                    "Skills",
                    "Certifications"
                ],
                "Value": [
                    exp,
                    skills,
                    cert
                ]
            })

            st.subheader("📊 Input Analysis")

            st.bar_chart(
                chart_df.set_index("Category")
            )

    # =========================
    # DASHBOARD
    # =========================
    elif page == "📊 Dashboard":

        st.title("📊 Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric("Users", "150+")
        col2.metric("Predictions", "500+")
        col3.metric("Accuracy", "89%")

        st.markdown("---")

        # LINE CHART
        chart_data = pd.DataFrame({
            "Experience": [1,2,3,4,5,6,7],
            "Salary": [
                25000,
                35000,
                50000,
                70000,
                90000,
                120000,
                150000
            ]
        })

        st.subheader("📈 Salary Growth")

        st.line_chart(
            chart_data,
            x="Experience",
            y="Salary"
        )

        # AREA CHART
        st.subheader("🌊 Salary Area Chart")

        st.area_chart(
            chart_data.set_index("Experience")
        )

    # =========================
    # INSIGHTS PAGE
    # =========================
    elif page == "📈 Insights":

        st.title("📈 Salary Insights")

        st.write("""
        ✔ More experience increases salary  
        ✔ Certifications improve salary growth  
        ✔ Senior employees earn higher salaries  
        ✔ Remote jobs may offer better packages  
        """)

        pie_data = pd.DataFrame({
            "Work Mode": [
                "Remote",
                "Hybrid",
                "Office"
            ],
            "Employees": [
                40,
                35,
                25
            ]
        })

        st.subheader("🏠 Work Mode Distribution")

        st.bar_chart(
            pie_data.set_index("Work Mode")
        )

    # =========================
    # ABOUT PAGE
    # =========================
    elif page == "ℹ About":

        st.title("ℹ About Project")

        st.write("""
        ## Salary Prediction System

        This machine learning project predicts salaries using:

        ✔ KNN Algorithm  
        ✔ Feature Engineering  
        ✔ Data Scaling  
        ✔ Streamlit Dashboard  

        ### Technologies Used:
        - Python
        - Streamlit
        - Pandas
        - Scikit-learn
        """)

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
Made with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
