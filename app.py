# =========================================================
# IMPORT LIBRARIES
# =========================================================
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pickle

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Salary Prediction",
    page_icon="💼",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp{
    background: linear-gradient(to right,#141e30,#243b55);
    color: white;
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
    background: linear-gradient(to bottom,#0f2027,#203a43,#2c5364);
}

/* TITLES */
.main-title{
    font-size:60px;
    font-weight:bold;
    text-align:center;
    color:white;
}

.sub-title{
    text-align:center;
    font-size:24px;
    color:#dcdcdc;
}

/* HERO BOX */
.hero{
    padding:40px;
    border-radius:25px;
    background: linear-gradient(135deg,#667eea,#764ba2);
    box-shadow:0px 10px 30px rgba(0,0,0,0.4);
    animation: fadeIn 2s;
}

/* CARDS */
.card{
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    padding:25px;
    border-radius:20px;
    transition:0.5s;
    box-shadow:0px 8px 20px rgba(0,0,0,0.3);
    height:250px;
}

.card:hover{
    transform:translateY(-10px) scale(1.03);
    background: linear-gradient(135deg,#ff6a00,#ee0979);
}

/* METRIC CARD */
.metric-card{
    background: rgba(255,255,255,0.1);
    padding:25px;
    border-radius:20px;
    text-align:center;
    transition:0.5s;
}

.metric-card:hover{
    transform:translateY(-8px);
    background: linear-gradient(135deg,#11998e,#38ef7d);
}

/* GRAPH BOX */
.graph-box{
    background: rgba(255,255,255,0.1);
    padding:20px;
    border-radius:20px;
    box-shadow:0px 8px 20px rgba(0,0,0,0.3);
}

/* BUTTON */
.stButton>button{
    background: linear-gradient(to right,#ff512f,#dd2476);
    color:white;
    border:none;
    padding:12px 25px;
    border-radius:10px;
    font-size:18px;
    transition:0.4s;
    width:100%;
}

.stButton>button:hover{
    transform:scale(1.05);
    background: linear-gradient(to right,#00c6ff,#0072ff);
}

/* ANIMATION */
@keyframes fadeIn{
    from{
        opacity:0;
        transform:translateY(-30px);
    }
    to{
        opacity:1;
        transform:translateY(0px);
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("💼 Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "🏠 Home",
        "🔮 Prediction",
        "📊 Dashboard",
        "📈 Visualization",
        "ℹ About"
    ]
)

# =========================================================
# SAMPLE DATA
# =========================================================
np.random.seed(42)

df = pd.DataFrame({
    "Experience": np.random.randint(1,20,200),
    "Salary": np.random.randint(30000,200000,200),
    "Age": np.random.randint(21,60,200),
    "Skill_Score": np.random.randint(1,10,200)
})

# =========================================================
# HOME PAGE
# =========================================================
if page == "🏠 Home":

    st.markdown("""
    <div class='hero'>
        <h1 class='main-title'>💼 AI Job Salary Prediction</h1>
        <p class='sub-title'>
        Predict Employee Salaries Using Artificial Intelligence & Machine Learning
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='card'>
            <h2>🤖 AI Prediction</h2>
            <p>
            Machine Learning based salary prediction system
            using employee details, skills and experience.
            </p>

            <ul>
                <li>Real-Time Prediction</li>
                <li>Fast Processing</li>
                <li>High Accuracy</li>
                <li>Easy To Use</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card'>
            <h2>📊 Smart Dashboard</h2>
            <p>
            Interactive analytics dashboard with graphs,
            charts and salary trends visualization.
            </p>

            <ul>
                <li>Dynamic Charts</li>
                <li>Salary Insights</li>
                <li>Live Analytics</li>
                <li>Visual Reports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='card'>
            <h2>⚡ Modern UI</h2>
            <p>
            Attractive responsive web design with hover
            effects, animations and gradient themes.
            </p>

            <ul>
                <li>Premium CSS</li>
                <li>Hover Effects</li>
                <li>Dark Theme</li>
                <li>Glassmorphism</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1,col2 = st.columns(2)

    with col1:
        st.image(
            "https://images.unsplash.com/photo-1552664730-d307ca884978",
            use_container_width=True
        )

    with col2:

        st.markdown("""
        ## 🌟 Why Use This Project?

        This project is specially designed for:
        
        ✔ HR Analytics
        
        ✔ Employee Salary Analysis
        
        ✔ Machine Learning Practice
        
        ✔ Data Science Portfolio
        
        ✔ AI Based Web Application
        
        ✔ Interactive Dashboard
        
        ✔ Professional UI Design
        
        ✔ Final Year Projects
        
        ---
        
        ## 🚀 Technologies Used
        
        - Python
        
        - Streamlit
        
        - Machine Learning
        
        - Plotly
        
        - Seaborn
        
        - Pandas
        
        - NumPy
        
        - CSS Animation
        
        """)

# =========================================================
# PREDICTION PAGE
# =========================================================
elif page == "🔮 Prediction":

    st.title("💰 Salary Prediction System")

    st.image(
        "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a",
        use_container_width=True
    )

    st.write("")

    col1,col2 = st.columns(2)

    with col1:
        experience = st.slider("Years of Experience",0,20,2)

        education = st.selectbox(
            "Education Level",
            [
                "High School",
                "Bachelor",
                "Master",
                "PhD"
            ]
        )

        age = st.slider("Age",18,60,25)

    with col2:
        gender = st.selectbox(
            "Gender",
            ["Male","Female"]
        )

        job_role = st.selectbox(
            "Job Role",
            [
                "Data Scientist",
                "Software Engineer",
                "AI Engineer",
                "Manager",
                "Analyst"
            ]
        )

        skill = st.slider("Skill Score",1,10,5)

    st.write("")

    if st.button("🚀 Predict Salary"):

        predicted_salary = (
            experience * 10000
            + skill * 5000
            + np.random.randint(10000,50000)
        )

        st.success(
            f"💸 Estimated Salary = ₹ {predicted_salary}"
        )

        st.balloons()

        st.markdown(f"""
        <div class='graph-box'>
        <h2>📌 Prediction Summary</h2>

        <ul>
            <li>Experience: {experience} Years</li>
            <li>Education: {education}</li>
            <li>Job Role: {job_role}</li>
            <li>Skill Score: {skill}</li>
            <li>Predicted Salary: ₹ {predicted_salary}</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

# =========================================================
# DASHBOARD PAGE
# =========================================================
elif page == "📊 Dashboard":

    st.title("📊 Salary Analytics Dashboard")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h2>👨‍💼 Employees</h2>
            <h1>{len(df)}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h2>💰 Avg Salary</h2>
            <h1>₹ {round(df['Salary'].mean(),2)}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h2>📈 Max Salary</h2>
            <h1>₹ {df['Salary'].max()}</h1>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    fig1 = px.scatter(
        df,
        x="Experience",
        y="Salary",
        color="Age",
        size="Skill_Score",
        title="Experience vs Salary"
    )

    st.plotly_chart(fig1,use_container_width=True)

    fig2 = px.histogram(
        df,
        x="Salary",
        nbins=20,
        title="Salary Distribution"
    )

    st.plotly_chart(fig2,use_container_width=True)

    fig3 = px.line(
        df.sort_values("Experience"),
        x="Experience",
        y="Salary",
        title="Salary Growth Trend"
    )

    st.plotly_chart(fig3,use_container_width=True)

# =========================================================
# VISUALIZATION PAGE
# =========================================================
elif page == "📈 Visualization":

    st.title("📈 Data Visualization")

    col1,col2 = st.columns(2)

    with col1:

        st.markdown("<div class='graph-box'>",
        unsafe_allow_html=True)

        fig,ax = plt.subplots(figsize=(6,4))

        sns.histplot(df["Salary"],kde=True,ax=ax)

        plt.title("Salary Distribution")

        st.pyplot(fig)

        st.markdown("</div>",
        unsafe_allow_html=True)

    with col2:

        st.markdown("<div class='graph-box'>",
        unsafe_allow_html=True)

        fig,ax = plt.subplots(figsize=(6,4))

        sns.boxplot(x=df["Salary"],ax=ax)

        plt.title("Salary Outliers")

        st.pyplot(fig)

        st.markdown("</div>",
        unsafe_allow_html=True)

    st.write("")

    col1,col2 = st.columns(2)

    with col1:

        st.markdown("<div class='graph-box'>",
        unsafe_allow_html=True)

        fig,ax = plt.subplots(figsize=(6,4))

        sns.violinplot(y=df["Salary"],ax=ax)

        plt.title("Violin Plot")

        st.pyplot(fig)

        st.markdown("</div>",
        unsafe_allow_html=True)

    with col2:

        st.markdown("<div class='graph-box'>",
        unsafe_allow_html=True)

        corr = df.corr(numeric_only=True)

        fig,ax = plt.subplots(figsize=(6,4))

        sns.heatmap(
            corr,
            annot=True,
            cmap="coolwarm",
            ax=ax
        )

        plt.title("Correlation Heatmap")

        st.pyplot(fig)

        st.markdown("</div>",
        unsafe_allow_html=True)

# =========================================================
# ABOUT PAGE
# =========================================================
elif page == "ℹ About":

    st.title("ℹ About Project")

    st.image(
        "https://images.unsplash.com/photo-1484417894907-623942c8ee29",
        use_container_width=True
    )

    st.write("")

    st.markdown("""
    <div class='graph-box'>

    ## 💼 AI Job Salary Prediction System

    This project is developed using Artificial Intelligence,
    Machine Learning and Streamlit Framework.

    The system predicts employee salaries using different
    parameters such as experience, skills, education and job role.

    ---

    ## 🚀 Main Features

    ✔ Multi Page Web Application

    ✔ Attractive Modern UI

    ✔ Hover Animation Effects

    ✔ Glassmorphism Cards

    ✔ Interactive Dashboard

    ✔ Real-Time Salary Prediction

    ✔ Advanced Data Visualization

    ✔ Responsive Layout

    ✔ Gradient Themes

    ✔ Plotly Interactive Charts

    ---

    ## 🛠 Technologies Used

    - Python
    
    - Streamlit
    
    - Machine Learning
    
    - Pandas
    
    - NumPy
    
    - Matplotlib
    
    - Seaborn
    
    - Plotly
    
    - CSS
    
    - HTML

    ---

    ## 📊 Project Objectives

    ✔ Predict Employee Salary
    
    ✔ Analyze Salary Trends
    
    ✔ Improve Decision Making
    
    ✔ Build AI Web Application
    
    ✔ Create Attractive User Interface

    ---

    ## 🌟 Future Scope

    ✔ Authentication System
    
    ✔ Database Integration
    
    ✔ AI Chatbot
    
    ✔ Resume Analyzer
    
    ✔ Live API
    
    ✔ PDF Report Download
    
    ✔ Deep Learning Model

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.write("")
st.write("---")

st.markdown("""
<h3 style='text-align:center;color:white'>
Made with ❤️ Using Streamlit
</h3>
""", unsafe_allow_html=True)
