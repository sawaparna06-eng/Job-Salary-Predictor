import streamlit as st
import pickle, pandas as pd, hashlib, json, os, re, random
from datetime import datetime

st.set_page_config(
    page_title="SalaryIQ Pro",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Models ──
model   = pickle.load(open("knn_model.pkl","rb"))
scaler  = pickle.load(open("scaler.pkl","rb"))
columns = pickle.load(open("columns.pkl","rb"))

def get_options(prefix):
    return sorted(set(c.replace(prefix,"") for c in columns if c.startswith(prefix)))

job_options     = ["Other"]+get_options("job_title_")
edu_options     = ["Other"]+get_options("education_level_")
loc_options     = ["Other"]+get_options("location_")
ind_options     = ["Other"]+get_options("industry_")
company_options = ["Other"]+get_options("company_size_")
remote_options  = ["Other"]+get_options("remote_work_")

# ── Storage ──
USERS_FILE = "users.json"
def load_users():
    return json.load(open(USERS_FILE)) if os.path.exists(USERS_FILE) else {}
def save_users(u):
    json.dump(u, open(USERS_FILE,"w"), indent=2)
def hp(pw): return hashlib.sha256(pw.encode()).hexdigest()

def register_user(name, email, password):
    u = load_users()
    if email.lower() in u: return False,"Email already registered."
    u[email.lower()] = {"name":name,"email":email.lower(),"password":hp(password),
        "created_at":datetime.now().isoformat(),"predictions":[],
        "bio":"","phone":"","location_city":"","linkedin":""}
    save_users(u); return True,"Account created!"

def login_user(email, password):
    u = load_users()
    if email.lower() not in u: return False,"No account found."
    if u[email.lower()]["password"] != hp(password): return False,"Incorrect password."
    return True, u[email.lower()]["name"]

def save_prediction(email, salary, job, exp, skills):
    u = load_users()
    if email.lower() in u:
        u[email.lower()].setdefault("predictions",[]).append(
            {"salary":salary,"job":job,"exp":exp,"skills":skills,
             "date":datetime.now().strftime("%d %b %Y")})
        save_users(u)

def update_profile(email, name, bio, phone, city, linkedin):
    u = load_users()
    if email.lower() in u:
        d = u[email.lower()]
        d.update({"name":name,"bio":bio,"phone":phone,"location_city":city,"linkedin":linkedin})
        save_users(u); return True
    return False

def update_password(email, old, new):
    u = load_users()
    if email.lower() not in u: return False,"User not found."
    if u[email.lower()]["password"] != hp(old): return False,"Current password wrong."
    u[email.lower()]["password"] = hp(new); save_users(u); return True,"Password updated!"

def get_user(email): return load_users().get(email.lower(),{})
def valid_email(e): return bool(re.match(r"^[\w.\-]+@[\w.\-]+\.\w{2,}$",e))

# ── Career data ──
SKILLS = {
    "Data Scientist":["Python","Machine Learning","Deep Learning","SQL","Statistics","TensorFlow","Spark"],
    "Software Engineer":["System Design","DSA","Cloud (AWS/GCP)","Docker","Kubernetes","CI/CD","Microservices"],
    "AI Engineer":["LLMs","PyTorch","MLOps","Vector Databases","Prompt Engineering","Transformers","CUDA"],
    "Data Analyst":["Power BI","Tableau","Advanced SQL","Python","Excel","Statistical Analysis","DAX"],
    "Machine Learning Engineer":["MLOps","Feature Engineering","Model Deployment","Kubeflow","PyTorch","Scalable ML"],
    "DevOps Engineer":["Kubernetes","Terraform","AWS","CI/CD","Monitoring","Docker","Linux"],
    "Cloud Engineer":["AWS/Azure/GCP","Terraform","Networking","Security","Serverless","Cost Optimization"],
    "Cybersecurity Analyst":["Ethical Hacking","SIEM","Incident Response","Network Security","Compliance","Forensics"],
    "Product Manager":["Roadmapping","OKRs","User Research","A/B Testing","SQL","Stakeholder Management"],
    "Business Analyst":["Power BI","Process Mapping","SQL","Requirements Gathering","Agile","JIRA"],
    "Frontend Developer":["React","TypeScript","Next.js","Tailwind CSS","GraphQL","Web Performance","Testing"],
    "Backend Developer":["Node.js","PostgreSQL","Redis","REST APIs","System Design","Docker","Message Queues"],
    "Other":["Communication","Project Management","Data Analysis","Cloud Basics","Agile","Python"],
}
ROADMAP = {
    "Data Scientist":["Junior Data Analyst","Data Scientist","Senior Data Scientist","Lead / Staff DS","Head of Data Science"],
    "Software Engineer":["Junior Developer","Software Engineer","Senior Engineer","Staff Engineer","Principal / VP Eng"],
    "AI Engineer":["ML Engineer","AI Engineer","Senior AI Engineer","AI Tech Lead","AI Research Director"],
    "Data Analyst":["Junior Analyst","Data Analyst","Senior Analyst","Analytics Manager","Director of Analytics"],
    "Machine Learning Engineer":["Junior ML Engineer","ML Engineer","Senior ML Engineer","ML Tech Lead","Head of ML"],
    "DevOps Engineer":["Junior DevOps","DevOps Engineer","Senior DevOps","Platform Lead","VP Infrastructure"],
    "Cloud Engineer":["Cloud Support","Cloud Engineer","Senior Cloud Engineer","Cloud Architect","CTO / VP Cloud"],
    "Cybersecurity Analyst":["Security Analyst","Senior Analyst","Security Lead","CISO Director","Chief Security Officer"],
    "Product Manager":["Associate PM","Product Manager","Senior PM","Group PM","VP / CPO"],
    "Business Analyst":["Junior BA","Business Analyst","Senior BA","BA Manager","Director of Strategy"],
    "Frontend Developer":["Junior Frontend","Frontend Developer","Senior Frontend","Frontend Lead","Head of Frontend"],
    "Backend Developer":["Junior Backend","Backend Developer","Senior Backend","Backend Lead","Engineering Manager"],
    "Other":["Entry Level","Mid Level","Senior Level","Lead / Manager","Director / VP"],
}
INDUSTRY = {
    "Technology":{"growth":"22%","outlook":"Excellent","top_pay":"₹1,80,000","demand":"Very High"},
    "Finance":{"growth":"15%","outlook":"Strong","top_pay":"₹1,60,000","demand":"High"},
    "Healthcare":{"growth":"18%","outlook":"Excellent","top_pay":"₹1,40,000","demand":"Very High"},
    "Consulting":{"growth":"12%","outlook":"Strong","top_pay":"₹1,70,000","demand":"High"},
    "Manufacturing":{"growth":"8%","outlook":"Moderate","top_pay":"₹1,10,000","demand":"Moderate"},
    "Education":{"growth":"10%","outlook":"Stable","top_pay":"₹90,000","demand":"Moderate"},
    "Retail":{"growth":"7%","outlook":"Moderate","top_pay":"₹95,000","demand":"Moderate"},
    "Media":{"growth":"9%","outlook":"Moderate","top_pay":"₹1,00,000","demand":"Moderate"},
    "Telecom":{"growth":"11%","outlook":"Strong","top_pay":"₹1,30,000","demand":"High"},
    "Government":{"growth":"6%","outlook":"Stable","top_pay":"₹85,000","demand":"Low"},
    "Other":{"growth":"10%","outlook":"Moderate","top_pay":"₹1,00,000","demand":"Moderate"},
}

# ── Session state ──
for k,v in [("logged_in",False),("user_name",""),("user_email",""),
            ("auth_page","login"),("active_tab","predict"),
            ("last_prediction",None),("last_inputs",None),("sb_tab","info")]:
    if k not in st.session_state: st.session_state[k] = v

# ── Helpers ──
def initials(name):
    p = name.strip().split()
    return (p[0][0]+(p[1][0] if len(p)>1 else "")).upper()

def boost_tips(job,exp,skills,cert,edu):
    t=[]
    if exp<3:   t.append(("🚀","Build a Portfolio","Create 3–5 GitHub projects. At junior levels, projects beat years of experience.","blue"))
    if 3<=exp<7:t.append(("📈","Target Senior Roles","Senior roles pay 35–50% more. Rewrite your resume around impact, not duties.","green"))
    if exp>=7:  t.append(("🏆","Move Into Leadership","Lead/Manager roles pay 50–80% more than IC positions.","amber"))
    if skills<8:t.append(("🛠️","Expand Your Skillset","10+ in-demand skills earn 28% more on average.","rose"))
    if cert<2:  t.append(("📜","Get Certified","AWS, Google Cloud, PMP add ₹10K–₹25K annually.","blue"))
    if edu in ["High School","Diploma","Other"]:
        t.append(("🎓","Upskill Online","Online degrees boost salary 15–20%. Try Coursera or edX.","green"))
    t.append(("🌍","Target Remote Roles","Global remote roles pay 2–4× Indian market rates.","amber"))
    t.append(("💬","Negotiate","60% never negotiate. Ask for 15–20% above the offer.","rose"))
    return t

def get_leaderboard():
    u=load_users(); lb=[]
    for e,d in u.items():
        ps=d.get("predictions",[])
        if ps:
            b=max(ps,key=lambda x:x["salary"])
            lb.append({"name":d["name"],"salary":b["salary"],"job":b.get("job","—"),"exp":b.get("exp",0)})
    lb.sort(key=lambda x:x["salary"],reverse=True)
    return lb[:10]

# ═══════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Syne:wght@700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }
#MainMenu, footer, header, .stDeployButton { display:none !important; }

/* ── remove default block padding ── */
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] > section.main { overflow-x: hidden; }

/* ── app background ── */
.stApp { background: #f0f2f8 !important; }

/* ════════════════════════════════
   SIDEBAR — native st.sidebar
   ════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
    box-shadow: 2px 0 16px rgba(0,0,0,0.07) !important;
    min-width: 270px !important;
    max-width: 270px !important;
    width: 270px !important;
    padding: 0 !important;
}
/* Remove all Streamlit-added padding inside the sidebar */
section[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 4px !important;
    padding: 0 !important;
}
/* Hide the collapse arrow */
[data-testid="stSidebarCollapseButton"] { display: none !important; }
[data-testid="collapsedControl"]        { display: none !important; }

/* ── Sidebar gradient header ── */
.sb-head {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    padding: 24px 18px 18px;
    margin: 0;
}
.sb-avatar {
    width: 60px; height: 60px; border-radius: 50%;
    border: 3px solid rgba(255,255,255,0.5);
    background: rgba(255,255,255,0.2);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; font-weight: 800; color: #fff;
    margin-bottom: 10px; position: relative;
}
.sb-online {
    position: absolute; bottom: 2px; right: 2px;
    width: 14px; height: 14px; border-radius: 50%;
    background: #10b981; border: 2px solid #8b5cf6;
}
.sb-uname  { font-family:'Syne',sans-serif; font-size:15px; font-weight:800; color:#fff; }
.sb-uemail { font-size:11px; color:rgba(255,255,255,0.7); margin-top:3px; word-break:break-all; }
.sb-usince { font-size:10px; color:rgba(255,255,255,0.45); margin-top:2px; }

/* ── Stats strip ── */
.sb-stats {
    display: grid; grid-template-columns: 1fr 1fr 1fr;
    gap: 6px; padding: 12px 14px;
    border-bottom: 1px solid #f1f5f9;
}
.sb-stat {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 8px 4px; text-align: center;
}
.sb-sv { font-family:'Syne',sans-serif; font-size:14px; font-weight:800; color:#4f46e5; }
.sb-sl { font-size:9px; color:#94a3b8; text-transform:uppercase; letter-spacing:.4px; margin-top:1px; }

/* ── Section tab pills ── */
.sb-tabs { display:flex; gap:0; border-bottom:1px solid #e2e8f0; background:#fff; }
.sb-tab-item {
    flex:1; padding:9px 4px; text-align:center; font-size:11px; font-weight:600;
    color:#64748b; cursor:pointer; border-bottom:2px solid transparent;
    background:#fff; transition:all .15s;
}
.sb-tab-item.on { color:#4f46e5; border-bottom-color:#6366f1; background:#eef2ff; }

/* ── Info rows ── */
.sb-info { padding: 12px 14px 6px; }
.sb-sec-label {
    font-size:10px; font-weight:700; color:#6366f1;
    text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;
}
.sb-bio {
    font-size:12px; color:#475569; line-height:1.6;
    background:#f8fafc; border-radius:8px; padding:9px 11px;
    border:1px solid #f1f5f9; margin-bottom:12px;
}
.sb-row {
    display:flex; gap:9px; align-items:flex-start;
    padding:8px 0; border-bottom:1px solid #f8fafc;
}
.sb-row:last-child { border-bottom:none; }
.sb-icon  { font-size:13px; min-width:18px; margin-top:1px; }
.sb-rlbl  { font-size:10px; color:#94a3b8; text-transform:uppercase; letter-spacing:.4px; font-weight:600; }
.sb-rval  { font-size:12px; color:#0f172a; font-weight:500; margin-top:1px; word-break:break-word; }

/* ── Sidebar tab buttons override ── */
section[data-testid="stSidebar"] .stButton > button {
    background: #f8fafc !important;
    color: #475569 !important;
    border: 1.5px solid #e2e8f0 !important;
    box-shadow: none !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    padding: 6px 4px !important;
    border-radius: 8px !important;
    width: 100% !important;
    transform: none !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #eef2ff !important;
    color: #4f46e5 !important;
    border-color: #c7d2fe !important;
    transform: none !important;
}
section[data-testid="stSidebar"] .stButton.active-tab > button {
    background: #eef2ff !important;
    color: #4f46e5 !important;
    border-color: #c7d2fe !important;
}
/* Sign-out button */
section[data-testid="stSidebar"] .sb-so .stButton > button {
    background: #fff1f2 !important;
    color: #ef4444 !important;
    border: 1.5px solid #fecaca !important;
    margin-top: 4px !important;
    font-size: 13px !important;
    padding: 9px 8px !important;
}
section[data-testid="stSidebar"] .sb-so .stButton > button:hover {
    background: #fee2e2 !important;
    color: #dc2626 !important;
    border-color: #fca5a5 !important;
}
/* Save / Update buttons in sidebar */
section[data-testid="stSidebar"] .sb-save .stButton > button {
    background: linear-gradient(135deg,#6366f1,#8b5cf6) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 3px 10px rgba(99,102,241,.3) !important;
    font-size: 13px !important;
    padding: 10px 8px !important;
    transform: none !important;
}
/* Input fields inside sidebar — tighter */
section[data-testid="stSidebar"] .stTextInput > div > div { border-radius:8px !important; }
section[data-testid="stSidebar"] .stTextInput label { font-size:11px !important; }
section[data-testid="stSidebar"] .stTextArea  > div > div { border-radius:8px !important; }
section[data-testid="stSidebar"] .stTextArea  label { font-size:11px !important; }

/* ════════════════════════════════
   TOP NAV
   ════════════════════════════════ */
.top-nav {
    background:#fff; border-bottom:1px solid #e2e8f0;
    padding:0 24px; display:flex; align-items:center; justify-content:space-between;
    height:52px; box-shadow:0 1px 4px rgba(0,0,0,.05);
    position:sticky; top:0; z-index:100;
}
.nav-brand { font-family:'Syne',sans-serif; font-size:17px; font-weight:800; color:#1e1b4b; }
.nav-brand em { color:#6366f1; font-style:normal; }
.nav-right { display:flex; align-items:center; gap:8px; }
.nav-av {
    width:32px; height:32px; border-radius:50%;
    background:linear-gradient(135deg,#6366f1,#8b5cf6);
    display:flex; align-items:center; justify-content:center;
    font-size:12px; font-weight:800; color:#fff;
}
.nav-nm { font-size:13px; font-weight:600; color:#334155; }

/* nav tab buttons */
.stButton > button {
    width:100% !important;
    background:linear-gradient(135deg,#6366f1,#8b5cf6) !important;
    color:#fff !important; border:none !important; border-radius:10px !important;
    padding:10px 16px !important; font-size:13px !important; font-weight:600 !important;
    box-shadow:0 4px 12px rgba(99,102,241,.28) !important; transition:all .2s !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
}
.stButton > button:hover { transform:translateY(-1px) !important; }
.ghost-btn > button {
    background:#fff !important; color:#475569 !important;
    border:1.5px solid #e2e8f0 !important; box-shadow:none !important;
    font-size:13px !important; transform:none !important;
}
.ghost-btn > button:hover { background:#f8fafc !important; }

/* ════════════════════════════════
   PAGE & CARDS
   ════════════════════════════════ */
.page-wrap  { padding:22px 26px; max-width:1100px; margin:0 auto; }
.page-title { font-family:'Syne',sans-serif !important; font-size:23px; font-weight:800; color:#0f172a; margin-bottom:3px; }
.page-sub   { font-size:13px; color:#64748b; margin-bottom:20px; }
.card       { background:#fff; border-radius:15px; border:1px solid #e2e8f0; padding:20px; box-shadow:0 1px 3px rgba(0,0,0,.04); margin-bottom:14px; }
.card-title { font-size:11px; font-weight:700; color:#6366f1; text-transform:uppercase; letter-spacing:1px; margin-bottom:13px; }
.metric-card{ background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:15px 13px; box-shadow:0 1px 3px rgba(0,0,0,.04); }
.metric-label{font-size:11px; color:#94a3b8; font-weight:500; margin-bottom:5px;}
.metric-value{font-family:'Syne',sans-serif !important; font-size:20px; font-weight:800; color:#0f172a;}
.metric-sub  {font-size:11px; color:#10b981; font-weight:500; margin-top:3px;}
.result-hero {background:linear-gradient(135deg,#6366f1,#8b5cf6); border-radius:18px; padding:30px 26px; text-align:center; margin-bottom:16px; box-shadow:0 8px 28px rgba(99,102,241,.28);}
.rh-label   {font-size:11px; color:rgba(255,255,255,.7); letter-spacing:1.4px; text-transform:uppercase;}
.rh-amount  {font-family:'Syne',sans-serif !important; font-size:50px; font-weight:800; color:#fff; margin:6px 0;}
.rh-sub     {font-size:12px; color:rgba(255,255,255,.6);}
.insight-card{background:#fff; border-radius:11px; border:1px solid #e2e8f0; padding:14px; margin-bottom:8px; display:flex; gap:11px; align-items:flex-start;}
.ic-icon    {width:34px; height:34px; border-radius:9px; display:flex; align-items:center; justify-content:center; font-size:16px; flex-shrink:0;}
.ic-blue{background:#eef2ff;} .ic-green{background:#f0fdf4;} .ic-amber{background:#fffbeb;} .ic-rose{background:#fff1f2;}
.ic-title   {font-size:13px; font-weight:600; color:#0f172a; margin-bottom:2px;}
.ic-desc    {font-size:12px; color:#64748b; line-height:1.5;}
.road-step  {display:flex; gap:13px; align-items:flex-start; padding:14px 0; border-bottom:1px solid #f1f5f9;}
.road-step:last-child{border-bottom:none;}
.rd-dot     {width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0; margin-top:2px;}
.rd-done    {background:#6366f1; color:#fff;}
.rd-curr    {background:linear-gradient(135deg,#6366f1,#8b5cf6); color:#fff; box-shadow:0 0 0 4px rgba(99,102,241,.2);}
.rd-next    {background:#f1f5f9; color:#94a3b8; border:2px dashed #cbd5e1;}
.rd-title   {font-size:14px; font-weight:600; color:#0f172a;}
.rd-sub     {font-size:11px; color:#64748b; margin-top:2px;}
.rd-badge   {display:inline-block; font-size:10px; font-weight:600; padding:2px 9px; border-radius:99px; margin-top:4px;}
.rdb-curr{background:#eef2ff;color:#4f46e5;} .rdb-done{background:#f0fdf4;color:#15803d;} .rdb-next{background:#f8fafc;color:#94a3b8;}
.lb-row     {display:flex; align-items:center; gap:11px; padding:11px 13px; border-radius:10px; margin-bottom:6px; background:#f8fafc; border:1px solid #f1f5f9; transition:all .15s;}
.lb-row:hover{background:#eef2ff; border-color:#c7d2fe;}
.lb-row.gold  {background:linear-gradient(135deg,#fffbeb,#fef3c7); border-color:#fde68a;}
.lb-row.silver{background:linear-gradient(135deg,#f8fafc,#f1f5f9); border-color:#e2e8f0;}
.lb-row.bronze{background:linear-gradient(135deg,#fff7ed,#ffedd5); border-color:#fed7aa;}
.lb-rank  {font-family:'Syne',sans-serif; font-size:14px; font-weight:800; min-width:24px;}
.lb-name  {flex:1; font-size:13px; font-weight:600; color:#0f172a;}
.lb-role  {font-size:11px; color:#64748b;}
.lb-sal   {font-family:'Syne',sans-serif; font-size:14px; font-weight:800; color:#4f46e5;}
.cbar-wrap {margin-bottom:12px;}
.cbar-lbl  {display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;}
.cbar-track{height:7px; background:#f1f5f9; border-radius:99px; overflow:hidden;}
.cbar-fill {height:100%; border-radius:99px;}
.trend-up  {color:#10b981; font-weight:600; font-size:12px;}
.pw-track  {height:4px; background:#e2e8f0; border-radius:99px; overflow:hidden; margin-bottom:4px;}
.pw-bar    {height:100%; border-radius:99px;}
.auth-div  {text-align:center; color:#cbd5e1; font-size:12px; margin:11px 0; position:relative;}
.auth-div::before,.auth-div::after{content:''; position:absolute; top:50%; width:calc(50% - 18px); height:1px; background:#e2e8f0;}
.auth-div::before{left:0;} .auth-div::after{right:0;}

/* global inputs */
.stTextInput>div>div{background:#f8fafc !important; border:1.5px solid #e2e8f0 !important; border-radius:10px !important;}
.stTextInput>div>div:focus-within{border-color:#6366f1 !important; box-shadow:0 0 0 3px rgba(99,102,241,.12) !important; background:#fff !important;}
.stTextInput input{color:#0f172a !important; background:transparent !important; font-size:13px !important; box-shadow:none !important;}
.stTextInput input::placeholder{color:#94a3b8 !important;}
.stTextInput label{color:#475569 !important; font-size:12px !important; font-weight:500 !important;}
.stNumberInput>div>div{background:#f8fafc !important; border:1.5px solid #e2e8f0 !important; border-radius:10px !important;}
.stNumberInput>div>div:focus-within{border-color:#6366f1 !important; box-shadow:0 0 0 3px rgba(99,102,241,.12) !important;}
.stNumberInput input{color:#0f172a !important; background:transparent !important; font-size:13px !important; box-shadow:none !important;}
.stNumberInput label{color:#475569 !important; font-size:12px !important; font-weight:500 !important;}
.stNumberInput button{color:#6366f1 !important;}
.stSelectbox>div>div{background:#f8fafc !important; border:1.5px solid #e2e8f0 !important; border-radius:10px !important;}
.stSelectbox>div>div:focus-within{border-color:#6366f1 !important; box-shadow:0 0 0 3px rgba(99,102,241,.12) !important;}
.stSelectbox [data-baseweb="select"]>div,.stSelectbox [data-baseweb="select"] span{color:#0f172a !important; background:transparent !important;}
.stSelectbox label{color:#475569 !important; font-size:12px !important; font-weight:500 !important;}
[data-baseweb="popover"],[data-baseweb="menu"],[role="listbox"]{background:#fff !important; border:1px solid #e2e8f0 !important; border-radius:11px !important; box-shadow:0 8px 28px rgba(0,0,0,.12) !important;}
[data-baseweb="menu"] li,[role="option"]{background:#fff !important; color:#1e293b !important; font-size:13px !important;}
[data-baseweb="menu"] li:hover,[role="option"]:hover,[role="option"][aria-selected="true"]{background:#eef2ff !important; color:#4f46e5 !important;}
.stTextArea>div>div{background:#f8fafc !important; border:1.5px solid #e2e8f0 !important; border-radius:10px !important;}
.stTextArea>div>div:focus-within{border-color:#6366f1 !important; box-shadow:0 0 0 3px rgba(99,102,241,.12) !important;}
.stTextArea textarea{color:#0f172a !important; background:transparent !important; font-size:13px !important;}
.stTextArea label{color:#475569 !important; font-size:12px !important; font-weight:500 !important;}
h1,h2,h3{font-family:'Syne',sans-serif !important; color:#0f172a !important;}
p,li{color:#475569;}
</style>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# SIDEBAR  — uses st.sidebar exclusively
# ═══════════════════════════════════════════════
def show_sidebar():
    ud      = get_user(st.session_state.user_email)
    ini     = initials(st.session_state.user_name)
    preds   = ud.get("predictions",[])
    best    = max([p["salary"] for p in preds], default=0)
    since   = ud.get("created_at","")[:10] or "—"
    tab     = st.session_state.sb_tab

    with st.sidebar:
        # ── gradient profile header ──
        st.markdown(f"""
        <div class="sb-head">
          <div class="sb-avatar">{ini}<div class="sb-online"></div></div>
          <div class="sb-uname">{ud.get('name','—')}</div>
          <div class="sb-uemail">{ud.get('email','—')}</div>
          <div class="sb-usince">Member since {since}</div>
        </div>""", unsafe_allow_html=True)

        # ── stats ──
        roles = len(set(p.get('job','') for p in preds)) if preds else 0
        st.markdown(f"""
        <div class="sb-stats">
          <div class="sb-stat"><div class="sb-sv">{len(preds)}</div><div class="sb-sl">Predictions</div></div>
          <div class="sb-stat"><div class="sb-sv">{'₹'+str(best//1000)+'K' if best else '—'}</div><div class="sb-sl">Best Sal.</div></div>
          <div class="sb-stat"><div class="sb-sv">{roles}</div><div class="sb-sl">Roles</div></div>
        </div>""", unsafe_allow_html=True)

        # ── tab switcher ──
        st.markdown(f"""
        <div class="sb-tabs">
          <div class="sb-tab-item {'on' if tab=='info' else ''}">👤 Info</div>
          <div class="sb-tab-item {'on' if tab=='edit' else ''}">✏️ Edit</div>
          <div class="sb-tab-item {'on' if tab=='security' else ''}">🔒 Security</div>
        </div>""", unsafe_allow_html=True)

        # real Streamlit buttons for tab switching (compact, below the visual tabs)
        c1,c2,c3 = st.columns(3)
        with c1:
            if st.button("👤 Info",     key="sbt_info"):     st.session_state.sb_tab="info";     st.rerun()
        with c2:
            if st.button("✏️ Edit",     key="sbt_edit"):     st.session_state.sb_tab="edit";     st.rerun()
        with c3:
            if st.button("🔒 Security", key="sbt_sec"):      st.session_state.sb_tab="security"; st.rerun()

        st.markdown("<div style='height:1px;background:#e2e8f0;margin:2px 0 8px;'></div>", unsafe_allow_html=True)

        # ── INFO tab ──
        if tab == "info":
            bio   = ud.get("bio","")           or "No bio added yet."
            phone = ud.get("phone","")         or "—"
            city  = ud.get("location_city","") or "—"
            li    = ud.get("linkedin","")      or "—"
            email = ud.get("email","—")
            st.markdown(f"""
            <div class="sb-info">
              <div class="sb-sec-label">About</div>
              <div class="sb-bio">{bio}</div>
              <div class="sb-sec-label">Contact</div>
              <div class="sb-row"><span class="sb-icon">📱</span>
                <div><div class="sb-rlbl">Phone</div><div class="sb-rval">{phone}</div></div></div>
              <div class="sb-row"><span class="sb-icon">📍</span>
                <div><div class="sb-rlbl">City</div><div class="sb-rval">{city}</div></div></div>
              <div class="sb-row"><span class="sb-icon">🔗</span>
                <div><div class="sb-rlbl">LinkedIn</div>
                <div class="sb-rval" style="color:#4f46e5;">{li}</div></div></div>
              <div class="sb-row"><span class="sb-icon">✉️</span>
                <div><div class="sb-rlbl">Email</div><div class="sb-rval">{email}</div></div></div>
            </div>""", unsafe_allow_html=True)

        # ── EDIT tab ──
        elif tab == "edit":
            st.markdown("<div style='padding:0 4px;'>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:10px;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:1px;margin:6px 0 10px;'>Edit Profile</p>", unsafe_allow_html=True)
            nm  = st.text_input("Full Name",    value=ud.get("name",""),          key="e_nm")
            bio = st.text_area( "Bio",          value=ud.get("bio",""),   height=72,key="e_bio", placeholder="Short intro…")
            ph  = st.text_input("Phone",        value=ud.get("phone",""),         key="e_ph",  placeholder="+91 98765 43210")
            cy  = st.text_input("City",         value=ud.get("location_city",""), key="e_cy",  placeholder="Bangalore, India")
            li  = st.text_input("LinkedIn URL", value=ud.get("linkedin",""),      key="e_li",  placeholder="linkedin.com/in/you")
            st.markdown('<div class="sb-save">', unsafe_allow_html=True)
            if st.button("💾 Save Changes", key="sb_save"):
                if not nm.strip(): st.error("Name can't be empty.")
                else:
                    update_profile(st.session_state.user_email,nm.strip(),bio.strip(),ph.strip(),cy.strip(),li.strip())
                    st.session_state.user_name = nm.strip()
                    st.success("✅ Profile updated!"); st.rerun()
            st.markdown('</div></div>', unsafe_allow_html=True)

        # ── SECURITY tab ──
        elif tab == "security":
            st.markdown("<div style='padding:0 4px;'>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:10px;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:1px;margin:6px 0 10px;'>Change Password</p>", unsafe_allow_html=True)
            op = st.text_input("Current Password", type="password", key="sc_op", placeholder="Current password")
            np = st.text_input("New Password",     type="password", key="sc_np", placeholder="Min. 8 characters")
            cp = st.text_input("Confirm New",      type="password", key="sc_cp", placeholder="Repeat new password")
            st.markdown('<div class="sb-save">', unsafe_allow_html=True)
            if st.button("🔒 Update Password", key="sb_pw"):
                if not all([op,np,cp]): st.error("Fill all fields.")
                elif len(np)<8: st.error("Min. 8 characters.")
                elif np!=cp: st.error("Passwords don't match.")
                else:
                    ok,msg = update_password(st.session_state.user_email,op,np)
                    st.success("✅ "+msg) if ok else st.error(msg)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("""
            <div style="margin:10px 4px 0;background:#fffbeb;border:1px solid #fde68a;border-radius:9px;padding:11px 12px;">
              <div style="font-size:10px;font-weight:700;color:#92400e;margin-bottom:5px;">🔐 Security Tips</div>
              <div style="font-size:11px;color:#78350f;line-height:1.8;">
                • Use 12+ characters<br>• Mix uppercase, numbers &amp; symbols<br>
                • Never reuse passwords<br>• Change every 6 months</div>
            </div></div>""", unsafe_allow_html=True)

        # ── Sign out ──
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="sb-so">', unsafe_allow_html=True)
        if st.button("🚪  Sign Out", key="sb_signout"):
            for k,v in [("logged_in",False),("user_name",""),("user_email",""),
                        ("active_tab","predict"),("last_prediction",None),("last_inputs",None)]:
                st.session_state[k]=v
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# AUTH
# ═══════════════════════════════════════════════
def show_login():
    st.markdown("""<div style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-1;
        background:linear-gradient(135deg,#eef0fb,#f4f0ff 55%,#edfaf3);"></div>""", unsafe_allow_html=True)
    _,col,_ = st.columns([1,1.4,1])
    with col:
        st.markdown("""
        <div style="background:#fff;border-radius:22px;padding:34px 34px 26px;margin-top:36px;
             box-shadow:0 4px 6px rgba(0,0,0,.04),0 20px 52px rgba(99,102,241,.12);
             border:1px solid rgba(99,102,241,.10);">
          <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:#1e1b4b;margin-bottom:18px;">
            💼 Salary<em style="color:#6366f1;font-style:normal;">IQ</em>
            <span style="font-size:11px;color:#94a3b8;font-weight:400;margin-left:4px;">PRO</span></div>
          <div style="font-family:'Syne',sans-serif;font-size:27px;font-weight:800;color:#0f172a;line-height:1.2;margin-bottom:5px;">
            Welcome<br><span style="background:linear-gradient(135deg,#6366f1,#8b5cf6);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;">back.</span></div>
          <div style="font-size:12px;color:#64748b;margin-bottom:20px;">Sign in to your career intelligence dashboard</div>
          <div style="display:flex;border-radius:10px;overflow:hidden;border:1px solid #e2e8f0;margin-bottom:22px;">
            <div style="flex:1;text-align:center;padding:10px 4px;border-right:1px solid #e2e8f0;background:#f8fafc;">
              <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:800;background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">95%</div>
              <div style="font-size:9px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin-top:1px;">Accuracy</div></div>
            <div style="flex:1;text-align:center;padding:10px 4px;border-right:1px solid #e2e8f0;background:#f8fafc;">
              <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:800;background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">50K+</div>
              <div style="font-size:9px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin-top:1px;">Predictions</div></div>
            <div style="flex:1;text-align:center;padding:10px 4px;background:#f8fafc;">
              <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:800;background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">120+</div>
              <div style="font-size:9px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin-top:1px;">Job Roles</div></div>
          </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        email = st.text_input("Email address", placeholder="you@example.com", key="li_em")
        pw    = st.text_input("Password", placeholder="Your password", key="li_pw", type="password")
        if st.button("Sign In →", key="li_btn"):
            if not email or not pw: st.error("Please fill in all fields.")
            elif not valid_email(email): st.error("Invalid email address.")
            else:
                ok,res = login_user(email,pw)
                if ok:
                    st.session_state.logged_in=True; st.session_state.user_name=res
                    st.session_state.user_email=email.lower(); st.rerun()
                else: st.error(res)
        st.markdown('<div class="auth-div">or</div>', unsafe_allow_html=True)
        st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
        if st.button("Create a free account →", key="li_su"):
            st.session_state.auth_page="signup"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;font-size:11px;color:#94a3b8;margin-top:8px;'>🔒 Your data is private and never shared.</p>", unsafe_allow_html=True)

def show_signup():
    st.markdown("""<div style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-1;
        background:linear-gradient(135deg,#eef0fb,#f4f0ff 55%,#edfaf3);"></div>""", unsafe_allow_html=True)
    _,col,_ = st.columns([1,1.4,1])
    with col:
        st.markdown("""
        <div style="background:#fff;border-radius:22px;padding:34px 34px 20px;margin-top:36px;
             box-shadow:0 4px 6px rgba(0,0,0,.04),0 20px 52px rgba(99,102,241,.12);
             border:1px solid rgba(99,102,241,.10);">
          <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:#1e1b4b;margin-bottom:18px;">
            💼 Salary<em style="color:#6366f1;font-style:normal;">IQ</em>
            <span style="font-size:11px;color:#94a3b8;font-weight:400;margin-left:4px;">PRO</span></div>
          <div style="font-family:'Syne',sans-serif;font-size:27px;font-weight:800;color:#0f172a;line-height:1.2;margin-bottom:5px;">
            Create your<br><span style="background:linear-gradient(135deg,#6366f1,#8b5cf6);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;">account.</span></div>
          <div style="font-size:12px;color:#64748b;margin-bottom:4px;">Join professionals discovering their true market value</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        nm = st.text_input("Full Name",        placeholder="John Doe",             key="su_nm")
        em = st.text_input("Email Address",    placeholder="you@example.com",      key="su_em")
        pw = st.text_input("Password",         placeholder="Min. 8 characters",    key="su_pw", type="password")
        cf = st.text_input("Confirm Password", placeholder="Repeat your password", key="su_cf", type="password")
        if pw:
            s,h=0,[]
            if len(pw)>=8: s+=1
            else: h.append("8+ chars")
            if re.search(r"[A-Z]",pw): s+=1
            else: h.append("uppercase")
            if re.search(r"\d",pw): s+=1
            else: h.append("number")
            if re.search(r"[^A-Za-z0-9]",pw): s+=1
            else: h.append("symbol")
            cs=["#ef4444","#f97316","#eab308","#10b981"]; ls=["Weak","Fair","Good","Strong"]
            i=min(s-1,3) if s>0 else 0; ht="" if s==4 else " · add "+(", ".join(h[:2]))
            st.markdown(f"""<div style='margin-top:-3px;margin-bottom:9px;'>
              <div class='pw-track'><div class='pw-bar' style='width:{[25,50,75,100][i]}%;background:{cs[i]};'></div></div>
              <span style='font-size:11px;color:{cs[i]};font-weight:600;'>{ls[i]}{ht}</span></div>""", unsafe_allow_html=True)
        if st.button("Create Account →", key="su_btn"):
            if not all([nm,em,pw,cf]): st.error("Fill all fields.")
            elif not valid_email(em): st.error("Invalid email.")
            elif len(pw)<8: st.error("Password min 8 chars.")
            elif pw!=cf: st.error("Passwords don't match.")
            else:
                ok,msg=register_user(nm.strip(),em.strip(),pw)
                if ok:
                    st.session_state.logged_in=True; st.session_state.user_name=nm.strip()
                    st.session_state.user_email=em.strip().lower(); st.rerun()
                else: st.error(msg)
        st.markdown('<div class="auth-div">or</div>', unsafe_allow_html=True)
        st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
        if st.button("Already have an account? Sign In", key="su_li"):
            st.session_state.auth_page="login"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# NAV
# ═══════════════════════════════════════════════
def show_nav():
    ini = initials(st.session_state.user_name)
    st.markdown(f"""
    <div class="top-nav">
      <div class="nav-brand">💼 Salary<em>IQ</em></div>
      <div class="nav-right">
        <div class="nav-av">{ini}</div>
        <span class="nav-nm">{st.session_state.user_name}</span>
      </div>
    </div>""", unsafe_allow_html=True)
    cols = st.columns(6)
    for col,tab,lbl in zip(cols,
        ["predict","insights","roadmap","dashboard","compare","leaderboard"],
        ["🔍 Predict","💡 Insights","🗺️ Roadmap","📊 Dashboard","⚖️ Compare","🏆 Leaderboard"]):
        with col:
            if st.button(lbl, key=f"nav_{tab}"):
                st.session_state.active_tab=tab; st.rerun()

# ═══════════════════════════════════════════════
# CONTENT TABS
# ═══════════════════════════════════════════════
def show_predict():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Salary Prediction</div><div class="page-sub">Fill in your profile — our KNN model trained on 250,000 records will estimate your market salary instantly.</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2,gap="large")
    with c1:
        st.markdown('<div class="card"><div class="card-title">📊 Experience & Skills</div>', unsafe_allow_html=True)
        exp    = st.number_input("Years of Experience",0,30,key="exp")
        skills = st.number_input("Number of Skills",   1,50,key="skills")
        cert   = st.number_input("Certifications",     0,20,key="cert")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><div class="card-title">🎓 Education & Role</div>', unsafe_allow_html=True)
        job = st.selectbox("Job Role",        job_options,key="job")
        edu = st.selectbox("Education Level", edu_options,key="edu")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><div class="card-title">🏢 Company & Location</div>', unsafe_allow_html=True)
        loc     = st.selectbox("Location",     loc_options,    key="loc")
        ind     = st.selectbox("Industry",     ind_options,    key="ind")
        company = st.selectbox("Company Size", company_options,key="company")
        remote  = st.selectbox("Remote Work",  remote_options, key="remote")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""<div class="card" style="background:linear-gradient(135deg,#eef2ff,#f5f3ff);border-color:#c7d2fe;">
        <div class="card-title" style="color:#4f46e5;">✨ What you'll get</div>
        <div style="font-size:13px;color:#475569;line-height:1.9;">
          💰 &nbsp;<strong>Instant salary prediction</strong><br>
          💡 &nbsp;<strong>Personalised growth tips</strong><br>
          🗺️ &nbsp;<strong>Step-by-step career roadmap</strong><br>
          📈 &nbsp;<strong>Industry trends & benchmarks</strong><br>
          ⚖️ &nbsp;<strong>Compare vs market salaries</strong></div></div>""", unsafe_allow_html=True)
    _,bc,_ = st.columns([1,2,1])
    with bc: clicked = st.button("🔍  Predict My Salary",key="pred_btn")
    if clicked:
        inp={"experience_years":exp,"skills_count":skills,"certifications":cert,
             "job_title":job,"education_level":edu,"location":loc,
             "industry":ind,"company_size":company,"remote_work":remote}
        df=pd.DataFrame([inp])
        df["exp_squared"]   =df["experience_years"]**2
        df["skill_per_exp"] =df["skills_count"]/(df["experience_years"]+1)
        df["cert_per_skill"]=df["certifications"]/(df["skills_count"]+1)
        df["seniority"]     =pd.cut(df["experience_years"],bins=[0,2,5,10,20],labels=["Fresher","Junior","Mid","Senior"])
        df=pd.get_dummies(df).reindex(columns=columns,fill_value=0)
        nc=["experience_years","skills_count","certifications","exp_squared","skill_per_exp","cert_per_skill"]
        df[nc]=scaler.transform(df[nc])
        sal=int(model.predict(df)[0])
        st.session_state.last_prediction=sal; st.session_state.last_inputs=inp
        save_prediction(st.session_state.user_email,sal,job,exp,skills)
        mo=f"₹{sal//12:,}"
        st.markdown(f"""<div class="result-hero">
          <div class="rh-label">Your Estimated Annual Salary</div>
          <div class="rh-amount">₹{sal:,}</div>
          <div class="rh-sub">≈ {mo} / month · Powered by K-Nearest Neighbors</div></div>""",unsafe_allow_html=True)
        sen="Fresher" if exp<=2 else("Junior" if exp<=5 else("Mid-Level" if exp<=10 else "Senior"))
        pct=min(95,max(30,int(30+(sal/220000)*65)))
        m1,m2,m3,m4=st.columns(4)
        for col,lbl,val in [(m1,"Seniority",sen),(m2,"Monthly",mo),(m3,"Growth Potential",f"₹{int(sal*1.35):,}"),(m4,"Percentile",f"{pct}th")]:
            with col: st.markdown(f'<div class="metric-card"><div class="metric-label">{lbl}</div><div class="metric-value" style="font-size:16px;">{val}</div></div>',unsafe_allow_html=True)
        st.markdown("""<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:11px 16px;margin-top:7px;">
          <span style="font-size:13px;color:#15803d;font-weight:600;">✅ Prediction saved!</span>
          <span style="font-size:12px;color:#166534;"> · Explore Insights, Roadmap and Compare tabs.</span></div>""",unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_insights():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Career Insights</div>', unsafe_allow_html=True)
    if not st.session_state.last_prediction:
        st.markdown('<div style="text-align:center;padding:50px;"><div style="font-size:44px;">💡</div><div style="font-size:17px;font-weight:600;color:#0f172a;margin-top:10px;">Run a prediction first</div></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True); return
    inp=st.session_state.last_inputs; sal=st.session_state.last_prediction
    job=inp["job_title"]; exp=inp["experience_years"]; sk=inp["skills_count"]
    ce=inp["certifications"]; edu=inp["education_level"]; ind=inp["industry"]
    st.markdown('<div class="card"><div class="card-title">🚀 How to Increase Your Salary</div>',unsafe_allow_html=True)
    cm={"blue":"ic-blue","green":"ic-green","amber":"ic-amber","rose":"ic-rose"}
    for ic,ti,de,co in boost_tips(job,exp,sk,ce,edu):
        st.markdown(f'<div class="insight-card"><div class="ic-icon {cm[co]}">{ic}</div><div><div class="ic-title">{ti}</div><div class="ic-desc">{de}</div></div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)
    ca,cb=st.columns(2,gap="large")
    with ca:
        top=SKILLS.get(job,SKILLS["Other"])[:6]; bs=["+₹8K–15K","+₹10K–20K","+₹6K–12K","+₹12K–25K","+₹5K–10K","+₹15K–30K"]
        st.markdown('<div class="card"><div class="card-title">🛠️ Top Skills to Learn</div>',unsafe_allow_html=True)
        for i,(s,b) in enumerate(zip(top,bs)):
            p=90-i*10
            st.markdown(f'<div class="cbar-wrap"><div class="cbar-lbl"><span style="font-size:12px;font-weight:500;color:#0f172a;">{s}</span><span class="trend-up">{b}/yr</span></div><div class="cbar-track"><div class="cbar-fill" style="width:{p}%;background:linear-gradient(90deg,#6366f1,#8b5cf6);"></div></div></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with cb:
        tr=INDUSTRY.get(ind,INDUSTRY["Other"])
        st.markdown('<div class="card"><div class="card-title">📈 Industry Trends</div>',unsafe_allow_html=True)
        st.markdown(f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:11px;">
          <div class="metric-card"><div class="metric-label">Growth</div><div class="metric-value">{tr['growth']}</div><div class="metric-sub">↑ YoY</div></div>
          <div class="metric-card"><div class="metric-label">Demand</div><div class="metric-value" style="font-size:14px;">{tr['demand']}</div></div>
          <div class="metric-card"><div class="metric-label">Top Pay</div><div class="metric-value" style="font-size:14px;">{tr['top_pay']}</div></div>
          <div class="metric-card"><div class="metric-label">Outlook</div><div class="metric-value" style="font-size:14px;">{tr['outlook']}</div></div></div>
        <div style="background:#eef2ff;border-radius:9px;padding:11px 13px;">
          <div style="font-size:12px;color:#4f46e5;font-weight:600;">💡 {ind}</div>
          <div style="font-size:12px;color:#475569;margin-top:4px;line-height:1.5;">Growing at <strong>{tr['growth']}</strong> with <strong>{tr['demand'].lower()}</strong> demand. Top earners: <strong>{tr['top_pay']}</strong>.</div></div>""",unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="card"><div class="card-title">⚡ What-If Simulator</div>',unsafe_allow_html=True)
    s1,s2,s3=st.columns(3)
    with s1:
        ee=st.slider("+ Yrs Experience",0,10,2,key="sim_e"); se=int(sal*(1+ee*.055))
        st.markdown(f'<div class="metric-card"><div class="metric-label">+{ee} years</div><div class="metric-value">₹{se:,}</div><div class="metric-sub trend-up">+₹{se-sal:,}</div></div>',unsafe_allow_html=True)
    with s2:
        es=st.slider("+ Skills",0,10,3,key="sim_s"); ss=int(sal*(1+es*.028))
        st.markdown(f'<div class="metric-card"><div class="metric-label">+{es} skills</div><div class="metric-value">₹{ss:,}</div><div class="metric-sub trend-up">+₹{ss-sal:,}</div></div>',unsafe_allow_html=True)
    with s3:
        ec=st.slider("+ Certs",0,5,1,key="sim_c"); sc=int(sal*(1+ec*.04))
        st.markdown(f'<div class="metric-card"><div class="metric-label">+{ec} certs</div><div class="metric-value">₹{sc:,}</div><div class="metric-sub trend-up">+₹{sc-sal:,}</div></div>',unsafe_allow_html=True)
    st.markdown('</div></div>',unsafe_allow_html=True)

def show_roadmap():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Career Roadmap</div>', unsafe_allow_html=True)
    if not st.session_state.last_inputs:
        st.markdown('<div style="text-align:center;padding:50px;"><div style="font-size:44px;">🗺️</div><div style="font-size:17px;font-weight:600;color:#0f172a;margin-top:10px;">Run a prediction first</div></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True); return
    inp=st.session_state.last_inputs; job=inp["job_title"]; exp=inp["experience_years"]
    steps=ROADMAP.get(job,ROADMAP["Other"]); cs=0 if exp<=2 else(1 if exp<=5 else(2 if exp<=10 else(3 if exp<=15 else 4)))
    cr,ci=st.columns([3,2],gap="large")
    sr=["₹40K–70K","₹70K–1.1L","₹1.1L–1.6L","₹1.6L–2.0L","₹2.0L+"]
    er=["0–2 yrs","2–5 yrs","5–10 yrs","10–15 yrs","15+ yrs"]
    with cr:
        st.markdown('<div class="card"><div class="card-title">🗺️ Career Path — '+job+'</div>',unsafe_allow_html=True)
        for i,step in enumerate(steps):
            if i<cs:    dot,bd,bt="rd-done","rdb-done","✓ Completed"
            elif i==cs: dot,bd,bt="rd-curr","rdb-curr","📍 You are here"
            else:       dot,bd,bt="rd-next","rdb-next",f"Next · {er[i]}"
            st.markdown(f'<div class="road-step"><div class="rd-dot {dot}">{i+1}</div><div><div class="rd-title">{step}</div><div class="rd-sub">{er[i]} · {sr[i]}</div><span class="rd-badge {bd}">{bt}</span></div></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with ci:
        curr=steps[cs]; nxt=steps[min(cs+1,len(steps)-1)]; sk=SKILLS.get(job,SKILLS["Other"])[:4]
        st.markdown(f'<div class="card" style="background:linear-gradient(135deg,#eef2ff,#f5f3ff);border-color:#c7d2fe;margin-bottom:11px;"><div class="card-title" style="color:#4f46e5;">🎯 Next Goal</div><div style="font-size:17px;font-weight:700;color:#1e1b4b;margin-bottom:7px;">{nxt}</div><div style="font-size:12px;color:#4338ca;line-height:1.6;">At <strong>{curr}</strong>. Build projects, master skills below, target the next level.</div></div>',unsafe_allow_html=True)
        st.markdown('<div class="card"><div class="card-title">🛠️ Skills for Next Level</div>',unsafe_allow_html=True)
        for s in sk:
            st.markdown(f'<span style="display:inline-block;background:#eef2ff;color:#4f46e5;border-radius:99px;padding:4px 11px;font-size:12px;font-weight:500;margin:3px;border:1px solid #c7d2fe;">{s}</span>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="card"><div class="card-title">📅 Timeline</div><div style="font-size:12px;color:#475569;line-height:2.0;">🟣 <strong>Now:</strong> {steps[cs]}<br>🟢 <strong>1–2 yrs:</strong> {steps[min(cs+1,4)]}<br>🔵 <strong>3–5 yrs:</strong> {steps[min(cs+2,4)]}<br>⭐ <strong>5–8 yrs:</strong> {steps[-1]}</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

def show_dashboard():
    st.markdown('<div class="page-wrap">',unsafe_allow_html=True)
    st.markdown('<div class="page-title">My Dashboard</div><div class="page-sub">Your prediction history and statistics.</div>',unsafe_allow_html=True)
    ud=get_user(st.session_state.user_email); ps=ud.get("predictions",[])
    if not ps:
        st.markdown('<div style="text-align:center;padding:50px;"><div style="font-size:44px;">📊</div><div style="font-size:17px;font-weight:600;color:#0f172a;margin-top:10px;">No predictions yet. Head to Predict!</div></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True); return
    sals=[p["salary"] for p in ps]; avg=int(sum(sals)/len(sals)); best=max(sals)
    m1,m2,m3,m4=st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Predictions</div><div class="metric-value">{len(ps)}</div></div>',unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><div class="metric-label">Latest</div><div class="metric-value" style="font-size:16px;">₹{sals[-1]:,}</div></div>',unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><div class="metric-label">Average</div><div class="metric-value" style="font-size:16px;">₹{avg:,}</div></div>',unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><div class="metric-label">Best</div><div class="metric-value" style="font-size:16px;">₹{best:,}</div><div class="metric-sub">↑ Peak</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="card" style="margin-top:11px;"><div class="card-title">📋 History</div>',unsafe_allow_html=True)
    st.markdown('<div style="display:flex;gap:10px;padding:6px 0;border-bottom:1px solid #f1f5f9;"><span style="flex:.4;font-size:10px;font-weight:700;color:#94a3b8;">#</span><span style="flex:2;font-size:10px;font-weight:700;color:#94a3b8;">ROLE</span><span style="flex:1;font-size:10px;font-weight:700;color:#94a3b8;">EXP</span><span style="flex:1;font-size:10px;font-weight:700;color:#94a3b8;">SKILLS</span><span style="flex:1.5;font-size:10px;font-weight:700;color:#94a3b8;">SALARY</span><span style="flex:1.5;font-size:10px;font-weight:700;color:#94a3b8;">DATE</span></div>',unsafe_allow_html=True)
    for i,p in enumerate(reversed(ps[-10:]),1):
        ib=p["salary"]==best
        st.markdown(f'<div style="display:flex;gap:10px;padding:9px 0;border-bottom:1px solid #f8fafc;align-items:center;"><span style="flex:.4;font-size:12px;color:#94a3b8;">{i}</span><span style="flex:2;font-size:12px;font-weight:500;color:#0f172a;">{p.get("job","—")}</span><span style="flex:1;font-size:12px;color:#64748b;">{p.get("exp",0)}y</span><span style="flex:1;font-size:12px;color:#64748b;">{p.get("skills",0)}</span><span style="flex:1.5;font-size:13px;font-weight:700;color:#4f46e5;">₹{p["salary"]:,}{"⭐" if ib else ""}</span><span style="flex:1.5;font-size:11px;color:#94a3b8;">{p.get("date","—")}</span></div>',unsafe_allow_html=True)
    st.markdown('</div></div>',unsafe_allow_html=True)

def show_compare():
    st.markdown('<div class="page-wrap">',unsafe_allow_html=True)
    st.markdown('<div class="page-title">Compare Yourself</div><div class="page-sub">See how your salary stacks up against market benchmarks.</div>',unsafe_allow_html=True)
    if not st.session_state.last_prediction:
        st.markdown('<div style="text-align:center;padding:50px;"><div style="font-size:44px;">⚖️</div><div style="font-size:17px;font-weight:600;color:#0f172a;margin-top:10px;">Run a prediction first</div></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True); return
    sal=st.session_state.last_prediction; inp=st.session_state.last_inputs; job=inp["job_title"]
    base=max(40000,sal-random.randint(10000,20000))
    t25=int(sal*1.22); t10=int(sal*1.48); t5=int(sal*1.75); mv=t5
    bm=[("Entry Level",int(base*.6),"#e2e8f0"),("Mid Level",int(base*.85),"#c7d2fe"),
        ("Your Salary",sal,"#6366f1"),("Top 25%",t25,"#8b5cf6"),("Top 10%",t10,"#7c3aed"),("Top 5%",t5,"#4338ca")]
    c1,c2=st.columns([3,2],gap="large")
    with c1:
        st.markdown(f'<div class="card"><div class="card-title">📊 Benchmarks — {job}</div>',unsafe_allow_html=True)
        for lbl,val,col in bm:
            pct=int((val/mv)*100); iy=lbl=="Your Salary"
            st.markdown(f'<div class="cbar-wrap" style="{"background:#eef2ff;border-radius:8px;padding:7px 9px;border:1px solid #c7d2fe;" if iy else ""}"><div class="cbar-lbl"><span style="font-size:12px;font-weight:{"700" if iy else "500"};color:{"#4f46e5" if iy else "#374151"};"> {"📍" if iy else ""}{lbl}</span><span style="font-size:12px;font-weight:600;color:{"#4f46e5" if iy else "#0f172a"};">₹{val:,}</span></div><div class="cbar-track"><div class="cbar-fill" style="width:{pct}%;background:{col};"></div></div></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with c2:
        pr=min(95,max(25,int(30+(sal/t5)*65))); gap=max(0,t10-sal)
        st.markdown(f'<div class="card" style="text-align:center;margin-bottom:11px;"><div class="card-title">🎯 Market Position</div><div style="font-size:48px;font-weight:800;font-family:\'Syne\',sans-serif;background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{pr}th</div><div style="font-size:13px;color:#64748b;">percentile</div><div style="font-size:12px;color:#475569;margin-top:9px;line-height:1.6;">More than <strong>{pr}%</strong> of similar roles. {"Target top skills to reach top 10%." if pr<90 else "🎉 Elite earner!"}</div></div>',unsafe_allow_html=True)
        st.markdown(f'<div class="card"><div class="card-title">💰 Gap to Top 10%</div><div style="font-size:21px;font-weight:800;color:#4f46e5;font-family:\'Syne\',sans-serif;">{"Already there! 🎉" if gap==0 else f"₹{gap:,}"}</div><div style="font-size:12px;color:#64748b;margin-top:4px;line-height:1.5;">{"Top 10% — excellent!" if gap==0 else "Add 2–3 high-demand skills and pursue senior roles."}</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

def show_leaderboard():
    st.markdown('<div class="page-wrap">',unsafe_allow_html=True)
    st.markdown('<div class="page-title">Leaderboard</div><div class="page-sub">Top predicted salaries across all SalaryIQ Pro users.</div>',unsafe_allow_html=True)
    lb=get_leaderboard(); ud=get_user(st.session_state.user_email)
    my_ps=ud.get("predictions",[]); my_b=max([p["salary"] for p in my_ps],default=0)
    if my_b:
        mr=sum(1 for e in lb if e["salary"]>my_b)+1
        st.markdown(f'<div style="background:linear-gradient(135deg,#eef2ff,#f5f3ff);border:1px solid #c7d2fe;border-radius:12px;padding:15px 20px;margin-bottom:16px;display:flex;align-items:center;justify-content:space-between;"><div><div style="font-size:10px;color:#6366f1;font-weight:700;text-transform:uppercase;">Your Position</div><div style="font-size:20px;font-weight:800;color:#1e1b4b;font-family:\'Syne\',sans-serif;">#{mr} <span style="font-size:12px;color:#64748b;font-weight:400;">of {len(lb)}</span></div></div><div style="text-align:right;"><div style="font-size:10px;color:#6366f1;font-weight:700;text-transform:uppercase;">Your Best</div><div style="font-size:20px;font-weight:800;color:#4f46e5;font-family:\'Syne\',sans-serif;">₹{my_b:,}</div></div></div>',unsafe_allow_html=True)
    st.markdown('<div class="card"><div class="card-title">🏆 Top Earners</div>',unsafe_allow_html=True)
    if not lb:
        st.markdown('<div style="text-align:center;padding:30px;color:#94a3b8;">No predictions yet.</div>',unsafe_allow_html=True)
    else:
        ms=["🥇","🥈","🥉"]; rc=["gold","silver","bronze"]
        for i,e in enumerate(lb):
            m=ms[i] if i<3 else f"#{i+1}"; r=rc[i] if i<3 else ""; im=e["name"]==st.session_state.user_name
            yb='&nbsp;<span style="font-size:10px;background:#eef2ff;color:#4f46e5;padding:2px 7px;border-radius:99px;font-weight:600;">You</span>' if im else ""
            st.markdown(f'<div class="lb-row {r}" style="{"border:2px solid #6366f1;" if im else ""}"><div class="lb-rank">{m}</div><div style="flex:1;"><div class="lb-name">{e["name"]}{yb}</div><div class="lb-role">{e["job"]} · {e["exp"]}y</div></div><div class="lb-sal">₹{e["salary"]:,}</div></div>',unsafe_allow_html=True)
    st.markdown('</div></div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════
def show_app():
    inject_css()
    show_sidebar()   # st.sidebar — always visible, fixed
    show_nav()
    tab = st.session_state.active_tab
    if   tab=="predict":     show_predict()
    elif tab=="insights":    show_insights()
    elif tab=="roadmap":     show_roadmap()
    elif tab=="dashboard":   show_dashboard()
    elif tab=="compare":     show_compare()
    elif tab=="leaderboard": show_leaderboard()

# ═══════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════
if st.session_state.logged_in:
    show_app()
else:
    inject_css()
    # hide sidebar on auth pages
    st.markdown("""<style>
    section[data-testid="stSidebar"]{display:none !important;}
    [data-testid="collapsedControl"]{display:none !important;}
    </style>""", unsafe_allow_html=True)
    if st.session_state.auth_page=="signup": show_signup()
    else: show_login()
