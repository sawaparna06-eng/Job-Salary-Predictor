# =========================
# IMPORT LIBRARIES
# =========================
import streamlit as st
import pickle
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Salary Prediction App", page_icon="💼")

# =========================
# SIMPLE USER DATABASE
# =========================
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": "1234"
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# =========================
# LOGIN / SIGNUP FUNCTIONS
# =========================
def login():
    st.subheader("🔐 Login")

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
# AUTHENTICATION PAGE
# =========================
if not st.session_state.logged_in:

    st.title("💼 Salary Prediction App")

    menu = st.sidebar.selectbox(
        "Menu",
        ["Login", "Sign Up"]
    )

    if menu == "Login":
        login()
    else:
        signup()

# =========================
# MAIN APP AFTER LOGIN
# =========================
else:

    # Logout Button
    st.sidebar.success(f"Logged in as {st.session_state.username}")

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
        opts = [col.replace(prefix, "") for col in columns if col.startswith(prefix)]
        opts = sorted(list(set(opts)))
        return opts

    # Extract all possible options
    job_options = get_options("job_title_")
    edu_options = get_options("education_level_")
    loc_options = get_options("location_")
    ind_options = get_options("industry_")
    company_options = get_options("company_size_")
    remote_options = get_options("remote_work_")

    # Add baseline category
    job_options = ["Other"] + job_options
    edu_options = ["Other"] + edu_options
    loc_options = ["Other"] + loc_options
    ind_options = ["Other"] + ind_options
    company_options = ["Other"] + company_options
    remote_options = ["Other"] + remote_options

    # =========================
    # TITLE
    # =========================
    st.title("💼 Salary Prediction App (KNN Improved)")

    # =========================
    # USER INPUT
    # =========================
    exp = st.number_input("Experience (years)", 0, 30)
    skills = st.number_input("Skills Count", 0, 50)
    cert = st.number_input("Certifications", 0, 20)

    job = st.selectbox("Job Role", job_options)
    edu = st.selectbox("Education", edu_options)
    loc = st.selectbox("Location", loc_options)
    ind = st.selectbox("Industry", ind_options)
    company = st.selectbox("Company Size", company_options)
    remote = st.selectbox("Remote Work", remote_options)

    # =========================
    # CREATE INPUT
    # =========================
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

    # =========================
    # FEATURE ENGINEERING
    # =========================
    input_df['exp_squared'] = input_df['experience_years'] ** 2

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

    # =========================
    # DUMMIES + ALIGN
    # =========================
    input_df = pd.get_dummies(input_df)

    input_df = input_df.reindex(
        columns=columns,
        fill_value=0
    )

    # =========================
    # SCALE
    # =========================
    num_cols = [
        'experience_years',
        'skills_count',
        'certifications',
        'exp_squared',
        'skill_per_exp',
        'cert_per_skill'
    ]

    input_df[num_cols] = scaler.transform(input_df[num_cols])

    # =========================
    # PREDICTION
    # =========================
    if st.button("Predict Salary"):

        prediction = model.predict(input_df)

        st.success(
            f"💰 Predicted Salary: ₹ {int(prediction[0]):,}"
        )

        st.balloons()
        # =========================
# PREDICTION + RECEIPT
# =========================
if st.button("Predict Salary"):

    prediction = model.predict(input_df)

    predicted_salary = int(prediction[0])

    st.success(
        f"💰 Predicted Salary: ₹ {predicted_salary:,}"
    )

    st.balloons()

    # =========================
    # RECEIPT SECTION
    # =========================
    st.markdown("---")
    st.subheader("🧾 Prediction Receipt")

    receipt_data = {
        "Field": [
            "Username",
            "Experience",
            "Skills Count",
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

    # =========================
    # DOWNLOAD RECEIPT
    # =========================
    csv = receipt_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇ Download Receipt",
        data=csv,
        file_name="salary_prediction_receipt.csv",
        mime="text/csv"
    )
