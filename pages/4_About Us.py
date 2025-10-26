import streamlit as st


st.set_page_config(page_title="About Us • CandidAI", page_icon="👥", layout="wide")

c1, c2, c3, c4 = st.columns(4)
with c1: st.page_link("1_Home.py", label="Home", icon="🏠")
with c2: st.page_link("pages/2_Demo.py", label="Demo", icon="🎥")
with c3: st.page_link("pages/3_Redactor.py", label="Redactor", icon="🧹")
with c4: st.page_link("pages/4_About Us.py", label="About Us", icon="👥")

st.subheader("About Us")
# --- Layout ---
left, right = st.columns([1, 1.2])

with left:
    st.markdown(
        """
        <style>
        .about-img img {
            height: 600px;        /* adjust this value for desired height */
            object-fit: cover;    /* crop neatly */
            border-radius: 18px;  /* match theme */
            box-shadow: 0 6px 18px rgba(0,0,0,0.2);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="about-img">', unsafe_allow_html=True)
    st.image("creatopy-oMtJYEbniH8-unsplash.jpg", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


with right:
    st.markdown(
        """
        <style>
        .textbox {
            background-color: #E3DACC;
            border-radius: 18px;
            padding: 24px;
            margin-bottom: 35px; /* added extra space between boxes */
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            color: #3D3A2A;
        }
        .textbox h3 {
            color: #D97757;
            margin-bottom: 10px;
        }
        .textbox p {
            line-height: 1.6;
            margin-bottom: 0.75rem;
        }
        </style>

        <!-- Mission box -->
        <div class="textbox">
            <h3>Our Mission</h3>
            <p>
                Women and underrepresented groups still face bias in hiring — sometimes invisible, but deeply impactful.
                We’ve seen qualified candidates lose opportunities simply because of their name, background, or gender cues.
            </p>
            <p>
                We wanted to build something that challenges that: a tool that levels the playing field.
                <strong>CandidAI</strong> was born from the belief that skills speak louder than stereotypes.
                Our mission is to make hiring a space where every voice — especially women’s voices — is heard,
                respected, and seen for its value.
            </p>
        </div>

        <!-- How it Works box -->
        <div class="textbox">
            <h3>How It Works</h3>
            <p>
                CandidAI uses natural language processing to automatically identify and remove bias-triggering
                details from resumes — things like names, pronouns, school names, and other demographic clues.
            </p>
            <p>
                The result? A fully anonymized resume that keeps professional achievements intact, letting hiring
                managers focus on skills and experience instead of identity. Our process is transparent, ethical,
                and designed with inclusion at its core.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
