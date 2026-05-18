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

     # =========================
# ALL INPUTS FOR SALARY PREDICTION
# =========================

st.title("💰 Salary Prediction")

col1, col2 = st.columns(2)

# =========================
# COLUMN 1
# =========================
with col1:

    exp = st.number_input(
        "Experience (Years)",
        min_value=0,
        max_value=40,
        value=1
    )

    skills = st.number_input(
        "Skills Count",
        min_value=0,
        max_value=50,
        value=1
    )

    cert = st.number_input(
        "Certifications",
        min_value=0,
        max_value=20,
        value=0
    )

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=65,
        value=22
    )

    education = st.selectbox(
        "Education Level",
        [
            "High School",
            "Diploma",
            "Bachelor",
            "Master",
            "PhD"
        ]
    )

# =========================
# COLUMN 2
# =========================
with col2:

    job = st.selectbox(
        "Job Role",
        [
            "Data Analyst",
            "Data Scientist",
            "Software Engineer",
            "Web Developer",
            "ML Engineer",
            "Manager",
            "HR",
            "Other"
        ]
    )

    industry = st.selectbox(
        "Industry",
        [
            "IT",
            "Finance",
            "Healthcare",
            "Education",
            "Manufacturing",
            "Retail",
            "Other"
        ]
    )

    location = st.selectbox(
        "Location",
        [
            "Delhi",
            "Mumbai",
            "Bangalore",
            "Hyderabad",
            "Pune",
            "Chennai",
            "Other"
        ]
    )

    company = st.selectbox(
        "Company Size",
        [
            "Small",
            "Medium",
            "Large"
        ]
    )

    remote = st.selectbox(
        "Remote Work",
        [
            "Remote",
            "Hybrid",
            "Office"
        ]
    )

# =========================
# EXTRA FEATURES
# =========================
st.markdown("---")

col3, col4 = st.columns(2)

with col3:

    performance = st.slider(
        "Performance Rating",
        1,
        10,
        5
    )

    projects = st.number_input(
        "Projects Completed",
        min_value=0,
        max_value=100,
        value=5
    )

with col4:

    overtime = st.selectbox(
        "Overtime",
        [
            "Yes",
            "No"
        ]
    )

    leadership = st.selectbox(
        "Leadership Role",
        [
            "Yes",
            "No"
        ]
    )

# =========================
# CREATE INPUT DATAFRAME
# =========================
input_dict = {

    "experience_years": exp,
    "skills_count": skills,
    "certifications": cert,
    "age": age,
    "performance_rating": performance,
    "projects_completed": projects,
    "education_level": education,
    "job_title": job,
    "industry": industry,
    "location": location,
    "company_size": company,
    "remote_work": remote,
    "overtime": overtime,
    "leadership_role": leadership
}

input_df = pd.DataFrame([input_dict])

# =========================
# FEATURE ENGINEERING
# =========================
input_df["exp_squared"] = (
    input_df["experience_years"] ** 2
)

input_df["skill_per_exp"] = (
    input_df["skills_count"] /
    (input_df["experience_years"] + 1)
)

input_df["cert_per_skill"] = (
    input_df["certifications"] /
    (input_df["skills_count"] + 1)
)

# =========================
# ONE HOT ENCODING
# =========================
input_df = pd.get_dummies(input_df)

# MATCH TRAINING COLUMNS
input_df = input_df.reindex(
    columns=columns,
    fill_value=0
)

# =========================
# SCALE NUMERICAL DATA
# =========================
num_cols = [

    "experience_years",
    "skills_count",
    "certifications",
    "age",
    "performance_rating",
    "projects_completed",
    "exp_squared",
    "skill_per_exp",
    "cert_per_skill"
]

input_df[num_cols] = scaler.transform(
    input_df[num_cols]
)

# =========================
# PREDICTION BUTTON
# =========================
if st.button("🚀 Predict Salary"):

    prediction = model.predict(input_df)

    predicted_salary = int(prediction[0])

    st.success(
        f"💰 Predicted Salary: ₹ {predicted_salary:,}"
    )

    st.balloons()

    # =========================
    # RESULT CHART
    # =========================
    graph_df = pd.DataFrame({

        "Factors": [
            "Experience",
            "Skills",
            "Certifications",
            "Projects"
        ],

        "Values": [
            exp,
            skills,
            cert,
            projects
        ]
    })

    st.subheader("📊 Employee Profile Analysis")

    st.bar_chart(
        graph_df.set_index("Factors")
    )

    # =========================
    # RECEIPT
    # =========================
    st.subheader("🧾 Prediction Summary")

    st.dataframe(input_df)

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
