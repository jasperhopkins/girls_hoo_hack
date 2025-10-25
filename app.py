import anthropic

import streamlit as st
import PyPDF2
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()


tools = [
    {
        "name": "debias_resume",
        "description": "Rewrites resume removing all identifying information",
        "input_schema": {
            "type": "object",
            "properties": {
                "resume_text": {"type": "string"},
                "previous_issues": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Issues found in previous attempt (if any)"
                }
            },
            "required": ["resume_text"]
        }
    },
    {
        "name": "verify_debiasing",
        "description": "Checks if resume still contains identifying information. Returns list of issues or confirms it's clean.",
        "input_schema": {
            "type": "object",
            "properties": {
                "resume_text": {"type": "string"}
            },
            "required": ["resume_text"]
        }
    }
]

# Set page configuration
st.set_page_config(
    page_title="PDF Text Extractor",
    page_icon="📄",
    layout="centered"
)

# Initialize session state for storing PDF text
if 'pdf_text' not in st.session_state:
    st.session_state.resume_pdf_text = ""
if 'file_name' not in st.session_state:
    st.session_state.resume_file_name = ""
if 'pdf_text' not in st.session_state:
    st.session_state.job_description = ""

# App title and description
st.title("📄 ResuRedact")
st.write("Empowering fair hiring through privacy and equality")

col1, col2 = st.columns(2)

with col1:
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a PDF file to extract text from it"
    )

    # Process the uploaded file
    if uploaded_file is not None:
        # Check if this is a new file
        if uploaded_file.name != st.session_state.resume_file_name:
            try:
                # Create a PDF reader object
                pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
                
                # Extract text from all pages
                extracted_text = ""
                num_pages = len(pdf_reader.pages)
                
                with st.spinner(f"Extracting text from {num_pages} pages..."):
                    for page_num, page in enumerate(pdf_reader.pages):
                        page_text = page.extract_text()
                        extracted_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                
                # Store in session state
                st.session_state.resume_pdf_text = extracted_text
                st.session_state.resume_file_name = uploaded_file.name
                
                st.success(f"✅ Successfully extracted text from '{uploaded_file.name}' ({num_pages} pages)")
                
            except Exception as e:
                st.error(f"❌ Error processing PDF: {str(e)}")
        else:
            st.info(f"📝 Using previously extracted text from '{uploaded_file.name}'")

    # Display stored text if available
    if st.session_state.resume_pdf_text:
        st.subheader("Extracted Text")
        
        # Show text statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Characters", len(st.session_state.resume_pdf_text))
        with col2:
            st.metric("Words", len(st.session_state.resume_pdf_text.split()))
        with col3:
            st.metric("Lines", st.session_state.resume_pdf_text.count('\n'))
        
        # Display the text in an expandable section
        with st.expander("View Full Text", expanded=True):
            st.text_area(
                "PDF Content",
                value=st.session_state.resume_pdf_text,
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )
        
        # Download button for the extracted text
        st.download_button(
            label="📥 Download as Text File",
            data=st.session_state.resume_pdf_text,
            file_name="redacted_resume.txt",
            mime="text/plain"
        )
        
        # Clear button
        if st.button("🗑️ Clear Session Data"):
            st.session_state.resume_pdf_text = ""
            st.session_state.resume_file_name = ""
            st.rerun()

    else:
        st.info("👆 Upload a PDF file to get started")

with col2:
    job_desc = st.text_area("Enter job desctiption...")


def debias_resume(resume_text, previous_issues=None):
    system_prompt = """You are a resume debiasing specialist. Your job is to rewrite resumes to remove ALL identifying information while preserving professional qualifications and experience.

MUST REMOVE:
- Names (replace with "Candidate")
- Gender indicators (pronouns, gendered titles like Mr./Ms., gendered scholarships)
- Specific universities (replace with "top-tier university" or "state university")
- Company names that reveal location
- Addresses, cities, neighborhoods
- Age indicators or graduation years
- Photos or physical descriptions
- Ethnic/cultural organization memberships that signal demographics

MUST PRESERVE:
- Skills and technical proficiencies
- Years of experience (but not specific dates)
- Project descriptions and achievements
- Education level and field of study
- Certifications and qualifications

OUTPUT: Only the debiased resume text. No explanations or commentary."""

    user_prompt = f"""Resume to debias:

{resume_text}

{f"IMPORTANT - Previous verification found these remaining issues that need addressing: {previous_issues}" if previous_issues else ""}"""
    
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=8192,
        system=system_prompt,  # Set the role/constraints
        messages=[{"role": "user", "content": user_prompt}]
    )
    st.session_state.resume_pdf_text = response.content[0].text
    st.rerun()
    return response.content[0].text

def verify_debiasing(resume_text):
    system_prompt = """You are a bias detection specialist. Your job is to identify ANY remaining personally identifying information in resumes.

Check for:
- Names or initials
- Gender indicators (he/she/his/her, Mr./Ms./Mrs., gendered awards like "Women in Tech")
- Specific institutions that reveal demographics (university names, high school names)
- Geographic identifiers (cities, states, neighborhoods, regional companies)
- Age indicators (graduation years, "recent graduate", age ranges)
- Physical descriptions or photos
- Cultural/ethnic organization names
- Anything else that could identify or reveal demographics

OUTPUT FORMAT:
If completely clean: "CLEAN"
If issues found: "ISSUES: [comma-separated list of specific problems found]"

Be thorough - even subtle indicators matter."""

    user_prompt = f"""Check this resume for identifying information:

{resume_text}"""
    
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1028,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )
    return response.content[0].text

TOOL_FUNCTIONS = {
    "debias_resume": debias_resume,
    "verify_debiasing": verify_debiasing
}

# Remove personally identifying information
if st.button("Remove personally identifying information from resume"):

    if not st.session_state.resume_pdf_text:
        st.error("Please upload a PDF first!")
    else:

        messages = [
            {"role": "user", "content": st.session_state.resume_pdf_text}
        ]
    
        messages_placeholder = st.empty()

        while True:
            messages_placeholder.json(messages)
            response = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4096,
                tools=tools,
                messages=messages,
                system = """You are a resume debiasing agent. Your goal is to iteratively remove all personally identifying information from resumes while preserving professional qualifications.

                    Your approach:
                    1. Start by debiasing the resume
                    2. Verify the result to check for any remaining identifying information
                    3. If issues are found, debias again using the verification feedback
                    4. Continue this cycle until verification confirms the resume is clean
                    5. Stop after successful verification OR after 3 debiasing attempts (to avoid infinite loops)

                    Key principles:
                    - Be thorough - even subtle identifiers (gendered language, specific institution names) must be caught
                    - Use verification feedback to improve each iteration
                    - Preserve all professional qualifications and achievements
                    - When verification returns "CLEAN", you're done

                    After completing the debiasing process, provide the user with the final clean resume.""" 
            )
            print(response)
            if response.stop_reason == "tool_use":
                # Execute tool
                tool_use = response.content[-1]
                result = TOOL_FUNCTIONS[tool_use.name](**tool_use.input)
                
                # Add to conversation
                messages.append({"role": "assistant", "content": response.content})
                messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": result
                    }]
                })
            else:
                # Done!
                break
    