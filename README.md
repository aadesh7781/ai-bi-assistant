An AI-powered Business Intelligence platform that combines SQL analytics with Retrieval-Augmented Generation (RAG) to answer questions from structured databases and unstructured annual reports through a single conversational interface.
Live Demo: https://ai-bi-assistant-bpxg7lvareaihkj89t5esr.streamlit.app/
🚀 Overview

AI Business Intelligence Assistant is a full-stack AI application that enables users to interact with business data using natural language.

Instead of switching between SQL clients, dashboards, and annual reports, users can simply ask questions like:

"What is our total revenue?"
"Describe Spotify's business model."
"Compare our revenue with Spotify's reported revenue."

The assistant intelligently determines whether the question should be answered using:

📊 SQL (PostgreSQL)
📄 Annual Reports (RAG)
🤝 A Hybrid of both
✨ Features
📊 SQL Analytics
Natural language to SQL generation
PostgreSQL execution
Business-friendly explanations
Automatic metric cards
Charts & visualizations
Secure SQL validation

Example:

"Show monthly revenue."

📄 Retrieval-Augmented Generation (RAG)

Searches uploaded Spotify Annual Reports using semantic search.

Supports questions like:

AI strategy
Business model
Financial risks
Shareholders
Revenue information
Podcasts & Audiobooks

Powered by:

Jina Embeddings v3
ChromaDB
Semantic Search
Query Expansion
🤝 Hybrid AI (SQL + RAG)

The assistant can combine:

Internal Business Data

External Annual Reports

into one grounded answer.

Example:

Compare our revenue with Spotify's reported revenue.

The system automatically:

Generates SQL
Retrieves relevant report sections
Combines both sources
Produces a business-focused response
🏗️ System Architecture
                User
                  │
                  ▼
          Streamlit Frontend
                  │
                  ▼
            FastAPI Backend
                  │
          Question Router
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
     SQL Pipeline       RAG Pipeline
        │                   │
        ▼                   ▼
 PostgreSQL          Chroma Vector DB
        │                   │
        └─────────┬─────────┘
                  ▼
          Hybrid Response Engine
                  │
                  ▼
        Business Intelligence Answer
🛠️ Tech Stack
Backend
FastAPI
Python
PostgreSQL
SQLAlchemy
AI
LangChain
Groq LLM
Jina Embeddings v3
ChromaDB
Retrieval-Augmented Generation (RAG)
Frontend
Streamlit
Plotly
Pandas
Deployment
Render
GitHub
📂 Project Structure
AI-BI-Assistant/
│
├── api/
├── agents/
├── rag/
├── database/
├── schemas/
├── documents/
├── chroma_db/
├── frontend/
├── app.py
└── README.md
🧠 AI Workflow
SQL Pipeline

Natural Language

↓

SQL Generation

↓

Validation

↓

PostgreSQL

↓

LLM Explanation

RAG Pipeline

Question

↓

Query Expansion

↓

Embeddings

↓

ChromaDB

↓

Semantic Retrieval

↓

LLM Response

Hybrid Pipeline

Question

↓

Question Decomposition

↓

SQL + RAG

↓

Hybrid Prompt

↓

Business Intelligence Answer

📸 Example Questions
SQL
Total revenue
Monthly revenue
Yearly revenue
Top 10 artists
Top genres
Revenue by country
RAG
What is Spotify's AI strategy?
Describe Spotify's business model.
What financial risks are mentioned?
Who are the major shareholders?
Hybrid
Compare our revenue with Spotify's reported revenue.
Compare our growth with Spotify's reported growth.
⚠️ Deployment Note

This project is hosted on Render's Free Tier.

If the backend has been inactive, the first request may take 30–90 seconds while the server wakes up.

If you encounter a connection error, simply wait a moment and try again.

⚙️ Installation
git clone https://github.com/aadesh7781/AI-BI-Assistant.git

cd AI-BI-Assistant

python -m venv .venv

source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt

Create a .env file:

DATABASE_URL=your_database_url
GROQ_API_KEY=your_groq_api_key
JINA_API_KEY=your_jina_api_key

Run the backend:

uvicorn ai_bi_assistant.api.main:app --reload

Run the frontend:

streamlit run app.py
🎯 Key Highlights
Hybrid AI Architecture (SQL + RAG)
Natural Language to SQL
Retrieval-Augmented Generation
Semantic Search over Annual Reports
Query Routing
Question Decomposition
Hybrid Response Generation
Interactive Business Dashboard
Modern Streamlit Interface
Cloud Deployment with Render
🔮 Future Improvements
Multi-document RAG
PDF Upload Support
Conversation Memory
Authentication & User Management
Role-Based Access Control
Dashboard Export (PDF/Excel)
Streaming Responses
Citation Highlighting
Multi-Database Support

Note: This project is a demonstration of an AI-powered Business Intelligence workflow. The structured analytics are generated from the sample CSV datasets included in the repository, while document-based answers are generated from the Spotify Annual Reports and SEC filings provided in the documents/ folder. This keeps the project fully reproducible without relying on external or live data sources.

👨‍💻 Author

Aadesh Sharma

If you found this project useful, consider giving it a ⭐ on GitHub!
