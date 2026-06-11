# 📚 Document QA ChatBot

[![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-ff4b4b)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-Classic-005830)](https://python.langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.1-FF6600)](https://groq.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org/)

A powerful **Document Question Answering ChatBot** that allows you to upload PDF documents and ask questions about their content.

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **PDF Upload** | Upload any PDF document (up to 200MB) |
| 🤖 **AI-Powered Answers** | Uses Groq's Llama 3.1 for fast, accurate responses |
| 💬 **Chat Interface** | User-friendly chat interface |
| 🔄 **Multiple Questions** | Ask unlimited questions without re-uploading |
| 🗑️ **Reset Button** | Clear all data and upload a new document |
| 📝 **Chat History** | Complete conversation history preserved |
| ⚡ **Session State** | Data persists even when page refreshes |

## 🛠️ Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| **Streamlit** | 1.35+ | Web application framework |
| **LangChain** | 0.3+ (Classic) | AI chain orchestration |
| **Groq** | Llama 3.1 8B | Fast language model for answers |
| **HuggingFace** | all-MiniLM-L6-v2 | Text to vector conversion |
| **FAISS** | 1.14+ | Vector database for similarity search |
| **PyPDF** | 4.2+ | PDF text extraction |
| **Python** | 3.8+ | Programming language |

## 🧠 How It Works (RAG in action)
1. **Ingestion**: Your PDF is split into chunks, each converted to a vector (embedding) and stored in FAISS.
2. **Retrieval**: When you ask a question, it's converted to a vector and the most relevant chunks are found.
3. **Generation**: Those chunks + your question are sent to Llama 3, which answers **only** from the provided context.

## 📋 Requirements

- Python 3.8 or higher
- Groq API Key (free: [console.groq.com](https://console.groq.com))
- 4GB RAM minimum
- Internet connection

## 🚀 Quick Start (5 minutes)
### Prerequisites
- Python 3.9 or later
- A free [Groq API key](https://console.groq.com) (sign up → API Keys)
1. **Clone the repo**  
   `git clone https://github.com/shihjen/Document_QA_ChatBot.git && cd Document_QA_ChatBot`
   `cd Document_QA_ChatBot`
2. **Create virtual environment**  
   - Windows: `python -m venv venv` → `venv\Scripts\activate`  
   - Mac/Linux: `python3 -m venv venv` → `source venv/bin/activate`
3. **Install dependencies**  
   `pip install streamlit langchain langchain-community langchain-groq langchain-text-splitters langchain-classic pypdf faiss-cpu sentence-transformers python-dotenv`
4. **Add your Groq API key**  
   Create a file named `.env` with: `GROQ_API_KEY=your_key_here` (no quotes, no spaces)
5. **Run the app**  
   `streamlit run app.py`

### 📁 Project File Structure

```
Document_QA_ChatBot/
├── app.py                 # Main application
├── .env                   # API key (ignored by git)
├── requirements.txt       # Dependencies
└── README.md              # This file

```

---

Made with ☕ and Python for developers who just want things to work.
