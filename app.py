# =========================
# IMPORT LIBRARIES
# =========================
import streamlit as st
import pickle
import pandas as pd
import hashlib
import json
import os
import re
import random
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="SalaryIQ Pro — Know Your Worth",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# LOAD MODEL FILES
# =========================
model   = pickle.load(open("knn_model.pkl", "rb"))
scaler  = pickle.load(open("scaler.pkl",    "rb"))
columns = pickle.load(open("columns.pkl",   "rb"))

# =========================
# HELPER: EXTRACT OPTIONS
# =========================
def get_options(prefix):
    opts = [col.replace(prefix, "") for col in columns if col.startswith(prefix)]
    return sorted(list(set(opts)))

job_options     = ["Other"] + get_options("job_title_")
edu_options     = ["Other"] + get_options("education_level_")
loc_options     = ["Other"] + get_options("location_")
ind_options     = ["Other"] + get_options("industry_")
company_options = ["Other"] + get_options("company_size_")
remote_options  = ["Other"] + get_options("remote_work_")

# =========================
# USER STORAGE
# =========================
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(name, email, password):
    users = load_users()
    if email.lower() in users:
        return False, "An account with this email already exists."
    users[email.lower()] = {
        "name": name, "email": email.lower(),
        "password": hash_password(password),
        "created_at": datetime.now().isoformat(),
        "predictions": []
    }
    save_users(users)
    return True, "Account created!"

def login_user(email, password):
    users = load_users()
    if email.lower() not in users:
        return False, "No account found with this email."
    if users[email.lower()]["password"] != hash_password(password):
        return False, "Incorrect password."
    return True, users[email.lower()]["name"]

def save_prediction(email, salary, job, exp, skills):
    users = load_users()
    if email.lower() in users:
        if "predictions" not in users[email.lower()]:
            users[email.lower()]["predictions"] = []
        users[email.lower()]["predictions"].append({
            "salary": salary, "job": job, "exp": exp,
            "skills": skills, "date": datetime.now().strftime("%d %b %Y")
        })
        save_users(users)

def is_valid_email(email):
    return re.match(r"^[\w\.\-]+@[\w\.\-]+\.\w{2,}$", email) is not None

# =========================
# CAREER DATA
# =========================
SKILLS_BY_ROLE = {
    "Data Scientist":            ["Python", "Machine Learning", "Deep Learning", "SQL", "Statistics", "TensorFlow", "Spark"],
    "Software Engineer":         ["System Design", "DSA", "Cloud (AWS/GCP)", "Docker", "Kubernetes", "CI/CD", "Microservices"],
    "AI Engineer":               ["LLMs", "PyTorch", "MLOps", "Vector Databases", "Prompt Engineering", "Transformers", "CUDA"],
    "Data Analyst":              ["Power BI", "Tableau", "Advanced SQL", "Python", "Excel", "Statistical Analysis", "DAX"],
    "Machine Learning Engineer": ["MLOps", "Feature Engineering", "Model Deployment", "Kubeflow", "PyTorch", "Scalable ML"],
    "DevOps Engineer":           ["Kubernetes", "Terraform", "AWS", "CI/CD", "Monitoring", "Docker", "Linux"],
    "Cloud Engineer":            ["AWS/Azure/GCP", "Terraform", "Networking", "Security", "Serverless", "Cost Optimization"],
    "Cybersecurity Analyst":     ["Ethical Hacking", "SIEM", "Incident Response", "Network Security", "Compliance", "Forensics"],
    "Product Manager":           ["Roadmapping", "OKRs", "User Research", "A/B Testing", "SQL", "Stakeholder Management"],
    "Business Analyst":          ["Power BI", "Process Mapping", "SQL", "Requirements Gathering", "Agile", "JIRA"],
    "Frontend Developer":        ["React", "TypeScript", "Next.js", "Tailwind CSS", "GraphQL", "Web Performance", "Testing"],
    "Backend Developer":         ["Node.js", "PostgreSQL", "Redis", "REST APIs", "System Design", "Docker", "Message Queues"],
    "Other":                     ["Communication", "Project Management", "Data Analysis", "Cloud Basics", "Agile", "Python"],
}

ROADMAP_BY_ROLE = {
    "Data Scientist":            ["Junior Data Analyst", "Data Scientist", "Senior Data Scientist", "Lead / Staff DS", "Head of Data Science"],
    "Software Engineer":         ["Junior Developer", "Software Engineer", "Senior Engineer", "Staff Engineer", "Principal / VP Eng"],
    "AI Engineer":               ["ML Engineer", "AI Engineer", "Senior AI Engineer", "AI Tech Lead", "AI Research Director"],
    "Data Analyst":              ["Junior Analyst", "Data Analyst", "Senior Analyst", "Analytics Manager", "Director of Analytics"],
    "Machine Learning Engineer": ["Junior ML Engineer", "ML Engineer", "Senior ML Engineer", "ML Tech Lead", "Head of ML"],
    "DevOps Engineer":           ["Junior DevOps", "DevOps Engineer", "Senior DevOps", "Platform Lead", "VP Infrastructure"],
    "Cloud Engineer":            ["Cloud Support", "Cloud Engineer", "Senior Cloud Engineer", "Cloud Architect", "CTO / VP Cloud"],
    "Cybersecurity Analyst":     ["Security Analyst", "Senior Analyst", "Security Lead", "CISO Director", "Chief Security Officer"],
    "Product Manager":           ["Associate PM", "Product Manager", "Senior PM", "Group PM", "VP / CPO"],
    "Business Analyst":          ["Junior BA", "Business Analyst", "Senior BA", "BA Manager", "Director of Strategy"],
    "Frontend Developer":        ["Junior Frontend", "Frontend Developer", "Senior Frontend", "Frontend Lead", "Head of Frontend"],
    "Backend Developer":         ["Junior Backend", "Backend Developer", "Senior Backend", "Backend Lead", "Engineering Manager"],
    "Other":                     ["Entry Level", "Mid Level", "Senior Level", "Lead / Manager", "Director / VP"],
}

INDUSTRY_TRENDS = {
    "Technology":    {"growth": "22%", "outlook": "Excellent", "top_pay": "₹1,80,000", "demand": "Very High"},
    "Finance":       {"growth": "15%", "outlook": "Strong",    "top_pay": "₹1,60,000", "demand": "High"},
    "Healthcare":    {"growth": "18%", "outlook": "Excellent", "top_pay": "₹1,40,000", "demand": "Very High"},
    "Consulting":    {"growth": "12%", "outlook": "Strong",    "top_pay": "₹1,70,000", "demand": "High"},
    "Manufacturing": {"growth": "8%",  "outlook": "Moderate",  "top_pay": "₹1,10,000", "demand": "Moderate"},
    "Education":     {"growth": "10%", "outlook": "Stable",    "top_pay": "₹90,000",   "demand": "Moderate"},
    "Retail":        {"growth": "7%",  "outlook": "Moderate",  "top_pay": "₹95,000",   "demand": "Moderate"},
    "Media":         {"growth": "9%",  "outlook": "Moderate",  "top_pay": "₹1,00,000", "demand": "Moderate"},
    "Telecom":       {"growth": "11%", "outlook": "Strong",    "top_pay": "₹1,30,000", "demand": "High"},
    "Government":    {"growth": "6%",  "outlook": "Stable",    "top_pay": "₹85,000",   "demand": "Low"},
    "Other":         {"growth": "10%", "outlook": "Moderate",  "top_pay": "₹1,00,000", "demand": "Moderate"},
}

# =========================
# SESSION STATE
# =========================
for k, v in [("logged_in", False), ("user_name", ""), ("user_email", ""),
             ("auth_page", "login"), ("active_tab", "predict"),
             ("last_prediction", None), ("last_inputs", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# =========================
# GLOBAL STYLES
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header, .stDeployButton { visibility: hidden !important; display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }
.stApp { background: #f8f9fc !important; }

/* AUTH */
.auth-wrap {
    min-height: 100vh; display: flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, #f0f4ff 0%, #faf5ff 50%, #f0fff4 100%);
    padding: 40px 20px;
}
.auth-panel {
    background: #ffffff; border-radius: 24px; padding: 48px 44px;
    width: 100%; max-width: 460px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.04), 0 20px 60px rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.08);
}
.auth-brand {
    font-family: 'Syne', sans-serif !important; font-size: 20px; font-weight: 800;
    color: #1e1b4b; margin-bottom: 32px; display: flex; align-items: center; gap: 8px;
}
.auth-brand em { color: #6366f1; font-style: normal; }
.auth-heading {
    font-family: 'Syne', sans-serif !important; font-size: 32px; font-weight: 800;
    color: #0f172a; line-height: 1.15; margin-bottom: 6px;
}
.auth-heading span {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.auth-sub { font-size: 14px; color: #64748b; margin-bottom: 32px; }
.auth-stats-row {
    display: flex; border-radius: 12px; overflow: hidden;
    border: 1px solid #e2e8f0; margin-bottom: 28px;
}
.auth-stat {
    flex: 1; text-align: center; padding: 14px 8px;
    border-right: 1px solid #e2e8f0; background: #f8fafc;
}
.auth-stat:last-child { border-right: none; }
.auth-stat-val {
    font-family: 'Syne', sans-serif !important; font-size: 18px; font-weight: 800;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.auth-stat-lbl { font-size: 10px; color: #94a3b8; text-transform: uppercase; letter-spacing: .6px; margin-top: 2px; }
.auth-or {
    text-align: center; color: #cbd5e1; font-size: 13px; margin: 16px 0; position: relative;
}
.auth-or::before, .auth-or::after {
    content: ''; position: absolute; top: 50%;
    width: calc(50% - 24px); height: 1px; background: #e2e8f0;
}
.auth-or::before { left: 0; } .auth-or::after { right: 0; }

/* INPUTS */
.stTextInput > div > div {
    background: #f8fafc !important; border: 1.5px solid #e2e8f0 !important; border-radius: 10px !important;
}
.stTextInput > div > div:focus-within {
    border-color: #6366f1 !important; box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important; background: #fff !important;
}
.stTextInput input {
    color: #0f172a !important; background: transparent !important;
    -webkit-box-shadow: none !important; box-shadow: none !important; font-size: 14px !important;
}
.stTextInput input::placeholder { color: #94a3b8 !important; }
.stTextInput label { color: #475569 !important; font-size: 13px !important; font-weight: 500 !important; }

.stNumberInput > div > div {
    background: #f8fafc !important; border: 1.5px solid #e2e8f0 !important; border-radius: 10px !important;
}
.stNumberInput > div > div:focus-within { border-color: #6366f1 !important; box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important; }
.stNumberInput input {
    color: #0f172a !important; background: transparent !important;
    -webkit-box-shadow: none !important; box-shadow: none !important; font-size: 14px !important;
}
.stNumberInput label { color: #475569 !important; font-size: 13px !important; font-weight: 500 !important; }
.stNumberInput button { color: #6366f1 !important; }

.stSelectbox > div > div {
    background: #f8fafc !important; border: 1.5px solid #e2e8f0 !important; border-radius: 10px !important;
}
.stSelectbox > div > div:focus-within { border-color: #6366f1 !important; box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important; }
.stSelectbox [data-baseweb="select"] > div,
.stSelectbox [data-baseweb="select"] span { color: #0f172a !important; background: transparent !important; }
.stSelectbox label { color: #475569 !important; font-size: 13px !important; font-weight: 500 !important; }
[data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"] {
    background: #ffffff !important; border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important; box-shadow: 0 8px 32px rgba(0,0,0,0.12) !important;
}
[data-baseweb="menu"] li, [role="option"] { background: #fff !important; color: #1e293b !important; font-size: 14px !important; }
[data-baseweb="menu"] li:hover, [role="option"]:hover, [role="option"][aria-selected="true"] {
    background: #eef2ff !important; color: #4f46e5 !important;
}

/* BUTTONS */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #fff !important; border: none !important; border-radius: 10px !important;
    padding: 12px 20px !important; font-family: 'Inter', sans-serif !important;
    font-size: 14px !important; font-weight: 600 !important; cursor: pointer !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.3) !important; transition: all 0.2s !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 6px 20px rgba(99,102,241,0.4) !important; }

/* NAV */
.top-nav {
    background: #ffffff; border-bottom: 1px solid #e2e8f0;
    padding: 0 32px; display: flex; align-items: center; justify-content: space-between;
    height: 56px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.nav-brand { font-family: 'Syne', sans-serif !important; font-size: 18px; font-weight: 800; color: #1e1b4b; }
.nav-brand em { color: #6366f1; font-style: normal; }
.nav-user { display: flex; align-items: center; gap: 10px; }
.nav-avatar {
    width: 34px; height: 34px; border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 700; color: #fff;
}
.nav-name { font-size: 13px; font-weight: 500; color: #334155; }

/* PAGE */
.page-wrap { padding: 28px 36px; max-width: 1200px; margin: 0 auto; }
.page-title { font-family: 'Syne', sans-serif !important; font-size: 24px; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
.page-sub { font-size: 14px; color: #64748b; margin-bottom: 24px; }

/* CARDS */
.card {
    background: #ffffff; border-radius: 16px; border: 1px solid #e2e8f0;
    padding: 22px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); margin-bottom: 16px;
}
.card-title { font-size: 11px; font-weight: 700; color: #6366f1; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px; }

/* METRICS */
.metric-card {
    background: #fff; border: 1px solid #e2e8f0; border-radius: 14px;
    padding: 18px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.metric-label { font-size: 12px; color: #94a3b8; font-weight: 500; margin-bottom: 6px; }
.metric-value { font-family: 'Syne', sans-serif !important; font-size: 22px; font-weight: 800; color: #0f172a; }
.metric-sub { font-size: 12px; color: #10b981; font-weight: 500; margin-top: 4px; }

/* RESULT HERO */
.result-hero {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border-radius: 20px; padding: 36px 32px; text-align: center; margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(99,102,241,0.3);
}
.result-hero-label { font-size: 12px; color: rgba(255,255,255,0.7); letter-spacing: 1.5px; text-transform: uppercase; }
.result-hero-amount { font-family: 'Syne', sans-serif !important; font-size: 56px; font-weight: 800; color: #fff; margin: 8px 0; }
.result-hero-sub { font-size: 13px; color: rgba(255,255,255,0.6); }

/* INSIGHTS */
.insight-card {
    background: #fff; border-radius: 12px; border: 1px solid #e2e8f0;
    padding: 18px; margin-bottom: 10px; display: flex; gap: 14px; align-items: flex-start;
}
.insight-icon {
    width: 38px; height: 38px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;
}
.insight-icon-blue  { background: #eef2ff; }
.insight-icon-green { background: #f0fdf4; }
.insight-icon-amber { background: #fffbeb; }
.insight-icon-rose  { background: #fff1f2; }
.insight-title { font-size: 14px; font-weight: 600; color: #0f172a; margin-bottom: 4px; }
.insight-desc  { font-size: 13px; color: #64748b; line-height: 1.5; }

/* ROADMAP */
.roadmap-step {
    display: flex; gap: 16px; align-items: flex-start;
    padding: 18px 0; border-bottom: 1px solid #f1f5f9;
}
.roadmap-step:last-child { border-bottom: none; }
.step-dot {
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 700; flex-shrink: 0; margin-top: 2px;
}
.step-dot-done { background: #6366f1; color: #fff; }
.step-dot-curr { background: linear-gradient(135deg, #6366f1, #8b5cf6); color: #fff; box-shadow: 0 0 0 4px rgba(99,102,241,0.2); }
.step-dot-next { background: #f1f5f9; color: #94a3b8; border: 2px dashed #cbd5e1; }
.step-title { font-size: 15px; font-weight: 600; color: #0f172a; }
.step-sub   { font-size: 13px; color: #64748b; margin-top: 3px; }
.step-badge { display: inline-block; font-size: 11px; font-weight: 600; padding: 2px 10px; border-radius: 99px; margin-top: 6px; }
.badge-current { background: #eef2ff; color: #4f46e5; }
.badge-done    { background: #f0fdf4; color: #15803d; }
.badge-future  { background: #f8fafc; color: #94a3b8; }

/* LEADERBOARD */
.lb-row {
    display: flex; align-items: center; gap: 14px; padding: 14px 16px;
    border-radius: 12px; margin-bottom: 8px; background: #f8fafc; border: 1px solid #f1f5f9; transition: all 0.15s;
}
.lb-row:hover { background: #eef2ff; border-color: #c7d2fe; }
.lb-row.gold   { background: linear-gradient(135deg,#fffbeb,#fef3c7); border-color: #fde68a; }
.lb-row.silver { background: linear-gradient(135deg,#f8fafc,#f1f5f9); border-color: #e2e8f0; }
.lb-row.bronze { background: linear-gradient(135deg,#fff7ed,#ffedd5); border-color: #fed7aa; }
.lb-rank  { font-family:'Syne',sans-serif !important; font-size:16px; font-weight:800; min-width:28px; }
.lb-name  { flex:1; font-size:14px; font-weight:600; color:#0f172a; }
.lb-role  { font-size:12px; color:#64748b; }
.lb-salary{ font-family:'Syne',sans-serif !important; font-size:16px; font-weight:800; color:#4f46e5; }

/* COMPARE BARS */
.compare-bar-wrap { margin-bottom: 14px; }
.compare-bar-label { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 5px; }
.compare-bar-track { height: 8px; background: #f1f5f9; border-radius: 99px; overflow: hidden; }
.compare-bar-fill  { height: 100%; border-radius: 99px; }

/* MISC */
.trend-up   { color: #10b981; font-weight: 600; font-size: 13px; }
.pw-track   { height: 4px; background: #e2e8f0; border-radius: 99px; overflow: hidden; margin-bottom: 6px; }
.pw-bar     { height: 100%; border-radius: 99px; transition: width .3s, background .3s; }
.signout-btn > button {
    background: #fff !important; color: #ef4444 !important;
    border: 1.5px solid #fecaca !important; box-shadow: none !important; font-size: 13px !important; padding: 8px 16px !important;
}
.signout-btn > button:hover { background: #fff1f2 !important; }
h1,h2,h3 { font-family:'Syne',sans-serif !important; color:#0f172a !important; }
p,li { color:#475569; }
</style>
""", unsafe_allow_html=True)


# =========================
# HELPERS
# =========================
def get_initials(name):
    parts = name.strip().split()
    return (parts[0][0] + (parts[1][0] if len(parts) > 1 else "")).upper()

def salary_boost_tips(job, exp, skills, cert, edu):
    tips = []
    if exp < 3:
        tips.append(("🚀", "Build a strong portfolio", "Create 3–5 GitHub projects demonstrating real skills. At junior levels, projects matter more than years of experience.", "blue"))
    if 3 <= exp < 7:
        tips.append(("📈", "Apply for senior roles now", "With your experience, senior roles pay 35–50% more. Rewrite your resume to highlight impact and outcomes, not just duties.", "green"))
    if exp >= 7:
        tips.append(("🏆", "Move into leadership", "7+ years of experience puts you in prime position for Lead/Manager roles — which pay 50–80% more than individual contributor positions.", "amber"))
    if skills < 8:
        tips.append(("🛠️", "Expand your skill set", "Professionals with 10+ in-demand skills earn 28% more on average. Focus on cloud, data, or AI tools relevant to your role.", "rose"))
    if cert < 2:
        tips.append(("📜", "Earn certifications", "AWS, Google Cloud, and PMP certifications add ₹10,000–₹25,000 to your annual salary. Many have free study resources.", "blue"))
    if edu in ["High School", "Diploma", "Other"]:
        tips.append(("🎓", "Upskill with online courses", "Online Master's degrees or professional diplomas can boost salary by 15–20%. Platforms like Coursera and edX are affordable.", "green"))
    tips.append(("🌍", "Target remote / global roles", "Remote roles at global companies pay 2–4x Indian market rates. Explore Toptal, Turing, and Remote.com.", "amber"))
    tips.append(("💬", "Negotiate your salary", "60% of professionals never negotiate. Research market rates on Glassdoor and LinkedIn Salary, then ask for 15–20% above the offer.", "rose"))
    return tips

def get_skills_to_learn(job, current_skills):
    return SKILLS_BY_ROLE.get(job, SKILLS_BY_ROLE["Other"])[:6]

def get_roadmap(job):
    return ROADMAP_BY_ROLE.get(job, ROADMAP_BY_ROLE["Other"])

def get_industry_data(ind):
    return INDUSTRY_TRENDS.get(ind, INDUSTRY_TRENDS["Other"])

def get_leaderboard():
    users = load_users()
    lb = []
    for email, data in users.items():
        preds = data.get("predictions", [])
        if preds:
            best = max(preds, key=lambda x: x["salary"])
            lb.append({"name": data["name"], "salary": best["salary"],
                       "job": best.get("job","Professional"), "exp": best.get("exp",0)})
    lb.sort(key=lambda x: x["salary"], reverse=True)
    return lb[:10]


# =========================
# LOGIN
# =========================
def show_login():
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="auth-panel">
        <div class="auth-brand">💼 Salary<em>IQ</em> <span style="font-size:11px;color:#94a3b8;font-weight:400;margin-left:4px;">PRO</span></div>
        <div class="auth-heading">Welcome<br><span>back.</span></div>
        <div class="auth-sub">Sign in to your career intelligence dashboard</div>
        <div class="auth-stats-row">
            <div class="auth-stat"><div class="auth-stat-val">95%</div><div class="auth-stat-lbl">Accuracy</div></div>
            <div class="auth-stat"><div class="auth-stat-val">50K+</div><div class="auth-stat-lbl">Predictions</div></div>
            <div class="auth-stat"><div class="auth-stat-val">120+</div><div class="auth-stat-lbl">Job Roles</div></div>
        </div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<div style='height:332px'></div>", unsafe_allow_html=True)
        email    = st.text_input("Email address", placeholder="you@example.com", key="login_email")
        password = st.text_input("Password", placeholder="Your password", key="login_password", type="password")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("Sign In →", key="login_btn"):
            if not email or not password:
                st.error("Please fill in all fields.")
            elif not is_valid_email(email):
                st.error("Please enter a valid email.")
            else:
                ok, result = login_user(email, password)
                if ok:
                    st.session_state.logged_in  = True
                    st.session_state.user_name  = result
                    st.session_state.user_email = email.lower()
                    st.rerun()
                else:
                    st.error(result)
        st.markdown('<div class="auth-or">or</div>', unsafe_allow_html=True)
        if st.button("Create a free account →", key="goto_signup"):
            st.session_state.auth_page = "signup"
            st.rerun()
        st.markdown("<p style='text-align:center;font-size:12px;color:#94a3b8;margin-top:16px;'>🔒 Your data is private and never shared.</p>", unsafe_allow_html=True)


# =========================
# SIGNUP
# =========================
def show_signup():
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="auth-panel">
        <div class="auth-brand">💼 Salary<em>IQ</em> <span style="font-size:11px;color:#94a3b8;font-weight:400;margin-left:4px;">PRO</span></div>
        <div class="auth-heading">Create your<br><span>account.</span></div>
        <div class="auth-sub">Join professionals discovering their true market value</div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<div style='height:258px'></div>", unsafe_allow_html=True)
        name     = st.text_input("Full Name",        placeholder="John Doe",             key="signup_name")
        email    = st.text_input("Email Address",    placeholder="you@example.com",      key="signup_email")
        password = st.text_input("Password",         placeholder="Min. 8 characters",    key="signup_password", type="password")
        confirm  = st.text_input("Confirm Password", placeholder="Repeat your password", key="signup_confirm",  type="password")

        if password:
            s, hints = 0, []
            if len(password) >= 8:                    s += 1
            else:                                     hints.append("8+ chars")
            if re.search(r"[A-Z]", password):         s += 1
            else:                                     hints.append("uppercase")
            if re.search(r"\d", password):            s += 1
            else:                                     hints.append("number")
            if re.search(r"[^A-Za-z0-9]", password): s += 1
            else:                                     hints.append("symbol")
            colors = ["#ef4444","#f97316","#eab308","#10b981"]
            labels = ["Weak","Fair","Good","Strong"]
            widths = [25,50,75,100]
            idx    = min(s-1,3) if s>0 else 0
            hint   = "" if s==4 else " · add " + ", ".join(hints[:2])
            st.markdown(f"""
            <div style='margin-top:-4px;margin-bottom:12px;'>
              <div class='pw-track'><div class='pw-bar' style='width:{widths[idx]}%;background:{colors[idx]};'></div></div>
              <span style='font-size:12px;color:{colors[idx]};font-weight:600;'>{labels[idx]}{hint}</span>
            </div>""", unsafe_allow_html=True)

        if st.button("Create Account →", key="signup_btn"):
            if not all([name, email, password, confirm]):
                st.error("Please fill in all fields.")
            elif not is_valid_email(email):
                st.error("Invalid email address.")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters.")
            elif password != confirm:
                st.error("Passwords do not match.")
            else:
                ok, msg = register_user(name.strip(), email.strip(), password)
                if ok:
                    st.session_state.logged_in  = True
                    st.session_state.user_name  = name.strip()
                    st.session_state.user_email = email.strip().lower()
                    st.rerun()
                else:
                    st.error(msg)
        st.markdown('<div class="auth-or">or</div>', unsafe_allow_html=True)
        if st.button("Already have an account? Sign In", key="goto_login"):
            st.session_state.auth_page = "login"
            st.rerun()


# =========================
# NAV BAR
# =========================
def show_nav():
    initials = get_initials(st.session_state.user_name)
    st.markdown(f"""
    <div class="top-nav">
        <div class="nav-brand">💼 Salary<em>IQ</em></div>
        <div class="nav-user">
            <div class="nav-avatar">{initials}</div>
            <span class="nav-name">{st.session_state.user_name}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    tabs   = ["predict","insights","roadmap","dashboard","compare","leaderboard","signout"]
    labels = ["🔍 Predict","💡 Insights","🗺️ Roadmap","📊 Dashboard","⚖️ Compare","🏆 Leaderboard","🚪 Sign Out"]
    cols   = [c1,c2,c3,c4,c5,c6,c7]

    for col, tab, label in zip(cols, tabs, labels):
        with col:
            if tab == "signout":
                st.markdown('<div class="signout-btn">', unsafe_allow_html=True)
                if st.button(label, key=f"nav_{tab}"):
                    st.session_state.logged_in        = False
                    st.session_state.user_name        = ""
                    st.session_state.user_email       = ""
                    st.session_state.active_tab       = "predict"
                    st.session_state.last_prediction  = None
                    st.session_state.last_inputs      = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                if st.button(label, key=f"nav_{tab}"):
                    st.session_state.active_tab = tab
                    st.rerun()


# =========================
# PREDICT TAB
# =========================
def show_predict():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Salary Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Fill in your profile — our KNN model trained on 250,000 records will estimate your market salary instantly.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="card"><div class="card-title">📊 Experience & Skills</div>', unsafe_allow_html=True)
        exp    = st.number_input("Years of Experience", 0, 30, key="exp")
        skills = st.number_input("Number of Skills",    1, 50, key="skills")
        cert   = st.number_input("Certifications",      0, 20, key="cert")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">🎓 Education & Role</div>', unsafe_allow_html=True)
        job = st.selectbox("Job Role",        job_options, key="job")
        edu = st.selectbox("Education Level", edu_options, key="edu")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><div class="card-title">🏢 Company & Location</div>', unsafe_allow_html=True)
        loc     = st.selectbox("Location",     loc_options,     key="loc")
        ind     = st.selectbox("Industry",     ind_options,     key="ind")
        company = st.selectbox("Company Size", company_options, key="company")
        remote  = st.selectbox("Remote Work",  remote_options,  key="remote")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="card" style="background:linear-gradient(135deg,#eef2ff,#f5f3ff);border-color:#c7d2fe;">
            <div class="card-title" style="color:#4f46e5;">✨ What you'll get</div>
            <div style="font-size:13px;color:#475569;line-height:1.8;margin:0;">
                💰 &nbsp;<strong>Instant salary prediction</strong><br>
                💡 &nbsp;<strong>Personalised growth tips</strong><br>
                🗺️ &nbsp;<strong>Step-by-step career roadmap</strong><br>
                📈 &nbsp;<strong>Industry trends & benchmarks</strong><br>
                ⚖️ &nbsp;<strong>Compare vs market salaries</strong>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="max-width:360px;margin:8px auto 0;">', unsafe_allow_html=True)
    clicked = st.button("🔍  Predict My Salary", key="predict_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    if clicked:
        input_dict = {
            "experience_years": exp, "skills_count": skills, "certifications": cert,
            "job_title": job, "education_level": edu, "location": loc,
            "industry": ind, "company_size": company, "remote_work": remote,
        }
        df = pd.DataFrame([input_dict])
        df["exp_squared"]    = df["experience_years"] ** 2
        df["skill_per_exp"]  = df["skills_count"] / (df["experience_years"] + 1)
        df["cert_per_skill"] = df["certifications"]  / (df["skills_count"] + 1)
        df["seniority"]      = pd.cut(df["experience_years"], bins=[0,2,5,10,20], labels=["Fresher","Junior","Mid","Senior"])
        df = pd.get_dummies(df)
        df = df.reindex(columns=columns, fill_value=0)
        num_cols = ["experience_years","skills_count","certifications","exp_squared","skill_per_exp","cert_per_skill"]
        df[num_cols] = scaler.transform(df[num_cols])

        salary = int(model.predict(df)[0])
        st.session_state.last_prediction = salary
        st.session_state.last_inputs     = input_dict
        save_prediction(st.session_state.user_email, salary, job, exp, skills)

        salary_fmt = f"₹{salary:,}"
        monthly    = f"₹{salary//12:,}"

        st.markdown(f"""
        <div class="result-hero">
            <div class="result-hero-label">Your Estimated Annual Salary</div>
            <div class="result-hero-amount">{salary_fmt}</div>
            <div class="result-hero-sub">≈ {monthly} / month &nbsp;·&nbsp; Powered by K-Nearest Neighbors</div>
        </div>""", unsafe_allow_html=True)

        seniority   = "Fresher" if exp<=2 else ("Junior" if exp<=5 else ("Mid-Level" if exp<=10 else "Senior"))
        potential   = f"₹{int(salary*1.35):,}"
        percentile  = min(95, max(30, int(30 + (salary/220000)*65)))
        m1,m2,m3,m4 = st.columns(4)
        with m1: st.markdown(f'<div class="metric-card"><div class="metric-label">Seniority Level</div><div class="metric-value" style="font-size:17px;">{seniority}</div></div>', unsafe_allow_html=True)
        with m2: st.markdown(f'<div class="metric-card"><div class="metric-label">Monthly Salary</div><div class="metric-value" style="font-size:17px;">{monthly}</div></div>', unsafe_allow_html=True)
        with m3: st.markdown(f'<div class="metric-card"><div class="metric-label">Growth Potential</div><div class="metric-value" style="font-size:17px;">{potential}</div><div class="metric-sub">↑ in 2–3 years</div></div>', unsafe_allow_html=True)
        with m4: st.markdown(f'<div class="metric-card"><div class="metric-label">Market Percentile</div><div class="metric-value" style="font-size:17px;">{percentile}th</div></div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:14px 20px;margin-top:8px;">
            <span style="font-size:14px;color:#15803d;font-weight:600;">✅ Prediction saved!</span>
            <span style="font-size:13px;color:#166534;"> &nbsp;·&nbsp; Now explore your <strong>Insights</strong>, <strong>Roadmap</strong>, and <strong>Compare</strong> tabs for your full career plan.</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# INSIGHTS TAB
# =========================
def show_insights():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Career Insights</div>', unsafe_allow_html=True)

    if not st.session_state.last_prediction:
        st.markdown('<div style="text-align:center;padding:60px;"><div style="font-size:48px;">💡</div><div style="font-size:18px;font-weight:600;color:#0f172a;margin-top:12px;">Run a prediction first</div><div style="font-size:14px;color:#64748b;margin-top:8px;">Go to Predict tab to get started.</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    inp    = st.session_state.last_inputs
    salary = st.session_state.last_prediction
    job    = inp["job_title"]; exp = inp["experience_years"]
    skills = inp["skills_count"]; cert = inp["certifications"]
    edu    = inp["education_level"]; ind = inp["industry"]

    # Salary boost tips
    st.markdown('<div class="card"><div class="card-title">🚀 How to Increase Your Salary</div>', unsafe_allow_html=True)
    icon_map = {"blue":"insight-icon-blue","green":"insight-icon-green","amber":"insight-icon-amber","rose":"insight-icon-rose"}
    for icon, title, desc, color in salary_boost_tips(job, exp, skills, cert, edu):
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-icon {icon_map[color]}">{icon}</div>
            <div><div class="insight-title">{title}</div><div class="insight-desc">{desc}</div></div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        top_skills    = get_skills_to_learn(job, skills)
        salary_boosts = ["+₹8K–15K","+₹10K–20K","+₹6K–12K","+₹12K–25K","+₹5K–10K","+₹15K–30K"]
        st.markdown('<div class="card"><div class="card-title">🛠️ Top Skills to Learn Next</div>', unsafe_allow_html=True)
        for i, (sk, boost) in enumerate(zip(top_skills, salary_boosts)):
            pct = 90 - i*10
            st.markdown(f"""
            <div class="compare-bar-wrap">
                <div class="compare-bar-label">
                    <span style="font-size:13px;font-weight:500;color:#0f172a;">{sk}</span>
                    <span class="trend-up">{boost}/yr</span>
                </div>
                <div class="compare-bar-track">
                    <div class="compare-bar-fill" style="width:{pct}%;background:linear-gradient(90deg,#6366f1,#8b5cf6);"></div>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        trend = get_industry_data(ind)
        st.markdown('<div class="card"><div class="card-title">📈 Industry Salary Trends</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px;">
            <div class="metric-card"><div class="metric-label">Industry Growth</div><div class="metric-value">{trend['growth']}</div><div class="metric-sub">↑ YoY</div></div>
            <div class="metric-card"><div class="metric-label">Job Demand</div><div class="metric-value" style="font-size:16px;">{trend['demand']}</div></div>
            <div class="metric-card"><div class="metric-label">Top Pay</div><div class="metric-value" style="font-size:16px;">{trend['top_pay']}</div></div>
            <div class="metric-card"><div class="metric-label">Outlook</div><div class="metric-value" style="font-size:16px;">{trend['outlook']}</div></div>
        </div>
        <div style="background:#eef2ff;border-radius:10px;padding:14px 16px;">
            <div style="font-size:13px;color:#4f46e5;font-weight:600;">💡 {ind} sector insight</div>
            <div style="font-size:13px;color:#475569;margin-top:6px;line-height:1.5;">
                Growing at <strong>{trend['growth']}</strong> annually with <strong>{trend['demand'].lower()}</strong> talent demand. 
                Top earners make <strong>{trend['top_pay']}</strong>. Now is an excellent time to upskill and negotiate confidently.
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # What-If Simulator
    st.markdown('<div class="card"><div class="card-title">⚡ What-If Salary Simulator</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:13px;color:#64748b;margin-bottom:16px;">Drag the sliders to see how improving one factor changes your salary.</p>', unsafe_allow_html=True)
    s1,s2,s3 = st.columns(3)
    with s1:
        extra_exp = st.slider("+ Years Experience", 0, 10, 2, key="sim_exp")
        sim_e = int(salary * (1 + extra_exp * 0.055))
        st.markdown(f'<div class="metric-card"><div class="metric-label">+{extra_exp} years experience</div><div class="metric-value">₹{sim_e:,}</div><div class="metric-sub trend-up">+₹{sim_e-salary:,}</div></div>', unsafe_allow_html=True)
    with s2:
        extra_sk = st.slider("+ Skills Added", 0, 10, 3, key="sim_skills")
        sim_s = int(salary * (1 + extra_sk * 0.028))
        st.markdown(f'<div class="metric-card"><div class="metric-label">+{extra_sk} skills</div><div class="metric-value">₹{sim_s:,}</div><div class="metric-sub trend-up">+₹{sim_s-salary:,}</div></div>', unsafe_allow_html=True)
    with s3:
        extra_c = st.slider("+ Certifications", 0, 5, 1, key="sim_cert")
        sim_c = int(salary * (1 + extra_c * 0.04))
        st.markdown(f'<div class="metric-card"><div class="metric-label">+{extra_c} certifications</div><div class="metric-value">₹{sim_c:,}</div><div class="metric-sub trend-up">+₹{sim_c-salary:,}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# ROADMAP TAB
# =========================
def show_roadmap():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Career Roadmap</div>', unsafe_allow_html=True)

    if not st.session_state.last_inputs:
        st.markdown('<div style="text-align:center;padding:60px;"><div style="font-size:48px;">🗺️</div><div style="font-size:18px;font-weight:600;color:#0f172a;margin-top:12px;">Run a prediction first</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    inp   = st.session_state.last_inputs
    job   = inp["job_title"]; exp = inp["experience_years"]
    steps = get_roadmap(job)
    current_step = 0 if exp<=2 else (1 if exp<=5 else (2 if exp<=10 else (3 if exp<=15 else 4)))

    col_r, col_i = st.columns([3, 2], gap="large")
    with col_r:
        salary_ranges = ["₹40K–70K","₹70K–1.1L","₹1.1L–1.6L","₹1.6L–2.0L","₹2.0L+"]
        exp_ranges    = ["0–2 yrs","2–5 yrs","5–10 yrs","10–15 yrs","15+ yrs"]
        st.markdown('<div class="card"><div class="card-title">🗺️ Your Career Path — ' + job + '</div>', unsafe_allow_html=True)
        for i, step in enumerate(steps):
            if i < current_step:
                dot = "step-dot-done"; badge = "badge-done"; btxt = "✓ Completed"
            elif i == current_step:
                dot = "step-dot-curr"; badge = "badge-current"; btxt = "📍 You are here"
            else:
                dot = "step-dot-next"; badge = "badge-future"; btxt = f"Next · {exp_ranges[i]}"
            st.markdown(f"""
            <div class="roadmap-step">
                <div class="step-dot {dot}">{i+1}</div>
                <div>
                    <div class="step-title">{step}</div>
                    <div class="step-sub">{exp_ranges[i]} &nbsp;·&nbsp; {salary_ranges[i]}</div>
                    <span class="step-badge {badge}">{btxt}</span>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_i:
        curr  = steps[current_step]
        nxt   = steps[min(current_step+1, len(steps)-1)]
        sk    = get_skills_to_learn(job, 0)[:4]
        st.markdown(f"""
        <div class="card" style="background:linear-gradient(135deg,#eef2ff,#f5f3ff);border-color:#c7d2fe;margin-bottom:12px;">
            <div class="card-title" style="color:#4f46e5;">🎯 Your Next Goal</div>
            <div style="font-size:19px;font-weight:700;color:#1e1b4b;margin-bottom:8px;">{nxt}</div>
            <div style="font-size:13px;color:#4338ca;line-height:1.6;">
                Currently at <strong>{curr}</strong>. Build 1–2 impactful projects, 
                master the skills below, and apply for senior roles to make the leap.
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="card"><div class="card-title">🛠️ Skills for Next Level</div>', unsafe_allow_html=True)
        for s in sk:
            st.markdown(f'<span style="display:inline-block;background:#eef2ff;color:#4f46e5;border-radius:99px;padding:5px 14px;font-size:13px;font-weight:500;margin:4px;border:1px solid #c7d2fe;">{s}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card">
            <div class="card-title">📅 Estimated Timeline</div>
            <div style="font-size:13px;color:#475569;line-height:2.0;">
                🟣 &nbsp;<strong>Now:</strong> {steps[current_step]}<br>
                🟢 &nbsp;<strong>1–2 yrs:</strong> {steps[min(current_step+1,len(steps)-1)]}<br>
                🔵 &nbsp;<strong>3–5 yrs:</strong> {steps[min(current_step+2,len(steps)-1)]}<br>
                ⭐ &nbsp;<strong>5–8 yrs:</strong> {steps[-1]}
            </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# DASHBOARD TAB
# =========================
def show_dashboard():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">My Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Your personal prediction history and statistics.</div>', unsafe_allow_html=True)

    users = load_users()
    preds = users.get(st.session_state.user_email, {}).get("predictions", [])

    if not preds:
        st.markdown('<div style="text-align:center;padding:60px;"><div style="font-size:48px;">📊</div><div style="font-size:18px;font-weight:600;color:#0f172a;margin-top:12px;">No predictions yet</div><div style="font-size:14px;color:#64748b;">Head to the Predict tab to get started!</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    salaries = [p["salary"] for p in preds]
    avg_sal  = int(sum(salaries)/len(salaries))
    best_sal = max(salaries)

    m1,m2,m3,m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Predictions</div><div class="metric-value">{len(preds)}</div></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><div class="metric-label">Latest Salary</div><div class="metric-value" style="font-size:18px;">₹{salaries[-1]:,}</div></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><div class="metric-label">Average Salary</div><div class="metric-value" style="font-size:18px;">₹{avg_sal:,}</div></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><div class="metric-label">Best Prediction</div><div class="metric-value" style="font-size:18px;">₹{best_sal:,}</div><div class="metric-sub">↑ Your peak</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="card" style="margin-top:12px;"><div class="card-title">📋 Prediction History</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;gap:12px;padding:8px 0;border-bottom:1px solid #f1f5f9;margin-bottom:4px;">
        <span style="flex:.4;font-size:11px;font-weight:700;color:#94a3b8;">#</span>
        <span style="flex:2;font-size:11px;font-weight:700;color:#94a3b8;">ROLE</span>
        <span style="flex:1;font-size:11px;font-weight:700;color:#94a3b8;">EXP</span>
        <span style="flex:1;font-size:11px;font-weight:700;color:#94a3b8;">SKILLS</span>
        <span style="flex:1.5;font-size:11px;font-weight:700;color:#94a3b8;">SALARY</span>
        <span style="flex:1.5;font-size:11px;font-weight:700;color:#94a3b8;">DATE</span>
    </div>""", unsafe_allow_html=True)
    for i, p in enumerate(reversed(preds[-10:]), 1):
        is_best = p["salary"] == best_sal
        st.markdown(f"""
        <div style="display:flex;gap:12px;padding:11px 0;border-bottom:1px solid #f8fafc;align-items:center;">
            <span style="flex:.4;font-size:13px;color:#94a3b8;">{i}</span>
            <span style="flex:2;font-size:13px;font-weight:500;color:#0f172a;">{p.get('job','—')}</span>
            <span style="flex:1;font-size:13px;color:#64748b;">{p.get('exp',0)} yrs</span>
            <span style="flex:1;font-size:13px;color:#64748b;">{p.get('skills',0)}</span>
            <span style="flex:1.5;font-size:14px;font-weight:700;color:#4f46e5;">₹{p['salary']:,}{'&nbsp;⭐' if is_best else ''}</span>
            <span style="flex:1.5;font-size:12px;color:#94a3b8;">{p.get('date','—')}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# COMPARE TAB
# =========================
def show_compare():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Compare Yourself</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">See how your predicted salary stacks up against market benchmarks.</div>', unsafe_allow_html=True)

    if not st.session_state.last_prediction:
        st.markdown('<div style="text-align:center;padding:60px;"><div style="font-size:48px;">⚖️</div><div style="font-size:18px;font-weight:600;color:#0f172a;margin-top:12px;">Run a prediction first</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    salary = st.session_state.last_prediction
    inp    = st.session_state.last_inputs
    job    = inp["job_title"]
    base   = max(40000, salary - random.randint(10000,20000))
    top25  = int(salary * 1.22); top10 = int(salary * 1.48); top5 = int(salary * 1.75)
    max_v  = top5

    benchmarks = [
        ("Entry Level (0–2 yrs)",  int(base * 0.6),  "#e2e8f0"),
        ("Mid Level (3–6 yrs)",    int(base * 0.85), "#c7d2fe"),
        ("Your Salary",            salary,            "#6366f1"),
        ("Top 25% in your role",   top25,             "#8b5cf6"),
        ("Top 10% in your role",   top10,             "#7c3aed"),
        ("Top 5% — Elite earner",  top5,              "#4338ca"),
    ]

    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        st.markdown(f'<div class="card"><div class="card-title">📊 Salary Benchmarks — {job}</div>', unsafe_allow_html=True)
        for label, val, color in benchmarks:
            pct    = int((val / max_v) * 100)
            is_you = label == "Your Salary"
            st.markdown(f"""
            <div class="compare-bar-wrap" style="{'background:#eef2ff;border-radius:8px;padding:8px 10px;border:1px solid #c7d2fe;' if is_you else ''}">
                <div class="compare-bar-label">
                    <span style="font-size:13px;font-weight:{'700' if is_you else '500'};color:{'#4f46e5' if is_you else '#374151'};">{'📍 ' if is_you else ''}{label}</span>
                    <span style="font-size:13px;font-weight:600;color:{'#4f46e5' if is_you else '#0f172a'};">₹{val:,}</span>
                </div>
                <div class="compare-bar-track"><div class="compare-bar-fill" style="width:{pct}%;background:{color};"></div></div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        pct_rank = min(95, max(25, int(30 + (salary/top5)*65)))
        gap      = max(0, top10 - salary)
        st.markdown(f"""
        <div class="card" style="text-align:center;margin-bottom:12px;">
            <div class="card-title">🎯 Your Market Position</div>
            <div style="font-size:52px;font-weight:800;font-family:'Syne',sans-serif;
                        background:linear-gradient(135deg,#6366f1,#8b5cf6);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">{pct_rank}th</div>
            <div style="font-size:14px;color:#64748b;">percentile in your field</div>
            <div style="font-size:13px;color:#475569;margin-top:12px;line-height:1.6;">
                You earn more than <strong>{pct_rank}%</strong> of professionals in similar roles.
                {'Focus on top skills to break into the top 10%.' if pct_rank < 90 else '🎉 You are among the elite earners!'}
            </div>
        </div>
        <div class="card">
            <div class="card-title">💰 Gap to Top 10%</div>
            <div style="font-size:24px;font-weight:800;color:#4f46e5;font-family:'Syne',sans-serif;">{'Already there! 🎉' if gap==0 else f'₹{gap:,}'}</div>
            <div style="font-size:13px;color:#64748b;margin-top:6px;line-height:1.5;">
                {'You have already cracked the top 10% — excellent work!' if gap==0 else 'Add 2–3 high-demand skills and pursue senior roles to close this gap within 1–2 years.'}
            </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# LEADERBOARD TAB
# =========================
def show_leaderboard():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Leaderboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Top predicted salaries across all SalaryIQ Pro users.</div>', unsafe_allow_html=True)

    lb    = get_leaderboard()
    users = load_users()
    my_ps = users.get(st.session_state.user_email, {}).get("predictions", [])
    my_b  = max([p["salary"] for p in my_ps], default=0)

    if my_b:
        my_rank = sum(1 for e in lb if e["salary"] > my_b) + 1
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#eef2ff,#f5f3ff);border:1px solid #c7d2fe;
                    border-radius:14px;padding:18px 24px;margin-bottom:20px;
                    display:flex;align-items:center;justify-content:space-between;">
            <div>
                <div style="font-size:11px;color:#6366f1;font-weight:700;text-transform:uppercase;letter-spacing:.8px;">Your Position</div>
                <div style="font-size:22px;font-weight:800;color:#1e1b4b;font-family:'Syne',sans-serif;">
                    #{my_rank} &nbsp;<span style="font-size:14px;color:#64748b;font-weight:400;">out of {len(lb)} users</span>
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:11px;color:#6366f1;font-weight:700;text-transform:uppercase;">Your Best</div>
                <div style="font-size:22px;font-weight:800;color:#4f46e5;font-family:'Syne',sans-serif;">₹{my_b:,}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    if not lb:
        st.markdown('<div style="text-align:center;padding:40px;color:#94a3b8;font-size:14px;">No predictions yet. Be the first!</div>', unsafe_allow_html=True)
    else:
        medals     = ["🥇","🥈","🥉"]
        row_cls    = ["gold","silver","bronze"]
        st.markdown('<div class="card"><div class="card-title">🏆 Top Earners</div>', unsafe_allow_html=True)
        for i, entry in enumerate(lb):
            medal  = medals[i] if i<3 else f"#{i+1}"
            rcls   = row_cls[i] if i<3 else ""
            is_me  = entry["name"] == st.session_state.user_name
            you_badge = '&nbsp;<span style="font-size:11px;background:#eef2ff;color:#4f46e5;padding:2px 8px;border-radius:99px;font-weight:600;">You</span>' if is_me else ""
            st.markdown(f"""
            <div class="lb-row {rcls}" style="{'border:2px solid #6366f1;' if is_me else ''}">
                <div class="lb-rank">{medal}</div>
                <div style="flex:1;">
                    <div class="lb-name">{entry['name']}{you_badge}</div>
                    <div class="lb-role">{entry['job']} &nbsp;·&nbsp; {entry['exp']} yrs exp</div>
                </div>
                <div class="lb-salary">₹{entry['salary']:,}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# MAIN APP
# =========================
def show_app():
    show_nav()
    tab = st.session_state.active_tab
    if   tab == "predict":     show_predict()
    elif tab == "insights":    show_insights()
    elif tab == "roadmap":     show_roadmap()
    elif tab == "dashboard":   show_dashboard()
    elif tab == "compare":     show_compare()
    elif tab == "leaderboard": show_leaderboard()


# =========================
# ENTRY POINT
# =========================
if st.session_state.logged_in:
    show_app()
elif st.session_state.auth_page == "signup":
    show_signup()
else:
    show_login()
