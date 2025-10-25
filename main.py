import os, base64, time
import streamlit as st

# Configure the page
st.set_page_config(
    page_title="ResuRedact",
    page_icon="🏠",
    layout="wide"  # Use wide layout for better presentation
)

# Create tabs at the top
tabHome, tabDemo, tabRedactor, tabResumeM, tabAbout = st.tabs(["Home", "Demo", "Redactor", "Resume Macth", "About Us"])

# ========================================
# HOME TAB (MAIN PAGE)
# ========================================
with tabHome:
  SLIDES = [
        "amy-hirschi-JaoVGh5aJ3E-unsplash.jpg",
        "resume-genius-72D3z_LfrQA-unsplash.jpg",
        "vitaly-gariev-nwmRGqPNu7M-unsplash.jpg", 
        "christina-wocintechchat-com-faEfWCdOKIg-unsplash.jpg",
        "cherrydeck-UpsEF48wAgk-unsplash.jpg"]
  
# Fallback if a file is missing
FALLBACK = "https://images.unsplash.com/photo-1546842931-886c185b4c8c?q=80&w=1600&auto=format&fit=crop"

def img_to_data_uri(path: str) -> str:
        if os.path.exists(path):
            ext = os.path.splitext(path)[1][1:].lower() or "jpg"
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/{ext};base64,{b64}"
        return FALLBACK

SLIDES = [img_to_data_uri(p) for p in SLIDES]

    # --- Slideshow state ---
if "slide_index" not in st.session_state:
        st.session_state.slide_index = 0
if "last_switch" not in st.session_state:
        st.session_state.last_switch = time.time()

AUTOPLAY = True
INTERVAL = 3  # seconds

    # Autoplay loop
if AUTOPLAY and time.time() - st.session_state.last_switch >= INTERVAL:
        st.session_state.slide_index = (st.session_state.slide_index + 1) % len(SLIDES)
        st.session_state.last_switch = time.time()
        st.experimental_rerun()

cur = SLIDES[st.session_state.slide_index]

    # --- Optional manual controls (small + centered) ---
c1, c2, c3 = st.columns([1, 6, 1], gap="small")
with c1:
        if st.button("◀", use_container_width=True):
            st.session_state.slide_index = (st.session_state.slide_index - 1) % len(SLIDES)
with c3:
        if st.button("▶", use_container_width=True):
            st.session_state.slide_index = (st.session_state.slide_index + 1) % len(SLIDES)
with c2:
        dot_cols = st.columns(len(SLIDES))
        for i, col in enumerate(dot_cols):
            with col:
                if st.button("●" if i == st.session_state.slide_index else "○", key=f"dot_{i}"):
                    st.session_state.slide_index = i



  

  
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
  