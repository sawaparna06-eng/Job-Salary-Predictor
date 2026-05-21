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
    initial_sidebar_state="expanded"
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

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def register_user(name, email, password):
    users = load_users()
    if email.lower() in users:
        return False, "An account with this email already exists."
    users[email.lower()] = {
        "name": name, "email": email.lower(),
        "password": hash_password(password),
        "created_at": datetime.now().isoformat(),
        "predictions": [],
        "bio": "", "phone": "", "location_city": "", "linkedin": "",
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
        users[email.lower()].setdefault("predictions", []).append({
            "salary": salary, "job": job, "exp": exp,
            "skills": skills, "date": datetime.now().strftime("%d %b %Y")
        })
        save_users(users)

def update_user_profile(email, name, bio, phone, location_city, linkedin):
    users = load_users()
    if email.lower() in users:
        u = users[email.lower()]
        u["name"] = name; u["bio"] = bio; u["phone"] = phone
        u["location_city"] = location_city; u["linkedin"] = linkedin
        save_users(users)
        return True
    return False

def update_user_password(email, old_pw, new_pw):
    users = load_users()
    if email.lower() not in users:
        return False, "User not found."
    if users[email.lower()]["password"] != hash_password(old_pw):
        return False, "Current password is incorrect."
    users[email.lower()]["password"] = hash_password(new_pw)
    save_users(users)
    return True, "Password updated!"

def get_user_data(email):
    return load_users().get(email.lower(), {})

def is_valid_email(email):
    return re.match(r"^[\w\.\-]+@[\w\.\-]+\.\w{2,}$", email) is not None

# =========================
# CAREER DATA
# =========================
SKILLS_BY_ROLE = {
    "Data Scientist":            ["Python","Machine Learning","Deep Learning","SQL","Statistics","TensorFlow","Spark"],
    "Software Engineer":         ["System Design","DSA","Cloud (AWS/GCP)","Docker","Kubernetes","CI/CD","Microservices"],
    "AI Engineer":               ["LLMs","PyTorch","MLOps","Vector Databases","Prompt Engineering","Transformers","CUDA"],
    "Data Analyst":              ["Power BI","Tableau","Advanced SQL","Python","Excel","Statistical Analysis","DAX"],
    "Machine Learning Engineer": ["MLOps","Feature Engineering","Model Deployment","Kubeflow","PyTorch","Scalable ML"],
    "DevOps Engineer":           ["Kubernetes","Terraform","AWS","CI/CD","Monitoring","Docker","Linux"],
    "Cloud Engineer":            ["AWS/Azure/GCP","Terraform","Networking","Security","Serverless","Cost Optimization"],
    "Cybersecurity Analyst":     ["Ethical Hacking","SIEM","Incident Response","Network Security","Compliance","Forensics"],
    "Product Manager":           ["Roadmapping","OKRs","User Research","A/B Testing","SQL","Stakeholder Management"],
    "Business Analyst":          ["Power BI","Process Mapping","SQL","Requirements Gathering","Agile","JIRA"],
    "Frontend Developer":        ["React","TypeScript","Next.js","Tailwind CSS","GraphQL","Web Performance","Testing"],
    "Backend Developer":         ["Node.js","PostgreSQL","Redis","REST APIs","System Design","Docker","Message Queues"],
    "Other":                     ["Communication","Project Management","Data Analysis","Cloud Basics","Agile","Python"],
}
ROADMAP_BY_ROLE = {
    "Data Scientist":            ["Junior Data Analyst","Data Scientist","Senior Data Scientist","Lead / Staff DS","Head of Data Science"],
    "Software Engineer":         ["Junior Developer","Software Engineer","Senior Engineer","Staff Engineer","Principal / VP Eng"],
    "AI Engineer":               ["ML Engineer","AI Engineer","Senior AI Engineer","AI Tech Lead","AI Research Director"],
    "Data Analyst":              ["Junior Analyst","Data Analyst","Senior Analyst","Analytics Manager","Director of Analytics"],
    "Machine Learning Engineer": ["Junior ML Engineer","ML Engineer","Senior ML Engineer","ML Tech Lead","Head of ML"],
    "DevOps Engineer":           ["Junior DevOps","DevOps Engineer","Senior DevOps","Platform Lead","VP Infrastructure"],
    "Cloud Engineer":            ["Cloud Support","Cloud Engineer","Senior Cloud Engineer","Cloud Architect","CTO / VP Cloud"],
    "Cybersecurity Analyst":     ["Security Analyst","Senior Analyst","Security Lead","CISO Director","Chief Security Officer"],
    "Product Manager":           ["Associate PM","Product Manager","Senior PM","Group PM","VP / CPO"],
    "Business Analyst":          ["Junior BA","Business Analyst","Senior BA","BA Manager","Director of Strategy"],
    "Frontend Developer":        ["Junior Frontend","Frontend Developer","Senior Frontend","Frontend Lead","Head of Frontend"],
    "Backend Developer":         ["Junior Backend","Backend Developer","Senior Backend","Backend Lead","Engineering Manager"],
    "Other":                     ["Entry Level","Mid Level","Senior Level","Lead / Manager","Director / VP"],
}
INDUSTRY_TRENDS = {
    "Technology":    {"growth":"22%","outlook":"Excellent","top_pay":"₹1,80,000","demand":"Very High"},
    "Finance":       {"growth":"15%","outlook":"Strong",   "top_pay":"₹1,60,000","demand":"High"},
    "Healthcare":    {"growth":"18%","outlook":"Excellent","top_pay":"₹1,40,000","demand":"Very High"},
    "Consulting":    {"growth":"12%","outlook":"Strong",   "top_pay":"₹1,70,000","demand":"High"},
    "Manufacturing": {"growth":"8%", "outlook":"Moderate", "top_pay":"₹1,10,000","demand":"Moderate"},
    "Education":     {"growth":"10%","outlook":"Stable",   "top_pay":"₹90,000",  "demand":"Moderate"},
    "Retail":        {"growth":"7%", "outlook":"Moderate", "top_pay":"₹95,000",  "demand":"Moderate"},
    "Media":         {"growth":"9%", "outlook":"Moderate", "top_pay":"₹1,00,000","demand":"Moderate"},
    "Telecom":       {"growth":"11%","outlook":"Strong",   "top_pay":"₹1,30,000","demand":"High"},
    "Government":    {"growth":"6%", "outlook":"Stable",   "top_pay":"₹85,000",  "demand":"Low"},
    "Other":         {"growth":"10%","outlook":"Moderate", "top_pay":"₹1,00,000","demand":"Moderate"},
}

# =========================
# SESSION STATE
# =========================
for k, v in [("logged_in",False),("user_name",""),("user_email",""),
             ("auth_page","login"),("active_tab","predict"),
             ("last_prediction",None),("last_inputs",None),
             ("sidebar_section","info")]:
    if k not in st.session_state:
        st.session_state[k] = v

# =========================
# HELPERS
# =========================
def get_initials(name):
    parts = name.strip().split()
    return (parts[0][0] + (parts[1][0] if len(parts)>1 else "")).upper()

def salary_boost_tips(job, exp, skills, cert, edu):
    tips = []
    if exp < 3:   tips.append(("🚀","Build a strong portfolio","Create 3–5 GitHub projects. At junior levels, projects matter more than years of experience.","blue"))
    if 3<=exp<7:  tips.append(("📈","Apply for senior roles now","Senior roles pay 35–50% more. Highlight impact and outcomes on your resume.","green"))
    if exp >= 7:  tips.append(("🏆","Move into leadership","Lead/Manager roles pay 50–80% more than individual contributor positions.","amber"))
    if skills<8:  tips.append(("🛠️","Expand your skill set","Professionals with 10+ skills earn 28% more. Focus on cloud, data, or AI tools.","rose"))
    if cert < 2:  tips.append(("📜","Earn certifications","AWS, Google Cloud, PMP add ₹10K–₹25K to your annual salary.","blue"))
    if edu in ["High School","Diploma","Other"]:
        tips.append(("🎓","Upskill with online courses","Online Master's or diplomas boost salary 15–20%. Try Coursera or edX.","green"))
    tips.append(("🌍","Target remote / global roles","Remote roles at global companies pay 2–4x Indian market rates.","amber"))
    tips.append(("💬","Negotiate your salary","60% of professionals never negotiate. Ask for 15–20% above the offer.","rose"))
    return tips

def get_skills_to_learn(job, _):    return SKILLS_BY_ROLE.get(job, SKILLS_BY_ROLE["Other"])[:6]
def get_roadmap(job):               return ROADMAP_BY_ROLE.get(job, ROADMAP_BY_ROLE["Other"])
def get_industry_data(ind):         return INDUSTRY_TRENDS.get(ind, INDUSTRY_TRENDS["Other"])

def get_leaderboard():
    users = load_users(); lb = []
    for email, data in users.items():
        preds = data.get("predictions",[])
        if preds:
            best = max(preds, key=lambda x: x["salary"])
            lb.append({"name":data["name"],"salary":best["salary"],
                       "job":best.get("job","Professional"),"exp":best.get("exp",0)})
    lb.sort(key=lambda x: x["salary"], reverse=True)
    return lb[:10]

# =========================
# GLOBAL CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap');

html, body, [class*="css"] { font-family:'Plus Jakarta Sans',sans-serif !important; }
#MainMenu, footer, header, .stDeployButton { visibility:hidden !important; display:none !important; }

/* ── remove ALL default top padding so auth card sits at top ── */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 100% !important;
}
[data-testid="stAppViewContainer"] > section > div:first-child { padding-top: 0 !important; }

.stApp { background: #f0f2f8 !important; }

/* ── Auth full-page wrapper ── */
.auth-bg {
    min-height: 100vh;
    background: linear-gradient(135deg,#eef0fb 0%,#f4f0ff 55%,#edfaf3 100%);
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding: 48px 20px 40px;
}
.auth-card {
    background: #fff;
    border-radius: 24px;
    padding: 40px 40px 32px;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.04), 0 20px 60px rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.10);
}
.auth-brand {
    font-family:'Syne',sans-serif !important;
    font-size:18px; font-weight:800; color:#1e1b4b;
    margin-bottom:22px; display:flex; align-items:center; gap:8px;
}
.auth-brand em { color:#6366f1; font-style:normal; }
.auth-title {
    font-family:'Syne',sans-serif !important;
    font-size:28px; font-weight:800; color:#0f172a;
    line-height:1.2; margin-bottom:6px;
}
.auth-title span {
    background:linear-gradient(135deg,#6366f1,#8b5cf6);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.auth-sub { font-size:13px; color:#64748b; margin-bottom:22px; }
.auth-stats {
    display:flex; border-radius:12px; overflow:hidden;
    border:1px solid #e2e8f0; margin-bottom:24px;
}
.auth-stat {
    flex:1; text-align:center; padding:12px 8px;
    border-right:1px solid #e2e8f0; background:#f8fafc;
}
.auth-stat:last-child { border-right:none; }
.auth-stat-v {
    font-family:'Syne',sans-serif !important; font-size:17px; font-weight:800;
    background:linear-gradient(135deg,#6366f1,#8b5cf6);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.auth-stat-l { font-size:10px; color:#94a3b8; text-transform:uppercase; letter-spacing:.6px; margin-top:2px; }
.auth-divider {
    text-align:center; color:#cbd5e1; font-size:12px;
    margin:12px 0; position:relative;
}
.auth-divider::before,.auth-divider::after {
    content:''; position:absolute; top:50%;
    width:calc(50% - 20px); height:1px; background:#e2e8f0;
}
.auth-divider::before { left:0; } .auth-divider::after { right:0; }

/* ── Inputs ── */
.stTextInput>div>div {
    background:#f8fafc !important; border:1.5px solid #e2e8f0 !important; border-radius:10px !important;
}
.stTextInput>div>div:focus-within {
    border-color:#6366f1 !important; box-shadow:0 0 0 3px rgba(99,102,241,.12) !important; background:#fff !important;
}
.stTextInput input { color:#0f172a !important; background:transparent !important; font-size:14px !important; box-shadow:none !important; -webkit-box-shadow:none !important; }
.stTextInput input::placeholder { color:#94a3b8 !important; }
.stTextInput label { color:#475569 !important; font-size:13px !important; font-weight:500 !important; }

.stNumberInput>div>div { background:#f8fafc !important; border:1.5px solid #e2e8f0 !important; border-radius:10px !important; }
.stNumberInput>div>div:focus-within { border-color:#6366f1 !important; box-shadow:0 0 0 3px rgba(99,102,241,.12) !important; }
.stNumberInput input { color:#0f172a !important; background:transparent !important; font-size:14px !important; box-shadow:none !important; }
.stNumberInput label { color:#475569 !important; font-size:13px !important; font-weight:500 !important; }
.stNumberInput button { color:#6366f1 !important; }

.stSelectbox>div>div { background:#f8fafc !important; border:1.5px solid #e2e8f0 !important; border-radius:10px !important; }
.stSelectbox>div>div:focus-within { border-color:#6366f1 !important; box-shadow:0 0 0 3px rgba(99,102,241,.12) !important; }
.stSelectbox [data-baseweb="select"]>div,
.stSelectbox [data-baseweb="select"] span { color:#0f172a !important; background:transparent !important; }
.stSelectbox label { color:#475569 !important; font-size:13px !important; font-weight:500 !important; }
[data-baseweb="popover"],[data-baseweb="menu"],[role="listbox"] {
    background:#fff !important; border:1px solid #e2e8f0 !important;
    border-radius:12px !important; box-shadow:0 8px 32px rgba(0,0,0,.12) !important;
}
[data-baseweb="menu"] li,[role="option"] { background:#fff !important; color:#1e293b !important; font-size:14px !important; }
[data-baseweb="menu"] li:hover,[role="option"]:hover,[role="option"][aria-selected="true"] { background:#eef2ff !important; color:#4f46e5 !important; }

.stTextArea>div>div { background:#f8fafc !important; border:1.5px solid #e2e8f0 !important; border-radius:10px !important; }
.stTextArea>div>div:focus-within { border-color:#6366f1 !important; box-shadow:0 0 0 3px rgba(99,102,241,.12) !important; }
.stTextArea textarea { color:#0f172a !important; background:transparent !important; font-size:14px !important; }
.stTextArea label { color:#475569 !important; font-size:13px !important; font-weight:500 !important; }

/* ── Buttons ── */
.stButton>button {
    width:100% !important;
    background:linear-gradient(135deg,#6366f1,#8b5cf6) !important;
    color:#fff !important; border:none !important; border-radius:10px !important;
    padding:12px 20px !important; font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:14px !important; font-weight:600 !important;
    box-shadow:0 4px 14px rgba(99,102,241,.3) !important; transition:all .2s !important;
}
.stButton>button:hover { transform:translateY(-1px) !important; box-shadow:0 6px 20px rgba(99,102,241,.4) !important; }

.signout-btn>button {
    background:#fff1f2 !important; color:#ef4444 !important;
    border:1.5px solid #fecaca !important; box-shadow:none !important;
    font-size:13px !important; padding:8px 16px !important;
}
.ghost-btn>button {
    background:#fff !important; color:#475569 !important;
    border:1.5px solid #e2e8f0 !important; box-shadow:none !important;
    font-size:14px !important;
}
.ghost-btn>button:hover { background:#f8fafc !important; }

/* ── Top nav ── */
.top-nav {
    background:#fff; border-bottom:1px solid #e2e8f0;
    padding:0 28px; display:flex; align-items:center; justify-content:space-between;
    height:56px; box-shadow:0 1px 4px rgba(0,0,0,.05);
}
.nav-brand { font-family:'Syne',sans-serif !important; font-size:18px; font-weight:800; color:#1e1b4b; }
.nav-brand em { color:#6366f1; font-style:normal; }
.nav-right { display:flex; align-items:center; gap:10px; }
.nav-avatar {
    width:36px; height:36px; border-radius:50%;
    background:linear-gradient(135deg,#6366f1,#8b5cf6);
    display:flex; align-items:center; justify-content:center;
    font-size:13px; font-weight:700; color:#fff;
    box-shadow:0 2px 8px rgba(99,102,241,.35);
}
.nav-name { font-size:13px; font-weight:600; color:#334155; }

/* ── Page ── */
.page-wrap { padding:28px 36px; max-width:1200px; margin:0 auto; }
.page-title { font-family:'Syne',sans-serif !important; font-size:24px; font-weight:800; color:#0f172a; margin-bottom:4px; }
.page-sub   { font-size:14px; color:#64748b; margin-bottom:24px; }

/* ── Cards ── */
.card { background:#fff; border-radius:16px; border:1px solid #e2e8f0; padding:22px; box-shadow:0 1px 3px rgba(0,0,0,.04); margin-bottom:16px; }
.card-title { font-size:11px; font-weight:700; color:#6366f1; text-transform:uppercase; letter-spacing:1px; margin-bottom:16px; }
.metric-card { background:#fff; border:1px solid #e2e8f0; border-radius:14px; padding:18px 16px; box-shadow:0 1px 3px rgba(0,0,0,.04); }
.metric-label { font-size:12px; color:#94a3b8; font-weight:500; margin-bottom:6px; }
.metric-value { font-family:'Syne',sans-serif !important; font-size:22px; font-weight:800; color:#0f172a; }
.metric-sub   { font-size:12px; color:#10b981; font-weight:500; margin-top:4px; }
.result-hero { background:linear-gradient(135deg,#6366f1 0%,#8b5cf6 100%); border-radius:20px; padding:36px 32px; text-align:center; margin-bottom:20px; box-shadow:0 8px 32px rgba(99,102,241,.3); }
.result-hero-label  { font-size:12px; color:rgba(255,255,255,.7); letter-spacing:1.5px; text-transform:uppercase; }
.result-hero-amount { font-family:'Syne',sans-serif !important; font-size:56px; font-weight:800; color:#fff; margin:8px 0; }
.result-hero-sub    { font-size:13px; color:rgba(255,255,255,.6); }
.insight-card { background:#fff; border-radius:12px; border:1px solid #e2e8f0; padding:18px; margin-bottom:10px; display:flex; gap:14px; align-items:flex-start; }
.insight-icon { width:38px; height:38px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:18px; flex-shrink:0; }
.insight-icon-blue  { background:#eef2ff; } .insight-icon-green { background:#f0fdf4; }
.insight-icon-amber { background:#fffbeb; } .insight-icon-rose  { background:#fff1f2; }
.insight-title { font-size:14px; font-weight:600; color:#0f172a; margin-bottom:4px; }
.insight-desc  { font-size:13px; color:#64748b; line-height:1.5; }
.roadmap-step { display:flex; gap:16px; align-items:flex-start; padding:18px 0; border-bottom:1px solid #f1f5f9; }
.roadmap-step:last-child { border-bottom:none; }
.step-dot { width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; flex-shrink:0; margin-top:2px; }
.step-dot-done { background:#6366f1; color:#fff; }
.step-dot-curr { background:linear-gradient(135deg,#6366f1,#8b5cf6); color:#fff; box-shadow:0 0 0 4px rgba(99,102,241,.2); }
.step-dot-next { background:#f1f5f9; color:#94a3b8; border:2px dashed #cbd5e1; }
.step-title { font-size:15px; font-weight:600; color:#0f172a; }
.step-sub   { font-size:13px; color:#64748b; margin-top:3px; }
.step-badge { display:inline-block; font-size:11px; font-weight:600; padding:2px 10px; border-radius:99px; margin-top:6px; }
.badge-current { background:#eef2ff; color:#4f46e5; }
.badge-done    { background:#f0fdf4; color:#15803d; }
.badge-future  { background:#f8fafc; color:#94a3b8; }
.lb-row { display:flex; align-items:center; gap:14px; padding:14px 16px; border-radius:12px; margin-bottom:8px; background:#f8fafc; border:1px solid #f1f5f9; transition:all .15s; }
.lb-row:hover { background:#eef2ff; border-color:#c7d2fe; }
.lb-row.gold   { background:linear-gradient(135deg,#fffbeb,#fef3c7); border-color:#fde68a; }
.lb-row.silver { background:linear-gradient(135deg,#f8fafc,#f1f5f9); border-color:#e2e8f0; }
.lb-row.bronze { background:linear-gradient(135deg,#fff7ed,#ffedd5); border-color:#fed7aa; }
.lb-rank   { font-family:'Syne',sans-serif !important; font-size:16px; font-weight:800; min-width:28px; }
.lb-name   { flex:1; font-size:14px; font-weight:600; color:#0f172a; }
.lb-role   { font-size:12px; color:#64748b; }
.lb-salary { font-family:'Syne',sans-serif !important; font-size:16px; font-weight:800; color:#4f46e5; }
.compare-bar-wrap  { margin-bottom:14px; }
.compare-bar-label { display:flex; justify-content:space-between; font-size:13px; margin-bottom:5px; }
.compare-bar-track { height:8px; background:#f1f5f9; border-radius:99px; overflow:hidden; }
.compare-bar-fill  { height:100%; border-radius:99px; }
.trend-up { color:#10b981; font-weight:600; font-size:13px; }
.pw-track { height:4px; background:#e2e8f0; border-radius:99px; overflow:hidden; margin-bottom:6px; }
.pw-bar   { height:100%; border-radius:99px; transition:width .3s,background .3s; }

/* ── Sidebar: fixed position, full height, internal scroll ── */
section[data-testid="stSidebar"] {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    height: 100vh !important;
    width: 280px !important;
    min-width: 280px !important;
    max-width: 280px !important;
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
    box-shadow: 4px 0 24px rgba(0,0,0,.08) !important;
    z-index: 200 !important;
    overflow: hidden !important;
    display: flex !important;
    flex-direction: column !important;
}
/* The inner scrollable wrapper Streamlit creates */
section[data-testid="stSidebar"] > div:first-child {
    height: 100vh !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
    display: flex !important;
    flex-direction: column !important;
}
/* Remove ALL default gap/padding from vertical blocks inside sidebar */
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0 !important;
    padding: 0 !important;
}
/* Hide collapse button */
[data-testid="stSidebarCollapseButton"],
button[data-testid="baseButton-headerNoPadding"],
[data-testid="collapsedControl"] {
    display: none !important;
    visibility: hidden !important;
}
/* Push main content right so it doesn't hide behind fixed sidebar */
section[data-testid="stMain"],
[data-testid="stAppViewContainer"] > section.main {
    margin-left: 280px !important;
}
section[data-testid="stSidebar"] .stMarkdown { margin: 0 !important; }
section[data-testid="stSidebar"] .stButton  { margin: 2px 0 !important; }
/* Thin scrollbar inside sidebar */
section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar { width: 4px; }
section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-track { background: #f8fafc; }
section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb { background: #c7d2fe; border-radius: 99px; }

h1,h2,h3 { font-family:'Syne',sans-serif !important; color:#0f172a !important; }
p,li { color:#475569; }
</style>
""", unsafe_allow_html=True)


# =====================================================
# AUTH PAGES  —  card rendered inside a centered column
# so HTML card header and Streamlit inputs are TOGETHER
# =====================================================

def show_login():
    # Full-page gradient background via fixed div
    st.markdown("""
    <div style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-1;
         background:linear-gradient(135deg,#eef0fb 0%,#f4f0ff 55%,#edfaf3 100%);"></div>
    """, unsafe_allow_html=True)

    # Tight centered column — max ~420 px wide
    gap, col, gap2 = st.columns([1, 1.5, 1])
    with col:
        # Card header (pure HTML — no interactive elements)
        st.markdown("""
        <div class="auth-card">
            <div class="auth-brand">💼 Salary<em>IQ</em>
                <span style="font-size:11px;color:#94a3b8;font-weight:400;margin-left:2px;">PRO</span>
            </div>
            <div class="auth-title">Welcome<br><span>back.</span></div>
            <div class="auth-sub">Sign in to your career intelligence dashboard</div>
            <div class="auth-stats">
                <div class="auth-stat"><div class="auth-stat-v">95%</div><div class="auth-stat-l">Accuracy</div></div>
                <div class="auth-stat"><div class="auth-stat-v">50K+</div><div class="auth-stat-l">Predictions</div></div>
                <div class="auth-stat"><div class="auth-stat-v">120+</div><div class="auth-stat-l">Job Roles</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Streamlit inputs rendered immediately below — visually inside card area
        email    = st.text_input("Email address", placeholder="you@example.com", key="login_email")
        password = st.text_input("Password",      placeholder="Your password",    key="login_pw", type="password")

        if st.button("Sign In →", key="login_btn"):
            if not email or not password:
                st.error("Please fill in all fields.")
            elif not is_valid_email(email):
                st.error("Please enter a valid email address.")
            else:
                ok, result = login_user(email, password)
                if ok:
                    st.session_state.logged_in  = True
                    st.session_state.user_name  = result
                    st.session_state.user_email = email.lower()
                    st.rerun()
                else:
                    st.error(result)

        st.markdown('<div class="auth-divider">or</div>', unsafe_allow_html=True)

        st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
        if st.button("Create a free account →", key="goto_signup"):
            st.session_state.auth_page = "signup"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<p style='text-align:center;font-size:12px;color:#94a3b8;margin-top:12px;'>🔒 Your data is private and never shared.</p>", unsafe_allow_html=True)


def show_signup():
    st.markdown("""
    <div style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-1;
         background:linear-gradient(135deg,#eef0fb 0%,#f4f0ff 55%,#edfaf3 100%);"></div>
    """, unsafe_allow_html=True)

    gap, col, gap2 = st.columns([1, 1.5, 1])
    with col:
        st.markdown("""
        <div class="auth-card">
            <div class="auth-brand">💼 Salary<em>IQ</em>
                <span style="font-size:11px;color:#94a3b8;font-weight:400;margin-left:2px;">PRO</span>
            </div>
            <div class="auth-title">Create your<br><span>account.</span></div>
            <div class="auth-sub">Join professionals discovering their true market value</div>
        </div>
        """, unsafe_allow_html=True)

        name    = st.text_input("Full Name",        placeholder="John Doe",             key="su_name")
        email   = st.text_input("Email Address",    placeholder="you@example.com",      key="su_email")
        pw      = st.text_input("Password",         placeholder="Min. 8 characters",    key="su_pw",   type="password")
        confirm = st.text_input("Confirm Password", placeholder="Repeat your password", key="su_conf", type="password")

        if pw:
            s, hints = 0, []
            if len(pw)>=8:                    s+=1
            else:                             hints.append("8+ chars")
            if re.search(r"[A-Z]",pw):        s+=1
            else:                             hints.append("uppercase")
            if re.search(r"\d",pw):           s+=1
            else:                             hints.append("number")
            if re.search(r"[^A-Za-z0-9]",pw): s+=1
            else:                             hints.append("symbol")
            cols=["#ef4444","#f97316","#eab308","#10b981"]; lbs=["Weak","Fair","Good","Strong"]; ws=[25,50,75,100]
            idx=min(s-1,3) if s>0 else 0
            hint="" if s==4 else " · add "+(", ".join(hints[:2]))
            st.markdown(f"""<div style='margin-top:-4px;margin-bottom:10px;'>
              <div class='pw-track'><div class='pw-bar' style='width:{ws[idx]}%;background:{cols[idx]};'></div></div>
              <span style='font-size:12px;color:{cols[idx]};font-weight:600;'>{lbs[idx]}{hint}</span>
            </div>""", unsafe_allow_html=True)

        if st.button("Create Account →", key="su_btn"):
            if not all([name,email,pw,confirm]):   st.error("Please fill in all fields.")
            elif not is_valid_email(email):        st.error("Invalid email address.")
            elif len(pw)<8:                        st.error("Password must be at least 8 characters.")
            elif pw != confirm:                    st.error("Passwords do not match.")
            else:
                ok, msg = register_user(name.strip(), email.strip(), pw)
                if ok:
                    st.session_state.logged_in  = True
                    st.session_state.user_name  = name.strip()
                    st.session_state.user_email = email.strip().lower()
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown('<div class="auth-divider">or</div>', unsafe_allow_html=True)
        st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
        if st.button("Already have an account? Sign In", key="goto_login"):
            st.session_state.auth_page = "login"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# NATIVE SIDEBAR  —  always rendered via st.sidebar
# =====================================================
def show_sidebar():
    user_data = get_user_data(st.session_state.user_email)
    initials  = get_initials(st.session_state.user_name)
    preds     = user_data.get("predictions", [])
    best_sal  = max([p["salary"] for p in preds], default=0)
    since     = user_data.get("created_at","")[:10] or "—"
    section   = st.session_state.sidebar_section

    with st.sidebar:
        # Remove every layer of default Streamlit padding inside the sidebar
        st.markdown("""
        <style>
        section[data-testid="stSidebar"] > div:first-child > div {
            padding: 0 !important; margin: 0 !important;
        }
        section[data-testid="stSidebar"] > div:first-child > div > div {
            padding: 0 !important; margin: 0 !important;
        }
        section[data-testid="stSidebar"] > div:first-child > div > div > div {
            padding: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        # ── Avatar header ──
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#6366f1,#8b5cf6);
                    padding:28px 20px 22px 20px; width:100%; box-sizing:border-box;">
            <div style="width:58px;height:58px;border-radius:50%;background:rgba(255,255,255,.22);
                        display:flex;align-items:center;justify-content:center;
                        font-size:21px;font-weight:800;color:#fff;
                        border:2.5px solid rgba(255,255,255,.45);
                        margin-bottom:12px;">{initials}</div>
            <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:800;color:#fff;
                        word-break:break-word;">{user_data.get("name","—")}</div>
            <div style="font-size:12px;color:rgba(255,255,255,.75);margin-top:4px;
                        word-break:break-all;">{user_data.get("email","—")}</div>
            <div style="font-size:11px;color:rgba(255,255,255,.5);margin-top:3px;">
                Member since {since}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Stats row ──
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;padding:14px 16px;
                    background:#fff;border-bottom:1px solid #f1f5f9;">
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:10px 6px;text-align:center;">
                <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:800;color:#4f46e5;">{len(preds)}</div>
                <div style="font-size:9px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin-top:2px;">Predictions</div>
            </div>
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:10px 6px;text-align:center;">
                <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:800;color:#4f46e5;">{'₹'+str(best_sal//1000)+'K' if best_sal else '—'}</div>
                <div style="font-size:9px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin-top:2px;">Best Sal.</div>
            </div>
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:10px 6px;text-align:center;">
                <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:800;color:#4f46e5;">{len(set(p.get('job','') for p in preds)) if preds else 0}</div>
                <div style="font-size:9px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin-top:2px;">Roles</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Section tab buttons — scoped to sidebar only ──
        info_active = "background:#eef2ff;color:#4f46e5;border:1.5px solid #c7d2fe;" if section=="info" else "background:#f8fafc;color:#64748b;border:1.5px solid #e2e8f0;"
        edit_active = "background:#eef2ff;color:#4f46e5;border:1.5px solid #c7d2fe;" if section=="edit" else "background:#f8fafc;color:#64748b;border:1.5px solid #e2e8f0;"
        sec_active  = "background:#eef2ff;color:#4f46e5;border:1.5px solid #c7d2fe;" if section=="security" else "background:#f8fafc;color:#64748b;border:1.5px solid #e2e8f0;"

        st.markdown("""
        <style>
        /* Sidebar tab buttons — compact, not full-width purple */
        div[data-testid="stSidebar"] .sb-tab-btn > button {
            width: auto !important;
            background: #f8fafc !important;
            color: #64748b !important;
            border: 1.5px solid #e2e8f0 !important;
            box-shadow: none !important;
            font-size: 12px !important;
            font-weight: 600 !important;
            padding: 7px 6px !important;
            border-radius: 8px !important;
            transform: none !important;
        }
        div[data-testid="stSidebar"] .sb-tab-btn > button:hover {
            background: #eef2ff !important;
            color: #4f46e5 !important;
            transform: none !important;
            box-shadow: none !important;
        }
        /* Sign out button in sidebar */
        div[data-testid="stSidebar"] .sb-signout > button {
            background: #fff1f2 !important; color: #ef4444 !important;
            border: 1.5px solid #fecaca !important; box-shadow: none !important;
            font-size: 13px !important; padding: 9px 16px !important;
            margin: 0 16px !important; width: calc(100% - 32px) !important;
            transform: none !important;
        }
        /* Save / Update buttons in sidebar */
        div[data-testid="stSidebar"] .sb-save > button {
            background: linear-gradient(135deg,#6366f1,#8b5cf6) !important;
            color: #fff !important; border: none !important;
            box-shadow: 0 3px 10px rgba(99,102,241,.3) !important;
            font-size: 13px !important; padding: 10px 16px !important;
            margin: 4px 16px !important; width: calc(100% - 32px) !important;
            border-radius: 9px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("<div style='padding:10px 12px 6px;'>", unsafe_allow_html=True)
        tc1, tc2, tc3 = st.columns(3)
        with tc1:
            st.markdown(f'<style>div[data-testid="stSidebar"] .sb-tab-btn.active-tab > button{{background:#eef2ff !important;color:#4f46e5 !important;border:1.5px solid #c7d2fe !important;}}</style>', unsafe_allow_html=True)
            st.markdown(f'<div class="sb-tab-btn{" active-tab" if section=="info" else ""}">', unsafe_allow_html=True)
            if st.button("👤 Info", key="sb_info"):
                st.session_state.sidebar_section = "info"; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with tc2:
            st.markdown(f'<div class="sb-tab-btn{" active-tab" if section=="edit" else ""}">', unsafe_allow_html=True)
            if st.button("✏️ Edit", key="sb_edit"):
                st.session_state.sidebar_section = "edit"; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with tc3:
            st.markdown(f'<div class="sb-tab-btn{" active-tab" if section=="security" else ""}">', unsafe_allow_html=True)
            if st.button("🔒 Security", key="sb_sec"):
                st.session_state.sidebar_section = "security"; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:1px;background:#e2e8f0;'></div>", unsafe_allow_html=True)

        # ── INFO section ──
        if section == "info":
            bio   = user_data.get("bio","")           or "No bio added yet."
            phone = user_data.get("phone","")         or "—"
            loc_c = user_data.get("location_city","") or "—"
            li    = user_data.get("linkedin","")      or "—"
            st.markdown(f"""
            <div style="padding:16px 16px 8px;">
                <div style="font-size:10px;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">About</div>
                <div style="font-size:13px;color:#475569;line-height:1.6;background:#f8fafc;border-radius:10px;
                            padding:11px 13px;border:1px solid #f1f5f9;margin-bottom:16px;">{bio}</div>
                <div style="font-size:10px;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">Contact</div>
            </div>
            """, unsafe_allow_html=True)
            for icon, label, val in [("📱","Phone",phone),("📍","City",loc_c),("🔗","LinkedIn",li),("✉️","Email",user_data.get("email","—"))]:
                st.markdown(f"""
                <div style="display:flex;gap:10px;padding:9px 16px;border-top:1px solid #f8fafc;">
                    <span style="font-size:15px;min-width:20px;">{icon}</span>
                    <div>
                        <div style="font-size:10px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;font-weight:600;">{label}</div>
                        <div style="font-size:13px;color:#0f172a;font-weight:500;margin-top:1px;">{val}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

        # ── EDIT section ──
        elif section == "edit":
            st.markdown("<div style='padding:14px 16px 0;font-size:10px;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:1px;'>Edit Profile</div>", unsafe_allow_html=True)
            new_name  = st.text_input("Full Name",    value=user_data.get("name",""),          key="e_name")
            new_bio   = st.text_area( "Bio",          value=user_data.get("bio",""),   height=80, key="e_bio",   placeholder="A short intro about yourself…")
            new_phone = st.text_input("Phone",        value=user_data.get("phone",""),          key="e_phone",  placeholder="+91 98765 43210")
            new_loc   = st.text_input("City",         value=user_data.get("location_city",""),  key="e_loc",    placeholder="Bangalore, India")
            new_li    = st.text_input("LinkedIn URL", value=user_data.get("linkedin",""),       key="e_li",     placeholder="linkedin.com/in/yourname")
            st.markdown('<div class="sb-save">', unsafe_allow_html=True)
            if st.button("💾  Save Changes", key="save_profile"):
                if not new_name.strip():
                    st.error("Name cannot be empty.")
                else:
                    if update_user_profile(st.session_state.user_email, new_name.strip(),
                                           new_bio.strip(), new_phone.strip(), new_loc.strip(), new_li.strip()):
                        st.session_state.user_name = new_name.strip()
                        st.success("✅ Profile updated!")
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # ── SECURITY section ──
        elif section == "security":
            st.markdown("<div style='padding:14px 16px 0;font-size:10px;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:1px;'>Change Password</div>", unsafe_allow_html=True)
            old_pw  = st.text_input("Current Password", type="password", key="sec_old",  placeholder="Your current password")
            new_pw  = st.text_input("New Password",     type="password", key="sec_new",  placeholder="Min. 8 characters")
            conf_pw = st.text_input("Confirm New",      type="password", key="sec_conf", placeholder="Repeat new password")
            st.markdown('<div class="sb-save">', unsafe_allow_html=True)
            if st.button("🔒  Update Password", key="upd_pw"):
                if not all([old_pw, new_pw, conf_pw]):
                    st.error("Fill in all fields.")
                elif len(new_pw) < 8:
                    st.error("New password must be 8+ characters.")
                elif new_pw != conf_pw:
                    st.error("Passwords don't match.")
                else:
                    ok, msg = update_user_password(st.session_state.user_email, old_pw, new_pw)
                    st.success("✅ "+msg) if ok else st.error(msg)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("""
            <div style="margin:12px 16px;background:#fffbeb;border:1px solid #fde68a;border-radius:10px;padding:12px 14px;">
                <div style="font-size:11px;font-weight:700;color:#92400e;margin-bottom:6px;">🔐 Security Tips</div>
                <div style="font-size:12px;color:#78350f;line-height:1.8;">
                    • Use 12+ characters<br>• Mix uppercase, numbers & symbols<br>
                    • Never reuse passwords<br>• Change every 6 months
                </div>
            </div>""", unsafe_allow_html=True)

        # ── Sign out button at bottom ──
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="sb-signout">', unsafe_allow_html=True)
        if st.button("🚪  Sign Out", key="sb_signout"):
            for k,v in [("logged_in",False),("user_name",""),("user_email",""),
                        ("active_tab","predict"),("last_prediction",None),("last_inputs",None)]:
                st.session_state[k] = v
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# TOP NAV  (no sidebar toggle needed — sidebar always visible when logged in)
# =====================================================
def show_nav():
    initials = get_initials(st.session_state.user_name)
    st.markdown(f"""
    <div class="top-nav">
        <div class="nav-brand">💼 Salary<em>IQ</em></div>
        <div class="nav-right">
            <div class="nav-avatar">{initials}</div>
            <span class="nav-name">{st.session_state.user_name}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    tabs   = ["predict","insights","roadmap","dashboard","compare","leaderboard"]
    labels = ["🔍 Predict","💡 Insights","🗺️ Roadmap","📊 Dashboard","⚖️ Compare","🏆 Leaderboard"]
    for col, tab, label in zip([c1,c2,c3,c4,c5,c6], tabs, labels):
        with col:
            if st.button(label, key=f"nav_{tab}"):
                st.session_state.active_tab = tab; st.rerun()


# =====================================================
# CONTENT TABS
# =====================================================
def show_predict():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Salary Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Fill in your profile — our KNN model trained on 250,000 records will estimate your market salary instantly.</div>', unsafe_allow_html=True)
    col1,col2 = st.columns(2, gap="large")
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
            <div style="font-size:13px;color:#475569;line-height:1.9;">
                💰 &nbsp;<strong>Instant salary prediction</strong><br>
                💡 &nbsp;<strong>Personalised growth tips</strong><br>
                🗺️ &nbsp;<strong>Step-by-step career roadmap</strong><br>
                📈 &nbsp;<strong>Industry trends & benchmarks</strong><br>
                ⚖️ &nbsp;<strong>Compare vs market salaries</strong>
            </div>
        </div>""", unsafe_allow_html=True)

    _, bc, _ = st.columns([1,2,1])
    with bc:
        clicked = st.button("🔍  Predict My Salary", key="predict_btn")

    if clicked:
        inp = {"experience_years":exp,"skills_count":skills,"certifications":cert,
               "job_title":job,"education_level":edu,"location":loc,
               "industry":ind,"company_size":company,"remote_work":remote}
        df = pd.DataFrame([inp])
        df["exp_squared"]    = df["experience_years"]**2
        df["skill_per_exp"]  = df["skills_count"]/(df["experience_years"]+1)
        df["cert_per_skill"] = df["certifications"]/(df["skills_count"]+1)
        df["seniority"]      = pd.cut(df["experience_years"],bins=[0,2,5,10,20],labels=["Fresher","Junior","Mid","Senior"])
        df = pd.get_dummies(df).reindex(columns=columns, fill_value=0)
        num_cols = ["experience_years","skills_count","certifications","exp_squared","skill_per_exp","cert_per_skill"]
        df[num_cols] = scaler.transform(df[num_cols])
        salary = int(model.predict(df)[0])
        st.session_state.last_prediction = salary
        st.session_state.last_inputs     = inp
        save_prediction(st.session_state.user_email, salary, job, exp, skills)
        monthly = f"₹{salary//12:,}"
        st.markdown(f"""
        <div class="result-hero">
            <div class="result-hero-label">Your Estimated Annual Salary</div>
            <div class="result-hero-amount">₹{salary:,}</div>
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
        st.markdown("""<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:14px 20px;margin-top:8px;">
            <span style="font-size:14px;color:#15803d;font-weight:600;">✅ Prediction saved!</span>
            <span style="font-size:13px;color:#166534;"> &nbsp;·&nbsp; Explore <strong>Insights</strong>, <strong>Roadmap</strong> and <strong>Compare</strong> for your full career plan.</span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


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
    im={"blue":"insight-icon-blue","green":"insight-icon-green","amber":"insight-icon-amber","rose":"insight-icon-rose"}
    for icon,title,desc,color in salary_boost_tips(job,exp,skills,cert,edu):
        st.markdown(f'<div class="insight-card"><div class="insight-icon {im[color]}">{icon}</div><div><div class="insight-title">{title}</div><div class="insight-desc">{desc}</div></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    ca,cb = st.columns(2, gap="large")
    with ca:
        top_skills=get_skills_to_learn(job,skills); boosts=["+₹8K–15K","+₹10K–20K","+₹6K–12K","+₹12K–25K","+₹5K–10K","+₹15K–30K"]
        st.markdown('<div class="card"><div class="card-title">🛠️ Top Skills to Learn</div>', unsafe_allow_html=True)
        for i,(sk,b) in enumerate(zip(top_skills,boosts)):
            pct=90-i*10
            st.markdown(f'<div class="compare-bar-wrap"><div class="compare-bar-label"><span style="font-size:13px;font-weight:500;color:#0f172a;">{sk}</span><span class="trend-up">{b}/yr</span></div><div class="compare-bar-track"><div class="compare-bar-fill" style="width:{pct}%;background:linear-gradient(90deg,#6366f1,#8b5cf6);"></div></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with cb:
        trend=get_industry_data(ind)
        st.markdown('<div class="card"><div class="card-title">📈 Industry Salary Trends</div>', unsafe_allow_html=True)
        st.markdown(f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px;">
            <div class="metric-card"><div class="metric-label">Industry Growth</div><div class="metric-value">{trend['growth']}</div><div class="metric-sub">↑ YoY</div></div>
            <div class="metric-card"><div class="metric-label">Job Demand</div><div class="metric-value" style="font-size:16px;">{trend['demand']}</div></div>
            <div class="metric-card"><div class="metric-label">Top Pay</div><div class="metric-value" style="font-size:16px;">{trend['top_pay']}</div></div>
            <div class="metric-card"><div class="metric-label">Outlook</div><div class="metric-value" style="font-size:16px;">{trend['outlook']}</div></div>
        </div>
        <div style="background:#eef2ff;border-radius:10px;padding:14px 16px;">
            <div style="font-size:13px;color:#4f46e5;font-weight:600;">💡 {ind} sector insight</div>
            <div style="font-size:13px;color:#475569;margin-top:6px;line-height:1.5;">Growing at <strong>{trend['growth']}</strong> with <strong>{trend['demand'].lower()}</strong> demand. Top earners make <strong>{trend['top_pay']}</strong>.</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><div class="card-title">⚡ What-If Salary Simulator</div>', unsafe_allow_html=True)
    s1,s2,s3=st.columns(3)
    with s1:
        ee=st.slider("+ Years Experience",0,10,2,key="sim_exp"); se=int(salary*(1+ee*.055))
        st.markdown(f'<div class="metric-card"><div class="metric-label">+{ee} yrs experience</div><div class="metric-value">₹{se:,}</div><div class="metric-sub trend-up">+₹{se-salary:,}</div></div>', unsafe_allow_html=True)
    with s2:
        es=st.slider("+ Skills Added",0,10,3,key="sim_sk"); ss=int(salary*(1+es*.028))
        st.markdown(f'<div class="metric-card"><div class="metric-label">+{es} skills</div><div class="metric-value">₹{ss:,}</div><div class="metric-sub trend-up">+₹{ss-salary:,}</div></div>', unsafe_allow_html=True)
    with s3:
        ec=st.slider("+ Certifications",0,5,1,key="sim_c"); sc=int(salary*(1+ec*.04))
        st.markdown(f'<div class="metric-card"><div class="metric-label">+{ec} certifications</div><div class="metric-value">₹{sc:,}</div><div class="metric-sub trend-up">+₹{sc-salary:,}</div></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


def show_roadmap():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Career Roadmap</div>', unsafe_allow_html=True)
    if not st.session_state.last_inputs:
        st.markdown('<div style="text-align:center;padding:60px;"><div style="font-size:48px;">🗺️</div><div style="font-size:18px;font-weight:600;color:#0f172a;margin-top:12px;">Run a prediction first</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True); return
    inp=st.session_state.last_inputs; job=inp["job_title"]; exp=inp["experience_years"]
    steps=get_roadmap(job); cs=0 if exp<=2 else(1 if exp<=5 else(2 if exp<=10 else(3 if exp<=15 else 4)))
    cr,ci=st.columns([3,2],gap="large")
    with cr:
        sr=["₹40K–70K","₹70K–1.1L","₹1.1L–1.6L","₹1.6L–2.0L","₹2.0L+"]; er=["0–2 yrs","2–5 yrs","5–10 yrs","10–15 yrs","15+ yrs"]
        st.markdown('<div class="card"><div class="card-title">🗺️ Career Path — '+job+'</div>', unsafe_allow_html=True)
        for i,step in enumerate(steps):
            if i<cs:   dot,badge,btxt="step-dot-done","badge-done","✓ Completed"
            elif i==cs: dot,badge,btxt="step-dot-curr","badge-current","📍 You are here"
            else:       dot,badge,btxt="step-dot-next","badge-future",f"Next · {er[i]}"
            st.markdown(f'<div class="roadmap-step"><div class="step-dot {dot}">{i+1}</div><div><div class="step-title">{step}</div><div class="step-sub">{er[i]} &nbsp;·&nbsp; {sr[i]}</div><span class="step-badge {badge}">{btxt}</span></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with ci:
        curr=steps[cs]; nxt=steps[min(cs+1,len(steps)-1)]; sk=get_skills_to_learn(job,0)[:4]
        st.markdown(f'<div class="card" style="background:linear-gradient(135deg,#eef2ff,#f5f3ff);border-color:#c7d2fe;margin-bottom:12px;"><div class="card-title" style="color:#4f46e5;">🎯 Your Next Goal</div><div style="font-size:19px;font-weight:700;color:#1e1b4b;margin-bottom:8px;">{nxt}</div><div style="font-size:13px;color:#4338ca;line-height:1.6;">Currently at <strong>{curr}</strong>. Build 1–2 impactful projects, master these skills, then apply for the next level.</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><div class="card-title">🛠️ Skills for Next Level</div>', unsafe_allow_html=True)
        for s in sk:
            st.markdown(f'<span style="display:inline-block;background:#eef2ff;color:#4f46e5;border-radius:99px;padding:5px 14px;font-size:13px;font-weight:500;margin:4px;border:1px solid #c7d2fe;">{s}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><div class="card-title">📅 Estimated Timeline</div><div style="font-size:13px;color:#475569;line-height:2.0;">🟣 &nbsp;<strong>Now:</strong> {steps[cs]}<br>🟢 &nbsp;<strong>1–2 yrs:</strong> {steps[min(cs+1,len(steps)-1)]}<br>🔵 &nbsp;<strong>3–5 yrs:</strong> {steps[min(cs+2,len(steps)-1)]}<br>⭐ &nbsp;<strong>5–8 yrs:</strong> {steps[-1]}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def show_dashboard():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">My Dashboard</div><div class="page-sub">Your personal prediction history and statistics.</div>', unsafe_allow_html=True)
    users=load_users(); preds=users.get(st.session_state.user_email,{}).get("predictions",[])
    if not preds:
        st.markdown('<div style="text-align:center;padding:60px;"><div style="font-size:48px;">📊</div><div style="font-size:18px;font-weight:600;color:#0f172a;margin-top:12px;">No predictions yet</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True); return
    sals=[p["salary"] for p in preds]; avg_sal=int(sum(sals)/len(sals)); best_sal=max(sals)
    m1,m2,m3,m4=st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Predictions</div><div class="metric-value">{len(preds)}</div></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><div class="metric-label">Latest Salary</div><div class="metric-value" style="font-size:18px;">₹{sals[-1]:,}</div></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><div class="metric-label">Average Salary</div><div class="metric-value" style="font-size:18px;">₹{avg_sal:,}</div></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><div class="metric-label">Best Prediction</div><div class="metric-value" style="font-size:18px;">₹{best_sal:,}</div><div class="metric-sub">↑ Your peak</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="card" style="margin-top:12px;"><div class="card-title">📋 Prediction History</div>', unsafe_allow_html=True)
    st.markdown('<div style="display:flex;gap:12px;padding:8px 0;border-bottom:1px solid #f1f5f9;"><span style="flex:.4;font-size:11px;font-weight:700;color:#94a3b8;">#</span><span style="flex:2;font-size:11px;font-weight:700;color:#94a3b8;">ROLE</span><span style="flex:1;font-size:11px;font-weight:700;color:#94a3b8;">EXP</span><span style="flex:1;font-size:11px;font-weight:700;color:#94a3b8;">SKILLS</span><span style="flex:1.5;font-size:11px;font-weight:700;color:#94a3b8;">SALARY</span><span style="flex:1.5;font-size:11px;font-weight:700;color:#94a3b8;">DATE</span></div>', unsafe_allow_html=True)
    for i,p in enumerate(reversed(preds[-10:]),1):
        ib=p["salary"]==best_sal
        st.markdown(f'<div style="display:flex;gap:12px;padding:11px 0;border-bottom:1px solid #f8fafc;align-items:center;"><span style="flex:.4;font-size:13px;color:#94a3b8;">{i}</span><span style="flex:2;font-size:13px;font-weight:500;color:#0f172a;">{p.get("job","—")}</span><span style="flex:1;font-size:13px;color:#64748b;">{p.get("exp",0)} yrs</span><span style="flex:1;font-size:13px;color:#64748b;">{p.get("skills",0)}</span><span style="flex:1.5;font-size:14px;font-weight:700;color:#4f46e5;">₹{p["salary"]:,}{"&nbsp;⭐" if ib else ""}</span><span style="flex:1.5;font-size:12px;color:#94a3b8;">{p.get("date","—")}</span></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


def show_compare():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Compare Yourself</div><div class="page-sub">See how your predicted salary stacks up against market benchmarks.</div>', unsafe_allow_html=True)
    if not st.session_state.last_prediction:
        st.markdown('<div style="text-align:center;padding:60px;"><div style="font-size:48px;">⚖️</div><div style="font-size:18px;font-weight:600;color:#0f172a;margin-top:12px;">Run a prediction first</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True); return
    salary=st.session_state.last_prediction; inp=st.session_state.last_inputs; job=inp["job_title"]
    base=max(40000,salary-random.randint(10000,20000))
    top25=int(salary*1.22); top10=int(salary*1.48); top5=int(salary*1.75); mv=top5
    benchmarks=[("Entry Level (0–2 yrs)",int(base*.6),"#e2e8f0"),("Mid Level (3–6 yrs)",int(base*.85),"#c7d2fe"),
                ("Your Salary",salary,"#6366f1"),("Top 25% in your role",top25,"#8b5cf6"),
                ("Top 10% in your role",top10,"#7c3aed"),("Top 5% — Elite earner",top5,"#4338ca")]
    c1,c2=st.columns([3,2],gap="large")
    with c1:
        st.markdown(f'<div class="card"><div class="card-title">📊 Salary Benchmarks — {job}</div>', unsafe_allow_html=True)
        for label,val,color in benchmarks:
            pct=int((val/mv)*100); iy=label=="Your Salary"
            st.markdown(f'<div class="compare-bar-wrap" style="{"background:#eef2ff;border-radius:8px;padding:8px 10px;border:1px solid #c7d2fe;" if iy else ""}"><div class="compare-bar-label"><span style="font-size:13px;font-weight:{"700" if iy else "500"};color:{"#4f46e5" if iy else "#374151"};"> {"📍 " if iy else ""}{label}</span><span style="font-size:13px;font-weight:600;color:{"#4f46e5" if iy else "#0f172a"};">₹{val:,}</span></div><div class="compare-bar-track"><div class="compare-bar-fill" style="width:{pct}%;background:{color};"></div></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        pr=min(95,max(25,int(30+(salary/top5)*65))); gap=max(0,top10-salary)
        st.markdown(f'<div class="card" style="text-align:center;margin-bottom:12px;"><div class="card-title">🎯 Your Market Position</div><div style="font-size:52px;font-weight:800;font-family:\'Syne\',sans-serif;background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{pr}th</div><div style="font-size:14px;color:#64748b;">percentile in your field</div><div style="font-size:13px;color:#475569;margin-top:12px;line-height:1.6;">You earn more than <strong>{pr}%</strong> of professionals in similar roles. {"Focus on top skills to break into the top 10%." if pr<90 else "🎉 You are among the elite earners!"}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><div class="card-title">💰 Gap to Top 10%</div><div style="font-size:24px;font-weight:800;color:#4f46e5;font-family:\'Syne\',sans-serif;">{"Already there! 🎉" if gap==0 else f"₹{gap:,}"}</div><div style="font-size:13px;color:#64748b;margin-top:6px;line-heigh
