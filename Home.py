import streamlit as st

st.set_page_config(page_title="ResuRedact", page_icon="🏠", layout="wide")

# --- Top nav (links behave like tabs) ---
c1, c2, c3, c4, c5 = st.columns(5)
with c1: st.page_link("Home.py", label="Home", icon="🏠")
with c2: st.page_link("pages/demoTab.py", label="Demo", icon="🎥")
with c3: st.page_link("pages/Redactor.py", label="Redactor", icon="🧹")
with c4: st.page_link("pages/resumeMatchTab.py", label="Resume Match", icon="🧠")
with c5: st.page_link("pages/aboutTab.py", label="About Us", icon="👥")

# ---------- Home content ----------
image1 = "image1.jpg"  # put this file next to app.py or use "images/image1.jpg"

st.markdown(
    f"""
    <style>
    .hero {{
        position: relative; width: 100%; height: 360px;
        border-radius: 16px; overflow: hidden;
        box-shadow: 0 6px 25px rgba(0,0,0,0.25);
        margin: 18px 0 26px 0;
    }}
    .hero img {{ width:100%; height:100%; object-fit:cover; filter:brightness(0.7); }}
    .hero-text {{
        position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
        color:#fff; text-align:center;
    }}
    .hero-text h1 {{ font-size:clamp(34px,6vw,64px); font-weight:900; margin:0 0 .25rem 0; }}
    .hero-text p {{ font-size:clamp(16px,2.5vw,26px); font-weight:600; opacity:.95; }}

    .info-row {{
        display:flex; justify-content:center; gap:22px; flex-wrap:wrap;
    }}
    .info-box {{
        width:260px; background:#2e3236; color:#f5f7fb;
        border-radius:18px; box-shadow:0 8px 20px rgba(0,0,0,0.3);
        padding:18px; text-align:center;
    }}
    .info-box h3 {{ margin:.2rem 0 .5rem 0; }}
    .info-box p {{ margin:0; color:#cbd3dc; font-size:.95rem; }}
    </style>

    <div class="hero">
      <img src="{image1}" alt="ResuRedact Header">
      <div class="hero-text">
        <h1>ResuRedact</h1>
        <p>Empowering fair hiring through privacy and equality.</p>
      </div>
    </div>

    <div class="info-row">
      <div class="info-box">
        <h3>Privacy First</h3>
        <p>Remove personal identifiers and let skills shine.</p>
      </div>
      <div class="info-box">
        <h3>AI-Powered</h3>
        <p>Smart detection with clear rationale.</p>
      </div>
      <div class="info-box">
        <h3>Fair Hiring</h3>
        <p>Encourage unbiased resume reviews.</p>
      </div>
      <div class="info-box">
        <h3>Fast & Secure</h3>
        <p>Upload, redact, download in seconds.</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)