# ============================================================
# ui_components.py
# FRONTEND VIEW COMPONENTS & PAGE LAYOUTS WITH INTERACTIVE CHARTS
# ============================================================

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import styles


def render_prediction_page(get_categorical_values_func, on_predict_callback):
    styles.render_jump_navbar()

    # --------------------------------------------------------
    # SECTION 1: Student Information
    # --------------------------------------------------------
    st.markdown(
        '<div id="student-info" data-jump-target="student-info" class="section-card-cyan">👤 1. Student Information</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    gender_values = get_categorical_values_func("gender")
    branch_values = get_categorical_values_func("branch")
    college_tier_values = get_categorical_values_func("college_tier")
    volunteer_values = get_categorical_values_func("volunteer_experience")

    with col1:
        age = st.number_input("Age", min_value=15, max_value=40, value=21)
        gender = st.selectbox("Gender", gender_values) if gender_values else st.text_input("Gender", "Male")

    with col2:
        branch = st.selectbox("Branch", branch_values) if branch_values else st.text_input("Branch", "CSE")
        college_tier = st.selectbox("College Tier", college_tier_values) if college_tier_values else st.text_input("College Tier", "Tier 1")

    with col3:
        volunteer_experience = st.selectbox("Volunteer Experience", volunteer_values) if volunteer_values else st.selectbox("Volunteer Experience", ["Yes", "No"])
        cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=7.5, step=0.01)

    # --------------------------------------------------------
    # SECTION 2: Academic & Career Profile
    # --------------------------------------------------------
    st.markdown(
        '<div id="academic-profile" data-jump-target="academic-profile" class="section-card-amber">📚 2. Academic & Career Profile</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        internships_count = st.number_input("Internships", min_value=0, max_value=20, value=1)
        projects_count = st.number_input("Projects", min_value=0, max_value=30, value=2)
        certifications_count = st.number_input("Certifications", min_value=0, max_value=30, value=2)
        hackathons_participated = st.number_input("Hackathons Participated", min_value=0, max_value=30, value=1)

    with col2:
        github_repos = st.number_input("GitHub Repositories", min_value=0, max_value=100, value=3)
        linkedin_connections = st.number_input("LinkedIn Connections", min_value=0, max_value=5000, value=100)
        backlogs = st.number_input("Backlogs", min_value=0, max_value=20, value=0)

    with col3:
        sleep_hours = st.number_input("Sleep Hours / Day", min_value=0.0, max_value=15.0, value=7.0, step=0.1)
        study_hours_per_day = st.number_input("Study Hours / Day", min_value=0.0, max_value=15.0, value=4.0, step=0.1)

    # --------------------------------------------------------
    # SECTION 3: Skills & Performance
    # --------------------------------------------------------
    st.markdown(
        '<div id="skills-profile" data-jump-target="skills-profile" class="section-card-purple">💻 3. Skills & Performance</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        coding_skill_score = st.slider("Coding Skill Score", 0.0, 100.0, 70.0)
        aptitude_score = st.slider("Aptitude Score", 0.0, 100.0, 70.0)
        communication_skill_score = st.slider("Communication Skill Score", 0.0, 100.0, 70.0)

    with col2:
        logical_reasoning_score = st.slider("Logical Reasoning Score", 0.0, 100.0, 70.0)
        mock_interview_score = st.slider("Mock Interview Score", 0.0, 100.0, 70.0)
        attendance_percentage = st.slider("Attendance Percentage", 0.0, 100.0, 80.0)

    with col3:
        extracurricular_score = st.slider("Extracurricular Score", 0.0, 100.0, 60.0)
        leadership_score = st.slider("Leadership Score", 0.0, 100.0, 60.0)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔮 Predict Placement Success", type="primary", use_container_width=True):
        candidate_data = {
            "age": age, "gender": gender, "cgpa": cgpa, "branch": branch,
            "college_tier": college_tier, "internships_count": internships_count,
            "projects_count": projects_count, "certifications_count": certifications_count,
            "coding_skill_score": coding_skill_score, "aptitude_score": aptitude_score,
            "communication_skill_score": communication_skill_score,
            "logical_reasoning_score": logical_reasoning_score,
            "hackathons_participated": hackathons_participated,
            "github_repos": github_repos, "linkedin_connections": linkedin_connections,
            "mock_interview_score": mock_interview_score,
            "attendance_percentage": attendance_percentage, "backlogs": backlogs,
            "extracurricular_score": extracurricular_score,
            "leadership_score": leadership_score,
            "volunteer_experience": volunteer_experience, "sleep_hours": sleep_hours,
            "study_hours_per_day": study_hours_per_day
        }
        on_predict_callback(candidate_data)


def render_prediction_results(
    prediction_label,
    prob_val,
    risk_level,
    risk_class,
    intervention_priority,
    prio_class,
    weaknesses,
    recommendations,
    profile_df,
    candidate_data
):
    st.markdown("---")
    st.subheader("📊 Prediction Result & Diagnostics")

    # 1. Metric Badges Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_class = "badge-placed" if prediction_label == "PLACED" else "badge-unplaced"
        styles.render_metric_card("Predicted Outcome", prediction_label, badge_class=status_class)
    with col2:
        styles.render_metric_card("Placement Probability", f"{prob_val:.2f}%", color="#10B981" if prob_val >= 60 else "#EF4444")
    with col3:
        styles.render_metric_card("Risk Level", risk_level, badge_class=risk_class)
    with col4:
        styles.render_metric_card("Intervention Priority", intervention_priority, badge_class=prio_class)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Charts Row: Gauge Meter & Radar Chart
    col_gauge, col_radar = st.columns([1, 1])

    with col_gauge:
        st.markdown("##### 🎯 Placement Probability Meter")
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob_val,
            number={'suffix': "%", 'font': {'size': 34, 'color': '#FFFFFF'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#94A3B8'},
                'bar': {'color': "#6366F1"},
                'bgcolor': "rgba(255, 255, 255, 0.05)",
                'borderwidth': 1,
                'bordercolor': "rgba(255, 255, 255, 0.2)",
                'steps': [
                    {'range': [0, 40], 'color': "rgba(239, 68, 68, 0.25)"},
                    {'range': [40, 70], 'color': "rgba(245, 158, 11, 0.25)"},
                    {'range': [70, 100], 'color': "rgba(16, 185, 129, 0.25)"}
                ],
                'threshold': {
                    'line': {'color': "#F43F5E", 'width': 3},
                    'thickness': 0.75,
                    'value': 60
                }
            }
        ))
        gauge_fig.update_layout(
            height=290,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(gauge_fig, use_container_width=True)

    with col_radar:
        st.markdown("##### 🕸️ Competency Benchmark Comparison")
        radar_categories = ['Coding', 'Aptitude', 'Reasoning', 'Communication', 'Mock Interview', 'Leadership']
        student_scores = [
            candidate_data.get('coding_skill_score', 0),
            candidate_data.get('aptitude_score', 0),
            candidate_data.get('logical_reasoning_score', 0),
            candidate_data.get('communication_skill_score', 0),
            candidate_data.get('mock_interview_score', 0),
            candidate_data.get('leadership_score', 0)
        ]
        benchmark_scores = [70, 65, 65, 70, 70, 60]

        radar_fig = go.Figure()
        radar_fig.add_trace(go.Scatterpolar(
            r=student_scores,
            theta=radar_categories,
            fill='toself',
            name='Candidate Profile',
            line_color='#8B5CF6'
        ))
        radar_fig.add_trace(go.Scatterpolar(
            r=benchmark_scores,
            theta=radar_categories,
            fill='toself',
            name='Placement Benchmark',
            line_color='#94A3B8',
            opacity=0.35
        ))
        radar_fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255, 255, 255, 0.1)"),
                angularaxis=dict(gridcolor="rgba(255, 255, 255, 0.1)")
            ),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=290,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(radar_fig, use_container_width=True)

    # 3. Actionable Insights Row
    c_left, c_right = st.columns([1, 1])
    with c_left:
        st.markdown("##### ⚠️ Focus Areas & Weaknesses")
        if weaknesses:
            chips_html = "".join([f'<div class="weakness-chip">🚨 {w}</div>' for w in weaknesses])
            st.markdown(chips_html, unsafe_allow_html=True)
        else:
            st.success("🎉 No major structural weaknesses identified.")

    with c_right:
        st.markdown("##### 💡 Prescriptive Strategy")
        for rec in recommendations:
            st.markdown(f'<div class="recommendation-box">📌 {rec}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("👤 Candidate Profile Details")
    st.dataframe(profile_df, use_container_width=True, hide_index=True)


# ============================================================
# ENHANCED STUDENT DASHBOARD WITH ADVANCED VISUALIZATIONS
# ============================================================

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_dashboard_page(intelligence_df):
    st.markdown("## 📊 Student Placement Intelligence Dashboard")
    st.caption("Macro institutional cohort analytics, placement probability distributions, and skill gap telemetry.")

    # ------------------------------------------------------------
    # 1. Interactive Cohort Filter Bar
    # ------------------------------------------------------------
    f_col1, f_col2, f_col3 = st.columns([1.5, 1.5, 3])
    with f_col1:
        selected_tier = st.selectbox(
            "🏛️ Filter by College Tier",
            options=["All Tiers"] + sorted(intelligence_df["college_tier"].dropna().unique().tolist()) if "college_tier" in intelligence_df.columns else ["All Tiers"]
        )
    with f_col2:
        selected_branch = st.selectbox(
            "🎓 Filter by Department",
            options=["All Departments"] + sorted(intelligence_df["branch"].dropna().unique().tolist()) if "branch" in intelligence_df.columns else ["All Departments"]
        )

    # Apply filters dynamically
    filtered_df = intelligence_df.copy()
    if selected_tier != "All Tiers" and "college_tier" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["college_tier"] == selected_tier]
    if selected_branch != "All Departments" and "branch" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["branch"] == selected_branch]

    # ------------------------------------------------------------
    # 2. Executive Metric KPI Cards
    # ------------------------------------------------------------
    total_students = len(filtered_df)
    
    # Placement probability calculation
    avg_prob = filtered_df["placement_probability"].mean() if "placement_probability" in filtered_df.columns else (
        (filtered_df["placement_status"] == "Placed").mean() * 100 if "placement_status" in filtered_df.columns else 0.0
    )
    
    # At-risk counts
    if "risk_level" in filtered_df.columns:
        high_risk_count = len(filtered_df[filtered_df["risk_level"].isin(["High Risk", "Very High Risk"])])
    else:
        high_risk_count = len(filtered_df[filtered_df["cgpa"] < 6.5]) if "cgpa" in filtered_df.columns else 0

    # Critical interventions count
    if "intervention_priority" in filtered_df.columns:
        critical_count = len(filtered_df[filtered_df["intervention_priority"] == "Critical"])
    else:
        critical_count = len(filtered_df[filtered_df["backlogs"] > 0]) if "backlogs" in filtered_df.columns else 0

    # Average salary for placed candidates
    avg_salary = (
        filtered_df[filtered_df["salary_package_lpa"] > 0]["salary_package_lpa"].mean()
        if "salary_package_lpa" in filtered_df.columns and not filtered_df[filtered_df["salary_package_lpa"] > 0].empty
        else None
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        styles.render_metric_card("Total Cohort Size", f"{total_students:,}")
    with c2:
        styles.render_metric_card("Mean Placement Rate", f"{avg_prob:.1f}%", color="#10B981" if avg_prob >= 60 else "#38BDF8")
    with c3:
        styles.render_metric_card("At-Risk Students", f"{high_risk_count:,}", color="#F59E0B")
    with c4:
        if avg_salary is not None:
            styles.render_metric_card("Avg Package (Placed)", f"₹{avg_salary:.2f} LPA", color="#A855F7")
        else:
            styles.render_metric_card("Critical Interventions", f"{critical_count:,}", color="#EF4444")

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------------
    # 3. Chart Row 1: Donut Charts (Risk & Priority Tiers)
    # ------------------------------------------------------------
    r1_left, r1_right = st.columns(2)

    with r1_left:
        st.markdown("##### 🚨 Risk Categorization Distribution")
        if "risk_level" in filtered_df.columns:
            risk_counts = filtered_df["risk_level"].value_counts().reset_index()
            risk_counts.columns = ["Risk Tier", "Students"]
            risk_color_map = {
                "Low Risk": "#10B981",
                "Moderate Risk": "#FBBF24",
                "High Risk": "#F97316",
                "Very High Risk": "#EF4444"
            }
            fig_risk = px.pie(
                risk_counts,
                names="Risk Tier",
                values="Students",
                hole=0.55,
                color="Risk Tier",
                color_discrete_map=risk_color_map
            )
            fig_risk.update_traces(textinfo="percent+label", textfont=dict(size=12))
            fig_risk.update_layout(
                height=340,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_risk, use_container_width=True)
        else:
            st.info("Risk level data not available.")

    with r1_right:
        st.markdown("##### 🎯 Intervention Priority Tiers")
        if "intervention_priority" in filtered_df.columns:
            prio_counts = filtered_df["intervention_priority"].value_counts().reset_index()
            prio_counts.columns = ["Priority Level", "Students"]
            prio_color_map = {
                "Low": "#34D399",
                "Medium": "#FCD34D",
                "High": "#FB923C",
                "Critical": "#F87171"
            }
            fig_prio = px.pie(
                prio_counts,
                names="Priority Level",
                values="Students",
                hole=0.55,
                color="Priority Level",
                color_discrete_map=prio_color_map
            )
            fig_prio.update_traces(textinfo="percent+label", textfont=dict(size=12))
            fig_prio.update_layout(
                height=340,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_prio, use_container_width=True)
        else:
            st.info("Intervention priority column not present.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------------
    # 4. Chart Row 2: Department Placement Breakdown & Salary Boxplot
    # ------------------------------------------------------------
    r2_left, r2_right = st.columns(2)

    with r2_left:
        st.markdown("##### 🏫 Departmental Placement Ratio")
        status_col = "placement_status" if "placement_status" in filtered_df.columns else "predicted_placement"
        
        if "branch" in filtered_df.columns and status_col in filtered_df.columns:
            branch_status = (
                filtered_df.groupby(["branch", status_col])
                .size()
                .reset_index(name="Count")
            )
            fig_branch = px.bar(
                branch_status,
                x="Count",
                y="branch",
                color=status_col,
                orientation="h",
                barmode="stack",
                color_discrete_map={"Placed": "#10B981", "Not Placed": "#EF4444"},
                labels={"branch": "Department", "Count": "Students"}
            )
            fig_branch.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)"),
                yaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_branch, use_container_width=True)

    with r2_right:
        st.markdown("##### 💼 Salary Package (LPA) Distribution by Tier")
        if "salary_package_lpa" in filtered_df.columns and "college_tier" in filtered_df.columns:
            placed_salaries = filtered_df[filtered_df["salary_package_lpa"] > 0]
            if not placed_salaries.empty:
                fig_box = px.box(
                    placed_salaries,
                    x="college_tier",
                    y="salary_package_lpa",
                    color="college_tier",
                    color_discrete_sequence=["#8B5CF6", "#06B6D4", "#EC4899"],
                    points="outliers",
                    labels={"college_tier": "Institution Tier", "salary_package_lpa": "Package (LPA)"}
                )
                fig_box.update_layout(
                    height=350,
                    showlegend=False,
                    margin=dict(l=20, r=20, t=20, b=20),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)"),
                    yaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)")
                )
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.info("No placed salary packages recorded for current filter.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------------
    # 5. Chart Row 3: Readiness Factors & CGPA vs Coding Heatmap
    # ------------------------------------------------------------
    r3_left, r3_right = st.columns(2)

    with r3_left:
        st.markdown("##### 🔬 Competency Drivers (Placed vs. Not Placed)")
        status_target = "placement_status" if "placement_status" in filtered_df.columns else "predicted_placement"
        tracked_metrics = [
            "coding_skill_score", "aptitude_score", "logical_reasoning_score",
            "communication_skill_score", "mock_interview_score"
        ]
        available_metrics = [m for m in tracked_metrics if m in filtered_df.columns]

        if status_target in filtered_df.columns and len(available_metrics) >= 3:
            avg_metrics = filtered_df.groupby(status_target)[available_metrics].mean().reset_index()
            melted = avg_metrics.melt(id_vars=status_target, var_name="Competency", value_name="Average Score")
            melted["Competency"] = melted["Competency"].str.replace("_score", "").str.replace("_", " ").str.title()

            fig_driver = px.bar(
                melted,
                x="Competency",
                y="Average Score",
                color=status_target,
                barmode="group",
                color_discrete_map={"Placed": "#6366F1", "Not Placed": "#94A3B8"}
            )
            fig_driver.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)"),
                yaxis=dict(range=[0, 100], gridcolor="rgba(255, 255, 255, 0.08)"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_driver, use_container_width=True)

    with r3_right:
        st.markdown("##### 📈 CGPA vs. Coding Skill Density")
        if "cgpa" in filtered_df.columns and "coding_skill_score" in filtered_df.columns:
            status_col = "placement_status" if "placement_status" in filtered_df.columns else None
            
            # Sample up to 1,500 points for smooth, non-blocking rendering
            sample_df = filtered_df.sample(min(1500, len(filtered_df)), random_state=42)
            
            fig_density = px.scatter(
                sample_df,
                x="cgpa",
                y="coding_skill_score",
                color=status_col if status_col else "backlogs",
                color_discrete_map={"Placed": "#10B981", "Not Placed": "#EF4444"} if status_col else None,
                color_continuous_scale="Viridis" if not status_col else None,
                opacity=0.6,
                labels={"cgpa": "Cumulative CGPA", "coding_skill_score": "Coding Assessment Score"}
            )
            fig_density.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)"),
                yaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_density, use_container_width=True)

def render_early_intervention_page(intelligence_df):
    st.header("🚨 Early Intervention & Triage Center")

    if "intervention_priority" not in intelligence_df.columns:
        st.warning("The intelligence dataset does not contain 'intervention_priority'.")
        return

    priority = st.selectbox("Filter by Priority Tier", ["All", "Critical", "High", "Medium", "Low"])
    filtered_df = intelligence_df.copy() if priority == "All" else intelligence_df[intelligence_df["intervention_priority"] == priority].copy()

    st.metric("Candidates Requiring Attention", f"{len(filtered_df):,}")
    st.markdown("---")

    display_columns = [
        "student_id", "cgpa", "branch", "placement_probability",
        "risk_level", "intervention_priority", "identified_weaknesses", "recommendations"
    ]
    available_columns = [col for col in display_columns if col in filtered_df.columns]

    if available_columns:
        st.dataframe(filtered_df[available_columns], use_container_width=True, hide_index=True)


def render_advisor_page(on_submit_query_callback):
    st.header("💬 AI Career & Placement Advisor")
    st.caption("Personalized placement tactics, interview guidance, and technical prep advice.")

    if "advisor_messages" not in st.session_state:
        st.session_state.advisor_messages = [
            {"role": "assistant", "content": "Hello! I am your AI Career Advisor. Share your current year, branch, target job roles, or weaknesses, and I will draft a tactical prep plan for you."}
        ]

    for msg in st.session_state.advisor_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask for advice (e.g., 'How can a Tier 3 CSE student prepare for tech interviews with 6.8 CGPA?')")
    if user_query:
        st.session_state.advisor_messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            reply = on_submit_query_callback(user_query, st.session_state.advisor_messages)
            st.markdown(reply)
            st.session_state.advisor_messages.append({"role": "assistant", "content": reply})


def render_model_info_page(features_list):
    st.markdown("## 🤖 Machine Learning System Architecture & Metadata")
    st.caption("Detailed architectural specifications, training dataset intelligence, and input feature registry.")

    # ------------------------------------------------------------
    # 1. Dataset & Pipeline High-Level KPIs
    # ------------------------------------------------------------
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        styles.render_metric_card("Training Cohort", "100,000 Records", color="#06B6D4")
    with k2:
        styles.render_metric_card("Monitored Dimensions", f"{len(features_list)} Features", color="#A855F7")
    with k3:
        styles.render_metric_card("Primary Objective", "Binary Placement", color="#10B981")
    with k4:
        styles.render_metric_card("Calibration Method", "Sigmoid Probability", color="#F59E0B")

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------------
    # 2. Section: Dataset Intelligence
    # ------------------------------------------------------------
    st.markdown('<div class="section-card-cyan">📁 1. Dataset Overview & Demographics</div>', unsafe_allow_html=True)
    
    col_d1, col_d2 = st.columns([1.2, 0.8])
    with col_d1:
        st.markdown(
            """
            The predictive engine is trained on **100,000 verified student records** simulating multi-campus university recruitment drives:
            - **Target Variable**: `placement_status` (0 = *Not Placed*, 1 = *Placed*) with balanced distribution (~54.5% Placed / ~45.5% Not Placed).
            - **Salary Package Tracking**: Tracks `salary_package_lpa` for placed candidates to evaluate package tier distributions.
            - **Multimodal Feature Spread**: Incorporates cognitive test percentiles, continuous GPA records, professional outreach activity, and health/lifestyle habits.
            - **Pre-processing Protocol**: Scaled using standard z-score normalization for continuous variables and one-hot encoding for categorical variables.
            """
        )
    with col_d2:
        st.markdown(
            """
            <div class="metric-card" style="padding: 16px;">
                <div style="font-size: 13px; font-weight: 700; color: #94A3B8; text-transform: uppercase;">Dataset Distribution</div>
                <div style="margin-top: 10px; font-size: 13.5px; line-height: 1.8;">
                    🏛️ <b>College Tiers</b>: Tier 1, Tier 2, Tier 3<br>
                    🎓 <b>Departments</b>: CSE, IT, ECE, EEE, Mechanical, Civil<br>
                    ⚖️ <b>Class Balance</b>: 54.46% Placed : 45.54% Unplaced<br>
                    🔍 <b>Missing Values</b>: 0 (Imputed & Cleaned)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------------
    # 3. Section: Model Architecture
    # ------------------------------------------------------------
    st.markdown('<div class="section-card-purple">🧠 2. Model Pipeline & Architecture</div>', unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    with m1:
        st.markdown(
            """
            <div class="metric-card">
                <div style="font-size: 15px; font-weight: 700; color: #C084FC; margin-bottom: 8px;">
                    ⚡ Ensemble Classifier Pipeline
                </div>
                <p style="font-size: 13.5px; color: #94A3B8; line-height: 1.6; margin: 0;">
                    Constructed using an optimized <b>Gradient Boosting & Random Forest ensemble</b> with probability calibration. 
                    The model generates soft class probabilities via <code>predict_proba</code>, enabling dynamic risk tier stratification:
                </p>
                <div style="margin-top: 12px; font-size: 12.5px;">
                    <span class="badge badge-low">Low Risk: ≥ 80%</span>
                    <span class="badge badge-medium">Moderate: 60% - 79%</span>
                    <span class="badge badge-high">High: 40% - 59%</span>
                    <span class="badge badge-critical">Critical: &lt; 40%</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            """
            <div class="metric-card">
                <div style="font-size: 15px; font-weight: 700; color: #C084FC; margin-bottom: 8px;">
                    🎯 Decision Thresholds & Inference Rules
                </div>
                <ul style="font-size: 13.5px; color: #94A3B8; line-height: 1.7; margin: 0; padding-left: 18px;">
                    <li><b>Decision Boundary</b>: Default threshold set at <i>p = 0.50</i> for binary placement determination.</li>
                    <li><b>Vulnerability Heuristics</b>: 17 rules cross-evaluate weaknesses across CGPA (&lt; 6.5), Backlogs (&gt; 0), and Coding (&lt; 60).</li>
                    <li><b>Inference Latency</b>: Sub-millisecond vectorized inference execution per single profile evaluation.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------------
    # 4. Section: Structured Feature Schema
    # ------------------------------------------------------------
    st.markdown('<div class="section-card-amber">📋 3. Categorized Input Feature Registry</div>', unsafe_allow_html=True)
    st.caption("All 23 input vectors categorized by domain with expected ranges and data types.")

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        st.markdown("##### 📚 Academic & Institutional Metrics")
        academic_features = pd.DataFrame([
            {"Feature": "cgpa", "Type": "Float", "Range": "0.0 - 10.0", "Description": "Cumulative Grade Point Average"},
            {"Feature": "branch", "Type": "Categorical", "Range": "6 Branches", "Description": "CSE, IT, ECE, EEE, ME, Civil"},
            {"Feature": "college_tier", "Type": "Categorical", "Range": "Tier 1 - 3", "Description": "Institutional ranking tier"},
            {"Feature": "attendance_percentage", "Type": "Float", "Range": "0% - 100%", "Description": "Overall semester lecture attendance"},
            {"Feature": "backlogs", "Type": "Integer", "Range": "0 - 10+", "Description": "Count of active failed subjects"},
            {"Feature": "age", "Type": "Integer", "Range": "18 - 35", "Description": "Candidate age in years"},
            {"Feature": "gender", "Type": "Categorical", "Range": "M / F / Other", "Description": "Demographic identification"}
        ])
        st.dataframe(academic_features, use_container_width=True, hide_index=True)

        st.markdown("##### 💼 Industry & Professional Exposure")
        industry_features = pd.DataFrame([
            {"Feature": "internships_count", "Type": "Integer", "Range": "0 - 10", "Description": "Completed corporate internships"},
            {"Feature": "projects_count", "Type": "Integer", "Range": "0 - 15", "Description": "Major software/hardware projects"},
            {"Feature": "certifications_count", "Type": "Integer", "Range": "0 - 15", "Description": "Industry recognized certifications"},
            {"Feature": "hackathons_participated", "Type": "Integer", "Range": "0 - 20", "Description": "Competitive hackathons attended"},
            {"Feature": "github_repos", "Type": "Integer", "Range": "0 - 50+", "Description": "Public code repositories hosted"},
            {"Feature": "linkedin_connections", "Type": "Integer", "Range": "0 - 5000+", "Description": "Professional network reach"}
        ])
        st.dataframe(industry_features, use_container_width=True, hide_index=True)

    with col_f2:
        st.markdown("##### 💻 Technical & Cognitive Competencies")
        cognitive_features = pd.DataFrame([
            {"Feature": "coding_skill_score", "Type": "Float", "Range": "0 - 100", "Description": "DSA and coding assessment score"},
            {"Feature": "aptitude_score", "Type": "Float", "Range": "0 - 100", "Description": "Quantitative ability and math score"},
            {"Feature": "logical_reasoning_score", "Type": "Float", "Range": "0 - 100", "Description": "Analytical & puzzle solving score"},
            {"Feature": "communication_skill_score", "Type": "Float", "Range": "0 - 100", "Description": "Verbal and presentation score"},
            {"Feature": "mock_interview_score", "Type": "Float", "Range": "0 - 100", "Description": "Behavioral round performance score"}
        ])
        st.dataframe(cognitive_features, use_container_width=True, hide_index=True)

        st.markdown("##### 🧘 Behavioral & Personal Habits")
        lifestyle_features = pd.DataFrame([
            {"Feature": "study_hours_per_day", "Type": "Float", "Range": "0.0 - 15.0", "Description": "Dedicated self-study hours daily"},
            {"Feature": "sleep_hours", "Type": "Float", "Range": "3.0 - 12.0", "Description": "Average daily sleep duration"},
            {"Feature": "extracurricular_score", "Type": "Float", "Range": "0 - 100", "Description": "Club and community involvement"},
            {"Feature": "leadership_score", "Type": "Float", "Range": "0 - 100", "Description": "Team lead and organizational roles"},
            {"Feature": "volunteer_experience", "Type": "Categorical", "Range": "Yes / No", "Description": "Social & non-profit volunteer work"}
        ])
        st.dataframe(lifestyle_features, use_container_width=True, hide_index=True)