"""
AI Resume Screening System
Main Streamlit Application

A professional ATS-style resume screening tool that analyzes resumes
against job descriptions, calculates compatibility scores, and
provides actionable recommendations.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os
import warnings
warnings.filterwarnings("ignore")

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.resume_parser import ResumeParser
from src.skill_extractor import SkillExtractor
from src.ats_scorer import ATSScorer
from src.recommendation_engine import RecommendationEngine
from src.utils import generate_pdf_report, get_score_color

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Page background: deep slate → indigo ── */
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 15% 0%, rgba(124, 58, 237, 0.12), transparent 40%),
            radial-gradient(circle at 85% 100%, rgba(30, 64, 175, 0.12), transparent 40%),
            linear-gradient(165deg, #0b1120 0%, #0f172a 50%, #131b36 100%);
        background-attachment: fixed;
    }
    [data-testid="stHeader"] {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(124, 58, 237, 0.2);
    }
    hr { border-color: #26334d !important; }

    /* ── Sidebar: deep navy gradient ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(200deg, #0b1120 0%, #1e1b4b 55%, #2e1065 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    [data-testid="stSidebar"] * { color: #cbd5e1; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] strong { color: #ffffff; }
    [data-testid="stSidebar"] hr { border-color: rgba(255, 255, 255, 0.12); }
    [data-testid="stSidebar"] [data-testid="stAlert"] {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 10px;
    }
    [data-testid="stSidebar"] [data-testid="stAlert"] * { color: #e0e7ff; }
    [data-testid="stSidebar"] [data-testid="stCheckbox"] label { color: #cbd5e1; }

    /* ── Main header banner ── */
    .main-header {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 45%, #db2777 100%);
        padding: 2rem 2.5rem;
        border-radius: 18px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .main-header::before {
        content: "";
        position: absolute;
        top: -60%;
        right: -10%;
        width: 320px;
        height: 320px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.22), transparent 65%);
    }
    .main-header h1 {
        color: #fff;
        font-size: 2.2rem;
        margin: 0;
        font-weight: 800;
        text-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
    }
    .main-header p {
        color: #ffe4ec;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
    }

    /* ── KPI cards: dark cards with glowing accent top border ── */
    .kpi-card {
        position: relative;
        background: linear-gradient(150deg, #16203a 0%, #101830 100%);
        border-radius: 16px;
        padding: 1.3rem 1.2rem;
        border: 1px solid #26334d;
        border-top: 4px solid var(--acc, #6366f1);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        overflow: hidden;
        text-align: center;
    }
    .kpi-card::before {
        content: "";
        position: absolute;
        inset: 0 auto 0 0;
        width: 6px;
        background: linear-gradient(180deg, var(--acc), transparent);
    }
    .kpi-card p {
        color: #94a3b8;
        margin: 0 0 0.4rem 0;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    .kpi-card h3 {
        font-size: 1.9rem;
        margin: 0;
        font-weight: 800;
        color: #f1f5f9;
    }

    /* ── Section headers: light text with gradient accent bar ── */
    .section-header {
        position: relative;
        color: #e0e7ff;
        border-bottom: 2px solid #26334d;
        padding-bottom: 0.5rem;
        padding-left: 0.9rem;
        margin: 1.6rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 700;
    }
    .section-header::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0.1rem;
        bottom: 0.1rem;
        width: 5px;
        border-radius: 4px;
        background: linear-gradient(180deg, #6366f1, #d946ef);
    }

    /* ── Skill tags: dark theme variants ── */
    .skill-tag {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 500px;
        font-size: 0.85rem;
        margin: 0.2rem;
        font-weight: 600;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
    }
    .skill-match {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid #065f46;
    }
    .skill-missing {
        background: rgba(244, 63, 94, 0.15);
        color: #fda4af;
        border: 1px solid #881337;
    }
    .skill-extra {
        background: rgba(99, 102, 241, 0.15);
        color: #a5b4fc;
        border: 1px solid #323fae;
    }

    /* ── Primary button: vivid gradient ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%) !important;
        color: #fff !important;
        font-weight: 700;
        font-size: 1rem;
        border: none !important;
        border-radius: 14px;
        padding: 0.7rem 1.2rem;
        letter-spacing: 0.3px;
        box-shadow: 0 6px 18px rgba(139, 92, 246, 0.4);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 26px rgba(236, 72, 153, 0.45);
    }
    .stButton > button[kind="primary"]:active { transform: translateY(0); }

    /* ── Secondary button ── */
    .stButton > button:not([kind="primary"]) {
        border-radius: 12px;
        border: 1px solid #334155;
        color: #c7d2fe;
        background: #1e293b;
        font-weight: 600;
        transition: all 0.15s ease;
    }
    .stButton > button:not([kind="primary"]):hover {
        border-color: #6366f1;
        background: #273449;
    }

    /* ── Download button ── */
    .stDownloadButton button {
        background: linear-gradient(90deg, #059669, #10b981) !important;
        color: white !important;
        border: none !important;
        font-weight: 700;
        border-radius: 12px;
        padding: 0.6rem 1.1rem;
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.35);
        transition: transform 0.15s ease;
    }
    .stDownloadButton button:hover { transform: translateY(-2px); }

    /* ── Tabs: dark container, colorful active pill ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid #26334d;
        padding: 6px;
        border-radius: 14px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 18px;
        font-weight: 600;
        color: #c7d2fe;
        background: transparent;
        transition: all 0.15s ease;
    }
    .stTabs [data-baseweb="tab"]:hover { background: #273449; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(90deg, #7c3aed, #db2777) !important;
        color: #fff !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.35);
    }

    /* ── Expanders ── */
    [data-testid="stExpander"] {
        border: 1px solid #26334d;
        border-radius: 14px;
        background: linear-gradient(150deg, #101830, #151d33);
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
    }
    [data-testid="stExpander"] summary { color: #a5b4fc; }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {
        border: 2px dashed #4f5d85;
        border-radius: 16px;
        background: rgba(30, 41, 59, 0.6);
        padding: 0.5rem;
    }

    /* ── Text inputs & areas ── */
    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input {
        border-radius: 12px;
        border: 1.5px solid #334155;
        background: #0f172a;
        color: #e2e8f0;
    }
    [data-testid="stTextArea"] textarea:focus,
    [data-testid="stTextInput"] input:focus {
        border-color: #818cf8;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.25);
    }

    /* ── Alerts ── */
    [data-testid="stAlert"] { border-radius: 12px; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: #0d1526; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #334155, #4c1d95);
        border-radius: 6px;
    }

    /* ── Text selection ── */
    ::selection { background: rgba(139, 92, 246, 0.4); }
</style>
""", unsafe_allow_html=True)


def create_gauge_chart(score: float, title: str = "ATS Score") -> go.Figure:
    """Create an ATS score gauge chart using Plotly."""
    color = "#00c853" if score >= 80 else "#ffc107" if score >= 60 else "#ff9800" if score >= 40 else "#f44336"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": title, "font": {"size": 20, "color": "#1a237e"}},
        number={"suffix": "%", "font": {"size": 36, "color": "#1a237e"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 2, "tickcolor": "#333",
                     "dtick": 20},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "#e0e0e0",
            "steps": [
                {"range": [0, 40], "color": "#ffebee"},
                {"range": [40, 60], "color": "#fff3e0"},
                {"range": [60, 80], "color": "#fff8e1"},
                {"range": [80, 100], "color": "#e8f5e9"},
            ],
            "threshold": {
                "line": {"color": "#1a237e", "width": 4},
                "thickness": 0.75,
                "value": score,
            },
        },
    ))
    fig.update_layout(
        height=300,
        margin=dict(l=30, r=30, t=60, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_skill_radar_chart(matching: int, missing: int, extra: int) -> go.Figure:
    """Create a radar chart for skill distribution."""
    categories = ["Matching", "Missing", "Extra"]
    values = [matching, missing, extra]

    fig = go.Figure(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        line=dict(color="#818cf8"),
        fillcolor="rgba(129, 140, 248, 0.25)",
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                showticklabels=True,
                gridcolor="rgba(148, 163, 184, 0.25)",
                tickfont=dict(color="#94a3b8"),
            ),
            radialaxis_gridcolor="rgba(148, 163, 184, 0.25)",
        ),
        showlegend=False,
        height=300,
        margin=dict(l=60, r=60, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1"),
        template="plotly_dark",
    )
    return fig


def create_score_breakdown_chart(ats_data: dict) -> go.Figure:
    """Create a horizontal bar chart for ATS score breakdown."""
    labels = ["Text Similarity", "Keyword Match", "Format Score", "Section Coverage"]
    values = [
        ats_data.get("text_similarity", 0),
        ats_data.get("keyword_score", 0),
        ats_data.get("format_score", 0),
        ats_data.get("section_score", 0),
    ]
    colors = ["#1a237e", "#283593", "#3949ab", "#5c6bc0"]

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker=dict(color=colors, line=dict(color="white", width=1)),
        text=[f"{v}%" for v in values],
        textposition="auto",
        textfont=dict(color="white", size=13, family="Arial Black"),
    ))
    fig.update_layout(
        xaxis=dict(
            range=[0, 100],
            title=dict(text="Score (%)", font=dict(color="#cbd5e1")),
            tickfont=dict(color="#94a3b8"),
            gridcolor="rgba(148, 163, 184, 0.2)",
        ),
        yaxis=dict(tickfont=dict(color="#cbd5e1")),
        height=250,
        margin=dict(l=10, r=10, t=10, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1"),
        template="plotly_dark",
    )
    return fig


def create_skill_category_chart(skills: list, categories: dict) -> go.Figure:
    """Create a pie chart of skills by category."""
    cat_counts = {}
    for skill in skills:
        cat = categories.get(skill, "Other")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    fig = go.Figure(go.Pie(
        labels=list(cat_counts.keys()),
        values=list(cat_counts.values()),
        hole=0.4,
        marker=dict(colors=px.colors.qualitative.Set2),
        textinfo="label+value",
        textfont=dict(size=12),
    ))
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, font=dict(color="#cbd5e1")),
        font=dict(color="#cbd5e1"),
        template="plotly_dark",
    )
    return fig


def main():
    """Main application entry point."""

    # ─── Header ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="main-header">
        <h1>🎯 AI Resume Screening System</h1>
        <p>Upload your resume and paste a job description to get instant ATS analysis, skill gap assessment, and personalized recommendations.</p>
    </div>
    """, unsafe_allow_html=True)

    # ─── Initialize Components ─────────────────────────────────────────────────
    parser = ResumeParser()
    skill_extractor = SkillExtractor()
    ats_scorer = ATSScorer()
    recommendation_engine = RecommendationEngine()

    # ─── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        st.markdown("---")
        st.markdown("### 📊 Analysis Options")
        show_raw_text = st.checkbox("Show raw resume text", value=False)
        show_sections = st.checkbox("Show parsed sections", value=False)
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.info(
            "This AI-powered system analyzes resumes against job descriptions "
            "using NLP techniques including TF-IDF, cosine similarity, and "
            "skill matching algorithms."
        )
        st.markdown("---")
        st.markdown("**Version:** 1.0.0")
        st.markdown("**Author:** Data Science Portfolio Project")

    # ─── Main Content ──────────────────────────────────────────────────────────
    col_upload, col_jd = st.columns([1, 1])

    with col_upload:
        st.markdown('<h2 class="section-header">📄 Upload Resume</h2>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            help="Upload your resume in PDF format",
        )

    with col_jd:
        st.markdown('<h2 class="section-header">💼 Job Description</h2>', unsafe_allow_html=True)
        job_description = st.text_area(
            "Paste the job description here",
            height=250,
            placeholder="Paste the complete job description including requirements, responsibilities, and qualifications...",
            help="The more detailed the job description, the better the analysis",
        )

    st.markdown("---")

    # ─── Analysis Button ───────────────────────────────────────────────────────
    analyze_col1, analyze_col2, analyze_col3 = st.columns([1, 2, 1])
    with analyze_col2:
        analyze_btn = st.button(
            "🚀 Analyze Resume",
            use_container_width=True,
            type="primary",
            help="Click to start the analysis",
        )

    # ─── Run Analysis ──────────────────────────────────────────────────────────
    if analyze_btn:
        if uploaded_file is None:
            st.error("⚠️ Please upload a resume PDF file.")
            return
        if not job_description.strip():
            st.error("⚠️ Please paste a job description.")
            return

        with st.spinner("🔄 Analyzing resume... This may take a moment."):
            # Step 1: Parse Resume
            pdf_bytes = uploaded_file.read()
            resume_data = parser.parse_resume(pdf_bytes, is_bytes=True)
            resume_text = resume_data["cleaned_text"]

            # Step 2: Extract Skills
            resume_skills = skill_extractor.extract_skills(resume_text)
            jd_skills = skill_extractor.extract_skills(job_description)

            # Step 3: Skill Matching
            skill_analysis = skill_extractor.get_skill_gap_analysis(
                resume_skills, jd_skills
            )

            # Step 4: ATS Score
            ats_data = ats_scorer.compute_ats_score(
                resume_text,
                job_description,
                resume_data.get("sections", {}),
                raw_text=resume_data["raw_text"],
            )
            suitability = ats_scorer.get_suitability_level(ats_data["overall_score"])

            # Step 5: Recommendations
            recommendations = recommendation_engine.recommend_skills_to_learn(
                skill_analysis["missing_skills"],
                skill_analysis["matching_skills"],
            )
            career_suggestions = recommendation_engine.generate_career_suggestions(
                resume_skills, jd_skills, skill_analysis["match_percentage"]
            )
            improvement_tips = recommendation_engine.get_resume_improvement_tips(
                resume_text, resume_data.get("sections", {})
            )

        # ─── Cache results so they persist across reruns ───────────────────────
        st.session_state["results"] = {
            "resume_data": resume_data,
            "resume_text": resume_text,
            "resume_skills": resume_skills,
            "skill_analysis": skill_analysis,
            "ats_data": ats_data,
            "suitability": suitability,
            "recommendations": recommendations,
            "career_suggestions": career_suggestions,
            "improvement_tips": improvement_tips,
        }

    # ─── Results Display ─────────────────────────────────────────────────────
    results = st.session_state.get("results")

    if results:
        resume_data = results["resume_data"]
        resume_text = results["resume_text"]
        resume_skills = results["resume_skills"]
        skill_analysis = results["skill_analysis"]
        ats_data = results["ats_data"]
        suitability = results["suitability"]
        recommendations = results["recommendations"]
        career_suggestions = results["career_suggestions"]
        improvement_tips = results["improvement_tips"]

        st.markdown("---")
        st.markdown('<h2 class="section-header">📊 Analysis Results</h2>', unsafe_allow_html=True)

        # ─── KPI Cards ─────────────────────────────────────────────────────────
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

        with kpi1:
            score = ats_data["overall_score"]
            color = get_score_color(score)
            st.markdown(f"""
            <div class="kpi-card" style="--acc: {color};">
                <p>ATS Score</p>
                <h3 style="color: {color};">{score}%</h3>
            </div>
            """, unsafe_allow_html=True)

        with kpi2:
            st.markdown(f"""
            <div class="kpi-card" style="--acc: #8b5cf6;">
                <p>Suitability</p>
                <h3 style="color: #a78bfa;">{suitability}</h3>
            </div>
            """, unsafe_allow_html=True)

        with kpi3:
            st.markdown(f"""
            <div class="kpi-card" style="--acc: #10b981;">
                <p>Skills Matched</p>
                <h3 style="color: #34d399;">{skill_analysis['match_count']}</h3>
            </div>
            """, unsafe_allow_html=True)

        with kpi4:
            st.markdown(f"""
            <div class="kpi-card" style="--acc: #f43f5e;">
                <p>Missing Skills</p>
                <h3 style="color: #fb7185;">{len(skill_analysis['missing_skills'])}</h3>
            </div>
            """, unsafe_allow_html=True)

        with kpi5:
            st.markdown(f"""
            <div class="kpi-card" style="--acc: #f59e0b;">
                <p>Resume Words</p>
                <h3 style="color: #fbbf24;">{resume_data['word_count']}</h3>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ─── Gauge and Score Breakdown ─────────────────────────────────────────
        col_gauge, col_breakdown = st.columns([1, 1])

        with col_gauge:
            st.markdown('<h3 class="section-header">🎯 ATS Score Gauge</h3>', unsafe_allow_html=True)
            gauge_fig = create_gauge_chart(ats_data["overall_score"])
            st.plotly_chart(gauge_fig, use_container_width=True)

        with col_breakdown:
            st.markdown('<h3 class="section-header">📈 Score Breakdown</h3>', unsafe_allow_html=True)
            breakdown_fig = create_score_breakdown_chart(ats_data)
            st.plotly_chart(breakdown_fig, use_container_width=True)

        # ─── Skills Analysis ───────────────────────────────────────────────────
        st.markdown('<h2 class="section-header">🔧 Skill Analysis</h2>', unsafe_allow_html=True)

        col_matching, col_missing, col_extra = st.columns(3)

        with col_matching:
            st.markdown("#### ✅ Matching Skills")
            st.markdown(f"**{skill_analysis['match_count']} skills matched**")
            if skill_analysis["matching_skills"]:
                for skill in skill_analysis["matching_skills"]:
                    st.markdown(
                        f'<span class="skill-tag skill-match">{skill}</span>',
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No matching skills found.")

        with col_missing:
            st.markdown("#### ❌ Missing Skills")
            st.markdown(f"**{len(skill_analysis['missing_skills'])} skills missing**")
            if skill_analysis["missing_skills"]:
                for skill in skill_analysis["missing_skills"]:
                    st.markdown(
                        f'<span class="skill-tag skill-missing">{skill}</span>',
                        unsafe_allow_html=True,
                    )
            else:
                st.success("No missing skills - great match!")

        with col_extra:
            st.markdown("#### ➕ Extra Skills")
            st.markdown(f"**{len(skill_analysis['extra_skills'])} additional skills**")
            if skill_analysis["extra_skills"]:
                for skill in skill_analysis["extra_skills"]:
                    st.markdown(
                        f'<span class="skill-tag skill-extra">{skill}</span>',
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No extra skills found.")

        # ─── Skill Charts ──────────────────────────────────────────────────────
        col_radar, col_pie = st.columns([1, 1])

        with col_radar:
            st.markdown('<h3 class="section-header">🕸️ Skill Distribution</h3>', unsafe_allow_html=True)
            radar_fig = create_skill_radar_chart(
                skill_analysis["match_count"],
                len(skill_analysis["missing_skills"]),
                len(skill_analysis["extra_skills"]),
            )
            st.plotly_chart(radar_fig, use_container_width=True)

        with col_pie:
            st.markdown('<h3 class="section-header">📊 Skills by Category</h3>', unsafe_allow_html=True)
            all_resume_skills = list(set(
                [s for s in skill_analysis["matching_skills"]]
                + [s for s in skill_analysis["extra_skills"]]
            ))
            if all_resume_skills:
                cat_chart = create_skill_category_chart(
                    all_resume_skills,
                    skill_extractor.skill_categories,
                )
                st.plotly_chart(cat_chart, use_container_width=True)
            else:
                st.info("No skills detected in resume to categorize.")

        # ─── Candidate Summary ─────────────────────────────────────────────────
        st.markdown('<h2 class="section-header">👤 Candidate Summary</h2>', unsafe_allow_html=True)

        summary_col1, summary_col2 = st.columns(2)

        with summary_col1:
            st.markdown("**Personal Information**")
            if resume_data.get("name"):
                st.write(f"**Name:** {resume_data['name']}")
            if resume_data.get("email"):
                st.write(f"**Email:** {resume_data['email']}")
            if resume_data.get("phone"):
                st.write(f"**Phone:** {resume_data['phone']}")
            st.write(f"**Word Count:** {resume_data['word_count']}")
            st.write(f"**Text Length:** {resume_data['text_length']} characters")

        with summary_col2:
            st.markdown("**Resume Strengths**")
            strengths = []
            if skill_analysis["match_percentage"] >= 60:
                strengths.append("Strong skill alignment with job requirements")
            if len(resume_skills) >= 10:
                strengths.append("Diverse technical skill set")
            if resume_data.get("email"):
                strengths.append("Contact information present")
            if resume_data.get("sections", {}).get("experience"):
                strengths.append("Work experience section found")
            if resume_data.get("sections", {}).get("education"):
                strengths.append("Education section found")
            if resume_data.get("sections", {}).get("projects"):
                strengths.append("Projects section found")

            if strengths:
                for s in strengths:
                    st.write(f"✅ {s}")
            else:
                st.info("Add more sections to your resume to highlight strengths.")

        # ─── Recommendations ───────────────────────────────────────────────────
        st.markdown('<h2 class="section-header">💡 Recommendations</h2>', unsafe_allow_html=True)

        rec_tab1, rec_tab2, rec_tab3 = st.tabs(
            ["📚 Skills to Learn", "🎯 Career Suggestions", "📝 Resume Tips"]
        )

        with rec_tab1:
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    priority_color = (
                        "#c62828" if rec["priority"] == "High"
                        else "#f57f17" if rec["priority"] == "Medium"
                        else "#2e7d32"
                    )
                    st.markdown(f"""
                    **{i}. {rec['skill'].title()}**
                    - Category: {rec['category']}
                    - Priority: <span style="color:{priority_color};font-weight:bold;">{rec['priority']}</span>
                    - Reason: {rec['reason']}
                    """, unsafe_allow_html=True)
                    if "resources" in rec:
                        with st.expander("📖 Learning Resources"):
                            for r in rec["resources"]:
                                st.write(f"• {r}")
            else:
                st.success("No critical skill gaps detected!")

        with rec_tab2:
            for i, suggestion in enumerate(career_suggestions, 1):
                st.write(f"**{i}.** {suggestion}")

        with rec_tab3:
            for i, tip in enumerate(improvement_tips, 1):
                st.write(f"**{i}.** {tip}")

        # ─── Download Report ───────────────────────────────────────────────────
        st.markdown('<h2 class="section-header">📥 Download Report</h2>', unsafe_allow_html=True)

        analysis_data = {
            "candidate_name": resume_data.get("name", "Candidate"),
            "ats_score": ats_data,
            "suitability": suitability,
            "matching_skills": skill_analysis["matching_skills"],
            "missing_skills": skill_analysis["missing_skills"],
            "extra_skills": skill_analysis["extra_skills"],
            "match_percentage": skill_analysis["match_percentage"],
            "recommendations": [r["reason"] for r in recommendations],
            "career_suggestions": career_suggestions,
            "improvement_tips": improvement_tips,
        }

        pdf_bytes_report = generate_pdf_report(
            analysis_data, resume_data.get("name", "Candidate")
        )

        if pdf_bytes_report:
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_bytes_report,
                file_name=f"resume_analysis_{resume_data.get('name', 'candidate').replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.info("PDF report generation requires reportlab. Install with: pip install reportlab")

        # ─── Raw Data (Optional) ───────────────────────────────────────────────
        if show_raw_text or show_sections:
            st.markdown('<h2 class="section-header">📋 Raw Data</h2>', unsafe_allow_html=True)

            if show_raw_text:
                with st.expander("📄 Extracted Resume Text", expanded=False):
                    st.text_area("Raw Text", resume_text, height=300)

            if show_sections:
                with st.expander("📑 Parsed Sections", expanded=False):
                    for section_name, section_text in resume_data.get("sections", {}).items():
                        st.markdown(f"**{section_name.title()}**")
                        st.text(section_text[:500] + ("..." if len(section_text) > 500 else ""))
                        st.markdown("---")

    # ─── Footer ────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center;color:#64748b;padding:1rem;">
            <p>AI Resume Screening System | Built with Streamlit | MSc Data Science Portfolio Project</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
