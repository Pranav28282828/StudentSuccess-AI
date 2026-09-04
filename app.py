# ============================================================
# app.py
# MAIN ORCHESTRATOR & APPLICATION BACKEND
# ============================================================

import os
import pickle
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Import frontend modules
import styles
import ui_components

# ============================================================
# 1. APPLICATION CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AgentraAi | Student Placement Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

styles.inject_styles()

# ============================================================
# 2. PATH RESOLUTION & ASSET VERIFICATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "notebook", "student_placement_model.pkl")
CONFIG_PATH = os.path.join(BASE_DIR, "notebook", "streamlit_config.pkl")
DATA_PATH = os.path.join(BASE_DIR, "dataset", "student_success_intelligence.csv")

required_files = {
    "Student Placement Model": MODEL_PATH,
    "Streamlit Configuration": CONFIG_PATH,
    "Student Intelligence Dataset": DATA_PATH
}

missing_files = [f"{n}: {p}" for n, p in required_files.items() if not os.path.exists(p)]
if missing_files:
    st.error("❌ Required project files were not found.")
    for f in missing_files:
        st.code(f)
    st.stop()

# ============================================================
# 3. RESOURCE LOADERS
# ============================================================

@st.cache_resource
def load_model():
    with open(MODEL_PATH, "rb") as file:
        return pickle.load(file)

@st.cache_resource
def load_config():
    with open(CONFIG_PATH, "rb") as file:
        return pickle.load(file)

@st.cache_data
def load_intelligence_data():
    return pd.read_csv(DATA_PATH)

try:
    model = load_model()
    config = load_config()
    intelligence_df = load_intelligence_data()
except Exception as e:
    st.error("❌ Unable to load model or configuration.")
    st.code(str(e))
    st.stop()

# ============================================================
# 4. BUSINESS LOGIC & INFERENCE ENGINE
# ============================================================

def get_model_features():
    if isinstance(config, dict) and "model_features" in config:
        return config["model_features"]
    return [
        "age", "gender", "cgpa", "branch", "college_tier",
        "internships_count", "projects_count", "certifications_count",
        "coding_skill_score", "aptitude_score", "communication_skill_score",
        "logical_reasoning_score", "hackathons_participated", "github_repos",
        "linkedin_connections", "mock_interview_score", "attendance_percentage",
        "backlogs", "extracurricular_score", "leadership_score",
        "volunteer_experience", "sleep_hours", "study_hours_per_day"
    ]

def get_categorical_values(column):
    if isinstance(config, dict):
        cat_vals = config.get("categorical_values", {})
        if column in cat_vals:
            return cat_vals[column]
    if column in intelligence_df.columns:
        return sorted(intelligence_df[column].dropna().astype(str).unique().tolist())
    return []

def calculate_risk(probability):
    if probability >= 80:
        return "Low Risk", "badge-low"
    elif probability >= 60:
        return "Moderate Risk", "badge-medium"
    elif probability >= 40:
        return "High Risk", "badge-high"
    return "Very High Risk", "badge-critical"

def get_placement_probability(input_data):
    if not hasattr(model, "predict_proba"):
        return None
    probabilities = model.predict_proba(input_data)[0]
    classes = getattr(model, "classes_", None)
    if classes is None:
        return float(probabilities[-1] * 100)

    for index, class_val in enumerate(classes):
        text = str(class_val).lower()
        if text in ["1", "placed", "yes", "true"] or "placed" in text:
            return float(probabilities[index] * 100)
    return float(probabilities[-1] * 100)

def get_prediction_label(pred):
    text = str(pred).lower()
    return "PLACED" if text in ["1", "placed", "yes", "true"] or "placed" in text else "NOT PLACED"

def identify_weaknesses(data):
    checks = [
        (data["cgpa"] < 6.5, "Academic Performance (CGPA < 6.5)"),
        (data["coding_skill_score"] < 60, "Coding Proficiency (< 60)"),
        (data["aptitude_score"] < 60, "Quantitative Aptitude (< 60)"),
        (data["communication_skill_score"] < 60, "Communication Skills (< 60)"),
        (data["logical_reasoning_score"] < 60, "Logical Reasoning (< 60)"),
        (data["mock_interview_score"] < 60, "Interview Preparation (< 60)"),
        (data["internships_count"] == 0, "No Industry Internships"),
        (data["projects_count"] < 2, "Insufficient Real-World Projects (< 2)"),
        (data["certifications_count"] < 2, "Lacking Relevant Certifications (< 2)"),
        (data["hackathons_participated"] == 0, "No Hackathon Participation"),
        (data["github_repos"] < 2, "Weak GitHub Portfolio (< 2 repos)"),
        (data["linkedin_connections"] < 50, "Low Professional Network (< 50)"),
        (data["attendance_percentage"] < 75, "Low Lecture Attendance (< 75%)"),
        (data["extracurricular_score"] < 50, "Minimal Extracurricular Engagement"),
        (data["leadership_score"] < 50, "Low Leadership Rating (< 50)"),
        (data["study_hours_per_day"] < 3, "Low Study Routine (< 3 hrs/day)"),
        (data["backlogs"] > 0, f"Active Backlogs ({data['backlogs']})")
    ]
    return [label for triggered, label in checks if triggered]

def generate_recommendations(weaknesses):
    recommendation_map = {
        "Academic Performance": "Improve semester CGPA through structured revision blocks.",
        "Coding Proficiency": "Solve 2 DSA problems daily focusing on arrays, strings, and trees.",
        "Quantitative Aptitude": "Practice timed tests covering arithmetic and logical deduction.",
        "Communication Skills": "Join group discussions and practice technical presentations.",
        "Logical Reasoning": "Solve analytical and logical puzzles on weekly schedules.",
        "Interview Preparation": "Schedule mock behavioral and technical interviews with mentors.",
        "No Industry Internships": "Pursue summer internships or open-source contribution projects.",
        "Insufficient Real-World Projects": "Build and deploy at least 2 full-stack/ML portfolio projects.",
        "Lacking Relevant Certifications": "Acquire recognized credentials in cloud or data engineering.",
        "No Hackathon Participation": "Compete in collegiate hackathons on Devpost or Unstop.",
        "Weak GitHub Portfolio": "Document projects with live demo URLs and clean READMEs.",
        "Low Professional Network": "Connect with alumni and tech recruiters on LinkedIn.",
        "Low Lecture Attendance": "Maintain at least 75% attendance to avoid institutional flags.",
        "Minimal Extracurricular Engagement": "Participate in departmental clubs and campus tech fests.",
        "Low Leadership Rating": "Lead team sprints, workshops, or student tech chapters.",
        "Low Study Routine": "Target at least 3-4 hours of focused, distraction-free study daily.",
        "Active Backlogs": "Prioritize clearing active backlogs before campus placement drives begin."
    }
    out = []
    for w in weaknesses:
        for k, v in recommendation_map.items():
            if k in w:
                out.append(v)
    return out or ["Maintain your performance and continue participating in mock placement rounds."]

def query_groq_llm(user_query, chat_history):
    if not GROQ_API_KEY:
        return (
            "**Advisor Guidance (Default Mode - No API Key Set):**\n\n"
            "- **Coding**: Master arrays, hashing, and trees.\n"
            "- **Aptitude**: Practice speed tests 30 minutes daily.\n"
            "- **Projects**: Deploy 2 apps with live URLs.\n"
            "- **Mock Rounds**: Use the STAR method for behavioral answers."
        )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY.strip()}",
        "Content-Type": "application/json"
    }

    # Filter chat history so previous error notices are not re-sent
    formatted_messages = [
        {
            "role": "system",
            "content": "You are an elite university placement counselor and technical career mentor. Provide direct, actionable, step-by-step guidance."
        }
    ]
    for m in chat_history:
        if not m["content"].startswith("⚠️") and not m["content"].startswith("*(Notice:"):
            formatted_messages.append({"role": m["role"], "content": m["content"]})

    # Updated active Groq model IDs based on the August 2026 deprecation notice
    candidate_models = [
        "openai/gpt-oss-20b",
        "qwen/qwen3.6-27b",
        "openai/gpt-oss-120b"
    ]

    last_error = ""
    for model_name in candidate_models:
        try:
            payload = {
                "model": model_name,
                "messages": formatted_messages,
                "temperature": 0.5
            }
            res = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=15
            )
            data = res.json()

            if res.status_code == 200 and "choices" in data:
                return data["choices"][0]["message"]["content"]
            else:
                last_error = data.get("error", {}).get("message", str(data))
        except Exception as ex:
            last_error = str(ex)

    return f"⚠️ **Groq API Error:** {last_error}"

# ============================================================
# 5. PREDICTION HANDLER (CALLBACK)
# ============================================================

def handle_prediction(candidate_data):
    input_df = pd.DataFrame([candidate_data])
    model_features = get_model_features()

    missing_features = [f for f in model_features if f not in input_df.columns]
    if missing_features:
        st.error(f"Missing required model features: {missing_features}")
        return

    input_df = input_df[model_features]

    try:
        pred = model.predict(input_df)[0]
        prediction_label = get_prediction_label(pred)
        placement_probability = get_placement_probability(input_df)
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")
        return

    prob_val = placement_probability if placement_probability is not None else 0.0
    risk_level, risk_class = calculate_risk(prob_val)
    weaknesses = identify_weaknesses(candidate_data)
    weakness_count = len(weaknesses)

    if risk_level == "Very High Risk" or weakness_count >= 6:
        prio, prio_class = "Critical", "badge-critical"
    elif risk_level == "High Risk" or weakness_count >= 4:
        prio, prio_class = "High", "badge-high"
    elif risk_level == "Moderate Risk" or weakness_count >= 2:
        prio, prio_class = "Medium", "badge-medium"
    else:
        prio, prio_class = "Low", "badge-low"

    recommendations = generate_recommendations(weaknesses)

    profile_df = pd.DataFrame({
        "Metric": [
            "CGPA", "Internships", "Projects", "Certifications",
            "Coding Score", "Aptitude Score", "Communication Score",
            "Logical Reasoning", "Mock Interview", "Attendance",
            "Backlogs", "Study Hours / Day"
        ],
        "Value": [
            candidate_data["cgpa"], candidate_data["internships_count"],
            candidate_data["projects_count"], candidate_data["certifications_count"],
            candidate_data["coding_skill_score"], candidate_data["aptitude_score"],
            candidate_data["communication_skill_score"], candidate_data["logical_reasoning_score"],
            candidate_data["mock_interview_score"], candidate_data["attendance_percentage"],
            candidate_data["backlogs"], candidate_data["study_hours_per_day"]
        ]
    })

    ui_components.render_prediction_results(
        prediction_label, prob_val, risk_level, risk_class,
        prio, prio_class, weaknesses, recommendations, profile_df,
        candidate_data
    )

# ============================================================
# 6. SIDEBAR NAVIGATION & ROUTING
# ============================================================

# 1. Read URL query params first (when coming from index.html links)
query_page = st.query_params.get("page")

if query_page == "advisor":
    st.session_state.current_page = "AI Career Advisor"
elif query_page == "prediction":
    st.session_state.current_page = "Student Prediction"
elif query_page == "dashboard":
    st.session_state.current_page = "Student Dashboard"
elif query_page == "intervention":
    st.session_state.current_page = "Early Intervention"

# 2. Default fallback if page is not yet set
if "current_page" not in st.session_state:
    st.session_state.current_page = "Student Prediction"

# 3. Sidebar UI rendering
with st.sidebar:
    styles.render_sidebar_header()
    st.markdown("<hr style='margin: 14px 0; border: none; border-top: 1px solid rgba(255, 255, 255, 0.08);'>", unsafe_allow_html=True)

    nav_items = [
        ("Student Prediction", "🔮  Student Prediction"),
        ("Student Dashboard", "📊  Student Dashboard"),
        ("Early Intervention", "🚨  Early Intervention"),
        ("AI Career Advisor", "💬  AI Career Advisor"),
        ("Model Information", "🤖  Model Information")
    ]

    for page_key, label in nav_items:
        is_active = (st.session_state.current_page == page_key)
        btn_type = "primary" if is_active else "secondary"
        if st.button(label, key=f"nav_btn_{page_key}", type=btn_type, use_container_width=True):
            st.session_state.current_page = page_key
            st.query_params.clear()  # Clears ?page= from URL so user can freely click other tabs
            st.rerun()

    st.markdown("<hr style='margin: 20px 0 14px 0; border: none; border-top: 1px solid rgba(255, 255, 255, 0.08);'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size: 11.5px; color: #64748B; text-align: center; line-height: 1.5;">
            AgentraAi Engine v2.4<br>Precision Placement Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

# 4. Render Global Banner
styles.render_hero_banner()

# 5. Route to Selected Page
if st.session_state.current_page == "Student Prediction":
    ui_components.render_prediction_page(get_categorical_values, handle_prediction)

elif st.session_state.current_page == "Student Dashboard":
    ui_components.render_dashboard_page(intelligence_df)

elif st.session_state.current_page == "Early Intervention":
    ui_components.render_early_intervention_page(intelligence_df)

elif st.session_state.current_page == "AI Career Advisor":
    ui_components.render_advisor_page(query_groq_llm)

elif st.session_state.current_page == "Model Information":
    ui_components.render_model_info_page(get_model_features())