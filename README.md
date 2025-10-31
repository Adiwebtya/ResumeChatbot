# ResumeChatbot

**AI-powered Resume Evaluation Chatbot** — A small LLM-powered web application that analyzes resumes, provides recruiter-style feedback, and helps users craft ATS-friendly resumes. Built with a lightweight Python stack and Streamlit for the front end.  

> Repo snapshot: contains `chatbot.py`, `main.py`, `prompt.py`, `streamlit_app.py`, `config.py` and `requirements.txt`. :contentReference[oaicite:1]{index=1}

---

## Features

- Resume parsing and skill extraction using prompt-based LLM logic.
- Retrieval + prompt composition (modular `prompt.py`) to create structured feedback.
- Streamlit front-end for interactive resume upload and iterative feedback (`streamlit_app.py`).
- Config-driven API access (`config.py`) so you can plug your LLM/embedding provider keys.
- Example PDF resume files included for demo/testing. :contentReference[oaicite:2]{index=2}

---

## Tech Stack

- Python 3.8+  
- Streamlit (UI)  
- LangChain-style prompt composition (custom prompt management)  
- Any LLM provider (OpenAI, Groq, Vertex AI, etc.) via API keys configured in `config.py`  
- Requirements listed in `requirements.txt` (see repo). :contentReference[oaicite:3]{index=3}

---

## Quickstart (Local)

1. **Clone the repo**
```bash
git clone https://github.com/Adiwebtya/ResumeChatbot.git
cd ResumeChatbot
