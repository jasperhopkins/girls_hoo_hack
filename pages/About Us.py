import streamlit as st
st.set_page_config(page_title="About Us • FairForm", page_icon="👥", layout="wide")

c1, c2, c3, c4 = st.columns(4)
with c1: st.page_link("Home.py", label="Home", icon="🏠")
with c2: st.page_link("pages/Demo.py", label="Demo", icon="🎥")
with c3: st.page_link("pages/Redactor.py", label="Redactor", icon="🧹")
with c4: st.page_link("pages/About Us.py", label="About Us", icon="👥")

st.subheader("About Us")
st.write("Team, values, and contact.")

import streamlit as st

st.set_page_config(page_title="About Us • EquiScreen", page_icon="👥", layout="wide")

# --- Layout ---
left, right = st.columns([1, 1.3], gap="large")

with left:
    # Relative path to the image (go up one level from /pages/ to project root, then into /photos/)
    st.image("creatopy-oMtJYEbniH8-unsplash.jpg")