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
# GLOBAL CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@300;400;500;600;700&display=swap');

*, html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header, .stDeployButton { visibility: hidden !important; display: none !important; }
[data-testid="stHeader"]         { display: none !important; }
[data-testid="stSidebarNav"]     { display: none !important; }

/* ── zero all padding ── */
.block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
.stApp > div, [data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section,
[data-testid="stAppViewContainer"] > section > div,
[data-testid="stVerticalBlock"] {
    padding-top: 0 !important; margin-top: 0 !important;
}

/* ══════════════════════════════════
   AUTH BACKGROUND
══════════════════════════════════ */
.auth-bg {
    position: fixed; inset: 0; z-index: 0;
    background: radial-gradient(ellipse 80% 60% at 20% 10%, rgba(92,61,232,.38) 0%, transparent 60%),
                radial-gradient(ellipse 60% 50% at 80% 80%, rgba(245,200,66,.13) 0%, transparent 60%),
                #120d30;
}

/* ── left purple panel (pure HTML, no Streamlit widgets inside) ── */
.auth-left-panel {
    background: #5c3de8;
    border-radius: 20px 0 0 20px;
    padding: 52px 40px;
    min-height: 560px;
    height: 100%;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.auth-left-panel::before {
    content: '';
    position: absolute; inset: 0;
    background: repeating-linear-gradient(
        -45deg, transparent, transparent 16px,
        rgba(255,255,255,.045) 16px, rgba(255,255,255,.045) 32px);
}
.auth-left-inner { position: relative; z-index: 1; }
.auth-brand {
    font-family: 'Syne', sans-serif;
    font-size: 13px; font-weight: 800;
    color: rgba(255,255,255,.55);
    letter-spacing: 2px; text-transform: uppercase;
    margin-bottom: 44px;
}
.auth-brand em { color: #f5c842; font-style: normal; }
.auth-left-panel h2 {
    font-family: 'Syne', sans-serif !important;
    font-size: 38px; font-weight: 800 !important;
    color: #fff !important; line-height: 1.15; margin-bottom: 14px;
}
.auth-left-panel p {
    font-size: 13.5px; color: rgba(255,255,255,.55);
    line-height: 1.7; margin-bottom: 36px;
}
.switch-label-txt { font-size: 12px; color: rgba(255,255,255,.4); margin-bottom: 12px; }
.auth-stats-row {
    display: flex; gap: 24px;
    margin-top: 40px; padding-top: 28px;
    border-top: 1px solid rgba(255,255,255,.13);
}
.auth-stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 22px; font-weight: 800; color: #f5c842;
}
.auth-stat-lbl {
    font-size: 10px; color: rgba(255,255,255,.4);
    text-transform: uppercase; letter-spacing: .6px; margin-top: 2px;
}

/* ── right white panel ── */
.auth-right-panel {
    background: #fff;
    border-radius: 0 20px 20px 0;
    padding: 52px 44px;
    min-height: 560px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.auth-right-panel h3 {
    font-family: 'Syne', sans-serif !important;
    font-size: 26px; font-weight: 800 !important;
    color: #5c3de8 !important; margin-bottom: 4px;
}
.auth-right-sub { font-size: 13px; color: #94a3b8; margin-bottom: 24px; }
.auth-help-txt  { font-size: 12px; color: #94a3b8; text-align: right; margin-bottom: 20px; }

/* ── auth divider ── */
.auth-or {
    text-align: center; color: #cbd5e1; font-size: 11px;
    margin: 10px 0; position: relative;
}
.auth-or::before, .auth-or::after {
    content: ''; position: absolute; top: 50%;
    width: calc(50% - 22px); height: 1px; background: #e2e8f0;
}
.auth-or::before { left: 0; } .auth-or::after { right: 0; }

/* ── password strength ── */
.pw-track { height: 3px; background: #e2e8f0; border-radius: 99px; overflow: hidden; margin: 6px 0 4px; }
.pw-bar   { height: 100%; border-radius: 99px; transition: width .3s, background .3s; }

/* ══════════════════════════════════
   BUTTON OVERRIDES
══════════════════════════════════ */

/* default (used in main app) */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg,#6366f1,#8b5cf6) !important;
    color: #fff !important; border: none !important; border-radius: 10px !important;
    padding: 12px 20px !important; font-size: 14px !important; font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(99,102,241,.3) !important; transition: all .2s !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 6px 20px rgba(99,102,241,.4) !important; }

/* purple submit */
div[data-testid="stVerticalBlock"] .submit-wrap > div > button,
.submit-wrap .stButton > button {
    background: #5c3de8 !important;
    box-shadow: 0 4px 18px rgba(92,61,232,.32) !important;
    border-radius: 9px !important; font-size: 15px !important;
}
.submit-wrap .stButton > button:hover { background: #3d28b5 !important; }

/* ghost switch button (left panel) */
.switch-wrap .stButton > button {
    background: transparent !important;
    color: #fff !important;
    border: 1.5px solid rgba(255,255,255,.45) !important;
    border-radius: 8px !important; padding: 9px 22px !important;
    font-size: 13px !important; font-weight: 500 !important;
    box-shadow: none !important; width: auto !important;
}
.switch-wrap .stButton > button:hover {
    background: rgba(255,255,255,.12) !important;
    border-color: #fff !important; transform: none !important; box-shadow: none !important;
}

/* ghost link button (right panel) */
.link-wrap .stButton > button {
    background: transparent !important;
    color: #5c3de8 !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 9px !important; font-size: 14px !important; font-weight: 500 !important;
    box-shadow: none !important;
}
.link-wrap .stButton > button:hover {
    background: #eef2ff !important; border-color: #5c3de8 !important;
    transform: none !important; box-shadow: none !important;
}

/* ══════════════════════════════════
   INPUTS
══════════════════════════════════ */
.stTextInput > div > div {
    background: #f8fafc !important; border: 1.5px solid #e2e8f0 !important; border-radius: 9px !important;
}
.stTextInput > div > div:focus-within {
    border-color: #5c3de8 !important; box-shadow: 0 0 0 3px rgba(92,61,232,.1) !important; background: #fff !important;
}
.stTextInput input { color: #0f172a !important; background: transparent !important; box-shadow: none !important; font-size: 14px !important; }
.stTextInput input::placeholder { color: #94a3b8 !important; }
.stTextInput label { color: #475569 !important; font-size: 12px !important; font-weight: 500 !important; }

.stNumberInput > div > div { background: #f8fafc !important; border: 1.5px solid #e2e8f0 !important; border-radius: 10px !important; }
.stNumberInput > div > div:focus-within { border-color: #6366f1 !important; box-shadow: 0 0 0 3px rgba(99,102,241,.12) !important; }
.stNumberInput input { color: #0f172a !important; background: transparent !important; box-shadow: none !important; font-size: 14px !important; }
.stNumberInput label { color: #475569 !important; font-size: 13px !important; font-weight: 500 !important; }
.stNumberInput button { color: #6366f1 !important; }

.stSelectbox > div > div { background: #f8fafc !important; border: 1.5px solid #e2e8f0 !important; border-radius: 10px !important; }
.stSelectbox > div > div:focus-within { border-color: #6366f1 !important; box-shadow: 0 0 0 3px rgba(99,102,241,.12) !important; }
.stSelectbox [data-baseweb="select"] > div, .stSelectbox [data-baseweb="select"] span { color: #0f172a !important; background: transparent !important; }
.stSelectbox label { color: #475569 !important; font-size: 13px !important; font-weight: 500 !important; }
[data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"] {
    background: #fff !important; border: 1px solid #e2e8f0 !important; border-radius: 12px !important; box-shadow: 0 8px 32px rgba(0,0,0,.12) !important;
}
[data-baseweb="menu"] li, [role="option"] { background: #fff !important; color: #1e293b !important; font-size: 14px !important; }
[data-baseweb="menu"] li:hover, [role="option"]:hover, [role="option"][aria-selected="true"] { background: #eef2ff !important; color: #4f46e5 !important; }

/* ══════════════════════════════════
   SIDEBAR
══════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: #1a2236 !important;
    border-right: 1px solid rgba(255,255,255,.08) !important;
    min-width: 260px !important; max-width: 260px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

/* ══════════════════════════════════
   NAV BAR
══════════════════════════════════ */
.top-nav {
    background: #1a2236;
    padding: 0 clamp(16px,4vw,48px);
    display: flex; align-items: center; justify-content: space-between;
    height: 64px;
    box-shadow: 0 2px 12px rgba(0,0,0,.25);
    position: sticky; top: 0; z-index: 999;
}
.nav-brand { font-family:'Syne',sans-serif !important; font-size:clamp(16px,2.5vw,22px); font-weight:800; color:#fff; letter-spacing:.3px; }
.nav-brand em { color:#f5a623; font-style:normal; }
.nav-links  { display:flex; align-items:center; gap:clamp(4px,2vw,28px); flex:1; justify-content:center; }
.nav-link   { font-size:14px; font-weight:500; color:rgba(255,255,255,.82); cursor:pointer; padding:4px 2px; border-bottom:2px solid transparent; transition:color .2s,border-color .2s; }
.nav-link:hover, .nav-link.active { color:#fff; border-bottom-color:#f5a623; }
.nav-link.active { color:#f5a623; }
.nav-avatar { width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#f5a623,#e07b10);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#fff;border:2px solid rgba(255,255,255,.3); }
.nav-name   { font-size:13px; font-weight:500; color:rgba(255,255,255,.85); white-space:nowrap; }

/* nav tab buttons */
.nav-tab-btn > button {
    background:transparent !important; color:rgba(255,255,255,.75) !important;
    border:none !important; border-radius:0 !important; border-bottom:2px solid transparent !important;
    padding:8px 4px !important; font-size:13px !important; font-weight:500 !important;
    box-shadow:none !important; width:100% !important;
}
.nav-tab-btn > button:hover { color:#fff !important; border-bottom-color:#f5a623 !important; transform:none !important; box-shadow:none !important; }
div[data-testid="stHorizontalBlock"]:has(.nav-tab-btn) { background:#1a2236 !important; padding:0 clamp(16px,4vw,48px) !important; margin:0 !important; gap:0 !important; }
div[data-testid="stHorizontalBlock"]:has(.nav-tab-btn) > div { padding:0 !important; min-width:0 !important; }

.nav-btn-primary > button { background:#f5a623 !important; color:#1a1a1a !important; border:none !important; border-radius:6px !important; padding:8px 20px !important; font-size:13px !important; font-weight:700 !important; box-shadow:0 2px 8px rgba(245,166,35,.35) !important; width:auto !important; }
.nav-btn-primary > button:hover { background:#e09610 !important; transform:translateY(-1px) !important; }
.nav-btn-logout  > button { background:transparent !important; color:#fff !important; border:1.5px solid rgba(255,255,255,.45) !important; border-radius:6px !important; padding:7px 18px !important; font-size:13px !important; font-weight:600 !important; box-shadow:none !important; width:auto !important; }
.nav-btn-logout  > button:hover { background:rgba(255,255,255,.1) !important; border-color:#fff !important; transform:none !important; }

/* ══════════════════════════════════
   MAIN APP STYLES
══════════════════════════════════ */
.stApp { background:#f8f9fc !important; }
.page-wrap { padding:clamp(16px,3vw,28px) clamp(12px,3vw,36px); max-width:1200px; margin:0 auto; }
.page-title { font-family:'Syne',sans-serif !important; font-size:clamp(18px,3vw,24px); font-weight:800; color:#0f172a; margin-bottom:4px; }
.page-sub   { font-size:14px; color:#64748b; margin-bottom:20px; }
.card { background:#fff; border-radius:16px; border:1px solid #e2e8f0; padding:clamp(14px,2vw,22px); box-shadow:0 1px 3px rgba(0,0,0,.04); margin-bottom:16px; }
.card-title { font-size:11px; font-weight:700; color:#6366f1; text-transform:uppercase; letter-spacing:1px; margin-bottom:16px; }
.metric-card { background:#fff; border:1px solid #e2e8f0; border-radius:14px; padding:16px 14px; box-shadow:0 1px 3px rgba(0,0,0,.04); }
.metric-label { font-size:12px; color:#94a3b8; font-weight:500; margin-bottom:6px; }
.metric-value { font-family:'Syne',sans-serif !important; font-size:clamp(16px,2vw,22px); font-weight:800; color:#0f172a; }
.metric-sub   { font-size:12px; color:#10b981; font-weight:500; margin-top:4px; }
.result-hero { background:linear-gradient(135deg,#6366f1 0%,#8b5cf6 100%); border-radius:20px; padding:clamp(20px,4vw,36px) clamp(16px,4vw,32px); text-align:center; margin-bottom:20px; box-shadow:0 8px 32px rgba(99,102,241,.3); }
.result-hero-label  { font-size:12px; color:rgba(255,255,255,.7); letter-spacing:1.5px; text-transform:uppercase; }
.result-hero-amount { font-family:'Syne',sans-serif !important; font-size:clamp(36px,8vw,56px); font-weight:800; color:#fff; margin:8px 0; }
.result-hero-sub    { font-size:13px; color:rgba(255,255,255,.6); }
.insight-card { background:#fff; border-radius:12px; border:1px solid #e2e8f0; padding:16px; margin-bottom:10px; display:flex; gap:14px; align-items:flex-start; }
.insight-icon { width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0; }
.insight-icon-blue{background:#eef2ff;} .insight-icon-green{background:#f0fdf4;} .insight-icon-amber{background:#fffbeb;} .insight-icon-rose{background:#fff1f2;}
.insight-title { font-size:14px; font-weight:600; color:#0f172a; margin-bottom:4px; }
.insight-desc  { font-size:13px; color:#64748b; line-height:1.5; }
.roadmap-step  { display:flex; gap:16px; align-items:flex-start; padding:16px 0; border-bottom:1px solid #f1f5f9; }
.roadmap-step:last-child { border-bottom:none; }
.step-dot      { width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;flex-shrink:0;margin-top:2px; }
.step-dot-done { background:#6366f1;color:#fff; }
.step-dot-curr { background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;box-shadow:0 0 0 4px rgba(99,102,241,.2); }
.step-dot-next { background:#f1f5f9;color:#94a3b8;border:2px dashed #cbd5e1; }
.step-title { font-size:15px; font-weight:600; color:#0f172a; }
.step-sub   { font-size:13px; color:#64748b; margin-top:3px; }
.step-badge { display:inline-block; font-size:11px; font-weight:600; padding:2px 10px; border-radius:99px; margin-top:6px; }
.badge-current{background:#eef2ff;color:#4f46e5;} .badge-done{background:#f0fdf4;color:#15803d;} .badge-future{background:#f8fafc;color:#94a3b8;}
.lb-row   { display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:12px;margin-bottom:8px;background:#f8fafc;border:1px solid #f1f5f9;transition:all .15s;flex-wrap:wrap; }
.lb-row:hover{background:#eef2ff;border-color:#c7d2fe;}
.lb-row.gold  {background:linear-gradient(135deg,#fffbeb,#fef3c7);border-color:#fde68a;}
.lb-row.silver{background:linear-gradient(135deg,#f8fafc,#f1f5f9);border-color:#e2e8f0;}
.lb-row.bronze{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fed7aa;}
.lb-rank  { font-family:'Syne',sans-serif !important;font-size:16px;font-weight:800;min-width:28px; }
.lb-name  { flex:1;font-size:14px;font-weight:600;color:#0f172a;min-width:100px; }
.lb-role  { font-size:12px;color:#64748b; }
.lb-salary{ font-family:'Syne',sans-serif !important;font-size:16px;font-weight:800;color:#4f46e5; }
.compare-bar-wrap  { margin-bottom:14px; }
.compare-bar-label { display:flex;justify-content:space-between;font-size:13px;margin-bottom:5px;flex-wrap:wrap;gap:4px; }
.compare-bar-track { height:8px;background:#f1f5f9;border-radius:99px;overflow:hidden; }
.compare-bar-fill  { height:100%;border-radius:99px; }
.trend-up { color:#10b981;font-weight:600;font-size:13px; }
h1,h2,h3  { font-family:'Syne',sans-serif !important; color:#0f172a !important; }
p,li      { color:#475569; }
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
        tips.append(("🚀","Build a strong portfolio","Create 3–5 GitHub projects demonstrating real skills. At junior levels, projects matter more than years of experience.","blue"))
    if 3 <= exp < 7:
        tips.append(("📈","Apply for senior roles now","With your experience, senior roles pay 35–50% more. Rewrite your resume to highlight impact and outcomes, not just duties.","green"))
    if exp >= 7:
        tips.append(("🏆","Move into leadership","7+ years of experience puts you in prime position for Lead/Manager roles — which pay 50–80% more than individual contributor positions.","amber"))
    if skills < 8:
        tips.append(("🛠️","Expand your skill set","Professionals with 10+ in-demand skills earn 28% more on average. Focus on cloud, data, or AI tools relevant to your role.","rose"))
    if cert < 2:
        tips.append(("📜","Earn certifications","AWS, Google Cloud, and PMP certifications add ₹10,000–₹25,000 to your annual salary. Many have free study resources.","blue"))
    if edu in ["High School","Diploma","Other"]:
        tips.append(("🎓","Upskill with online courses","Online Master's degrees or professional diplomas can boost salary by 15–20%. Platforms like Coursera and edX are affordable.","green"))
    tips.append(("🌍","Target remote / global roles","Remote roles at global companies pay 2–4x Indian market rates. Explore Toptal, Turing, and Remote.com.","amber"))
    tips.append(("💬","Negotiate your salary","60% of professionals never negotiate. Research market rates on Glassdoor and LinkedIn Salary, then ask for 15–20% above the offer.","rose"))
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


# =========================================================
# LOGIN PAGE
# =========================================================
def show_login():

    # Background
    st.markdown('<div class="auth-bg"></div>', unsafe_allow_html=True)

    st.markdown("""
    <style>

    .stApp{
        background: transparent !important;
    }

    section[data-testid="stAppViewContainer"] > div:first-child{
        display:flex;
        align-items:center;
        justify-content:center;
        min-height:100vh;
        padding:25px;
    }

    /* MAIN LOGIN CARD */
    .login-wrapper{
        max-width:1100px;
        width:100%;
        background:white;
        border-radius:24px;
        overflow:hidden;
        box-shadow:0 20px 60px rgba(0,0,0,0.35);
    }

    /* LEFT PANEL */
    .auth-left-panel{
        background:linear-gradient(135deg,#5c3de8,#6d4dff);
        min-height:650px;
        padding:60px 45px;
        position:relative;
        overflow:hidden;
        display:flex;
        flex-direction:column;
        justify-content:space-between;
    }

    .auth-left-panel::before{
        content:'';
        position:absolute;
        inset:0;
        background:repeating-linear-gradient(
            -45deg,
            transparent,
            transparent 18px,
            rgba(255,255,255,0.04) 18px,
            rgba(255,255,255,0.04) 36px
        );
    }

    .auth-left-inner{
        position:relative;
        z-index:2;
    }

    .auth-brand{
        font-size:18px;
        font-weight:800;
        color:white;
        margin-bottom:70px;
        letter-spacing:1px;
    }

    .auth-brand em{
        color:#f5c842;
        font-style:normal;
    }

    .auth-left-panel h2{
        color:white !important;
        font-size:58px;
        font-weight:800 !important;
        line-height:1.1;
        margin-bottom:20px;
    }

    .auth-left-panel p{
        color:rgba(255,255,255,0.75);
        font-size:18px;
        line-height:1.7;
        max-width:350px;
    }

    .switch-label-txt{
        color:rgba(255,255,255,0.75);
        margin-top:45px;
        margin-bottom:14px;
        font-size:16px;
    }

    .switch-wrap{
        position:relative;
        z-index:10;
        width:160px;
    }

    .switch-wrap .stButton button{
        background:transparent !important;
        border:2px solid rgba(255,255,255,0.5) !important;
        color:white !important;
        border-radius:14px !important;
        padding:12px 25px !important;
        font-size:18px !important;
        font-weight:600 !important;
        width:100% !important;
        box-shadow:none !important;
    }

    .switch-wrap .stButton button:hover{
        background:rgba(255,255,255,0.15) !important;
        border-color:white !important;
    }

    /* STATS */
    .auth-stats-row{
        display:flex;
        gap:40px;
        margin-top:50px;
        position:relative;
        z-index:10;
    }

    .auth-stat-num{
        color:#f5c842;
        font-size:42px;
        font-weight:800;
    }

    .auth-stat-lbl{
        color:rgba(255,255,255,0.7);
        font-size:15px;
        margin-top:4px;
    }

    /* RIGHT PANEL */
    .auth-right-panel{
        background:white;
        min-height:650px;
        padding:70px 55px;
        display:flex;
        flex-direction:column;
        justify-content:center;
    }

    .auth-help-txt{
        text-align:right;
        color:#94a3b8;
        margin-bottom:30px;
        font-size:15px;
    }

    .auth-right-panel h3{
        color:#5c3de8 !important;
        font-size:42px;
        font-weight:800 !important;
        margin-bottom:10px;
    }

    .auth-right-sub{
        color:#94a3b8;
        font-size:18px;
        margin-bottom:35px;
    }

    /* INPUTS */
    .stTextInput > div > div{
        background:#f8fafc !important;
        border:1.5px solid #e2e8f0 !important;
        border-radius:12px !important;
        height:56px !important;
    }

    .stTextInput input{
        font-size:18px !important;
        color:#0f172a !important;
    }

    .stTextInput label{
        color:#475569 !important;
        font-size:15px !important;
        font-weight:600 !important;
    }

    /* LOGIN BUTTON */
    .submit-wrap .stButton button{
        background:#5c3de8 !important;
        color:white !important;
        border:none !important;
        border-radius:12px !important;
        height:56px !important;
        font-size:20px !important;
        font-weight:700 !important;
        margin-top:15px;
        box-shadow:0 8px 25px rgba(92,61,232,0.35) !important;
    }

    .submit-wrap .stButton button:hover{
        background:#4b2de0 !important;
        transform:translateY(-2px);
    }

    .auth-or{
        text-align:center;
        margin:30px 0;
        color:#94a3b8;
        position:relative;
    }

    .auth-or::before,
    .auth-or::after{
        content:'';
        position:absolute;
        top:50%;
        width:40%;
        height:1px;
        background:#e2e8f0;
    }

    .auth-or::before{ left:0; }
    .auth-or::after{ right:0; }

    .link-wrap .stButton button{
        background:white !important;
        border:1.5px solid #e2e8f0 !important;
        color:#5c3de8 !important;
        border-radius:12px !important;
        height:54px !important;
        font-size:16px !important;
        font-weight:600 !important;
        box-shadow:none !important;
    }

    .link-wrap .stButton button:hover{
        background:#eef2ff !important;
        border-color:#5c3de8 !important;
    }

    </style>
    """, unsafe_allow_html=True)

    # MAIN CARD
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)

    left, right = st.columns([5,7], gap="small")

    # =====================================================
    # LEFT PANEL
    # =====================================================
    with left:

        st.markdown("""
        <div class="auth-left-panel">

            <div class="auth-left-inner">

                <div class="auth-brand">
                    SALARY<em>IQ</em> PRO
                </div>

                <h2>
                    Welcome<br>
                    Back!
                </h2>

                <p>
                    Sign in to your career intelligence dashboard
                    and discover your true market value.
                </p>

                <div class="switch-label-txt">
                    Don't have an account?
                </div>

        """, unsafe_allow_html=True)

        st.markdown('<div class="switch-wrap">', unsafe_allow_html=True)

        if st.button("Sign Up", key="goto_signup"):
            st.session_state.auth_page = "signup"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""

                <div class="auth-stats-row">

                    <div>
                        <div class="auth-stat-num">95%</div>
                        <div class="auth-stat-lbl">ACCURACY</div>
                    </div>

                    <div>
                        <div class="auth-stat-num">50K+</div>
                        <div class="auth-stat-lbl">PREDICTIONS</div>
                    </div>

                    <div>
                        <div class="auth-stat-num">120+</div>
                        <div class="auth-stat-lbl">JOB ROLES</div>
                    </div>

                </div>

            </div>
        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # RIGHT PANEL
    # =====================================================
    with right:

        st.markdown('<div class="auth-right-panel">', unsafe_allow_html=True)

        st.markdown("""
        <div class="auth-help-txt">
            Need help?
        </div>

        <h3>Log in</h3>

        <div class="auth-right-sub">
            Enter your credentials to continue
        </div>
        """, unsafe_allow_html=True)

        email = st.text_input(
            "Username or Email",
            placeholder="Username",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            placeholder="Password",
            type="password",
            key="login_password"
        )

        st.markdown('<div class="submit-wrap">', unsafe_allow_html=True)

        login_clicked = st.button(
            "Log in",
            key="login_btn"
        )

        st.markdown('</div>', unsafe_allow_html=True)

        if login_clicked:

            if not email or not password:
                st.error("Please fill all fields")

            else:

                ok, result = login_user(email, password)

                if ok:
                    st.session_state.logged_in = True
                    st.session_state.user_name = result
                    st.session_state.user_email = email
                    st.rerun()

                else:
                    st.error(result)

        st.markdown('<div class="auth-or">or</div>', unsafe_allow_html=True)

        st.markdown('<div class="link-wrap">', unsafe_allow_html=True)

        if st.button(
            "Create Free Account",
            key="create_account"
        ):
            st.session_state.auth_page = "signup"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <p style="
            text-align:center;
            color:#94a3b8;
            font-size:14px;
            margin-top:35px;
        ">
            Privacy Policy · Terms & Conditions
        </p>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SIGNUP PAGE
# =========================================================
def show_signup():
    st.markdown('<div class="auth-bg"></div>', unsafe_allow_html=True)
    st.markdown("""
    <style>
    .stApp { background: transparent !important; }
    section[data-testid="stAppViewContainer"] > div:first-child {
        display: flex; align-items: center; justify-content: center;
        min-height: 100vh; padding: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

    left, right = st.columns([5, 6], gap="small")

    with left:
        st.markdown("""
        <div class="auth-left-panel">
          <div class="auth-left-inner">
            <div class="auth-brand">Salary<em>IQ</em> Pro</div>
            <h2>Get<br>Started!</h2>
            <p>Join professionals discovering their true market value. Free forever, no credit card needed.</p>
            <div class="switch-label-txt">Already have an account?</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="switch-wrap" style="margin-top:-8px;">', unsafe_allow_html=True)
        if st.button("← Log In", key="s_goto_login"):
            st.session_state.auth_page = "login"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="auth-right-panel">', unsafe_allow_html=True)
        st.markdown('<div class="auth-help-txt">Need help?</div>', unsafe_allow_html=True)
        st.markdown('<h3>Create Account</h3>', unsafe_allow_html=True)
        st.markdown('<div class="auth-right-sub">Fill in your details to get started</div>', unsafe_allow_html=True)

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
            idx = min(s-1,3) if s>0 else 0
            hint = "" if s==4 else " · add " + ", ".join(hints[:2])
            st.markdown(f"""
            <div style='margin-top:-6px;margin-bottom:10px;'>
              <div class='pw-track'><div class='pw-bar' style='width:{widths[idx]}%;background:{colors[idx]};'></div></div>
              <span style='font-size:12px;color:{colors[idx]};font-weight:600;'>{labels[idx]}{hint}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="submit-wrap">', unsafe_allow_html=True)
        signup_clicked = st.button("Create Account →", key="signup_btn")
        st.markdown('</div>', unsafe_allow_html=True)

        if signup_clicked:
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
        st.markdown('<div class="link-wrap">', unsafe_allow_html=True)
        if st.button("Already have an account? Sign In", key="goto_login"):
            st.session_state.auth_page = "login"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# =========================
# NAV BAR
# =========================
def show_nav():
    initials = get_initials(st.session_state.user_name)
    active   = st.session_state.active_tab
    nav_tabs = [
        ("predict","Predict"),("insights","Insights"),("roadmap","Roadmap"),
        ("dashboard","Dashboard"),("compare","Compare"),("leaderboard","Leaderboard"),
    ]
    links_html = "".join(
        f'<span class="nav-link{"active" if active==k else ""}">{l}</span>'
        for k,l in nav_tabs
    )
    st.markdown(f"""
    <div class="top-nav">
      <div class="nav-brand">💼 Salary<em>IQ</em></div>
      <nav class="nav-links">{links_html}</nav>
      <div style="display:flex;align-items:center;gap:8px;">
        <div class="nav-avatar">{initials}</div>
        <span class="nav-name">{st.session_state.user_name}</span>
      </div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6,c7,c8 = st.columns([1,1,1,1,1,1,1,1])
    for col,(key,label) in zip([c1,c2,c3,c4,c5,c6], nav_tabs):
        with col:
            st.markdown('<div class="nav-tab-btn">', unsafe_allow_html=True)
            if st.button(label, key=f"nav_{key}"):
                st.session_state.active_tab = key; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    with c7:
        st.markdown('<div class="nav-btn-primary">', unsafe_allow_html=True)
        if st.button("🔍 Predict", key="nav_predict_cta"):
            st.session_state.active_tab = "predict"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c8:
        st.markdown('<div class="nav-btn-logout">', unsafe_allow_html=True)
        if st.button("Logout", key="nav_logout"):
            for k in ["logged_in","user_name","user_email","last_prediction","last_inputs"]:
                st.session_state[k] = False if k=="logged_in" else (None if k in ["last_prediction","last_inputs"] else "")
            st.session_state.active_tab = "predict"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


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
            <div style="font-size:13px;color:#475569;line-height:1.8;">
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
            "experience_years":exp,"skills_count":skills,"certifications":cert,
            "job_title":job,"education_level":edu,"location":loc,
            "industry":ind,"company_size":company,"remote_work":remote,
        }
        df = pd.DataFrame([input_dict])
        df["exp_squared"]    = df["experience_years"]**2
        df["skill_per_exp"]  = df["skills_count"]/(df["experience_years"]+1)
        df["cert_per_skill"] = df["certifications"]/(df["skills_count"]+1)
        df["seniority"]      = pd.cut(df["experience_years"],bins=[0,2,5,10,20],labels=["Fresher","Junior","Mid","Senior"])
        df = pd.get_dummies(df)
        df = df.reindex(columns=columns, fill_value=0)
        num_cols = ["experience_years","skills_count","certifications","exp_squared","skill_per_exp","cert_per_skill"]
        df[num_cols] = scaler.transform(df[num_cols])
        salary = int(model.predict(df)[0])
        st.session_state.last_prediction = salary
        st.session_state.last_inputs     = input_dict
        save_prediction(st.session_state.user_email, salary, job, exp, skills)

        salary_fmt = f"₹{salary:,}"; monthly = f"₹{salary//12:,}"
        st.markdown(f"""
        <div class="result-hero">
            <div class="result-hero-label">Your Estimated Annual Salary</div>
            <div class="result-hero-amount">{salary_fmt}</div>
            <div class="result-hero-sub">≈ {monthly} / month &nbsp;·&nbsp; Powered by K-Nearest Neighbors</div>
        </div>""", unsafe_allow_html=True)

        seniority  = "Fresher" if exp<=2 else ("Junior" if exp<=5 else ("Mid-Level" if exp<=10 else "Senior"))
        potential  = f"₹{int(salary*1.35):,}"
        percentile = min(95, max(30, int(30+(salary/220000)*65)))
        m1,m2,m3,m4 = st.columns(4)
        with m1: st.markdown(f'<div class="metric-card"><div class="metric-label">Seniority Level</div><div class="metric-value" style="font-size:17px;">{seniority}</div></div>', unsafe_allow_html=True)
        with m2: st.markdown(f'<div class="metric-card"><div class="metric-label">Monthly Salary</div><div class="metric-value" style="font-size:17px;">{monthly}</div></div>', unsafe_allow_html=True)
        with m3: st.markdown(f'<div class="metric-card"><div class="metric-label">Growth Potential</div><div class="metric-value" style="font-size:17px;">{potential}</div><div class="metric-sub">↑ in 2–3 years</div></div>', unsafe_allow_html=True)
        with m4: st.markdown(f'<div class="metric-card"><div class="metric-label">Market Percentile</div><div class="metric-value" style="font-size:17px;">{percentile}th</div></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:14px 20px;margin-top:8px;">
            <span style="font-size:14px;color:#15803d;font-weight:600;">✅ Prediction saved!</span>
            <span style="font-size:13px;color:#166534;"> &nbsp;·&nbsp; Now explore your <strong>Insights</strong>, <strong>Roadmap</strong>, and <strong>Compare</strong> tabs.</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# INSIGHTS TAB
# =========================
def show_insights():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Career Insights</div>', unsafe_allow_html=True)
    if not st.session_state.last_prediction:
        st.markdown('<div style="text-align:center;padding:60px;"><div style="font-size:48px;">💡</div><div style="font-size:18px;font-weight:600;color:#0f172a;margin-top:12px;">Run a prediction first</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True); return

    inp=st.session_state.last_inputs; salary=st.session_state.last_prediction
    job=inp["job_title"]; exp=inp["experience_years"]; skills=inp["skills_count"]
    cert=inp["certifications"]; edu=inp["education_level"]; ind=inp["industry"]

    st.markdown('<div class="card"><div class="card-title">🚀 How to Increase Your Salary</div>', unsafe_allow_html=True)
    icon_map={"blue":"insight-icon-blue","green":"insight-icon-green","amber":"insight-icon-amber","rose":"insight-icon-rose"}
    for icon,title,desc,color in salary_boost_tips(job,exp,skills,cert,edu):
        st.markdown(f'<div class="insight-card"><div class="insight-icon {icon_map[color]}">{icon}</div><div><div class="insight-title">{title}</div><div class="insight-desc">{desc}</div></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_a,col_b = st.columns(2,gap="large")
    with col_a:
        top_skills=[( s,b) for s,b in zip(get_skills_to_learn(job,skills),["+₹8K–15K","+₹10K–20K","+₹6K–12K","+₹12K–25K","+₹5K–10K","+₹15K–30K"])]
        st.markdown('<div class="card"><div class="card-title">🛠️ Top Skills to Learn Next</div>', unsafe_allow_html=True)
        for i,(sk,boost) in enumerate(top_skills):
            pct=90-i*10
            st.markdown(f'<div class="compare-bar-wrap"><div class="compare-bar-label"><span style="font-size:13px;font-weight:500;color:#0f172a;">{sk}</span><span class="trend-up">{boost}/yr</span></div><div class="compare-bar-track"><div class="compare-bar-fill" style="width:{pct}%;background:linear-gradient(90deg,#6366f1,#8b5cf6);"></div></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_b:
        trend=get_industry_data(ind)
        st.markdown('<div class="card"><div class="card-title">📈 Industry Salary Trends</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px;"><div class="metric-card"><div class="metric-label">Industry Growth</div><div class="metric-value">{trend["growth"]}</div><div class="metric-sub">↑ YoY</div></div><div class="metric-card"><div class="metric-label">Job Demand</div><div class="metric-value" style="font-size:16px;">{trend["demand"]}</div></div><div class="metric-card"><div class="metric-label">Top Pay</div><div class="metric-value" style="font-size:16px;">{trend["top_pay"]}</div></div><div class="metric-card"><div class="metric-label">Outlook</div><div class="metric-value" style="font-size:16px;">{trend["outlook"]}</div></div></div><div style="background:#eef2ff;border-radius:10px;padding:14px 16px;"><div style="font-size:13px;color:#4f46e5;font-weight:600;">💡 {ind} sector insight</div><div style="font-size:13px;color:#475569;margin-top:6px;line-height:1.5;">Growing at <strong>{trend["growth"]}</strong> annually with <strong>{trend["demand"].lower()}</strong> talent demand. Top earners make <strong>{trend["top_pay"]}</strong>.</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">⚡ What-If Salary Simulator</div>', unsafe_allow_html=True)
    s1,s2,s3=st.columns(3)
    with s1:
        extra_exp=st.slider("+ Years Experience",0,10,2,key="sim_exp"); sim_e=int(salary*(1+extra_exp*0.055))
        st.markdown(f'<div class="metric-card"><div class="metric-label">+{extra_exp} yrs experience</div><div class="metric-value">₹{sim_e:,}</div><div class="metric-sub trend-up">+₹{sim_e-salary:,}</div></div>', unsafe_allow_html=True)
    with s2:
        extra_sk=st.slider("+ Skills Added",0,10,3,key="sim_skills"); sim_s=int(salary*(1+extra_sk*0.028))
        st.markdown(f'<div class="metric-card"><div class="metric-label">+{extra_sk} skills</div><div class="metric-value">₹{sim_s:,}</div><div class="metric-sub trend-up">+₹{sim_s-salary:,}</div></div>', unsafe_allow_html=True)
    with s3:
        extra_c=st.slider("+ Certifications",0,5,1,key="sim_cert"); sim_c=int(salary*(1+extra_c*0.04))
        st.markdown(f'<div class="metric-card"><div class="metric-label">+{extra_c} certifications</div><div class="metric-value">₹{sim_c:,}</div><div class="metric-sub trend-up">+₹{sim_c-salary:,}</div></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


# =========================
# ROADMAP TAB
# =========================
def show_roadmap():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Career Roadmap</div>', unsafe_allow_html=True)
    if not st.session_state.last_inputs:
        st.markdown('<div style="text-align:center;padding:60px;"><div style="font-size:48px;">🗺️</div><div style="font-size:18px;font-weight:600;color:#0f172a;margin-top:12px;">Run a prediction first</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True); return

    inp=st.session_state.last_inputs; job=inp["job_title"]; exp=inp["experience_years"]
    steps=get_roadmap(job)
    current_step=0 if exp<=2 else(1 if exp<=5 else(2 if exp<=10 else(3 if exp<=15 else 4)))

    col_r,col_i=st.columns([3,2],gap="large")
    with col_r:
        salary_ranges=["₹40K–70K","₹70K–1.1L","₹1.1L–1.6L","₹1.6L–2.0L","₹2.0L+"]
        exp_ranges=["0–2 yrs","2–5 yrs","5–10 yrs","10–15 yrs","15+ yrs"]
        st.markdown(f'<div class="card"><div class="card-title">🗺️ Your Career Path — {job}</div>', unsafe_allow_html=True)
        for i,step in enumerate(steps):
            if i<current_step:   dot="step-dot-done"; badge="badge-done";    btxt="✓ Completed"
            elif i==current_step:dot="step-dot-curr"; badge="badge-current"; btxt="📍 You are here"
            else:                dot="step-dot-next"; badge="badge-future";  btxt=f"Next · {exp_ranges[i]}"
            st.markdown(f'<div class="roadmap-step"><div class="step-dot {dot}">{i+1}</div><div><div class="step-title">{step}</div><div class="step-sub">{exp_ranges[i]} · {salary_ranges[i]}</div><span class="step-badge {badge}">{btxt}</span></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_i:
        curr=steps[current_step]; nxt=steps[min(current_step+1,len(steps)-1)]; sk=get_skills_to_learn(job,0)[:4]
        st.markdown(f'<div class="card" style="background:linear-gradient(135deg,#eef2ff,#f5f3ff);border-color:#c7d2fe;margin-bottom:12px;"><div class="card-title" style="color:#4f46e5;">🎯 Your Next Goal</div><div style="font-size:19px;font-weight:700;color:#1e1b4b;margin-bottom:8px;">{nxt}</div><div style="font-size:13px;color:#4338ca;line-height:1.6;">Currently at <strong>{curr}</strong>. Build 1–2 impactful projects and apply for senior roles.</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><div class="card-title">🛠️ Skills for Next Level</div>', unsafe_allow_html=True)
        for s in sk:
            st.markdown(f'<span style="display:inline-block;background:#eef2ff;color:#4f46e5;border-radius:99px;padding:5px 14px;font-size:13px;font-weight:500;margin:4px;border:1px solid #c7d2fe;">{s}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><div class="card-title">📅 Estimated Timeline</div><div style="font-size:13px;color:#475569;line-height:2.0;">🟣 &nbsp;<strong>Now:</strong> {steps[current_step]}<br>🟢 &nbsp;<strong>1–2 yrs:</strong> {steps[min(current_step+1,len(steps)-1)]}<br>🔵 &nbsp;<strong>3–5 yrs:</strong> {steps[min(current_step+2,len(steps)-1)]}<br>⭐ &nbsp;<strong>5–8 yrs:</strong> {steps[-1]}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# DASHBOARD TAB
# =========================
def show_dashboard():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">My Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Your personal prediction history and statistics.</div>', unsafe_allow_html=True)

    users=load_users(); preds=users.get(st.session_state.user_email,{}).get("predictions",[])
    if not preds:
        st.markdown('<div style="text-align:center;padding:60px;"><div style="font-size:48px;">📊</div><div style="font-size:18px;font-weight:600;color:#0f172a;margin-top:12px;">No predictions yet</div><div style="font-size:14px;color:#64748b;">Head to the Predict tab!</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True); return

    salaries=[p["salary"] for p in preds]; avg_sal=int(sum(salaries)/len(salaries)); best_sal=max(salaries)
    m1,m2,m3,m4=st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Predictions</div><div class="metric-value">{len(preds)}</div></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><div class="metric-label">Latest Salary</div><div class="metric-value" style="font-size:18px;">₹{salaries[-1]:,}</div></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><div class="metric-label">Average Salary</div><div class="metric-value" style="font-size:18px;">₹{avg_sal:,}</div></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><div class="metric-label">Best Prediction</div><div class="metric-value" style="font-size:18px;">₹{best_sal:,}</div><div class="metric-sub">↑ Your peak</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="card" style="margin-top:12px;"><div class="card-title">📋 Prediction History</div>', unsafe_allow_html=True)
    st.markdown('<div style="display:flex;gap:12px;padding:8px 0;border-bottom:1px solid #f1f5f9;"><span style="flex:.4;font-size:11px;font-weight:700;color:#94a3b8;">#</span><span style="flex:2;font-size:11px;font-weight:700;color:#94a3b8;">ROLE</span><span style="flex:1;font-size:11px;font-weight:700;color:#94a3b8;">EXP</span><span style="flex:1;font-size:11px;font-weight:700;color:#94a3b8;">SKILLS</span><span style="flex:1.5;font-size:11px;font-weight:700;color:#94a3b8;">SALARY</span><span style="flex:1.5;font-size:11px;font-weight:700;color:#94a3b8;">DATE</span></div>', unsafe_allow_html=True)
    for i,p in enumerate(reversed(preds[-10:]),1):
        is_best=p["salary"]==best_sal
        st.markdown(f'<div style="display:flex;gap:12px;padding:11px 0;border-bottom:1px solid #f8fafc;align-items:center;"><span style="flex:.4;font-size:13px;color:#94a3b8;">{i}</span><span style="flex:2;font-size:13px;font-weight:500;color:#0f172a;">{p.get("job","—")}</span><span style="flex:1;font-size:13px;color:#64748b;">{p.get("exp",0)} yrs</span><span style="flex:1;font-size:13px;color:#64748b;">{p.get("skills",0)}</span><span style="flex:1.5;font-size:14px;font-weight:700;color:#4f46e5;">₹{p["salary"]:,}{"&nbsp;⭐" if is_best else ""}</span><span style="flex:1.5;font-size:12px;color:#94a3b8;">{p.get("date","—")}</span></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


# =========================
# COMPARE TAB
# =========================
def show_compare():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Compare Yourself</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">See how your predicted salary stacks up against market benchmarks.</div>', unsafe_allow_html=True)
    if not st.session_state.last_prediction:
        st.markdown('<div style="text-align:center;padding:60px;"><div style="font-size:48px;">⚖️</div><div style="font-size:18px;font-weight:600;color:#0f172a;margin-top:12px;">Run a prediction first</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True); return

    salary=st.session_state.last_prediction; inp=st.session_state.last_inputs; job=inp["job_title"]
    base=max(40000,salary-random.randint(10000,20000))
    top25=int(salary*1.22); top10=int(salary*1.48); top5=int(salary*1.75); max_v=top5
    benchmarks=[("Entry Level (0–2 yrs)",int(base*0.6),"#e2e8f0"),("Mid Level (3–6 yrs)",int(base*0.85),"#c7d2fe"),("Your Salary",salary,"#6366f1"),("Top 25% in your role",top25,"#8b5cf6"),("Top 10% in your role",top10,"#7c3aed"),("Top 5% — Elite earner",top5,"#4338ca")]

    col1,col2=st.columns([3,2],gap="large")
    with col1:
        st.markdown(f'<div class="card"><div class="card-title">📊 Salary Benchmarks — {job}</div>', unsafe_allow_html=True)
        for label,val,color in benchmarks:
            pct=int((val/max_v)*100); is_you=label=="Your Salary"
            st.markdown(f'<div class="compare-bar-wrap" style="{"background:#eef2ff;border-radius:8px;padding:8px 10px;border:1px solid #c7d2fe;" if is_you else ""}"><div class="compare-bar-label"><span style="font-size:13px;font-weight:{"700" if is_you else "500"};color:{"#4f46e5" if is_you else "#374151"};"> {"📍 " if is_you else ""}{label}</span><span style="font-size:13px;font-weight:600;color:{"#4f46e5" if is_you else "#0f172a"};">₹{val:,}</span></div><div class="compare-bar-track"><div class="compare-bar-fill" style="width:{pct}%;background:{color};"></div></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        pct_rank=min(95,max(25,int(30+(salary/top5)*65))); gap=max(0,top10-salary)
        st.markdown(f'<div class="card" style="text-align:center;margin-bottom:12px;"><div class="card-title">🎯 Your Market Position</div><div style="font-size:52px;font-weight:800;font-family:\'Syne\',sans-serif;background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{pct_rank}th</div><div style="font-size:14px;color:#64748b;">percentile in your field</div><div style="font-size:13px;color:#475569;margin-top:12px;line-height:1.6;">You earn more than <strong>{pct_rank}%</strong> of professionals in similar roles.</div></div><div class="card"><div class="card-title">💰 Gap to Top 10%</div><div style="font-size:24px;font-weight:800;color:#4f46e5;font-family:\'Syne\',sans-serif;">{"Already there! 🎉" if gap==0 else f"₹{gap:,}"}</div><div style="font-size:13px;color:#64748b;margin-top:6px;line-height:1.5;">{"You have already cracked the top 10%!" if gap==0 else "Add 2–3 high-demand skills to close this gap."}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# LEADERBOARD TAB
# =========================
def show_leaderboard():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Leaderboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Top predicted salaries across all SalaryIQ Pro users.</div>', unsafe_allow_html=True)

    lb=get_leaderboard(); users=load_users()
    my_ps=users.get(st.session_state.user_email,{}).get("predictions",[])
    my_b=max([p["salary"] for p in my_ps],default=0)

    if my_b:
        my_rank=sum(1 for e in lb if e["salary"]>my_b)+1
        st.markdown(f'<div style="background:linear-gradient(135deg,#eef2ff,#f5f3ff);border:1px solid #c7d2fe;border-radius:14px;padding:18px 24px;margin-bottom:20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;"><div><div style="font-size:11px;color:#6366f1;font-weight:700;text-transform:uppercase;">Your Position</div><div style="font-size:22px;font-weight:800;color:#1e1b4b;font-family:\'Syne\',sans-serif;">#{my_rank} <span style="font-size:14px;color:#64748b;font-weight:400;">out of {len(lb)} users</span></div></div><div style="text-align:right;"><div style="font-size:11px;color:#6366f1;font-weight:700;text-transform:uppercase;">Your Best</div><div style="font-size:22px;font-weight:800;color:#4f46e5;font-family:\'Syne\',sans-serif;">₹{my_b:,}</div></div></div>', unsafe_allow_html=True)

    if not lb:
        st.markdown('<div style="text-align:center;padding:40px;color:#94a3b8;font-size:14px;">No predictions yet. Be the first!</div>', unsafe_allow_html=True)
    else:
        medals=["🥇","🥈","🥉"]; row_cls=["gold","silver","bronze"]
        for i,entry in enumerate(lb):
            medal=medals[i] if i<3 else f"#{i+1}"; cls=row_cls[i] if i<3 else ""
            st.markdown(f'<div class="lb-row {cls}"><span class="lb-rank">{medal}</span><div style="flex:1;min-width:100px;"><div class="lb-name">{entry["name"]}</div><div class="lb-role">{entry["job"]} · {entry["exp"]} yrs exp</div></div><span class="lb-salary">₹{entry["salary"]:,}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# MAIN ROUTER
# =========================
if not st.session_state.logged_in:
    if st.session_state.auth_page == "login":
        show_login()
    else:
        show_signup()
else:
    show_nav()
    tab = st.session_state.active_tab
    if   tab == "predict":     show_predict()
    elif tab == "insights":    show_insights()
    elif tab == "roadmap":     show_roadmap()
    elif tab == "dashboard":   show_dashboard()
    elif tab == "compare":     show_compare()
    elif tab == "leaderboard": show_leaderboard()

