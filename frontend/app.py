import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Plagiarism Detection System",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1020, #111827);
    font-family: 'Segoe UI', sans-serif;
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: 700;
    color: white;
}
.subtitle {
    text-align: center;
    font-size: 16px;
    color: #cbd5f5;
    margin-bottom: 40px;
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    color: white;
    margin-bottom: 16px;
}

/* ---- UPLOAD CARD & GLOW EFFECTS ---- */
.upload-card {
    background: rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 32px;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.18);
    transition: all 0.3s ease-in-out; /* Smooth transition for glow */
}

/* Glow effect on hover for the card */
.upload-card:hover {
    box-shadow: 0 0 25px rgba(99, 102, 241, 0.5), inset 0 0 0 1px rgba(99, 102, 241, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.3);
}

.icon-wrapper {
    width: 56px;
    height: 56px;
    border-radius: 14px;
    background: linear-gradient(135deg, #0f172a, #020617);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 18px rgba(96,165,250,0.25);
}

.upload-text {
    font-size: 18px;
    color: #e5e7eb;
}
.upload-subtext {
    font-size: 14px;
    color: #cbd5f5;
    margin-bottom: 16px;
}

/* ---- ANALYZE BUTTON ANIMATION ---- */
@keyframes breathe {
    0% { box-shadow: 0 0 0 rgba(99,102,241,0.4); }
    50% { box-shadow: 0 0 18px rgba(99,102,241,0.7); }
    100% { box-shadow: 0 0 0 rgba(99,102,241,0.4); }
}

.stButton > button {
    background: linear-gradient(90deg, #6366f1, #06b6d4);
    color: white;
    font-size: 16px;
    border-radius: 12px;
    border: none;
    padding: 10px 24px;
    animation: breathe 3s ease-in-out infinite;
}

/* ---- HIDE DEFAULT STREAMLIT UPLOADER STYLES ---- */
/* Remove the default file uploader background and border (the "useless bar") */
div[data-testid="stFileUploader"] section {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

/* Remove the small "Limit 200MB" text if it appears outside our custom UI */
div[data-testid="stFileUploader"] small {
    display: none;
}

/* ---- GLOW ON "BROWSE FILES" BUTTON ---- */
div[data-testid="stFileUploader"] button {
    background: rgba(255, 255, 255, 0.1);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    transition: all 0.3s ease;
}

div[data-testid="stFileUploader"] button:hover {
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.8);
    border-color: #6366f1;
    color: #cbd5f5;
    transform: translateY(-1px);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">AI Plagiarism Detection System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Semantic plagiarism analysis with AI-generated content detection</div>', unsafe_allow_html=True)

# ---------------- UPLOAD ----------------
st.markdown('<div class="section-title">Upload Document</div>', unsafe_allow_html=True)
st.markdown('<div class="upload-card">', unsafe_allow_html=True)

st.markdown("""
<div class="icon-wrapper">
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
    <path d="M12 16V4" stroke="#60A5FA" stroke-width="2" stroke-linecap="round"/>
    <path d="M8 8L12 4L16 8" stroke="#60A5FA" stroke-width="2" stroke-linecap="round"/>
    <path d="M4 16V20H20V16" stroke="#60A5FA" stroke-width="2"/>
  </svg>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="upload-text">Drag & drop your file here</div>', unsafe_allow_html=True)
st.markdown('<div class="upload-subtext">TXT • PDF • JPG • JPEG • PNG</div>', unsafe_allow_html=True)

file = st.file_uploader("", type=["txt","pdf","jpg","jpeg","png"], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

analyze = st.button("Analyze Document")

# ---------------- ANALYSIS ----------------
if file and analyze:
    with st.spinner("Analyzing document..."):
        # Make sure your backend API is running at this URL
        res = requests.post("http://127.0.0.1:8000/analyze", files={"file": file})

    if res.status_code == 200:
        data = res.json()
        report = data["report"]

        # ---- SUMMARY ----
        st.markdown("## Plagiarism Summary")
        st.markdown(
            f"<h2 style='color:{report['overall_color']}'>Overall Plagiarism: {report['overall_plagiarism']}%</h2>",
            unsafe_allow_html=True
        )

        # ---- DETECTED SOURCES ----
        st.markdown("## Detected Sources")

        for src in report["detected_sources"]:
            card_html = f"""
            <div style="
                display:flex;
                gap:14px;
                background:rgba(255,255,255,0.12);
                padding:16px;
                border-radius:14px;
                margin-bottom:12px;
                border-left:6px solid {src['color']};
            ">
                <div class="icon-wrapper">
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
                    <path d="M6 2H14L18 6V22H6V2Z"
                          stroke="#60A5FA" stroke-width="2"/>
                    <path d="M14 2V6H18"
                          stroke="#60A5FA" stroke-width="2"/>
                    <path d="M9 12H15M9 16H15"
                          stroke="#60A5FA" stroke-width="2"/>
                  </svg>
                </div>
                <div style="color:#e5e7eb;">
                    <div style="font-weight:600;">{src['file']}</div>
                    <div style="color:#cbd5f5;">Page {src['page']}</div>
                    <div>Similarity:
                        <b style="color:{src['color']};">{src['similarity']}%</b>
                    </div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

        # ---- AI USAGE ----
        st.markdown("## AI-Generated Content Analysis")
        ai_text = data.get("ai_generated_likelihood", "Unknown")
        ai_color = "red" if "High" in ai_text else "orange" if "Moderate" in ai_text else "green"

        st.markdown(
            f"<h3 style='color:{ai_color}'>AI Usage Likelihood: {ai_text}</h3>",
            unsafe_allow_html=True
        )
    else:
        st.error(f"Error: Unable to analyze document. Server returned {res.status_code}.")