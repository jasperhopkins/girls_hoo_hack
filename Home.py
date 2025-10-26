import streamlit as st

st.set_page_config(page_title="CandidAI", page_icon="🏠", layout="wide")

# --- Top nav ---
c1, c2, c3, c4 = st.columns(4)
with c1: st.page_link("Home.py", label="Home", icon="🏠")
with c2: st.page_link("pages/Demo.py", label="Demo", icon="🎥")
with c3: st.page_link("pages/Redactor.py", label="Redactor", icon="🧹")
with c4: st.page_link("pages/About Us.py", label="About Us", icon="👥")

# --- ORANGE HEADER ---
st.markdown(
    """
    <style>
    .hero {
        position: relative;
        width: 100%;
        max-width: 1100px;
        height: 280px;
        margin: 0 auto 40px auto;
        border-radius: 16px;
        background: #D97757; /* orange background */
        color: white;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .hero h1 {
        font-size: 48px;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .hero p {
        font-size: 20px;
        margin-top: 8px;
        color: #fff8f0;
        text-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }
    .info-row {
        display: flex;
        justify-content: center;
        gap: 22px;
        flex-wrap: wrap;
        margin-top: 40px;
    }
    .info-box {
        width: 260px;
        background: #2e3236;
        color: #f5f7fb;
        border-radius: 18px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        padding: 18px;
        text-align: center;
    }
    .info-box h3 {
        margin-bottom: 8px;
    }
    .info-box p {
        margin: 0;
        color: #cbd3dc;
        font-size: .95rem;
    }
    </style>

    <div class="hero">
        <h1>CandidAI</h1>
        <p>Empowering fair hiring through privacy and equality.</p>
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
            <p>Upload, redact, and download in seconds.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)