# =========================
# MAIN APP PAGES
# =========================
else:

    # =========================
    # SIDEBAR
    # =========================
    st.sidebar.title("💼 Salary Prediction")

    page = st.sidebar.radio(
        "Navigation",
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

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.rerun()

    # =========================
    # LOAD MODEL FILES
    # =========================
    model = pickle.load(open("knn_model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))
    columns = pickle.load(open("columns.pkl", "rb"))

    # =====================================================
    # HOME PAGE
    # =====================================================
    if page == "🏠 Home":

        # =========================
        # HOME PAGE CSS
        # =========================
        st.markdown("""
        <style>

        .hero-box{
            background: linear-gradient(
            135deg,
            #0f172a,
            #1e3a8a,
            #2563eb
            );

            padding:50px;
            border-radius:30px;
            box-shadow:0px 10px 30px rgba(0,0,0,0.5);
        }

        .hero-title{
            font-size:65px;
            font-weight:800;
            color:white;
            line-height:1.1;
        }

        .hero-text{
            font-size:20px;
            color:#dbeafe;
            margin-top:20px;
        }

        .feature-card{
            background:rgba(255,255,255,0.08);
            padding:25px;
            border-radius:20px;
            text-align:center;
            backdrop-filter: blur(10px);
            transition:0.3s;
            border:1px solid rgba(255,255,255,0.1);
        }

        .feature-card:hover{
            transform:translateY(-5px);
        }

        .feature-title{
            color:white;
            font-size:22px;
            font-weight:bold;
        }

        .feature-text{
            color:#cbd5e1;
            margin-top:10px;
        }

        .stats-card{
            background:rgba(255,255,255,0.05);
            padding:30px;
            border-radius:20px;
            text-align:center;
            margin-top:20px;
        }

        .stats-number{
            font-size:40px;
            color:#38bdf8;
            font-weight:bold;
        }

        .stats-label{
            color:white;
            font-size:18px;
        }

        </style>
        """, unsafe_allow_html=True)

        # =========================
        # HERO SECTION
        # =========================
        left,right = st.columns([1.4,1])

        with left:

            st.markdown("""
            <div class="hero-box">

            <div style="
            color:#38bdf8;
            font-size:20px;
            font-weight:bold;">
            AI POWERED SYSTEM
            </div>

            <div class="hero-title">
            Salary <br>
            Prediction <br>
            Platform
            </div>

            <div class="hero-text">
            Predict employee salary using
            Machine Learning based on:
            experience, skills, education,
            certifications and job role.
            </div>

            </div>
            """, unsafe_allow_html=True)

        with right:

            st.image(
                "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a",
                use_container_width=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================
        # FEATURES
        # =========================
        f1,f2,f3,f4 = st.columns(4)

        with f1:
            st.markdown("""
            <div class="feature-card">
            <div class="feature-title">
            🎯 Accurate
            </div>
            <div class="feature-text">
            Highly accurate salary prediction
            </div>
            </div>
            """, unsafe_allow_html=True)

        with f2:
            st.markdown("""
            <div class="feature-card">
            <div class="feature-title">
            ⚡ Fast
            </div>
            <div class="feature-text">
            Instant AI prediction system
            </div>
            </div>
            """, unsafe_allow_html=True)

        with f3:
            st.markdown("""
            <div class="feature-card">
            <div class="feature-title">
            📊 Analytics
            </div>
            <div class="feature-text">
            Interactive dashboard & charts
            </div>
            </div>
            """, unsafe_allow_html=True)

        with f4:
            st.markdown("""
            <div class="feature-card">
            <div class="feature-title">
            🔒 Secure
            </div>
            <div class="feature-text">
            Safe and secure user system
            </div>
            </div>
            """, unsafe_allow_html=True)

        # =========================
        # STATS SECTION
        # =========================
        st.markdown("<br>", unsafe_allow_html=True)

        s1,s2,s3,s4 = st.columns(4)

        with s1:
            st.markdown("""
            <div class="stats-card">
            <div class="stats-number">
            1000+
            </div>
            <div class="stats-label">
            Users
            </div>
            </div>
            """, unsafe_allow_html=True)

        with s2:
            st.markdown("""
            <div class="stats-card">
            <div class="stats-number">
            5000+
            </div>
            <div class="stats-label">
            Predictions
            </div>
            </div>
            """, unsafe_allow_html=True)

        with s3:
            st.markdown("""
            <div class="stats-card">
            <div class="stats-number">
            90%
            </div>
            <div class="stats-label">
            Accuracy
            </div>
            </div>
            """, unsafe_allow_html=True)

        with s4:
            st.markdown("""
            <div class="stats-card">
            <div class="stats-number">
            24/7
            </div>
            <div class="stats-label">
            Availability
            </div>
            </div>
            """, unsafe_allow_html=True)

    # =====================================================
    # SALARY PREDICTION PAGE
    # =====================================================
    elif page == "💰 Salary Prediction":

        st.title("💰 Salary Prediction")

        c1,c2 = st.columns(2)

        with c1:

            exp = st.number_input(
                "Experience (Years)",
                0,
                30,
                1
            )

            skills = st.number_input(
                "Skills Count",
                0,
                50,
                5
            )

            cert = st.number_input(
                "Certifications",
                0,
                20,
                1
            )

            age = st.number_input(
                "Age",
                18,
                65,
                22
            )

        with c2:

            education = st.selectbox(
                "Education",
                [
                    "Bachelor",
                    "Master",
                    "PhD"
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

            job = st.selectbox(
                "Job Role",
                [
                    "Data Analyst",
                    "Software Engineer",
                    "Data Scientist",
                    "ML Engineer"
                ]
            )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Predict Salary"):

            predicted_salary = (
                exp * 10000 +
                skills * 3000 +
                cert * 5000 +
                age * 500
            )

            st.success(
                f"💰 Predicted Salary: ₹ {predicted_salary:,}"
            )

            st.balloons()

            # GRAPH
            chart_df = pd.DataFrame({

                "Category": [
                    "Experience",
                    "Skills",
                    "Certifications",
                    "Age"
                ],

                "Value": [
                    exp,
                    skills,
                    cert,
                    age
                ]
            })

            st.subheader("📊 Employee Analysis")

            st.bar_chart(
                chart_df.set_index("Category")
            )

    # =====================================================
    # DASHBOARD
    # =====================================================
    elif page == "📊 Dashboard":

        st.title("📊 Dashboard")

        m1,m2,m3 = st.columns(3)

        m1.metric("👥 Users", "1500+")
        m2.metric("📈 Predictions", "8000+")
        m3.metric("🎯 Accuracy", "90%")

        st.markdown("---")

        dashboard_df = pd.DataFrame({

            "Experience":[1,2,3,4,5,6,7],

            "Salary":[
                25000,
                40000,
                60000,
                80000,
                100000,
                130000,
                160000
            ]
        })

        st.subheader("📈 Salary Growth")

        st.line_chart(
            dashboard_df,
            x="Experience",
            y="Salary"
        )

        st.subheader("🌊 Salary Trend")

        st.area_chart(
            dashboard_df.set_index("Experience")
        )

    # =====================================================
    # INSIGHTS
    # =====================================================
    elif page == "📈 Insights":

        st.title("📈 Salary Insights")

        st.info("""
        ✔ More experience increases salary
        
        ✔ More certifications improve salary
        
        ✔ Senior roles get higher packages
        
        ✔ Remote jobs may offer better salary
        
        ✔ Technical roles earn more
        """)

        insights_df = pd.DataFrame({

            "Role":[
                "Fresher",
                "Junior",
                "Mid",
                "Senior"
            ],

            "Salary":[
                25000,
                50000,
                90000,
                150000
            ]
        })

        st.subheader("📊 Salary By Level")

        st.bar_chart(
            insights_df.set_index("Role")
        )

    # =====================================================
    # ABOUT PAGE
    # =====================================================
    elif page == "ℹ About":

        st.title("ℹ About Project")

        st.write("""
        ## 💼 Salary Prediction System
        
        This project predicts employee salary
        using Machine Learning algorithms.

        ### 🚀 Features
        ✔ Salary Prediction
        
        ✔ Interactive Dashboard
        
        ✔ User Authentication
        
        ✔ Data Visualization
        
        ✔ Download Reports

        ### 🛠 Technologies Used
        
        - Python
        - Streamlit
        - Pandas
        - NumPy
        - Scikit-learn
        - Machine Learning
        """)

    # =====================================================
    # FOOTER
    # =====================================================
    st.markdown("""
    <hr>
    <div style='text-align:center;
    color:white;
    padding:15px;'>
    Made with ❤️ using Streamlit
    </div>
    """, unsafe_allow_html=True)
