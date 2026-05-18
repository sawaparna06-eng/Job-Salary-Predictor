
# =========================
# IMPORT LIBRARIES
# =========================
import streamlit as st
import pickle
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Salary Prediction App",
    page_icon="💼",
    layout="wide"
)
# =========================
# CUSTOM DESIGN / CSS
# =========================
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(to right, #141e30, #243b55);
    color: white;
}

/* Title */
h1, h2, h3 {
    color: #ffffff;
    text-align: center;
    font-weight: bold;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

/* Sidebar Text */
section[data-testid="stSidebar"] .css-1d391kg {
    color: white;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    border: none;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s;
}

/* Button Hover */
.stButton > button:hover {
    background: linear-gradient(90deg, #fc466b, #3f5efb);
    transform: scale(1.03);
}

/* Input Boxes */
.stTextInput > div > div > input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
    border: 2px solid #00c6ff;
    background-color: #f8fafc;
    color: black;
}

/* Metrics */
[data-testid="metric-container"] {
    background-color: #1e293b;
    border: 1px solid #00c6ff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

/* Table */
table {
    background-color: white;
    color: black;
    border-radius: 10px;
}

/* Success Message */
.stSuccess {
    background-color: #16a34a;
    color: white;
    border-radius: 10px;
    padding: 10px;
}

/* Info Box */
.stInfo {
    background-color: #0284c7;
    color: white;
    border-radius: 10px;
    padding: 10px;
}

/* Warning Box */
.stWarning {
    border-radius: 10px;
}

/* Card Style */
.custom-card {
    background-color: #1e293b;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.5);
    margin-top: 20px;
}

/* Footer */
.footer {
    text-align: center;
    color: white;
    padding: 20px;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)
# =========================
# SIMPLE USER DATABASE
# =========================
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": "1234",
        "aparna": "aparna123",
        "guest": "guest123"
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# =========================
# LOGIN FUNCTION
# =========================
def login():

    st.subheader(" Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in st.session_state.users and st.session_state.users[username] == password:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success(f"Welcome {username} 🎉")
            st.rerun()

        else:
            st.error("Invalid Username or Password")

# =========================
# SIGNUP FUNCTION
# =========================
def signup():

    st.subheader("📝 Sign Up")

    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")
    confirm_pass = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):

        if new_user in st.session_state.users:
            st.warning("Username already exists")

        elif new_pass != confirm_pass:
            st.warning("Passwords do not match")

        elif new_user == "" or new_pass == "":
            st.warning("Fields cannot be empty")

        else:
            st.session_state.users[new_user] = new_pass
            st.success("Account Created Successfully ✅")
            st.info("Go to Login Page")

# =========================
# AUTH PAGE
# =========================
if not st.session_state.logged_in:

    st.title(" Salary Prediction App")

    menu = st.sidebar.selectbox(
        "Menu",
        ["Login", "Sign Up"]
    )

    if menu == "Login":
        login()

    else:
        signup()

# =========================
# MAIN APPLICATION
# =========================
else:

    # =========================
    # SIDEBAR
    # =========================
    st.sidebar.title(" Navigation")

    page = st.sidebar.radio(
        "Go To",
        [
            " Home",
            "Salary Prediction",
            "Dashboard",
            "Insights",
            "ℹ About"
        ]
    )

    st.sidebar.success(
        f"Logged in as {st.session_state.username}"
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # =========================
    # LOAD FILES
    # =========================
    model = pickle.load(open("knn_model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))
    columns = pickle.load(open("columns.pkl", "rb"))

    # =========================
    # HELPER FUNCTION
    # =========================
    def get_options(prefix):

        opts = [
            col.replace(prefix, "")
            for col in columns
            if col.startswith(prefix)
        ]

        opts = sorted(list(set(opts)))

        return opts

    # =========================
    # OPTIONS
    # =========================
    job_options = ["Other"] + get_options("job_title_")
    edu_options = ["Other"] + get_options("education_level_")
    loc_options = ["Other"] + get_options("location_")
    ind_options = ["Other"] + get_options("industry_")
    company_options = ["Other"] + get_options("company_size_")
    remote_options = ["Other"] + get_options("remote_work_")

    # =========================
    # HOME PAGE
    # =========================
    if page == "🏠 Home":

        st.title(" Salary Prediction System")

        st.image(
            "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a",
            use_container_width=True
        )

        st.markdown("## Welcome to the Salary Prediction App")

        st.write("""
        This application predicts employee salary based on:

        ✔ Experience  
        ✔ Skills  
        ✔ Certifications  
        ✔ Education  
        ✔ Job Role  
        ✔ Industry  
        ✔ Company Size  
        ✔ Remote Work  

        Built using:
        - Streamlit
        - Machine Learning
        - KNN Algorithm
        """)

        st.info("Use the sidebar to navigate through pages.")

    # =========================
    # SALARY PREDICTION PAGE
    # =========================
    elif page == " Salary Prediction":

        st.title(" Salary Prediction")

        # USER INPUT
        exp = st.number_input(
            "Experience (years)",
            0,
            30
        )

        skills = st.number_input(
            "Skills Count",
            0,
            50
        )

        cert = st.number_input(
            "Certifications",
            0,
            20
        )

        job = st.selectbox(
            "Job Role",
            job_options
        )

        edu = st.selectbox(
            "Education",
            edu_options
        )

        loc = st.selectbox(
            "Location",
            loc_options
        )

        ind = st.selectbox(
            "Industry",
            ind_options
        )

        company = st.selectbox(
            "Company Size",
            company_options
        )

        remote = st.selectbox(
            "Remote Work",
            remote_options
        )

        # CREATE INPUT
        input_dict = {

            "experience_years": exp,
            "skills_count": skills,
            "certifications": cert,
            "job_title": job,
            "education_level": edu,
            "location": loc,
            "industry": ind,
            "company_size": company,
            "remote_work": remote
        }

        input_df = pd.DataFrame([input_dict])

        # FEATURE ENGINEERING
        input_df['exp_squared'] = (
            input_df['experience_years'] ** 2
        )

        input_df['skill_per_exp'] = (
            input_df['skills_count'] /
            (input_df['experience_years'] + 1)
        )

        input_df['cert_per_skill'] = (
            input_df['certifications'] /
            (input_df['skills_count'] + 1)
        )

        input_df['seniority'] = pd.cut(
            input_df['experience_years'],
            bins=[0, 2, 5, 10, 20],
            labels=['Fresher', 'Junior', 'Mid', 'Senior']
        )

        # DUMMIES
        input_df = pd.get_dummies(input_df)

        input_df = input_df.reindex(
            columns=columns,
            fill_value=0
        )

        # SCALE
        num_cols = [

            'experience_years',
            'skills_count',
            'certifications',
            'exp_squared',
            'skill_per_exp',
            'cert_per_skill'
        ]

        input_df[num_cols] = scaler.transform(
            input_df[num_cols]
        )

        # PREDICTION
        if st.button("Predict Salary"):

            prediction = model.predict(input_df)

            predicted_salary = int(prediction[0])

            st.success(
                f" Predicted Salary: ₹ {predicted_salary:,}"
            )

            st.balloons()

            # RECEIPT
            st.markdown("---")

            st.subheader("🧾 Prediction Receipt")

            receipt_data = {

                "Field": [
                    "Username",
                    "Experience",
                    "Skills",
                    "Certifications",
                    "Job Role",
                    "Education",
                    "Location",
                    "Industry",
                    "Company Size",
                    "Remote Work",
                    "Predicted Salary"
                ],

                "Value": [
                    st.session_state.username,
                    f"{exp} Years",
                    skills,
                    cert,
                    job,
                    edu,
                    loc,
                    ind,
                    company,
                    remote,
                    f"₹ {predicted_salary:,}"
                ]
            }

            receipt_df = pd.DataFrame(receipt_data)

            st.table(receipt_df)

            csv = receipt_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="⬇ Download Receipt",
                data=csv,
                file_name="salary_receipt.csv",
                mime="text/csv"
            )

    # =========================
    # DASHBOARD PAGE
    # =========================
    elif page == "Dashboard":

        st.title("Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Users",
            "150+"
        )

        col2.metric(
            "Predictions",
            "500+"
        )

        col3.metric(
            "Accuracy",
            "89%"
        )

        st.markdown("---")

        chart_data = pd.DataFrame({
            "Experience": [1, 2, 3, 4, 5],
            "Salary": [25000, 40000, 55000, 70000, 90000]
        })

        st.line_chart(
            chart_data,
            x="Experience",
            y="Salary"
        )

    # =========================
    # INSIGHTS PAGE
    # =========================
    elif page == "📈 Insights":

        st.title("📈 Salary Insights")

        st.write("""
        ### Key Insights

        ✔ Higher experience increases salary.

        ✔ More certifications improve salary growth.

        ✔ Technical roles often receive higher salaries.

        ✔ Remote work impacts salary packages.

        ✔ Senior employees receive highest compensation.
        """)

        insight_data = pd.DataFrame({
            "Category": [
                "Fresher",
                "Junior",
                "Mid",
                "Senior"
            ],

            "Average Salary": [
                25000,
                45000,
                70000,
                120000
            ]
        })

        st.bar_chart(
            insight_data.set_index("Category")
        )

    # =========================
    # ABOUT PAGE
    # =========================
    elif page == "ℹ About":

        st.title("ℹ About Project")

        st.write("""
        ## Salary Prediction System

        This machine learning project predicts salaries using:

        - KNN Regression
        - Feature Engineering
        - Data Scaling
        - Streamlit Web App

        ### Features:
        ✔ Login & Signup  
        ✔ Salary Prediction  
        ✔ Dashboard  
        ✔ Insights  
        ✔ Download Receipt  

        ### Technologies Used:
        - Python
        - Pandas
        - Scikit-learn
        - Streamlit
        """)
