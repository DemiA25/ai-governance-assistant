import streamlit as st
import pandas as pd
import json
from document_processor import process_document, truncate_text
from generators.raid_generator import generate_raid_log
from generators.summary_generator import generate_executive_summary


# --- Page config ---
st.set_page_config(
    page_title="AI Governance Assistant",
    page_icon="📋",
    layout="wide",
)

# --- Custom CSS ---
st.markdown("""
    <style>
    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Overall page background */
    .stApp {
        background-color: #F7F9FB;
    }

    /* Header banner */
    .header-banner {
        background: linear-gradient(135deg, #1B4F72 0%, #2E86C1 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .header-banner h1 {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0 0 0.3rem 0;
    }
    .header-banner p {
        color: #D4E6F1;
        font-size: 1rem;
        margin: 0;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1B4F72;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    [data-testid="stSidebar"] .stFileUploader label {
        color: white !important;
    }

    /* Make upload button visible */
    [data-testid="stSidebar"] .stFileUploader section {
        background-color: #FFFFFF !important;
        border: 2px dashed #2E86C1 !important;
        border-radius: 10px !important;
        padding: 1rem !important;
    }
    [data-testid="stSidebar"] .stFileUploader section * {
        color: #1B4F72 !important;
    }
    [data-testid="stSidebar"] .stFileUploader section button {
        background-color: #2E86C1 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: white;
        border-radius: 10px;
        padding: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 0.95rem;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1B4F72 !important;
        color: white !important;
    }

    /* RAID category cards */
    .raid-card {
        background: white;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        border-left: 5px solid #CCCCCC;
    }
    .raid-card.risks { border-left-color: #E74C3C; }
    .raid-card.assumptions { border-left-color: #F39C12; }
    .raid-card.issues { border-left-color: #E67E22; }
    .raid-card.dependencies { border-left-color: #3498DB; }

    .raid-card h4 {
        margin: 0 0 0.8rem 0;
        font-size: 1.05rem;
        color: #1C2833;
    }

    /* Summary output card */
    .summary-card {
        background: white;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        border-top: 4px solid #2E86C1;
        line-height: 1.7;
    }

    /* Info box styling */
    .upload-prompt {
        background: white;
        border-radius: 12px;
        padding: 3rem 2rem;
        text-align: center;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        margin-top: 2rem;
    }
    .upload-prompt h3 {
        color: #1B4F72;
        margin-bottom: 0.5rem;
    }
    .upload-prompt p {
        color: #5D6D7E;
        font-size: 1rem;
    }

    /* Button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #1B4F72 0%, #2E86C1 100%);
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(27,79,114,0.3);
    }

    /* Download button */
    .stDownloadButton > button {
        border-radius: 8px;
        font-weight: 500;
    }

    /* Dataframe styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }

    /* Expander */
    .streamlit-expanderHeader {
        font-size: 0.9rem;
        color: #5D6D7E;
    }

    /* Stats row */
    .stats-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .stat-box {
        background: white;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        flex: 1;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        text-align: center;
    }
    .stat-box .number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1B4F72;
    }
    .stat-box .label {
        font-size: 0.8rem;
        color: #5D6D7E;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    </style>
""", unsafe_allow_html=True)


# --- Header banner ---
st.markdown("""
    <div class="header-banner">
        <h1>📋 AI Programme Governance Assistant</h1>
        <p>Upload project documentation to generate RAID logs and 
        executive summaries powered by AI</p>
    </div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 📂 Document Upload")
    st.markdown("---")
    uploaded_file = st.file_uploader(
        "Upload a project document",
        type=["pdf", "docx"],
        help="Supports PDF and DOCX files up to 10MB",
    )

    if uploaded_file:
        st.success(f"✓ {uploaded_file.name}")
        st.caption(f"Size: {uploaded_file.size / 1024:.0f} KB")
        st.markdown("---")
        st.markdown("### ℹ️ How it works")
        st.markdown(
            "1. Upload your document\n"
            "2. Choose RAID Log or Executive Summary\n"
            "3. Click Generate\n"
            "4. Download the output"
        )

# --- No file uploaded state ---
if not uploaded_file:
    st.markdown("""
        <div class="upload-prompt">
            <h3>👈 Upload a document to get started</h3>
            <p>The assistant will analyse your project documentation and 
            generate structured governance outputs including RAID logs 
            and executive summaries.</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# --- Extract text ---
try:
    document_text = process_document(uploaded_file)
    document_text = truncate_text(document_text)
except Exception as e:
    st.error(f"Could not process document: {e}")
    st.stop()

if len(document_text.strip()) < 50:
    st.warning(
        "Document appears to be empty or image-based. "
        "Please upload a text-based PDF or DOCX."
    )
    st.stop()

# --- Document stats ---
word_count = len(document_text.split())
st.markdown(f"""
    <div class="stats-row">
        <div class="stat-box">
            <div class="number">{word_count:,}</div>
            <div class="label">Words Extracted</div>
        </div>
        <div class="stat-box">
            <div class="number">{uploaded_file.size / 1024:.0f} KB</div>
            <div class="label">File Size</div>
        </div>
        <div class="stat-box">
            <div class="number">{uploaded_file.name.split('.')[-1].upper()}</div>
            <div class="label">File Type</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Show extracted text
with st.expander("📄 View extracted text", expanded=False):
    st.text(document_text[:3000] + ("..." if len(document_text) > 3000 else ""))

# --- Tabs ---
tab_raid, tab_summary = st.tabs(["🎯 RAID Log", "📊 Executive Summary"])

# --- RAID Log Tab ---
with tab_raid:
    st.markdown("#### Generate RAID Log")
    st.caption(
        "Extracts Risks, Assumptions, Issues, and Dependencies "
        "from your project documentation."
    )

    if st.button("Generate RAID Log", key="raid_btn", type="primary"):
        with st.spinner("Analysing document and generating RAID log..."):
            try:
                raid_data = generate_raid_log(document_text)
                st.session_state["raid_data"] = raid_data
            except Exception as e:
                st.error(f"Error generating RAID log: {e}")

    if "raid_data" in st.session_state:
        raid = st.session_state["raid_data"]

        if "error" in raid:
            st.error(raid["error"])
        else:
            # Summary counts
            total_items = sum(
                len(raid.get(cat, []))
                for cat in ["risks", "assumptions", "issues", "dependencies"]
            )
            st.markdown(f"**{total_items} items identified across 4 categories**")
            st.markdown("")

            for category, label, emoji, css_class in [
                ("risks", "Risks", "🔴", "risks"),
                ("assumptions", "Assumptions", "🟡", "assumptions"),
                ("issues", "Issues", "🟠", "issues"),
                ("dependencies", "Dependencies", "🔵", "dependencies"),
            ]:
                items = raid.get(category, [])
                st.markdown(
                    f'<div class="raid-card {css_class}">'
                    f"<h4>{emoji} {label} ({len(items)})</h4></div>",
                    unsafe_allow_html=True,
                )
                if items:
                    df = pd.DataFrame(items)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.caption("No items identified in the document.")
                st.markdown("")

            # Download
            raid_json = json.dumps(raid, indent=2)
            st.download_button(
                label="📥 Download RAID Log (JSON)",
                data=raid_json,
                file_name="raid_log.json",
                mime="application/json",
            )

# --- Executive Summary Tab ---
with tab_summary:
    st.markdown("#### Generate Executive Summary")
    st.caption(
        "Produces an SLT-ready executive summary with RAG status, "
        "key progress, decisions required, and next steps."
    )

    if st.button("Generate Executive Summary", key="summary_btn", type="primary"):
        with st.spinner("Generating executive summary..."):
            try:
                summary = generate_executive_summary(document_text)
                st.session_state["summary"] = summary
            except Exception as e:
                st.error(f"Error generating summary: {e}")

    if "summary" in st.session_state:
        st.markdown(
            f'<div class="summary-card">{st.session_state["summary"]}</div>',
            unsafe_allow_html=True,
        )

        st.markdown("")
        st.download_button(
            label="📥 Download Summary (Markdown)",
            data=st.session_state["summary"],
            file_name="executive_summary.md",
            mime="text/markdown",
        )
