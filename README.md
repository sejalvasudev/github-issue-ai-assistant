# 🧠 GitHub Issue AI Assistant

An AI-powered assistant that summarizes GitHub issues and classifies them by type, priority score, labels, and potential impact using a Large Language Model. Built using **FastAPI**, **Streamlit**, and **GROQ API**.

---

## ✨ Features

- 🔗 Accepts any GitHub Issue URL
- 🤖 Summarizes title, body, and comments using LLM
- 🏷️ Suggests issue type, priority score, relevant labels, and potential impact
- 🧠 Uses GROQ API (Mixtral-8x7b) for smart analysis
- 🌐 Offers both REST API (FastAPI) and Web UI (Streamlit)

---

## 🚀 Quickstart: Run in <5 mins

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/github-issue-ai-assistant.git
cd github-issue-ai-assistant

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate       # For Windows
# or
source .venv/bin/activate    # For Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file and add your keys
echo GITHUB_TOKEN=your_github_pat >> .env
echo GROQ_API_KEY=your_groq_api_key >> .env

# 5. Run the FastAPI server
uvicorn app.main:app --reload
# Visit http://127.0.0.1:8000/docs

# 6. (Optional) Run the Streamlit UI
streamlit run ui/main.py
# Visit http://localhost:8501
