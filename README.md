# InsightAI

InsightAI is a high-performance, citation-aware Retrieval-Augmented Generation (RAG) platform designed for semantic search and conversational QA over research papers and documents. It enables users to upload PDF documents, automatically index their content into a vector database, and chat with them using modern Large Language Models (LLMs) with precise source citations.

---

## 🚀 Key Features

* **PDF Document Processing**: Extracts, cleans, and pre-processes PDF text, filtering out OCR noise and bibliography garbage.
* **Vector Search Database**: Generates high-quality semantic embeddings using SentenceTransformers (`all-MiniLM-L6-v2`) and indexes them in a persistent ChromaDB database.
* **Conversational Query Rewriting**: Utilizes a Groq LLM (`llama-3.3-70b-versatile`) to resolve pronouns and context, rewriting follow-up queries into complete standalone questions.
* **Citation-Aware Answers**: Generates detailed, structured answers referencing specific documents and page numbers.
* **Interactive Dashboard**: Modern glassmorphic web interface containing a document manager and stateful chat room with smooth micro-animations.

---

## 🛠️ Technology Stack

| Component | Technology Used |
| :--- | :--- |
| **Frontend** | React (v19), Vite, TypeScript, Tailwind CSS (v4), Lucide React |
| **Backend** | FastAPI, Python (v3.10+), ChromaDB, SentenceTransformers, pdfplumber, Groq SDK |
| **Orchestration** | Docker, Docker Compose |

---

## 📂 Repository Structure

```
InsightAI/
├── docker-compose.yml       # Docker Compose setup for both services
├── backend/                 # FastAPI RAG API service
│   ├── main.py              # API entry point & CORS configuration
│   ├── api/routes/          # API endpoints (document upload, listing, deletion, QA chat)
│   ├── models/schemas.py    # Pydantic data schemas
│   ├── services/            # PDF extracting & text cleaning helpers
│   ├── rag/                 # RAG pipeline implementation (chunker, embedder, retriever, rewriter, generator)
│   └── requirements.txt     # Python requirements
└── frontend/                # React Vite TypeScript frontend client
    ├── src/App.tsx          # Application layout
    ├── src/components/      # UI components (ChatInterface, DocumentManager, Header)
    └── src/hooks/useAPI.ts  # HTTP client integrations
```

---

## 🏁 Quick Start with Docker

The fastest way to spin up the entire application (both frontend and backend) is using Docker Compose.

### **1. Set up Environment Variables**
Create a `.env` file in the root directory or inside the `backend/` folder and include your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### **2. Launch Container Services**
Run the following command in the repository root directory:
```bash
docker compose up --build
```

* **Frontend Web App**: Access via [http://localhost:80](http://localhost:80)
* **Backend API Docs**: Access via [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔧 Local Development

If you prefer to run the components independently for development, please refer to the respective manuals:
* **Backend Instructions**: Read the [Backend README](file:///c:/Users/hemas/OneDrive/Desktop/InsightAI/backend/README.md).
* **Frontend Instructions**: Read the [Frontend README](file:///c:/Users/hemas/OneDrive/Desktop/InsightAI/frontend/README.md).
