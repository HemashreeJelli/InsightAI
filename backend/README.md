# InsightAI - Backend API Service

This is the backend service for **InsightAI**, a high-performance Retrieval-Augmented Generation (RAG) API built with **FastAPI**, **ChromaDB**, and **Groq LLMs**.

---

## ⚡ Technical Highlights & RAG Pipeline

The backend implements a highly specialized, citation-aware RAG pipeline:
1. **Document Extraction (`services/extractor.py`)**: Uses `pdfplumber` to extract text page-by-page.
2. **Text Preprocessing (`services/preprocessor.py`)**: Cleans extracted text, removing double spacing, control characters, citation garbage patterns (e.g., `(Author et al., Year)`), page numbers, and bibliography/references headers to prevent context dilution.
3. **Smart Chunking (`rag/chunker.py`)**: Splits page text using LangChain's `RecursiveCharacterTextSplitter` (1024-character size, 100-character overlap) and performs quality validation (rejecting extremely short/malformed fragments).
4. **Vector Embedding & Storage (`rag/embedder.py`)**: Creates local embeddings using the `all-MiniLM-L6-v2` SentenceTransformer model and stores them in a persistent `ChromaDB` collection.
5. **Contextual Query Rewriting (`rag/query_rewriter.py`)**: Before querying the vector store, the system feeds current question & conversation history to a Groq LLM (`llama-3.3-70b-versatile`) to rewrite follow-up questions into standalone queries, resolving pronoun ambiguities (e.g., "how does it compare?" -> "how does [Model] compare to [Baseline]?").
6. **Two-Stage Semantic Retrieval (`rag/retriever.py`)**: Performs a semantic lookup to retrieve 15 candidate vector chunks, and then utilizes a Cross-Encoder reranker (`cross-encoder/ms-marco-MiniLM-L-6-v2`) to re-score and select the top 5 most relevant context blocks, stripping out boilerplate noise.
7. **Answer Generation (`rag/generator.py`)**: Generates citation-aligned Markdown responses using Groq with precise instructions to avoid hallucinations.

---

## 🛠️ API Endpoints

### **Documents Router** (`/api/documents`)
* **`POST /upload`**: Uploads a PDF document, verifies the strict 5-document library size limit, processes text, chunks content, and loads vector embeddings.
* **`GET /`**: Lists all uploaded and processed PDF documents.
* **`DELETE /{filename}`**: Deletes a document from server disk and purges its vector embeddings from ChromaDB.

### **Chat Router** (`/api/chat`)
* **`POST /`**: Receives current message, conversation history, and target documents. Performs query rewriting, semantic context retrieval, answers queries, and returns formatted citations.

---

## 🚀 Local Setup & Installation

### **1. Prerequisites**
* Python 3.10 or higher
* Valid Groq API Key

### **2. Setup Virtual Environment**
Navigate to this directory:
```bash
cd backend
```
Create and activate your virtual environment:
```bash
python -m venv venv

# On Windows:
.\venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure Environment**
Create a `.env` file inside the `backend` folder:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### **5. Run Server**
Run the server in hot-reload development mode:
```bash
python main.py
```
The server will boot on **`http://localhost:8000`**. You can explore and test the endpoints visually at **`http://localhost:8000/docs`**.

---

## 🧪 Testing
The backend is equipped with several utility test scripts:
* `test_api.py`: Complete suite of API integration tests.
* `test_chat.py`: Basic validation for the Groq LLM integration.
* `test_conversation.py`: Simulated chat session simulating multiple turns.
* `test_pipeline.py`: Validates the internal embedder, chunker, and retriever pipeline.

To run tests (ensure the server is running or call them directly):
```bash
python test_pipeline.py
```
