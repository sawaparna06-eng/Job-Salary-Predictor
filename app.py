
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
    page_title="AI Salary Predictor",
    page_icon="💼",
    layout="wide"
)

# =========================
# LOAD FILES
# =========================
model = pickle.load(open("knn_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b, #111827);
    color: white;
    font-family: 'Poppins', sans-serif;
}

/* Top Navbar */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 70px;
    background: rgba(15, 23, 42, 0.95);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0px 40px;
    z-index: 999;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
}

.nav-title {
    font-size: 28px;
    font-weight: bold;
    color: #38bdf8;
}

.nav-links {
    display: flex;
    gap: 25px;
    margin-right: 70px;
}

.nav-links a {
    color: white;
    text-decoration: none;
    font-size: 17px;
    transition: 0.3s;
}

.nav-links a:hover {
    color: #38bdf8;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #1e293b);
    border-right: 1px solid rgba(255,255,255,0.1);
}

.sidebar-card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
}

.sidebar-card h3 {
    color: #38bdf8;
}

/* Main Container */
.main-container {
    margin-top: 100px;
    padding: 20px;
}

/* Prediction Card */
.prediction-card {
    background: rgba(255,255,255,0.08);
    padding: 35px;
    border-radius: 25px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0px 0px 25px rgba(0,0,0,0.3);
}

.prediction-card:hover {
    transform: translateY(-5px);
    transition: 0.4s;
}

/* Input Boxes */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
}

.stNumberInput input {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 10px !important;
}

/* Button */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #0ea5e9, #2563eb);
    color: white;
    font-size: 20px;
    font-weight: bold;
    border-radius: 14px;
    border: none;
    padding: 14px;
    transition: 0.4s;
}

.stButton > button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #2563eb, #0ea5e9);
}

/* Success Box */
.stSuccess {
    border-radius: 15px;
}

/* Footer */
.footer {
    text-align: center;
    padding: 20px;
    color: #94a3b8;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# NAVBAR
# =========================
st.markdown("""
<div class="navbar">
    <div class="nav-title">💼 AI Salary Predictor</div>

    <div class="nav-links">
        <a href="#">Home</a>
        <a href="#">Prediction</a>
        <a href="#">Analytics</a>
        <a href="#">About</a>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR USER INFO
# =========================
st.sidebar.markdown("## 👤 User Information")

st.sidebar.markdown("""
<div class="sidebar-card">
    <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="90">
    <h3>Welcome User</h3>
    <p>AI Salary Prediction Dashboard</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.info("📊 Predict salary using AI & Machine Learning")
st.sidebar.success("✅ Responsive UI Fixed")
st.sidebar.warning("⚡ Modern Navbar Added")

# =========================
# HELPER FUNCTION
# =========================
def get_options(prefix):
    opts = [col.replace(prefix, "") for col in columns if col.startswith(prefix)]
    return sorted(list(set(opts)))

job_options = ["Other"] + get_options("job_title_")
edu_options = ["Other"] + get_options("education_level_")
loc_options = ["Other"] + get_options("location_")
ind_options = ["Other"] + get_options("industry_")
company_options = ["Other"] + get_options("company_size_")
remote_options = ["Other"] + get_options("remote_work_")

# =========================
# MAIN PAGE
# =========================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center;color:#38bdf8;'>💰 Smart Salary Prediction System</h1>
<p style='text-align:center;color:#cbd5e1;font-size:18px;'>
Predict employee salaries using AI & Machine Learning with beautiful visualization.
</p>
""", unsafe_allow_html=True)

st.markdown('<div class="prediction-card">', unsafe_allow_html=True)

# =========================
# INPUTS
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    exp = st.number_input("Experience (Years)", 0, 30)
    job = st.selectbox("Job Role", job_options)
    company = st.selectbox("Company Size", company_options)

with col2:
    skills = st.number_input("Skills Count", 0, 50)
    edu = st.selectbox("Education", edu_options)
    remote = st.selectbox("Remote Work", remote_options)

with col3:
    cert = st.number_input("Certifications", 0, 20)
    loc = st.selectbox("Location", loc_options)
    ind = st.selectbox("Industry", ind_options)

# =========================
# INPUT DATAFRAME
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
input_df['skill_per_exp'] = input_df['skills_count'] / (input_df['experience_years'] + 1)
input_df['cert_per_skill'] = input_df['certifications'] / (input_df['skills_count'] + 1)

input_df['seniority'] = pd.cut(
    input_df['experience_years'],
    bins=[0, 2, 5, 10, 20],
    labels=['Fresher', 'Junior', 'Mid', 'Senior']
)

# =========================
# DUMMIES + ALIGN
# =========================
input_df = pd.get_dummies(input_df)
input_df = input_df.reindex(columns=columns, fill_value=0)

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
# PREDICTION BUTTON
# =========================
if st.button("🚀 Predict Salary"):

    prediction = model.predict(input_df)
    salary = int(prediction[0])

    st.success(f"💰 Predicted Salary: ₹ {salary:,}")

    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg,#0ea5e9,#2563eb);
        padding:25px;
        border-radius:20px;
        text-align:center;
        margin-top:20px;
        color:white;
        font-size:30px;
        font-weight:bold;
        box-shadow:0px 0px 20px rgba(37,99,235,0.5);
    ">
        Estimated Salary: ₹ {salary:,}
    </div>
    """, unsafe_allow_html=True)

    st.balloons()

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
    Made with ❤️ using Streamlit | AI Salary Prediction System
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

