import streamlit as st

c1, c2, c3, c4 = st.columns(4)
with c1: st.page_link("1_Home.py", label="Home", icon="🏠")
with c2: st.page_link("pages/2_Demo.py", label="Demo", icon="🎥")
with c3: st.page_link("pages/3_Redactor.py", label="Redactor", icon="🧹")
with c4: st.page_link("pages/4_About Us.py", label="About Us", icon="👥")

st.subheader("About Us")

import streamlit as st

st.set_page_config(page_title="About Us • CandidAI", page_icon="👥", layout="wide")

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
                Women and underrepresented groups still face bias in hiring — sometimes invisible, but deeply impactful.
                We’ve seen qualified candidates lose opportunities simply because of their name, background, or gender cues.
                We wanted to build something that challenges that: a tool that levels the playing field.
                <strong>CandidAI</strong> was born from the belief that skills speak louder than stereotypes.
                Our mission is to make hiring a space where every voice — especially women’s voices — is heard, respected, and seen for its value.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
