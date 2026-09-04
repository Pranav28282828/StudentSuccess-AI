# ============================================================
# styles.py
# FRONTEND STYLING, THEMES & REUSABLE HTML GENERATORS
# ============================================================

import streamlit as st

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html {
    scroll-behavior: smooth;
}

html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, span, label, input, button {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

[data-testid="stIconMaterial"],
.material-symbols-rounded,
.material-icons,
[data-testid="stSidebarCollapseButton"] span,
button[kind="header"] span {
    font-family: 'Material Symbols Rounded', 'Material Icons' !important;
}

[data-testid="stSidebarCollapseButton"]::after,
[data-testid="stSidebarCollapseButton"] span::after {
    display: none !important;
    content: "" !important;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
}

/* SIDEBAR STYLING */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B0F19 0%, #080C14 100%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.sidebar-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 4px 6px 4px;
}

.brand-icon-box {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    box-shadow: 0 4px 18px rgba(99, 102, 241, 0.4);
}

.brand-title {
    font-size: 20px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.5px;
    margin: 0;
    line-height: 1.1;
}

.brand-subtitle {
    font-size: 11.5px;
    color: #94A3B8;
    margin: 3px 0 0 0;
    font-weight: 500;
}

section[data-testid="stSidebar"] div.stButton > button {
    width: 100% !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    padding: 11px 16px !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    letter-spacing: 0.2px !important;
    border-radius: 12px !important;
    margin-bottom: 6px !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

section[data-testid="stSidebar"] div.stButton > button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #94A3B8 !important;
}

section[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {
    background: rgba(99, 102, 241, 0.12) !important;
    border-color: rgba(147, 51, 234, 0.4) !important;
    color: #F8FAFC !important;
    transform: translateX(4px) !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3) !important;
}

section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%) !important;
    border: 1px solid rgba(167, 139, 250, 0.4) !important;
    color: #FFFFFF !important;
    box-shadow: 0 6px 20px -2px rgba(99, 102, 241, 0.5) !important;
    font-weight: 700 !important;
}

/* HERO BANNER */
.hero-container {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.18) 0%, rgba(236, 72, 153, 0.12) 50%, rgba(168, 85, 247, 0.18) 100%);
    border: 1px solid rgba(168, 85, 247, 0.35);
    border-radius: 20px;
    padding: 28px 24px;
    margin-bottom: 24px;
    text-align: center;
    box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.25);
}
.hero-title {
    font-size: 32px;
    font-weight: 800;
    background: linear-gradient(90deg, #6366F1, #EC4899, #8B5CF6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}
.hero-subtitle {
    font-size: 15px;
    color: #94A3B8;
    max-width: 800px;
    margin: 0 auto;
}

/* JUMP NAVBAR */
.jump-nav-bar {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 25px;
    position: sticky;
    top: 0;
    z-index: 99;
    background: rgba(15, 23, 42, 0.9);
    padding: 12px 16px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(12px);
}
.jump-button {
    border: none;
    cursor: pointer;
    padding: 9px 18px;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 13px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: transform 0.15s ease, filter 0.2s ease, box-shadow 0.2s ease;
}
.jump-button:hover {
    transform: translateY(-2px);
    filter: brightness(1.15);
}
.btn-student {
    background: linear-gradient(135deg, #06B6D4, #3B82F6);
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(6, 182, 212, 0.4);
}
.btn-academic {
    background: linear-gradient(135deg, #F59E0B, #EF4444);
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(245, 158, 11, 0.4);
}
.btn-skills {
    background: linear-gradient(135deg, #8B5CF6, #EC4899);
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(139, 92, 246, 0.4);
}

/* SECTION STRIPS */
.section-card-cyan {
    border-left: 5px solid #06B6D4;
    background: linear-gradient(90deg, rgba(6, 182, 212, 0.1) 0%, transparent 100%);
    padding: 12px 18px;
    border-radius: 8px;
    margin: 20px 0 14px 0;
    font-size: 18px;
    font-weight: 700;
    color: #38BDF8;
}
.section-card-amber {
    border-left: 5px solid #F59E0B;
    background: linear-gradient(90deg, rgba(245, 158, 11, 0.1) 0%, transparent 100%);
    padding: 12px 18px;
    border-radius: 8px;
    margin: 24px 0 14px 0;
    font-size: 18px;
    font-weight: 700;
    color: #FBBF24;
}
.section-card-purple {
    border-left: 5px solid #A855F7;
    background: linear-gradient(90deg, rgba(168, 85, 247, 0.1) 0%, transparent 100%);
    padding: 12px 18px;
    border-radius: 8px;
    margin: 24px 0 14px 0;
    font-size: 18px;
    font-weight: 700;
    color: #C084FC;
}

/* CARDS & BADGES */
.metric-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.2);
}
.metric-label {
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #94A3B8;
    margin-bottom: 6px;
}
.metric-val {
    font-size: 26px;
    font-weight: 800;
}

.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 700;
}
.badge-critical { background: rgba(239, 68, 68, 0.2); color: #F87171; border: 1px solid #EF4444; }
.badge-high { background: rgba(249, 115, 22, 0.2); color: #FB923C; border: 1px solid #F97316; }
.badge-medium { background: rgba(245, 158, 11, 0.2); color: #FCD34D; border: 1px solid #F59E0B; }
.badge-low { background: rgba(16, 185, 129, 0.2); color: #4ADE80; border: 1px solid #10B981; }
.badge-placed { background: rgba(16, 185, 129, 0.2); color: #4ADE80; border: 1px solid #10B981; }
.badge-unplaced { background: rgba(239, 68, 68, 0.2); color: #F87171; border: 1px solid #EF4444; }

.weakness-chip {
    display: inline-flex;
    align-items: center;
    background: rgba(239, 68, 68, 0.12);
    color: #F87171;
    border: 1px solid rgba(239, 68, 68, 0.35);
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    margin: 4px;
}

.recommendation-box {
    border-left: 4px solid #8B5CF6;
    background: rgba(139, 92, 246, 0.1);
    padding: 12px 16px;
    border-radius: 0 10px 10px 0;
    margin-bottom: 8px;
    font-size: 13.5px;
}
</style>
"""

def inject_styles():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def render_sidebar_header():
    st.markdown(
        """
        <div class="sidebar-header">
            <div class="brand-icon-box">🎓</div>
            <div>
                <div class="brand-title">AgentraAi</div>
                <div class="brand-subtitle">Student Placement Suite</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_hero_banner():
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-title">🎓 AgentraAi Early Student Success & Placement Platform</div>
            <div class="hero-subtitle">
                Forecast placement probability, triage student vulnerabilities, and implement personalized intervention roadmaps.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_jump_navbar():
    st.markdown(
        """
        <div class="jump-nav-bar">
            <span style="font-size: 12.5px; font-weight: 700; color: #94A3B8; align-self: center;">Quick Jump:</span>
            <button type="button" onclick="jumpToSection('student-info')" class="jump-button btn-student">👤 Student Info</button>
            <button type="button" onclick="jumpToSection('academic-profile')" class="jump-button btn-academic">📚 Academic & Career</button>
            <button type="button" onclick="jumpToSection('skills-profile')" class="jump-button btn-skills">💻 Skills & Performance</button>
        </div>

        <script>
        function jumpToSection(targetId) {
            try {
                // Look for the element in top window parent document or current document
                const doc = window.parent.document || document;
                const target = doc.getElementById(targetId) || doc.querySelector('[data-jump-target="' + targetId + '"]');
                
                if (target) {
                    // Streamlit scrolls the container with data-testid="stAppViewContainer" or "stMain"
                    const scrollContainer = doc.querySelector('[data-testid="stAppViewContainer"]') || doc.querySelector('.main') || window.parent;
                    
                    const rect = target.getBoundingClientRect();
                    const scrollTop = (scrollContainer.scrollTop !== undefined) ? scrollContainer.scrollTop : window.parent.pageYOffset;
                    const targetPosition = rect.top + scrollTop - 100; // 100px offset for the sticky navbar
                    
                    if (scrollContainer.scrollTo) {
                        scrollContainer.scrollTo({
                            top: targetPosition,
                            behavior: 'smooth'
                        });
                    } else {
                        window.parent.scrollTo({
                            top: targetPosition,
                            behavior: 'smooth'
                        });
                    }
                }
            } catch (err) {
                console.error("Jump navigation error:", err);
            }
        }
        </script>
        """,
        unsafe_allow_html=True
    )

def render_metric_card(label, value, color=None, badge_class=None):
    if badge_class:
        content = f'<span class="badge {badge_class}" style="font-size: 16px;">{value}</span>'
    else:
        style_color = f'style="color: {color};"' if color else ""
        content = f'<div class="metric-val" {style_color}>{value}</div>'
    
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )