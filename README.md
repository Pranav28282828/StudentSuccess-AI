🤖 AgentAI
AI-Based Early Student Success & Placement Intelligence Platform

AgentAI is an AI-powered student success and placement intelligence platform designed to help students understand their placement readiness before placement season.

The platform combines Machine Learning, predictive analytics, early intervention, personalized recommendations, and Generative AI to analyze student profiles, predict placement probability, identify areas requiring improvement, and provide actionable career guidance.

Predict. Analyze. Improve. Prepare.

🚀 Key Features
🔮 Student Placement Prediction

Predicts a student's placement status and placement probability using a trained Machine Learning model.

The system analyzes factors such as:

CGPA
Branch
College Tier
Internships
Projects
Certifications
Coding Skills
Aptitude
Communication
Logical Reasoning
Mock Interview Performance
Attendance
GitHub Activity
Hackathons
Backlogs
Leadership
Study Habits
📊 Student Success Dashboard

Provides an analytical overview of student placement readiness.

Includes:

Total Students
Average Placement Probability
High-Risk Students
Critical Students
Risk Distribution
Intervention Priority
Predicted Placement Distribution
Branch-wise Placement Analysis
🚨 Early Intervention

Identifies students who may require additional placement support.

Students are categorized into:

🔴 Critical
🟠 High
🟡 Medium
🟢 Low

The system identifies specific areas that may require attention and helps prioritize intervention.

💡 Personalized Recommendations

AgentAI converts identified weaknesses into actionable recommendations.

Examples include:

Improving coding skills
Building real-world projects
Gaining internship experience
Improving aptitude
Practicing interviews
Strengthening communication
Building a GitHub portfolio
Improving professional networking
💬 AI Career Advisor

An AI-powered career assistant helps students with:

Coding
Data Structures & Algorithms
Aptitude
Technical Interviews
HR Interviews
Resume Improvement
LinkedIn Profiles
GitHub Portfolios
Projects
Internships
Certifications
Placement Preparation
Career Planning

The advisor can use student profile information to provide personalized guidance.

🌐 Dedicated Landing Page

AgentAI includes a dedicated landing page that introduces the platform and its capabilities.

The landing page provides navigation to the respective features of the platform, allowing users to explore and access:

Landing Page
     ↓
Student Prediction
     ↓
Student Dashboard
     ↓
Early Intervention
     ↓
AI Career Advisor
     ↓
Model Information

The frontend has been organized using:

index.html
styles.py
ui_components.py
🧠 Machine Learning

The placement prediction system uses a Random Forest Classifier.

Machine Learning Workflow
Student Dataset
      ↓
Data Preparation
      ↓
Feature Selection
      ↓
Train/Test Split
      ↓
Numerical Scaling
      ↓
Categorical Encoding
      ↓
Random Forest
      ↓
Placement Prediction
      ↓
Placement Probability
      ↓
Risk Analysis
Preprocessing

The model uses:

StandardScaler for numerical features
OneHotEncoder for categorical features
ColumnTransformer for feature-specific preprocessing
Pipeline to combine preprocessing and model training

The complete trained pipeline is stored as:

student_placement_model.pkl
🤖 Machine Learning + Generative AI

AgentAI combines predictive Machine Learning with Generative AI.

                  Student Profile
                        │
            ┌───────────┴───────────┐
            ↓                       ↓
     Machine Learning        Generative AI
            │                       │
            ↓                       ↓
 Placement Prediction        Career Guidance
            │                       │
            ↓                       ↓
      Risk Analysis          Personalized Advice
            │                       │
            └───────────┬───────────┘
                        ↓
                 Student Action Plan

Machine Learning helps answer:

What is the student's estimated placement readiness?

Generative AI helps answer:

What can the student do to improve?

🏗️ System Architecture
                         AgentAI
                            │
              ┌─────────────┴─────────────┐
              ↓                           ↓
        Landing Page                 Application
         index.html                      app.py
              │                           │
              │              ┌────────────┼────────────┐
              │              ↓            ↓            ↓
              │         Prediction    Dashboard    Intervention
              │              │            │            │
              │              └────────────┼────────────┘
              │                           ↓
              │                    ML Model Pipeline
              │                           │
              │                           ↓
              │                    Random Forest
              │                           │
              │                           ↓
              │                  Placement Probability
              │                           │
              │                  ┌────────┴────────┐
              │                  ↓                 ↓
              │            Risk Analysis    Recommendations
              │
              └──────────────────────┐
                                     ↓
                              AI Career Advisor
                                     │
                                     ↓
                                  Groq API
                                     │
                                     ↓
                                   GPT-OSS
📁 Project Structure
AgentAI/
│
├── app.py
├── index.html
├── styles.py
├── ui_components.py
│
├── README.md
├── requirements.txt
├── .gitignore
├── Architecture.png
│
├── dataset/
│   ├── student_placement_prediction_dataset_2026.csv
│   ├── student_prediction_results.csv
│   └── student_success_intelligence.csv
│
└── notebook/
    ├── Model_Building.ipynb
    ├── Model_Evaluation.ipynb
    ├── Early_Intervention_Recommendation.ipynb
    ├── Streamlit_Preparation.ipynb
    │
    ├── early_intervention_students.csv
    ├── feature_importance.csv
    │
    ├── model_features.pkl
    ├── recommendation_config.pkl
    ├── streamlit_config.pkl
    └── student_placement_model.pkl
🛠️ Technology Stack
Programming & Frontend
Python
HTML
CSS
Streamlit
Machine Learning
Scikit-learn
Random Forest
Pandas
NumPy
Generative AI
Groq API
GPT-OSS
Development
Jupyter Notebook
Visual Studio Code
Git
GitHub
⚙️ Installation
1. Clone the repository
git clone https://github.com/Pranav28282828/StudentSuccess-AI.git
2. Navigate to the project
cd StudentSuccess-AI
3. Create a virtual environment
python -m venv venv
4. Activate the environment

Windows:

venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
🔑 Environment Configuration

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key_here

The .env file contains sensitive credentials and should never be committed to GitHub.

▶️ Run the Application

Start the Streamlit application:

streamlit run app.py
🔄 Application Workflow
1. Open Landing Page
        ↓
2. Explore Platform Features
        ↓
3. Select a Feature
        ↓
4. Enter / Analyze Student Information
        ↓
5. Generate Placement Prediction
        ↓
6. View Placement Probability
        ↓
7. Analyze Risk
        ↓
8. Identify Weaknesses
        ↓
9. Receive Recommendations
        ↓
10. Use AI Career Advisor
🎯 Project Objectives
Predict student placement readiness.
Estimate placement probability.
Identify students who may require early support.
Detect academic and career-readiness weaknesses.
Prioritize intervention.
Generate personalized recommendations.
Provide AI-powered career guidance.
Help students prepare before placement season.
Provide mentors with data-driven student insights.
🔐 Data Leakage Prevention

The following fields are excluded from the prediction model:

student_id

Excluded because it is an identifier and does not represent meaningful student characteristics.

salary_package_lpa

Excluded because salary is known after placement and using it during prediction would introduce data leakage.

The model therefore focuses on information that can realistically be available before placement.

🌱 Future Enhancements
AI Resume Analysis
Resume-to-Job Matching
AI Mock Interviews
Personalized Learning Paths
Automated Study Plans
Job Recommendations
Student Progress Tracking
Mentor Notifications
College-Level Analytics
Placement Trend Forecasting
Explainable AI
Continuous Model Improvement
College ERP/LMS Integration
⚠️ Disclaimer

AgentAI provides estimated predictions and recommendations and does not guarantee placement outcomes.

Placement probability should be treated as an analytical estimate. Actual placement outcomes depend on multiple factors, including student preparation, interview performance, company requirements, hiring conditions, competition, and available opportunities.

👨‍💻 Project Information

Project: AgentAI

Domain: Artificial Intelligence / Machine Learning / Generative AI / Education Technology

Focus: Student Success & Placement Intelligence

Core Approach:

Predict. Analyze. Improve. Prepare.