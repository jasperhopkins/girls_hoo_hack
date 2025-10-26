import anthropic

import streamlit as st
import PyPDF2
import json
import os
from io import BytesIO
from dotenv import load_dotenv
import voyageai
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

client = anthropic.Anthropic()

voyage_client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))

st.set_page_config(page_title="Redactor • CandidAI", page_icon="🧹", layout="wide")

c1, c2, c3, c4 = st.columns(4)
with c1: st.page_link("1_Home.py", label="Home", icon="🏠")
with c2: st.page_link("pages/2_Demo.py", label="Demo", icon="🎥")
with c3: st.page_link("pages/3_Redactor.py", label="Redactor", icon="🧹")
with c4: st.page_link("pages/4_About Us.py", label="About Us", icon="👥")

redaction_tools = [
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

matching_tools = [
    {
        "name": "compute_semantic_similarity",
        "description": "Computes embedding-based semantic similarity between resume content (work experience, project, skills) and job description. Returns similarity score 0-100. Use this for each individual experience entry, each project entry, and once for technical skills. Higher scores indicate stronger semantic alignment.",
        "input_schema": {
            "type": "object",
            "properties": {
                "resume_content": {
                    "type": "string",
                    "description": "The specific resume content to evaluate - can be a single work experience, a single project description, or the full technical skills section"
                },
                "job_description": {
                    "type": "string",
                    "description": "The complete job description to compare against"
                }
            },
            "required": ["resume_content", "job_description"]
        }
    },
    {
        "name": "evaluate_education_match",
        "description": "Evaluates how well candidate's education meets job requirements using structured scoring (1-5 scale). Returns education match score with reasoning. Use LLM logic to handle degree hierarchies, equivalencies, and 'or equivalent experience' clauses.",
        "input_schema": {
            "type": "object",
            "properties": {
                "candidate_education": {
                    "type": "string",
                    "description": "Candidate's education background from resume (degrees, institutions, fields of study, graduation years, relevant coursework)"
                },
                "required_education": {
                    "type": "string",
                    "description": "Required education qualifications from job description"
                },
                "preferred_education": {
                    "type": "string",
                    "description": "Preferred/nice-to-have education qualifications from job description (if any)"
                }
            },
            "required": ["candidate_education", "required_education"]
        }
    },
    {
        "name": "compute_final_match_score",
        "description": "Synthesizes all individual evaluation scores into a weighted overall match score (0-100) with detailed breakdown. Applies intelligent aggregation - uses top-performing experiences/projects rather than simple averaging to fairly represent candidate's strongest qualifications.",
        "input_schema": {
            "type": "object",
            "properties": {
                "experience_scores": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "List of similarity scores for each individual work experience evaluated (0-100 scale)"
                },
                "project_scores": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "List of similarity scores for each individual project evaluated (0-100 scale)"
                },
                "skills_score": {
                    "type": "number",
                    "description": "Similarity score for technical skills match (0-100 scale)"
                },
                "education_score": {
                    "type": "number",
                    "description": "Education match score (1-5 scale from evaluate_education_match)"
                }
            },
            "required": ["skills_score", "education_score"]
        }
    }
]

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
    
    # response = client.messages.create(
    #     model="claude-sonnet-4-5-20250929",
    #     max_tokens=8192,
    #     system=system_prompt,  # Set the role/constraints
    #     messages=[{"role": "user", "content": user_prompt}]
    # )
    # st.session_state.redacted_resume = response.content[0].text
    # return response.content[0].text

    full_response = ""
    
    # Stream the response
    with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=8192,
        system=system_prompt,  # Set the role/constraints
        messages=[{"role": "user", "content": user_prompt}],
    ) as stream:
        for text in stream.text_stream:
            full_response += text
            # Update the placeholder with accumulated text
            redaction_messages_placeholder.markdown(full_response)
    st.session_state.redacted_resume = full_response
    return full_response

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

def compute_semantic_similarity(resume_content, job_description):
    """
    Computes semantic similarity using Voyage AI embeddings.
    Deterministic - same inputs produce same outputs.
    """
    if not resume_content.strip() or not job_description.strip():
        return json.dumps({
            "score": 0.0,
            "note": "Empty input provided"
        })
    
    try:
        # Batch embed both texts (more efficient than separate calls)
        result = voyage_client.embed(
            texts=[resume_content, job_description],
            model="voyage-3",
            input_type="document"
        )
        
        embeddings = result.embeddings
        
        # Compute cosine similarity
        similarity = cosine_similarity(
            [embeddings[0]], 
            [embeddings[1]]
        )[0][0]
        
        score = float(similarity * 100)
        
        return json.dumps({
            "score": round(score, 2),
            "method": "voyage_embeddings",
            "model": "voyage-3"
        })
        
    except Exception as e:
        # Handle API errors gracefully
        return json.dumps({
            "score": 0.0,
            "error": str(e),
            "note": "Failed to compute embeddings"
        })

def evaluate_education_match(candidate_education, required_education, preferred_education=None):
    """
    LLM-based education evaluation with structured 1-5 scoring.
    More stable than binary or percentage scoring.
    """
    system_prompt = """You are an education requirements evaluator. Assess how well a candidate's education meets job requirements using a strict 1-5 scoring scale.

SCORING RUBRIC (1-5):

5 - EXCEEDS REQUIREMENTS
- Has higher degree than required (e.g., PhD when Master's required)
- OR meets required degree + has preferred qualifications
- Field of study is highly relevant

4 - FULLY MEETS REQUIREMENTS  
- Has exactly the required degree level (e.g., Bachelor's when Bachelor's required)
- Field of study is directly relevant (e.g., CS degree for software role)
- Meets all stated requirements

3 - SUBSTANTIALLY MEETS REQUIREMENTS
- Has required degree level but field is related but not exact (e.g., Engineering vs Computer Science)
- OR has one level below required + significant relevant experience that may compensate
- Meets most requirements with minor gaps

2 - PARTIALLY MEETS REQUIREMENTS
- Has degree but in unrelated field
- OR has degree below required level without compensating experience
- Meets some requirements but has notable gaps

1 - DOES NOT MEET REQUIREMENTS
- Lacks required degree level entirely
- Field of study is unrelated
- Does not meet minimum requirements

IMPORTANT CONSIDERATIONS:
- "Bachelor's or equivalent experience" clauses: If 4+ years relevant experience, can score 3-4 even without degree
- Degree hierarchies: High School < Associate's < Bachelor's < Master's < PhD
- Field relevance: "Computer Science" ≠ "Computer Engineering" (related but not identical)
- Recency: Recent degrees are slightly preferred but not heavily weighted

OUTPUT FORMAT (must be valid JSON):
{
    "score": <1-5>,
    "reasoning": "<2-3 sentence explanation of score>",
    "meets_required": <true/false>,
    "meets_preferred": <true/false>
}"""

    user_prompt = f"""REQUIRED EDUCATION:
{required_education}

{f"PREFERRED EDUCATION:\n{preferred_education}\n" if preferred_education else ""}
CANDIDATE'S EDUCATION:
{candidate_education}

Evaluate using the 1-5 rubric. Return JSON only."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        temperature=0,  # Maximize consistency
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )
    
    return response.content[0].text

def compute_final_match_score(skills_score, education_score, experience_scores=None, project_scores=None):
    """
    Synthesizes individual scores into weighted overall match.
    Uses top-N aggregation for experiences/projects to fairly represent strongest qualifications.
    """
    
    # Weights for final score
    weights = {
        "experience": 0.40,  # 40% - most important
        "projects": 0.20,    # 20%
        "skills": 0.25,      # 25%
        "education": 0.15    # 15%
    }
    
    # Handle experience scores - use top 3 to avoid penalizing diverse backgrounds
    if experience_scores and len(experience_scores) > 0:
        # Sort and take top 3 (or all if fewer than 3)
        top_experiences = sorted(experience_scores, reverse=True)[:3]
        experience_score = np.mean(top_experiences)
        num_experiences_evaluated = len(experience_scores)
        num_experiences_used = len(top_experiences)
    else:
        experience_score = 0
        num_experiences_evaluated = 0
        num_experiences_used = 0
    
    # Handle project scores - use top 2
    if project_scores and len(project_scores) > 0:
        top_projects = sorted(project_scores, reverse=True)[:2]
        projects_score = np.mean(top_projects)
        num_projects_evaluated = len(project_scores)
        num_projects_used = len(top_projects)
    else:
        projects_score = 0
        num_projects_evaluated = 0
        num_projects_used = 0
    
    # Convert education score from 1-5 scale to 0-100 scale
    # 1 -> 0, 2 -> 25, 3 -> 50, 4 -> 75, 5 -> 100
    education_score_normalized = (education_score - 1) * 25
    
    # Calculate weighted overall score
    overall_score = (
        experience_score * weights["experience"] +
        projects_score * weights["projects"] +
        skills_score * weights["skills"] +
        education_score_normalized * weights["education"]
    )
    
    # Determine match level
    if overall_score >= 60:
        match_level = "Excellent Match"
        recommendation = "Highly recommended - strong alignment across all dimensions"
    elif overall_score >= 50:
        match_level = "Strong Match"
        recommendation = "Recommended - good overall fit with notable strengths"
    elif overall_score >= 40:
        match_level = "Moderate Match"
        recommendation = "Consider - adequate fit with some gaps"
    elif overall_score >= 30:
        match_level = "Weak Match"
        recommendation = "Questionable fit - significant gaps in qualifications"
    else:
        match_level = "Poor Match"
        recommendation = "Not recommended - substantial misalignment with requirements"
    
    st.write("Overall Score:", round(overall_score, 2))
    st.write("Match Level:", match_level)
    st.write("Reccomendation:", recommendation)

    return json.dumps({
        "overall_score": round(overall_score, 2),
        "match_level": match_level,
        "recommendation": recommendation,
        "breakdown": {
            "experience": {
                "score": round(experience_score, 2),
                "weight": weights["experience"],
                "contribution": round(experience_score * weights["experience"], 2),
                "evaluated": num_experiences_evaluated,
                "used_for_score": num_experiences_used,
                "note": f"Using top {num_experiences_used} of {num_experiences_evaluated} experiences"
            },
            "projects": {
                "score": round(projects_score, 2),
                "weight": weights["projects"],
                "contribution": round(projects_score * weights["projects"], 2),
                "evaluated": num_projects_evaluated,
                "used_for_score": num_projects_used,
                "note": f"Using top {num_projects_used} of {num_projects_evaluated} projects"
            },
            "skills": {
                "score": round(skills_score, 2),
                "weight": weights["skills"],
                "contribution": round(skills_score * weights["skills"], 2)
            },
            "education": {
                "score_raw": education_score,
                "score_normalized": round(education_score_normalized, 2),
                "weight": weights["education"],
                "contribution": round(education_score_normalized * weights["education"], 2),
                "note": "Score 1-5 converted to 0-100 scale"
            }
        },
        "weights_applied": weights
    })
    
TOOL_FUNCTIONS = {
    "debias_resume": debias_resume,
    "verify_debiasing": verify_debiasing,
    "compute_semantic_similarity": compute_semantic_similarity,
    "evaluate_education_match": evaluate_education_match,
    "compute_final_match_score": compute_final_match_score
}

# Set page configuration
st.set_page_config(
    page_title="CandidAI",
    page_icon="📄",
    layout="centered"
)

# Initialize session state for storing PDF text
if 'resume_pdf_text' not in st.session_state:
    st.session_state.resume_pdf_text = ""
if 'redacted_resume' not in st.session_state:
    st.session_state.redacted_resume = ""
if 'resume_file_name' not in st.session_state:
    st.session_state.resume_file_name = ""
if 'job_desc' not in st.session_state:
    st.session_state.job_desc = ""

# App title and description
st.title("📄 CandidAI")
st.write("Empowering fair hiring through privacy and equality")


redactor_col, matcher_col = st.columns(2)

with redactor_col:

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
            st.markdown(
            """
            <style>
            textarea {
                border-radius: 6px !important;
                border: 1px solid #DCCFB7 !important;
                background-color: #F0EEE6 !important;
                color: #3D3A2A !important;
                font-family: sans-serif !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
            st.text_area(
                "PDF Content",
                value=st.session_state.resume_pdf_text,
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )

        
        with col3: 
            # Download button for the extracted text
            st.download_button(
                label="📥 Download as Text File",
                data=st.session_state.redacted_resume,
                file_name="redacted_resume.txt",
                mime="text/plain"
            )
        
        with col2:
            # Clear button
            if st.button("🗑️ Clear Session Data"):
                st.session_state.resume_pdf_text = ""
                st.session_state.redacted_resume = ""
                st.session_state.resume_file_name = ""
                st.session_state.job_desc = ""
                st.rerun()

        redaction_messages_placeholder = st.empty()
        matching_messages_placeholder = st.empty()

        with col1:
            # Remove personally identifying information
            if st.button("🧹 Redact Personal Info"):

                if not st.session_state.resume_pdf_text:
                    st.error("Please upload a PDF first!")
                else:

                    messages = [
                        {"role": "user", "content": st.session_state.resume_pdf_text}
                    ]
                

                    for _ in range(30): # avoid infitinite loops failsafe
                        # redaction_messages_placeholder.json(messages)
                        response = client.messages.create(
                            model="claude-sonnet-4-5-20250929",
                            max_tokens=4096,
                            tools=redaction_tools,
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
        
                    st.success("🧹 Resume Redaction Complete")
    else:
        st.info("👆 Upload a PDF file to get started")

    with matcher_col:
    
        st.text_area("Job Description:", key='job_desc', placeholder="Enter Job Description or Details...")

        if st.button("Resume Match"):

            if not st.session_state.resume_pdf_text:
                st.error("Please upload a PDF first!")
            elif not st.session_state.job_desc:
                st.error("Please enter a job description first!")
            else:

                messages = [{
                    "role": "user",
                    "content": f"""Evaluate how well this resume matches the job description:

                        JOB DESCRIPTION:
                        {st.session_state.job_desc}

                        RESUME:
                        {st.session_state.redacted_resume}

                    Evaluate each work experience and project individually for thorough analysis."""
                }]

                for _ in range(30):
                    # matching_messages_placeholder.json(messages)
                    response = client.messages.create(
                        model="claude-sonnet-4-5-20250929",
                        max_tokens=4096,
                        tools=matching_tools,
                        messages=messages,
                        system = """You are a resume matching agent that evaluates candidate fit through granular, structured analysis.

                            Your evaluation process:
                            1. Analyze the resume to identify individual work experiences, projects, and technical skills
                            2. For EACH work experience entry, use compute_semantic_similarity to score alignment with the job description
                            3. For EACH project entry, use compute_semantic_similarity to score alignment with the job description
                            4. Use compute_semantic_similarity once for the complete technical skills section
                            5. Use evaluate_education_match to assess education requirements (returns 1-5 score)
                            6. Use compute_final_match_score to synthesize all individual scores into an overall match rating

                            Be thorough: Evaluate every distinct work experience and project individually.

                            After completing your evaluation, provide:
                            - Overall match score and level
                            - Breakdown showing strongest matching experiences and projects  
                            - Key qualifications that align well
                            - Any notable gaps or areas where fit is weaker"""
                        )
                    if response.stop_reason == "tool_use":
                        # Execute tool
                        messages.append({"role": "assistant", "content": response.content})
                        tool_results = []
                        for tool_use in response.content:
                            if tool_use.type == "tool_use":
                                result = TOOL_FUNCTIONS[tool_use.name](**tool_use.input)
                                tool_results.append({
                                        "type": "tool_result",
                                        "tool_use_id": tool_use.id,
                                        "content": result
                                })
                        messages.append({
                            "role": "user",
                            "content": tool_results
                        })
                    else:
                        # Done!
                        break
        

