import streamlit as st

# Configure the page
st.set_page_config(
    page_title="ResuRedact",
    page_icon="📋",
    layout="wide"  # Use wide layout for better presentation
)

# Create tabs at the top
tabHome, tabDemo, tabRedactor, tabResumeM, tabAbout = st.tabs(["Home", "Demo", "Redactor", "Resume Match", "About Us"])

# ========================================
# HOME TAB (MAIN PAGE)
# ========================================
with tabHome:
  image1 = ""
  image2 = ""
  image3 = ""

st.markdown(
        f"""
        <style>
        .hero {{
            position: relative;
            width: 100%;
            height: 360px;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 6px 25px rgba(0,0,0,0.25);
            margin-bottom: 30px;
        }}
        .hero img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: brightness(0.7);
        }}
        .hero-text {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            text-align: center;
        }}
        .hero-text h1 {{
            font-size: clamp(34px, 6vw, 64px);
            font-weight: 900;
            margin-bottom: 0.25rem;
        }}
        .hero-text p {{
            font-size: clamp(16px, 2.5vw, 26px);
            font-weight: 600;
            opacity: 0.95;
        }}
        .info-row {{
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
            margin-top: 16px;
        }}
        .info-box {{
            width: 320px;
            background: #2e3236;
            color: #f5f7fb;
            border-radius: 18px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            padding: 20px;
            text-align: center;
        }}
        .info-box h3 {{
            margin-top: 0;
            margin-bottom: 6px;
        }}
        .info-box p {{
            font-size: 0.95rem;
            color: #cbd3dc;
            margin: 0;
        }}
        </style>

        <div class="hero">
            <img src="{image1}" alt="ResuRedact Header">
            <div class="hero-text">
                <h1>ResuRedact</h1>
                <p>Empowering fair hiring through privacy and equality.</p>
            </div>
        </div>

        <!-- Four centered info boxes -->
        <div class="info-row">
            <div class="info-box">
                <h3>Privacy First</h3>
                <p>Remove personal identifiers and let skills take the spotlight.</p>
            </div>
            <div class="info-box">
                <h3>AI-Powered</h3>
                <p>Smart detection with context-aware explanations.</p>
            </div>
            <div class="info-box">
                <h3>Fair Hiring</h3>
                <p>Encouraging unbiased candidate reviews across all industries.</p>
            </div>
            <div class="info-box">
                <h3>Fast & Secure</h3>
                <p>Upload, redact, and download — all in seconds, locally and safely.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  
# ========================================
# DEMO TAB
# ========================================
with tabDemo:
  st.subheader("Demo Video")

  
# ========================================
# REDACTOR TAB
# ========================================
with tabRedactor:
  st.subheader("Redactor")

  
# ========================================
# RESUME MATCH TAB
# ========================================
with tabResumeM:
  st.subheader("Resume Match")


# ========================================
# ABOUT US TAB
# ========================================
with tabAbout:
  st.subheader("About Us")
  