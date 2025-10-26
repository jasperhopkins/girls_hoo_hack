import streamlit as st
st.set_page_config(page_title="About Us • FairForm", page_icon="👥", layout="wide")

c1, c2, c3, c4 = st.columns(4)
with c1: st.page_link("1_Home.py", label="Home", icon="🏠")
with c2: st.page_link("pages/2_Demo.py", label="Demo", icon="🎥")
with c3: st.page_link("pages/3_Redactor.py", label="Redactor", icon="🧹")
with c4: st.page_link("pages/4_About Us.py", label="About Us", icon="👥")

st.subheader("About Us")

import streamlit as st

st.set_page_config(page_title="About Us • EquiScreen", page_icon="👥", layout="wide")

# --- Layout ---
left, right = st.columns([1, 1.2])

with left:
    # Relative path to the image (go up one level from /pages/ to project root, then into /photos/)
    st.image("creatopy-oMtJYEbniH8-unsplash.jpg")

with right:
    st.markdown(
        """
        <style>
        .textbox {
            background-color: #E3DACC;
            border-radius: 18px;
            padding: 24px;
            height: 100%;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            color: #3D3A2A;
        }
        .textbox h3 {
            color: #D97757;
            margin-bottom: 10px;
        }
        </style>

        <div class="textbox">
            <h3>Our Mission</h3>
            <p>
                At <strong>CandidAI</strong>, we believe in empowering fair hiring through privacy and equality.
                Our goal is to eliminate unconscious bias from the recruitment process, allowing candidates to
                shine based on merit and skill.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
