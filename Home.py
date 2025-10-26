import streamlit as st

st.set_page_config(page_title="CandidAI", page_icon="🏠", layout="wide")

# ===================== NAV (buttons + switch_page) =====================
st.markdown("""
<style>
.nav-wrap { display:flex; justify-content:center; gap:14px; margin:18px 0 24px; }
.nav-wrap .stButton>button{
  background:#E3DACC;            /* same as info boxes */
  color:#3D3A2A;                  /* theme text */
  border:0; border-radius:18px;
  padding:10px 22px; font-weight:700; font-size:16px;
  box-shadow:0 3px 6px rgba(0,0,0,.15);
  transition:.15s ease;
}
.nav-wrap .stButton>button:hover{ background:#DCCFB7; transform:translateY(-2px); }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="nav-wrap">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([1,1,1,1], gap="small")
with c1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
with c2:
    if st.button("🎥 Demo", use_container_width=True):
        st.switch_page("pages/Demo.py")
with c3:
    if st.button("🧹 Redactor", use_container_width=True):
        st.switch_page("pages/Redactor.py")
with c4:
    if st.button("👥 About Us", use_container_width=True):
        st.switch_page("pages/About Us.py")
st.markdown('</div>', unsafe_allow_html=True)

# ===================== PAGE STYLES =====================
st.markdown("""
<style>
body { background:#F0EEE6; color:#3D3A2A; }

/* Hero */
.hero{
  position:relative; width:100%; max-width:1100px; height:280px;
  margin:0 auto 40px; border-radius:16px;
  background:#D97757; /* primaryColor */
  color:white; display:flex; align-items:center; justify-content:center;
  flex-direction:column; text-align:center;
  box-shadow:0 6px 20px rgba(0,0,0,.2);
}
.hero h1{ font-size:48px; font-weight:900; margin:0; }
.hero p{ font-size:20px; margin-top:8px; color:#F0EEE6; font-style: italic; }

/* Info boxes row */
.info-row{ display:flex; justify-content:center; gap:22px; flex-wrap:wrap; margin-top:40px; }
.info-box{
  width:260px; background:#E3DACC; /* secondaryBackgroundColor */
  color:#3D3A2A; border-radius:18px;
  box-shadow:0 4px 10px rgba(0,0,0,.1);
  padding:18px; text-align:center; transition:all .2s ease;
}
.info-box:hover{ background:#DCCFB7; transform:translateY(-3px); }
.info-box h3{ margin-bottom:8px; color:#D97757; } /* primaryColor */
.info-box p{ margin:0; font-size:.95rem; color:#3D3A2A; }
</style>
""", unsafe_allow_html=True)

# ===================== HERO =====================
st.markdown("""
<div class="hero">
  <h1>CandidAI</h1>
  <p>Empowering fair hiring through privacy and equality.</p>
</div>
""", unsafe_allow_html=True)

# ===================== INFO BOXES =====================
st.markdown("""
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
""", unsafe_allow_html=True)