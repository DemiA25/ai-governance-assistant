# AI Governance Assist

I have created an AI-powered tool that analyses project documentation and generates useful structured governance outputs: RAID logs, executive summaries and lessons learnt documents that support project, programme and further portfolio decision-making.


## Live Demo

[Link to deployed app](https://ai-governance-assist.streamlit.app/)

## The Problem

Throughout my years within project management, I noticed that Project, Risk and Programme  managers would spend hours manually producing RAID logs, executive summaries and lessons learnt  from project documentation to evaluate both Project and programme scope, performance and output. During my experience in UKHSA, I worked with the Risk Manager to weekly track the RAID Log and manually update new information given through team or 1-1 meetings. I also worked with the chief consultant to execute the end of programme lessons learnt workshops. We had countless primary research interviews, using quarterly report data as well in the final in person workshop to hand off the Lessons recommendation to the Government. The idea for this tool is to save time in automating processes of labour tasks to produce faster updates; and provide a more robust project view while maintaining the structured, professional output that senior leadership teams expect.

## How It Works

1. Upload a project document (PDF or DOCX)
2. The app extracts and processes the document text
3. Choose your output: RAID Log, Executive Summary or Lessons Learnt; or all three
4. AI Government Assist analyses the document using domain-specific prompt engineering
5. Download the structured output

## Architecture

- **Frontend**: Streamlit with custom styling
- **LLM**: Anthropic Claude (claude-sonnet-4-6) with structured JSON output
- **Document Processing**: pdfplumber (PDF), python-docx (DOCX)
- **Deployment**: Streamlit Community Cloud

## Design Decisions

- **Domain-specific prompts over generic ones**: The prompts encode real programme governance knowledge — distinguishing between risks and issues, flagging cross-organisational dependencies, structuring summaries for SLT audiences and gathering data for lessons learnt reporting.
- **Structured JSON output for RAID**: Ensures consistent, parseable output that can be exported and used in existing governance tools.
- **Low temperature (0.2)**: Prioritises factual extraction over creative generation, reducing hallucination when analysing documents.
- **Text truncation**: Documents exceeding 6,000 words are truncated to maintain output quality within the LLM context window.

## Future Improvements

- Governance report generation (third output type)
- RAG with vector search for large document sets
- Multi-document comparison (compare RAID logs across programme phases)
- Export to DOCX/XLSX format for direct use in governance packs
- User authentication and report history
- Batch processing for multiple documents

## Local Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/DemiA25/ai-governance-assistant.git
   cd ai-governance-assistant
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your Anthropic API key to `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

5. Run the app:
   ```bash
   streamlit run app.py
   ```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11+ |
| UI Framework | Streamlit |
| LLM Provider | Anthropic Claude API |
| PDF Processing | pdfplumber |
| DOCX Processing | python-docx |
| Data Display | pandas |
| Deployment | Streamlit Community Cloud |


