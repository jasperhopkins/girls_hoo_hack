import streamlit as st
import time

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
        "",
        "",
        "",]
  

  
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
  