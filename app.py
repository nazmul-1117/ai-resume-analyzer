import streamlit as st
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer, util

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Pro-ATS Analyzer",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>

/* =========================
   BACKGROUND IMAGE
========================= */
.stApp {
    # background: url("assets/background.jpg");
    background-image: url("./assets/background.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* DARK OVERLAY (IMPORTANT FOR READABILITY) */
.stApp::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    background: rgba(10, 12, 20, 0.75);
    z-index: 0;
}

/* keep content above overlay */
.block-container {
    position: relative;
    z-index: 1;
    padding-top: 2rem;
}


/* =========================
   BUTTONS (MODERN GRADIENT)
========================= */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    padding: 10px 16px;
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border: none;
    font-weight: 600;
    transition: 0.3s ease;
    box-shadow: 0px 4px 15px rgba(0, 114, 255, 0.3);
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 6px 20px rgba(0, 114, 255, 0.5);
}


/* =========================
   SKILL TAGS
========================= */
.skill-tag {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    background: rgba(255,255,255,0.08);
    margin: 5px;
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(8px);
    font-size: 13px;
}


/* =========================
   SCORE CARD (GLASS UI)
========================= */
.score-card {
    text-align: center;
    padding: 30px;
    border-radius: 20px;
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}


/* =========================
   HEADINGS
========================= */
h1, h2, h3 {
    color: #ffffff;
    font-weight: 700;
}

/* center main title */
h1 {
    text-align: center;
}


/* =========================
   SIDEBAR (if used later)
========================= */
section[data-testid="stSidebar"] {
    background: rgba(10, 12, 20, 0.6);
    backdrop-filter: blur(10px);
}

</style>
""", unsafe_allow_html=True)


# --- MODEL ---
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()


# --- PDF TEXT EXTRACTION ---
def extract_text(file):
    pdf_bytes = file.read()  # safe read
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# --- UI ---
st.title("🚀 AI-Powered ATS Optimizer")
st.markdown("---")

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📂 Upload Documents")

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    jd_text = st.text_area("Paste Job Description", height=250)

    st.subheader("🎯 Target Skills")
    all_skills = [
        "RAG", "LLM", "Fine-tuning", "LangChain",
        "Docker", "PyTorch", "Kubernetes", "Vector DB"
    ]

    selected_skills = st.multiselect(
        "Select core skills to check for:",
        all_skills
    )


with col2:
    st.subheader("📊 Analysis Results")

    if st.button("Analyze Resume"):

        if not uploaded_file or not jd_text.strip():
            st.error("Please provide both Resume and Job Description")
            st.stop()

        # --- PROCESS ---
        resume_text = extract_text(uploaded_file)

        # --- EMBEDDING SCORE ---
        emb_resume = model.encode(resume_text, normalize_embeddings=True)
        emb_jd = model.encode(jd_text, normalize_embeddings=True)

        score = util.cos_sim(emb_resume, emb_jd).item() * 100

        # --- SCORE UI ---
        st.markdown(f"""
        <div class="score-card">
            <h3>Overall Match Score</h3>
            <h1 style="color:{'#00ffcc' if score > 70 else '#ff4b4b'}">
                {score:.2f}%
            </h1>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🔍 Skill Verification")

        resume_lower = resume_text.lower()

        if selected_skills:
            for skill in selected_skills:
                present = skill.lower() in resume_lower
                icon = "✅" if present else "❌"

                st.markdown(
                    f"<div class='skill-tag'>{icon} {skill}</div>",
                    unsafe_allow_html=True
                )
        else:
            st.info("Select skills to check gap analysis")


        # --- SIMPLE AI INSIGHT ---
        if score < 60:
            st.warning("Low match score — consider tailoring your resume to the job description.")
        elif score < 80:
            st.info("Moderate match — improving keywords can boost your ATS score.")
        else:
            st.success("Strong match — your resume aligns well with this role!")

st.markdown("---")
st.caption("Powered by Sentence-Transformers & PyMuPDF | ATS AI Engine")