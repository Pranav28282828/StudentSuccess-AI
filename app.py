# ============================================================
# app.py
# AI-BASED EARLY STUDENT SUCCESS & PLACEMENT PREDICTION SYSTEM
# ============================================================

import os
import pickle
import requests
import pandas as pd
import streamlit as st

from dotenv import load_dotenv

# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)
# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Student Success & Placement",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# 2. PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "notebook",
    "student_placement_model.pkl"
)

CONFIG_PATH = os.path.join(
    BASE_DIR,
    "notebook",
    "streamlit_config.pkl"
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "student_success_intelligence.csv"
)


# ============================================================
# 3. CHECK REQUIRED FILES
# ============================================================

required_files = {
    "Student Placement Model": MODEL_PATH,
    "Streamlit Configuration": CONFIG_PATH,
    "Student Intelligence Dataset": DATA_PATH
}

missing_files = []

for name, path in required_files.items():

    if not os.path.exists(path):

        missing_files.append(
            f"{name}: {path}"
        )


if missing_files:

    st.error(
        "❌ Required project files were not found."
    )

    st.write(
        "The application is looking for:"
    )

    for file in missing_files:

        st.code(file)

    st.stop()


# ============================================================
# 4. LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    with open(
        MODEL_PATH,
        "rb"
    ) as file:

        return pickle.load(file)


# ============================================================
# 5. LOAD CONFIGURATION
# ============================================================

@st.cache_resource
def load_config():

    with open(
        CONFIG_PATH,
        "rb"
    ) as file:

        return pickle.load(file)


# ============================================================
# 6. LOAD STUDENT INTELLIGENCE DATA
# ============================================================

@st.cache_data
def load_intelligence_data():

    return pd.read_csv(
        DATA_PATH
    )


# ============================================================
# 7. LOAD ALL COMPONENTS
# ============================================================

try:

    model = load_model()

    config = load_config()

    intelligence_df = load_intelligence_data()

except Exception as e:

    st.error(
        "❌ Unable to load the model or configuration."
    )

    st.code(
        str(e)
    )

    st.stop()


# ============================================================
# 8. CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 9. SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title(
    "🎓 Student Success AI"
)

st.sidebar.caption(
    "Early Success & Placement Intelligence"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🔮 Student Prediction",
        "📊 Student Dashboard",
        "🚨 Early Intervention",
        "💬 AI Career Advisor",
        "🤖 Model Information"
    ]
)


# ============================================================
# 10. MAIN HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
        🎓 AI-Based Early Student Success & Placement Prediction
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Predict placement probability, identify student risk,
        and provide personalized early-intervention support.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# 11. HELPER FUNCTIONS
# ============================================================

def get_model_features():

    """
    Get the exact feature order stored during model preparation.
    """

    if isinstance(config, dict):

        if "model_features" in config:

            return config["model_features"]

    # Fallback based on the final dataset structure
    return [
        "age",
        "gender",
        "cgpa",
        "branch",
        "college_tier",
        "internships_count",
        "projects_count",
        "certifications_count",
        "coding_skill_score",
        "aptitude_score",
        "communication_skill_score",
        "logical_reasoning_score",
        "hackathons_participated",
        "github_repos",
        "linkedin_connections",
        "mock_interview_score",
        "attendance_percentage",
        "backlogs",
        "extracurricular_score",
        "leadership_score",
        "volunteer_experience",
        "sleep_hours",
        "study_hours_per_day"
    ]


def get_categorical_values(column):

    """
    Get categorical values from configuration.
    """

    if isinstance(config, dict):

        categorical_values = config.get(
            "categorical_values",
            {}
        )

        if column in categorical_values:

            return categorical_values[column]

    # Fallback values from the final dataset
    if column in intelligence_df.columns:

        return sorted(
            intelligence_df[column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    return []


def calculate_risk(probability):

    if probability >= 80:

        return "Low Risk"

    elif probability >= 60:

        return "Moderate Risk"

    elif probability >= 40:

        return "High Risk"

    else:

        return "Very High Risk"


def get_placement_probability(input_data):

    """
    Safely obtain the probability of the positive/placed class.
    """

    if not hasattr(
        model,
        "predict_proba"
    ):

        return None

    probabilities = model.predict_proba(
        input_data
    )[0]

    classes = getattr(
        model,
        "classes_",
        None
    )

    if classes is None:

        return float(
            probabilities[-1] * 100
        )

    # Look for the positive/placed class
    for index, class_value in enumerate(classes):

        class_text = str(
            class_value
        ).lower()

        if (
            class_text in [
                "1",
                "placed",
                "yes",
                "true"
            ]
            or "placed" in class_text
        ):

            return float(
                probabilities[index] * 100
            )

    # Fallback
    return float(
        probabilities[-1] * 100
    )


def get_prediction_label(prediction):

    prediction_text = str(
        prediction
    ).lower()

    if prediction_text in [
        "1",
        "placed",
        "yes",
        "true"
    ]:

        return "PLACED"

    if "placed" in prediction_text:

        return "PLACED"

    return "NOT PLACED"


def identify_weaknesses(
    cgpa,
    coding_skill_score,
    aptitude_score,
    communication_skill_score,
    logical_reasoning_score,
    mock_interview_score,
    internships_count,
    projects_count,
    certifications_count,
    hackathons_participated,
    github_repos,
    linkedin_connections,
    attendance_percentage,
    extracurricular_score,
    leadership_score,
    study_hours_per_day,
    backlogs
):

    weaknesses = []

    if cgpa < 6.5:
        weaknesses.append(
            "Academic Performance"
        )

    if coding_skill_score < 60:
        weaknesses.append(
            "Coding Skills"
        )

    if aptitude_score < 60:
        weaknesses.append(
            "Aptitude Skills"
        )

    if communication_skill_score < 60:
        weaknesses.append(
            "Communication Skills"
        )

    if logical_reasoning_score < 60:
        weaknesses.append(
            "Logical Reasoning"
        )

    if mock_interview_score < 60:
        weaknesses.append(
            "Interview Preparation"
        )

    if internships_count == 0:
        weaknesses.append(
            "Industry Experience"
        )

    if projects_count < 2:
        weaknesses.append(
            "Projects"
        )

    if certifications_count < 2:
        weaknesses.append(
            "Certifications"
        )

    if hackathons_participated == 0:
        weaknesses.append(
            "Hackathon Participation"
        )

    if github_repos < 2:
        weaknesses.append(
            "GitHub Portfolio"
        )

    if linkedin_connections < 50:
        weaknesses.append(
            "Professional Networking"
        )

    if attendance_percentage < 75:
        weaknesses.append(
            "Attendance"
        )

    if extracurricular_score < 50:
        weaknesses.append(
            "Extracurricular Activities"
        )

    if leadership_score < 50:
        weaknesses.append(
            "Leadership Skills"
        )

    if study_hours_per_day < 3:
        weaknesses.append(
            "Study Routine"
        )

    if backlogs > 0:
        weaknesses.append(
            "Academic Backlogs"
        )

    return weaknesses


def generate_recommendations(
    weaknesses
):

    recommendations = []

    recommendation_map = {

        "Academic Performance":
            "Improve CGPA through consistent study and revision.",

        "Coding Skills":
            "Practice coding and problem-solving regularly.",

        "Aptitude Skills":
            "Practice quantitative aptitude and logical reasoning.",

        "Communication Skills":
            "Improve communication through presentations and group discussions.",

        "Logical Reasoning":
            "Practice analytical and logical reasoning questions.",

        "Interview Preparation":
            "Attend mock interviews and improve interview preparation.",

        "Industry Experience":
            "Gain practical industry experience through internships.",

        "Projects":
            "Build additional real-world projects.",

        "Certifications":
            "Complete relevant technical certifications.",

        "Hackathon Participation":
            "Participate in hackathons and technical competitions.",

        "GitHub Portfolio":
            "Build a stronger GitHub project portfolio.",

        "Professional Networking":
            "Improve professional networking and LinkedIn presence.",

        "Attendance":
            "Improve attendance and academic participation.",

        "Extracurricular Activities":
            "Participate in extracurricular activities.",

        "Leadership Skills":
            "Develop leadership skills through team activities.",

        "Study Routine":
            "Increase focused daily study time.",

        "Academic Backlogs":
            "Focus on clearing academic backlogs."
    }

    for weakness in weaknesses:

        if weakness in recommendation_map:

            recommendations.append(
                recommendation_map[weakness]
            )

    if not recommendations:

        recommendations.append(
            "Maintain current performance and focus on placement preparation."
        )

    return recommendations


# ============================================================
# 12. STUDENT PREDICTION PAGE
# ============================================================

if page == "🔮 Student Prediction":

    st.header(
        "🔮 Student Placement Prediction"
    )

    st.write(
        "Enter the student's academic, technical, "
        "professional and personal information."
    )

    # --------------------------------------------------------
    # Student Information
    # --------------------------------------------------------

    st.subheader(
        "👤 Student Information"
    )

    col1, col2, col3 = st.columns(3)

    gender_values = get_categorical_values(
        "gender"
    )

    branch_values = get_categorical_values(
        "branch"
    )

    college_tier_values = get_categorical_values(
        "college_tier"
    )

    volunteer_values = get_categorical_values(
        "volunteer_experience"
    )

    with col1:

        age = st.number_input(
            "Age",
            min_value=15,
            max_value=40,
            value=21
        )

        if gender_values:

            gender = st.selectbox(
                "Gender",
                gender_values
            )

        else:

            gender = st.text_input(
                "Gender",
                "Male"
            )

    with col2:

        if branch_values:

            branch = st.selectbox(
                "Branch",
                branch_values
            )

        else:

            branch = st.text_input(
                "Branch",
                "CSE"
            )

        if college_tier_values:

            college_tier = st.selectbox(
                "College Tier",
                college_tier_values
            )

        else:

            college_tier = st.text_input(
                "College Tier",
                "Tier 1"
            )

    with col3:

        if volunteer_values:

            volunteer_experience = st.selectbox(
                "Volunteer Experience",
                volunteer_values
            )

        else:

            volunteer_experience = st.selectbox(
                "Volunteer Experience",
                ["Yes", "No"]
            )

        cgpa = st.number_input(
            "CGPA",
            min_value=0.0,
            max_value=10.0,
            value=7.5,
            step=0.01
        )

    st.divider()

    # --------------------------------------------------------
    # Academic & Career Profile
    # --------------------------------------------------------

    st.subheader(
        "📚 Academic & Career Profile"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        internships_count = st.number_input(
            "Internships",
            min_value=0,
            max_value=20,
            value=1
        )

        projects_count = st.number_input(
            "Projects",
            min_value=0,
            max_value=30,
            value=2
        )

        certifications_count = st.number_input(
            "Certifications",
            min_value=0,
            max_value=30,
            value=2
        )

        hackathons_participated = st.number_input(
            "Hackathons Participated",
            min_value=0,
            max_value=30,
            value=1
        )

    with col2:

        github_repos = st.number_input(
            "GitHub Repositories",
            min_value=0,
            max_value=100,
            value=3
        )

        linkedin_connections = st.number_input(
            "LinkedIn Connections",
            min_value=0,
            max_value=5000,
            value=100
        )

        backlogs = st.number_input(
            "Backlogs",
            min_value=0,
            max_value=20,
            value=0
        )

    with col3:

        sleep_hours = st.number_input(
            "Sleep Hours / Day",
            min_value=0.0,
            max_value=15.0,
            value=7.0,
            step=0.1
        )

        study_hours_per_day = st.number_input(
            "Study Hours / Day",
            min_value=0.0,
            max_value=15.0,
            value=4.0,
            step=0.1
        )

    st.divider()

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    st.subheader(
        "💻 Skills & Performance"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        coding_skill_score = st.slider(
            "Coding Skill Score",
            0.0,
            100.0,
            70.0
        )

        aptitude_score = st.slider(
            "Aptitude Score",
            0.0,
            100.0,
            70.0
        )

        communication_skill_score = st.slider(
            "Communication Skill Score",
            0.0,
            100.0,
            70.0
        )

    with col2:

        logical_reasoning_score = st.slider(
            "Logical Reasoning Score",
            0.0,
            100.0,
            70.0
        )

        mock_interview_score = st.slider(
            "Mock Interview Score",
            0.0,
            100.0,
            70.0
        )

        attendance_percentage = st.slider(
            "Attendance Percentage",
            0.0,
            100.0,
            80.0
        )

    with col3:

        extracurricular_score = st.slider(
            "Extracurricular Score",
            0.0,
            100.0,
            60.0
        )

        leadership_score = st.slider(
            "Leadership Score",
            0.0,
            100.0,
            60.0
        )

    st.divider()

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    predict = st.button(
        "🔮 Predict Student Success",
        type="primary",
        use_container_width=True
    )

    if predict:

        input_data = pd.DataFrame(
            [{
                "age": age,
                "gender": gender,
                "cgpa": cgpa,
                "branch": branch,
                "college_tier": college_tier,
                "internships_count": internships_count,
                "projects_count": projects_count,
                "certifications_count": certifications_count,
                "coding_skill_score": coding_skill_score,
                "aptitude_score": aptitude_score,
                "communication_skill_score": communication_skill_score,
                "logical_reasoning_score": logical_reasoning_score,
                "hackathons_participated": hackathons_participated,
                "github_repos": github_repos,
                "linkedin_connections": linkedin_connections,
                "mock_interview_score": mock_interview_score,
                "attendance_percentage": attendance_percentage,
                "backlogs": backlogs,
                "extracurricular_score": extracurricular_score,
                "leadership_score": leadership_score,
                "volunteer_experience": volunteer_experience,
                "sleep_hours": sleep_hours,
                "study_hours_per_day": study_hours_per_day
            }]
        )

        # ----------------------------------------------------
        # Arrange features exactly as model expects
        # ----------------------------------------------------

        model_features = get_model_features()

        missing_features = [
            feature
            for feature in model_features
            if feature not in input_data.columns
        ]

        if missing_features:

            st.error(
                "The following model features are missing:"
            )

            st.write(
                missing_features
            )

            st.stop()

        input_data = input_data[
            model_features
        ]

        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        try:

            prediction = model.predict(
                input_data
            )[0]

            prediction_label = get_prediction_label(
                prediction
            )

            placement_probability = (
                get_placement_probability(
                    input_data
                )
            )

        except Exception as e:

            st.error(
                "❌ Prediction failed."
            )

            st.code(
                str(e)
            )

            st.stop()

        # ----------------------------------------------------
        # Risk
        # ----------------------------------------------------

        if placement_probability is not None:

            risk_level = calculate_risk(
                placement_probability
            )

        else:

            risk_level = "Not Available"

        # ----------------------------------------------------
        # Weaknesses
        # ----------------------------------------------------

        weaknesses = identify_weaknesses(
            cgpa,
            coding_skill_score,
            aptitude_score,
            communication_skill_score,
            logical_reasoning_score,
            mock_interview_score,
            internships_count,
            projects_count,
            certifications_count,
            hackathons_participated,
            github_repos,
            linkedin_connections,
            attendance_percentage,
            extracurricular_score,
            leadership_score,
            study_hours_per_day,
            backlogs
        )

        weakness_count = len(
            weaknesses
        )

        # ----------------------------------------------------
        # Intervention Priority
        # ----------------------------------------------------

        if (
            risk_level == "Very High Risk"
            or weakness_count >= 6
        ):

            intervention_priority = "Critical"

        elif (
            risk_level == "High Risk"
            or weakness_count >= 4
        ):

            intervention_priority = "High"

        elif (
            risk_level == "Moderate Risk"
            or weakness_count >= 2
        ):

            intervention_priority = "Medium"

        else:

            intervention_priority = "Low"

        # ----------------------------------------------------
        # Recommendations
        # ----------------------------------------------------

        recommendations = generate_recommendations(
            weaknesses
        )

        # ----------------------------------------------------
        # Results
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "📊 Prediction Result"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            if prediction_label == "PLACED":

                st.success(
                    "🎉 PLACED"
                )

            else:

                st.error(
                    "⚠️ NOT PLACED"
                )

        with col2:

            if placement_probability is not None:

                st.metric(
                    "Placement Probability",
                    f"{placement_probability:.2f}%"
                )

            else:

                st.metric(
                    "Placement Probability",
                    "N/A"
                )

        with col3:

            st.metric(
                "Risk Level",
                risk_level
            )

        with col4:

            st.metric(
                "Intervention",
                intervention_priority
            )

        if placement_probability is not None:

            st.progress(
                min(
                    max(
                        int(
                            placement_probability
                        ),
                        0
                    ),
                    100
                )
            )

        # ----------------------------------------------------
        # Areas Requiring Attention
        # ----------------------------------------------------

        st.subheader(
            "⚠️ Areas Requiring Attention"
        )

        if weaknesses:

            for weakness in weaknesses:

                st.warning(
                    weakness
                )

        else:

            st.success(
                "No major weaknesses identified."
            )

        # ----------------------------------------------------
        # Recommendations
        # ----------------------------------------------------

        st.subheader(
            "💡 Personalized Recommendations"
        )

        for recommendation in recommendations:

            st.info(
                recommendation
            )

        # ----------------------------------------------------
        # Student Profile
        # ----------------------------------------------------

        st.subheader(
            "👤 Student Profile"
        )

        profile_df = pd.DataFrame(
            {
                "Metric": [
                    "CGPA",
                    "Internships",
                    "Projects",
                    "Certifications",
                    "Coding Score",
                    "Aptitude Score",
                    "Communication Score",
                    "Logical Reasoning",
                    "Mock Interview",
                    "Attendance",
                    "Backlogs",
                    "Study Hours / Day"
                ],
                "Value": [
                    cgpa,
                    internships_count,
                    projects_count,
                    certifications_count,
                    coding_skill_score,
                    aptitude_score,
                    communication_skill_score,
                    logical_reasoning_score,
                    mock_interview_score,
                    attendance_percentage,
                    backlogs,
                    study_hours_per_day
                ]
            }
        )

        st.dataframe(
            profile_df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# 13. STUDENT DASHBOARD
# ============================================================

elif page == "📊 Student Dashboard":

    st.header(
        "📊 Student Success Dashboard"
    )

    total_students = len(
        intelligence_df
    )

    col1, col2, col3, col4 = st.columns(4)

    if "placement_probability" in intelligence_df.columns:

        average_probability = (
            intelligence_df[
                "placement_probability"
            ].mean()
        )

    else:

        average_probability = None

    if "risk_level" in intelligence_df.columns:

        high_risk_students = intelligence_df[
            intelligence_df[
                "risk_level"
            ].isin(
                [
                    "High Risk",
                    "Very High Risk"
                ]
            )
        ]

    else:

        high_risk_students = pd.DataFrame()

    if "intervention_priority" in intelligence_df.columns:

        critical_students = intelligence_df[
            intelligence_df[
                "intervention_priority"
            ] == "Critical"
        ]

    else:

        critical_students = pd.DataFrame()

    with col1:

        st.metric(
            "Total Students",
            f"{total_students:,}"
        )

    with col2:

        if average_probability is not None:

            st.metric(
                "Average Placement Probability",
                f"{average_probability:.2f}%"
            )

        else:

            st.metric(
                "Average Placement Probability",
                "N/A"
            )

    with col3:

        st.metric(
            "High-Risk Students",
            f"{len(high_risk_students):,}"
        )

    with col4:

        st.metric(
            "Critical Students",
            f"{len(critical_students):,}"
        )

    st.divider()

    # --------------------------------------------------------
    # Risk Distribution
    # --------------------------------------------------------

    if "risk_level" in intelligence_df.columns:

        st.subheader(
            "🚨 Risk Distribution"
        )

        st.bar_chart(
            intelligence_df[
                "risk_level"
            ].value_counts()
        )

    # --------------------------------------------------------
    # Intervention Priority
    # --------------------------------------------------------

    if "intervention_priority" in intelligence_df.columns:

        st.subheader(
            "🎯 Intervention Priority"
        )

        st.bar_chart(
            intelligence_df[
                "intervention_priority"
            ].value_counts()
        )

    # --------------------------------------------------------
    # Placement Distribution
    # --------------------------------------------------------

    if "predicted_placement" in intelligence_df.columns:

        st.subheader(
            "🎓 Predicted Placement Distribution"
        )

        st.bar_chart(
            intelligence_df[
                "predicted_placement"
            ].value_counts()
        )

    # --------------------------------------------------------
    # Branch Analysis
    # --------------------------------------------------------

    if (
        "branch" in intelligence_df.columns
        and
        "placement_probability" in intelligence_df.columns
    ):

        st.subheader(
            "🏫 Placement Probability by Branch"
        )

        branch_analysis = (
            intelligence_df
            .groupby("branch")[
                "placement_probability"
            ]
            .mean()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            branch_analysis
        )


# ============================================================
# 14. EARLY INTERVENTION
# ============================================================

elif page == "🚨 Early Intervention":

    st.header(
        "🚨 Early Intervention Center"
    )

    if "intervention_priority" not in intelligence_df.columns:

        st.warning(
            "The intelligence dataset does not contain "
            "'intervention_priority'."
        )

    else:

        priority = st.selectbox(
            "Intervention Priority",
            [
                "All",
                "Critical",
                "High",
                "Medium",
                "Low"
            ]
        )

        if priority == "All":

            filtered_df = intelligence_df.copy()

        else:

            filtered_df = intelligence_df[
                intelligence_df[
                    "intervention_priority"
                ] == priority
            ].copy()

        st.metric(
            "Students Found",
            f"{len(filtered_df):,}"
        )

        st.divider()

        display_columns = [
            "student_id",
            "cgpa",
            "branch",
            "placement_probability",
            "risk_level",
            "intervention_priority",
            "identified_weaknesses",
            "recommendations"
        ]

        available_columns = [
            column
            for column in display_columns
            if column in filtered_df.columns
        ]

        if available_columns:

            st.dataframe(
                filtered_df[
                    available_columns
                ],
                use_container_width=True,
                hide_index=True
            )

        else:

            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # Download
        # ----------------------------------------------------

        csv_data = filtered_df.to_csv(
            index=False
        )

        st.download_button(
            "⬇️ Download Intervention Report",
            data=csv_data,
            file_name="early_intervention_report.csv",
            mime="text/csv",
            use_container_width=True
        )


# ============================================================
# 15. AI CAREER ADVISOR CHATBOT
# ============================================================

elif page == "💬 AI Career Advisor":

    st.header(
        "💬 AI Student Success Advisor"
    )

    st.write(
        """
        Your AI-powered career and placement assistant.
        Ask questions about academics, coding, internships,
        projects, interviews, aptitude and placement preparation.
        """
    )

    st.divider()

    # ========================================================
    # CHECK GROQ API KEY
    # ========================================================

    if not GROQ_API_KEY:

        st.error(
            "❌ Groq API key was not found."
        )

        st.info(
            "Please check your .env file."
        )

        st.code(
            "GROQ_API_KEY=your_api_key_here"
        )

        st.stop()


    # ========================================================
    # STUDENT PROFILE
    # ========================================================

    st.subheader(
        "👤 Student Profile"
    )

    use_profile = st.checkbox(
        "Use my profile for personalized advice",
        value=True
    )

    student_context = ""

    if use_profile:

        col1, col2 = st.columns(2)

        with col1:

            chat_cgpa = st.number_input(
                "CGPA",
                min_value=0.0,
                max_value=10.0,
                value=7.5,
                step=0.01,
                key="chat_cgpa"
            )

            chat_coding = st.slider(
                "Coding Skill",
                0.0,
                100.0,
                70.0,
                key="chat_coding"
            )

            chat_aptitude = st.slider(
                "Aptitude Score",
                0.0,
                100.0,
                70.0,
                key="chat_aptitude"
            )

            chat_communication = st.slider(
                "Communication Skill",
                0.0,
                100.0,
                70.0,
                key="chat_communication"
            )

        with col2:

            chat_internships = st.number_input(
                "Internships",
                min_value=0,
                max_value=20,
                value=1,
                key="chat_internships"
            )

            chat_projects = st.number_input(
                "Projects",
                min_value=0,
                max_value=30,
                value=2,
                key="chat_projects"
            )

            chat_certifications = st.number_input(
                "Certifications",
                min_value=0,
                max_value=30,
                value=2,
                key="chat_certifications"
            )

            chat_interview = st.slider(
                "Mock Interview Score",
                0.0,
                100.0,
                70.0,
                key="chat_interview"
            )

        student_context = f"""
Student Profile:

CGPA: {chat_cgpa}/10

Coding Skill: {chat_coding}/100

Aptitude Score: {chat_aptitude}/100

Communication Skill: {chat_communication}/100

Internships: {chat_internships}

Projects: {chat_projects}

Certifications: {chat_certifications}

Mock Interview Score: {chat_interview}/100
"""


    # ========================================================
    # AI CHATBOT FUNCTION
    # ========================================================

    def ask_groq(
        user_question,
        student_context
    ):

        system_prompt = """
You are an AI Student Success and Placement Advisor.

Your purpose is to help college students improve their
academic performance, employability and placement readiness.

You can help with:

1. Academic improvement
2. Coding skills
3. Data structures and algorithms
4. Aptitude preparation
5. Communication skills
6. Technical interviews
7. HR interviews
8. Mock interview preparation
9. Resume improvement
10. LinkedIn profile improvement
11. GitHub portfolio
12. Projects
13. Internships
14. Certifications
15. Placement preparation
16. Career planning

IMPORTANT RULES:

- Give practical and actionable advice.
- Personalize the answer when student information is available.
- Do not guarantee placement.
- Do not claim that an ML prediction is certain.
- Treat placement predictions as estimates.
- Encourage students to improve their skills rather than
  labeling them permanently as successful or unsuccessful.
- Keep responses clear and student-friendly.
- Use bullet points when useful.
- For plans, provide step-by-step actions.
"""

        if student_context:

            system_prompt += f"""

The following is the student's current profile:

{student_context}

Use this information to personalize your response.
"""


        # ====================================================
        # GROQ API REQUEST
        # ====================================================

        url = (
            "https://api.groq.com/openai/v1/"
            "chat/completions"
        )

        headers = {

            "Authorization":
                f"Bearer {GROQ_API_KEY}",

            "Content-Type":
                "application/json"
        }

        payload = {

            "model":
                "openai/gpt-oss-20b",

            "messages": [

                {
                    "role":
                        "system",

                    "content":
                        system_prompt
                },

                {
                    "role":
                        "user",

                    "content":
                        user_question
                }
            ],

            "temperature":
                0.5,

            "max_tokens":
                1000
        }


        # ====================================================
        # SEND REQUEST
        # ====================================================

        try:

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=60
            )

        except requests.exceptions.Timeout:

            return (
                "⚠️ The AI service took too long "
                "to respond. Please try again."
            )

        except requests.exceptions.RequestException as e:

            return (
                f"⚠️ Connection error:\n\n{e}"
            )


        # ====================================================
        # PROCESS RESPONSE
        # ====================================================

        if response.status_code == 200:

            try:

                result = response.json()

                answer = (
                    result[
                        "choices"
                    ][0][
                        "message"
                    ][
                        "content"
                    ]
                )

                return answer

            except Exception as e:

                return (
                    "⚠️ The AI returned an unexpected response.\n\n"
                    f"{e}"
                )


        # ====================================================
        # API ERROR
        # ====================================================

        try:

            error_data = response.json()

            error_message = error_data.get(
                "error",
                {}
            ).get(
                "message",
                response.text
            )

        except Exception:

            error_message = response.text


        return (
            f"⚠️ Groq API Error "
            f"({response.status_code})\n\n"
            f"{error_message}"
        )


    # ========================================================
    # CHAT HISTORY
    # ========================================================

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []


    # ========================================================
    # DISPLAY CHAT HISTORY
    # ========================================================

    for message in st.session_state.chat_history:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # ========================================================
    # CHAT INPUT
    # ========================================================

    user_question = st.chat_input(
        "Ask your career or placement question..."
    )


    # ========================================================
    # PROCESS USER QUESTION
    # ========================================================

    if user_question:

        # ----------------------------------------------------
        # Store User Message
        # ----------------------------------------------------

        st.session_state.chat_history.append(
            {
                "role":
                    "user",

                "content":
                    user_question
            }
        )


        # ----------------------------------------------------
        # Display User Message
        # ----------------------------------------------------

        with st.chat_message(
            "user"
        ):

            st.markdown(
                user_question
            )


        # ----------------------------------------------------
        # Generate AI Response
        # ----------------------------------------------------

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "🤖 AI Advisor is thinking..."
            ):

                answer = ask_groq(
                    user_question,
                    student_context
                )


            st.markdown(
                answer
            )


        # ----------------------------------------------------
        # Store AI Response
        # ----------------------------------------------------

        st.session_state.chat_history.append(
            {
                "role":
                    "assistant",

                "content":
                    answer
            }
        )


    # ========================================================
    # CHAT CONTROLS
    # ========================================================

    if st.session_state.chat_history:

        st.divider()

        if st.button(
            "🗑️ Clear Chat"
        ):

            st.session_state.chat_history = []

            st.rerun()
# ============================================================
# 16. MODEL INFORMATION
# ============================================================

elif page == "🤖 Model Information":

    st.header(
        "🤖 Model Information"
    )

    st.write(
        """
        This application uses the trained machine-learning
        model developed from the final student placement dataset.
        """
    )

    st.subheader(
        "📌 Model Features"
    )

    model_features = get_model_features()

    for feature in model_features:

        st.write(
            f"• {feature}"
        )

    st.subheader(
        "📊 System Outputs"
    )

    outputs = [
        "Placement Status",
        "Placement Probability",
        "Risk Level",
        "Intervention Priority",
        "Student Weaknesses",
        "Personalized Recommendations"
    ]

    for output in outputs:

        st.write(
            f"• {output}"
        )

    st.subheader(
        "📁 Project Files"
    )

    st.write(
        "✅ student_placement_model.pkl"
    )

    st.write(
        "✅ streamlit_config.pkl"
    )

    st.write(
        "✅ student_success_intelligence.csv"
    )


# ============================================================
# 17. FOOTER
# ============================================================

st.divider()

st.caption(
    "AI-Based Early Student Success & Placement Prediction System"
)