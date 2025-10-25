import streamlit as st
st.set_page_config(page_title="Demo • ResuRedact", page_icon="🎥", layout="wide")

# Top nav
c1, c2, c3, c4, c5 = st.columns(5)
with c1: st.page_link("Home.py", label="Home", icon="🏠")
with c2: st.page_link("pages/Demo.py", label="Demo", icon="🎥")
with c3: st.page_link("pages/Redactor.py", label="Redactor", icon="🧹")
with c4: st.page_link("pages/Resume Match.py", label="Resume Match", icon="🧠")
with c5: st.page_link("pages/About Us.py", label="About Us", icon="👥")

st.subheader("Demo Video")
st.write("Embed a walkthrough with `st.video('URL')`.")
# st.video("https://www.youtube.com/watch?v=XXXXXXXX")


