# =========================================================
# IMPORT LIBRARIES
# =========================================================
import streamlit as st
import pandas as pd
import pickle
import time

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Salary Prediction",
    page_icon="💼",
    layout="wide"
)

# =========================================================
# UNIQUE PREMIUM CSS DESIGN
# =========================================================
st.markdown("""
<style>

/* Background */
.stApp{
    background: linear-gradient(
    135deg,
    #0f172a,
    #111827,
    #1e1b4b,
    #312e81
    );

    background-size:400% 400%;
    animation:gradientBG 15s ease infinite;
    color:white;
}

/* Animated Background */
@keyframes gradientBG{

    0%{
        background-position:0% 50%;
    }

    50%{
        background-position:100% 50%;
    }

    100%{
        background-position:0% 50%;
    }
}

/* Title */
.main-title{

    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:white;

    animation:glow 2s infinite alternate;
}

@keyframes glow{

    from{
        text-shadow:
        0 0 10px #38bdf8,
        0 0 20px #38bdf8;
    }

    to{
        text-shadow:
        0 0 20px #8b5cf6,
        0 0 40px #8b5cf6;
    }
}

/* Subtitle */
.sub-title{

    text-align:center;
    font-size:22px;
    color:#d1d5db;

    margin-bottom:30px;
}

/* Glass Card */
.custom-card{

    background:rgba(255,255,255,0.08);

    border:1px solid rgba(255,255,255,0.2);

    backdrop-filter:blur(12px);

    border-radius:25px;

    padding:30px;

    margin-top:20px;

    transition:0.5s;

    box-shadow:
    0px 8px 25px rgba(0,0,0,0.4);
}

/* Hover */
.custom-card:hover{

    transform:
    translateY(-10px)
    scale(1.02);

    box-shadow:
    0px 12px 30px rgba(59,130,246,0.5);
}

/* Buttons */
.stButton>button{

    width:100%;
    height:55px;

    border:none;

    border-radius:15px;

    background:
    linear-gradient(
    90deg,
    #06b6d4,
    #3b82f6,
    #8b5cf6
    );

    color:white;

    font-size:18px;
    font-weight:bold;

    transition:0.4s;
}

/* Button Hover */
.stButton>button:hover{

    transform:scale(1.04);

    background:
    linear-gradient(
    90deg,
    #ec4899,
    #8b5cf6,
    #3b82f6
    );
}

/* Inputs */
.stTextInput input,
.stNumberInput input{

    border-radius:15px;

    border:2px solid #38bdf8;

    background:white;

    color:black;
}

/* Select */
.stSelectbox div[data-baseweb="select"]{

    background:white;

    border-radius:15px;

    color:black;
}

/* Sidebar */
section[data-testid="stSidebar"]{

    background:
    linear-gradient(
    180deg,
    #111827,
    #1e3a8a,
    #312e81
    );
}

/* Sidebar Text */
section[data-testid="stSidebar"] *{
    color:white;
}

/* Metrics */
[data-testid="metric-container"]{

    background:rgba(255,255,255,0.08);

    padding:20px;

    border-radius:20px;

    transition:0.4s;
}

/* Metric Hover */
[data-testid="metric-container"]:hover{

    transform:translateY(-5px);
}

/* Footer */
.footer{

    text-align:center;

    color:#d1d5db;

    margin-top:40px;

    font-size:16px;
}

/* Images */
img{

    border-radius:20px;

    transition:0.4s;
}

/* Image Hover */
img:hover{

    transform:scale(1.02);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# USER DATABASE
# =========================================================
if "users" not in st.session_state:

    st.session_state.users = {
        "admin":"1234",
        "aparna":"aparna123"
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# =========================================================
# LOAD MODEL FILES
# =========================================================
model = pickle.load(open("knn_model.pkl","rb"))
scaler = pickle.load(open("scaler.pkl","rb"))
columns = pickle.load(open("columns.pkl","rb"))

# =========================================================
# GET OPTIONS
# =========================================================
def get_options(prefix):

    opts = [
        col.replace(prefix,"")
        for col in columns
        if col.startswith(prefix)
    ]

    return ["Other"] + sorted(list(set(opts)))

job_options = get_options("job_title_")
edu_options = get_options("education_level_")
loc_options = get_options("location_")
ind_options = get_options("industry_")
company_options = get_options("company_size_")
remote_options = get_options("remote_work_")

# =========================================================
# LOGIN PAGE
# =========================================================
def login():

    st.markdown(
        "<h1 class='main-title'>🔐 Login</h1>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):

        if username in st.session_state.users and st.session_state.users[username] == password:

            with st.spinner("Logging In..."):
                time.sleep(2)

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success(f"Welcome {username} 🎉")

            st.balloons()

            st.rerun()

        else:
            st.error("Invalid Username or Password")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# SIGNUP PAGE
# =========================================================
def signup():

    st.markdown(
        "<h1 class='main-title'>📝 Sign Up</h1>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)

    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")
    confirm_pass = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):

        if new_user in st.session_state.users:
            st.warning("Username already exists")

        elif new_pass != confirm_pass:
            st.warning("Passwords do not match")

        else:

            st.session_state.users[new_user] = new_pass

            st.success("Account Created Successfully ✅")

            st.info("Now Login")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# AUTH PAGE
# =========================================================
if not st.session_state.logged_in:

    st.markdown(
        "<h1 class='main-title'>💼 AI Salary Prediction</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p class='sub-title'>Modern AI Powered Salary Prediction Website</p>",
        unsafe_allow_html=True
    )

    st.image(
        "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a",
        use_container_width=True
    )

    menu = st.sidebar.selectbox(
        "Choose",
        ["Login","Sign Up"]
    )

    if menu == "Login":
        login()

    else:
        signup()

# =========================================================
# MAIN WEBSITE
# =========================================================
else:

    st.sidebar.success(
        f"👤 {st.session_state.username}"
    )

    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Home",
            "💰 Salary Prediction",
            "📊 Dashboard",
            "📈 Insights",
            "📄 Receipt",
            "ℹ About"
        ]
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()

    # =====================================================
    # HOME PAGE
    # =====================================================
    if page == "🏠 Home":

        st.markdown(
            "<h1 class='main-title'>💼 Welcome</h1>",
            unsafe_allow_html=True
        )

        st.image(
            "https://images.unsplash.com/photo-1554224155-6726b3ff858f",
            use_container_width=True
        )

        st.markdown(
            """
            <p class='sub-title'>
            Predict Salary using Artificial Intelligence
            </p>
            """,
            unsafe_allow_html=True
        )

        col1,col2,col3 = st.columns(3)

        with col1:

            st.markdown("""
            <div class='custom-card'>
            <h2>🤖 AI Prediction</h2>

            <p>
            Smart salary prediction using
            machine learning algorithms.
            </p>

            </div>
            """, unsafe_allow_html=True)

        with col2:

            st.markdown("""
            <div class='custom-card'>
            <h2>📊 Analytics</h2>

            <p>
            Interactive graphs and
            visual insights.
            </p>

            </div>
            """, unsafe_allow_html=True)

        with col3:

            st.markdown("""
            <div class='custom-card'>
            <h2>⚡ Fast Results</h2>

            <p>
            Get instant prediction
            within seconds.
            </p>

            </div>
            """, unsafe_allow_html=True)

    # =====================================================
    # SALARY PREDICTION PAGE
    # =====================================================
    elif page == "💰 Salary Prediction":

        st.markdown(
            "<h1 class='main-title'>💰 Salary Prediction</h1>",
            unsafe_allow_html=True
        )

        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)

        exp = st.number_input("Experience",0,30)

        skills = st.number_input("Skills",0,50)

        cert = st.number_input("Certifications",0,20)

        job = st.selectbox("Job Role",job_options)

        edu = st.selectbox("Education",edu_options)

        loc = st.selectbox("Location",loc_options)

        ind = st.selectbox("Industry",ind_options)

        company = st.selectbox("Company Size",company_options)

        remote = st.selectbox("Remote Work",remote_options)

        input_dict = {

            "experience_years":exp,
            "skills_count":skills,
            "certifications":cert,
            "job_title":job,
            "education_level":edu,
            "location":loc,
            "industry":ind,
            "company_size":company,
            "remote_work":remote
        }

        input_df = pd.DataFrame([input_dict])

        input_df['exp_squared'] = input_df['experience_years']**2

        input_df['skill_per_exp'] = (
            input_df['skills_count']/
            (input_df['experience_years']+1)
        )

        input_df['cert_per_skill'] = (
            input_df['certifications']/
            (input_df['skills_count']+1)
        )

        input_df['seniority'] = pd.cut(
            input_df['experience_years'],
            bins=[0,2,5,10,20],
            labels=['Fresher','Junior','Mid','Senior']
        )

        input_df = pd.get_dummies(input_df)

        input_df = input_df.reindex(
            columns=columns,
            fill_value=0
        )

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

        if st.button("Predict Salary 🚀"):

            prediction = model.predict(input_df)

            predicted_salary = int(prediction[0])

            st.success(
                f"💰 Predicted Salary: ₹ {predicted_salary:,}"
            )

            st.balloons()

            st.session_state["salary"] = predicted_salary

            # WhatsApp
            phone = st.text_input(
                "📱 WhatsApp Number",
                placeholder="91XXXXXXXXXX"
            )

            message = f'''
💼 AI Salary Prediction Receipt

👤 User: {st.session_state.username}
💼 Job Role: {job}
📚 Education: {edu}
⭐ Experience: {exp} Years

💰 Predicted Salary:
₹ {predicted_salary:,}

Thank You 🚀
'''

            whatsapp_url = (
                f"https://wa.me/{phone}?text={message}"
            )

            st.markdown(
                f"""
                <a href="{whatsapp_url}" target="_blank">
                    <button style="
                        background:linear-gradient(90deg,#25D366,#128C7E);
                        color:white;
                        padding:14px;
                        border:none;
                        border-radius:12px;
                        width:100%;
                        font-size:18px;
                        cursor:pointer;
                    ">
                    📲 Send To WhatsApp
                    </button>
                </a>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # DASHBOARD PAGE
    # =====================================================
    elif page == "📊 Dashboard":

        st.markdown(
            "<h1 class='main-title'>📊 Dashboard</h1>",
            unsafe_allow_html=True
        )

        col1,col2,col3 = st.columns(3)

        col1.metric("👥 Users","150+")
        col2.metric("📈 Predictions","500+")
        col3.metric("🎯 Accuracy","89%")

        chart_data = pd.DataFrame({

            "Experience":[1,2,3,4,5,6],
            "Salary":[25000,40000,60000,80000,100000,140000]
        })

        st.line_chart(
            chart_data,
            x="Experience",
            y="Salary"
        )

        st.bar_chart(
            chart_data.set_index("Experience")
        )

        st.image(
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f",
            use_container_width=True
        )

    # =====================================================
    # INSIGHTS PAGE
    # =====================================================
    elif page == "📈 Insights":

        st.markdown(
            "<h1 class='main-title'>📈 Insights</h1>",
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class='custom-card'>

        <h2>💡 Key Insights</h2>

        ✔ More experience increases salary <br><br>

        ✔ Technical skills improve salary growth <br><br>

        ✔ Certifications increase opportunities <br><br>

        ✔ Senior employees receive highest salary <br><br>

        </div>
        """, unsafe_allow_html=True)

        st.image(
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71",
            use_container_width=True
        )

    # =====================================================
    # RECEIPT PAGE
    # =====================================================
    elif page == "📄 Receipt":

        st.markdown(
            "<h1 class='main-title'>📄 Receipt</h1>",
            unsafe_allow_html=True
        )

        salary = st.session_state.get(
            "salary",
            "No Prediction Yet"
        )

        st.markdown("""
        <div class='custom-card'>
        """, unsafe_allow_html=True)

        st.write(f"👤 User: {st.session_state.username}")

        st.write(f"💰 Salary: ₹ {salary}")

        st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # ABOUT PAGE
    # =====================================================
    elif page == "ℹ About":

        st.markdown(
            "<h1 class='main-title'>ℹ About Project</h1>",
            unsafe_allow_html=True
        )

        st.image(
            "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            width=150
        )

        st.markdown("""
        <div class='custom-card'>

        <h2>💼 AI Salary Prediction System</h2>

        <p>
        This project predicts employee salary
        using Machine Learning algorithms.
        </p>

        <h2>🚀 Features</h2>

        ✔ Login & Signup <br><br>

        ✔ Salary Prediction <br><br>

        ✔ Dashboard Analytics <br><br>

        ✔ Graph Visualization <br><br>

        ✔ WhatsApp Receipt <br><br>

        ✔ Modern UI Design <br><br>

        </div>
        """, unsafe_allow_html=True)

        st.subheader("🛠 Tools Used")

        col1,col2,col3 = st.columns(3)

        with col1:

            st.markdown("""
            <div class='custom-card'>
            <h2>🐍 Python</h2>

            <p>
            Main programming language.
            </p>

            </div>
            """, unsafe_allow_html=True)

        with col2:

            st.markdown("""
            <div class='custom-card'>
            <h2>🎨 Streamlit</h2>

            <p>
            Used for web application UI.
            </p>

            </div>
            """, unsafe_allow_html=True)

        with col3:

            st.markdown("""
            <div class='custom-card'>
            <h2>🤖 Machine Learning</h2>

            <p>
            KNN model used for prediction.
            </p>

            </div>
            """, unsafe_allow_html=True)

    # =====================================================
    # FOOTER
    # =====================================================
    st.markdown(
        """
        <div class='footer'>
        Developed with ❤️ using Streamlit & AI
        </div>
        """,
        unsafe_allow_html=True
    )
