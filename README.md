## RAG Q&A Chatbot 🤖

This project is a Retrieval-Augmented Generation (RAG) based Q&A chatbot built using LangGraph, ChromaDB, and FastAPI.
It leverages vector search for document retrieval, OpenAI models for response generation, and MongoDB for short-term memory storage.

The chatbot is exposed via REST APIs that support both single-response requests and streaming responses.

### 🚀 Features

 - 🔎 RAG with LangGraph – Combines LLM reasoning with vector search.

 - 📂 Chroma Cloud Integration – Persistent vector storage using ChromaDB.

 - 🧠 Short-Term Memory – Powered by MongoDB for conversation persistence.

 - ⚡ FastAPI Endpoints – REST APIs for synchronous and streaming responses.
 
 - 📥 Data Injection Pipeline – Upload and embed PDF files into the vector store for retrieval.

 - 🌐 Upload Endpoint – Secure API for injecting new knowledge into the RAG system.

 - 🔑 Environment Variables – Securely configured via .env file.

### 📂 Project Structure

```bash
├── PDF/                     # Folder containing source PDF files
├── src/                     # Core project source code
│   ├── __init__.py          # Marks the src directory as a package
|   ├── embedding.py         # Data Injection pipeline
│   ├── RAG.py               # LangGraph RAG agent logic
│   ├── router.py            # FastAPI routes for chat & streaming
│   ├── utils.py             # Utility functions (DB, memory, helpers)
├── .env                     # Environment variables (API keys, DB URLs)
├── embedding.ipynb          # Jupyter Notebook for PDF data ingestion & embeddings
├── main.py                  # Entry point to run the FastAPI application
└── requirements.txt         # Python dependencies
```

### ⚙️ Environment Variables

Create a .env file in the root directory and set the following:
```env
CHROMA_API_KEY = your_chroma_api_key
CHROMA_TENANT = your_chroma_tenant
OPENAI_API_KEY = your_openai_api_key
MONGODB_URL = your_mongodb_connection_url
```

### 🛠️ Installation & Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/CodeByFelix/Q-A-RAG-Chatbot-with-Endpoint.git
cd Q-A-RAG-Chatbot-with-Endpoint
```


#### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
```


#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```


#### 4. Run the App

```bash
uvicorn main:app --reload
```

### 📡 API Endpoints

#### 1. Get Chat Response

##### Endpoint:
```http
POST /chat/chat_response
```

##### Request Body:
```json
{
  "message": "What is LangGraph?",
  "thread_id": "1234"
}
```

##### Response:
```json
{
  "message": "LangGraph is a framework for building LLM-powered agents..."
}
```

#### 2. Get Streaming Response

##### Endpoint:
```http
POST /chat/stream_response
```

##### Request Body:
```json
{
  "message": "Explain RAG in detail",
  "thread_id": "1234"
}
```

##### Response:

 - Returns a streaming text/plain response.

#### 3. Upload and Embed PDF

##### Endpoint:
```http
Post /chat/upload
```
##### Request:
```http
 - File -> PDF File only
 ```

 ##### Response:
 200 success:
 ```json
 {
  "status": "Successful",
  "detail": "File sample.pdf Uploaded successfully"
}
```

400 file alrady uploaded
```json
{
  "detail": "File 'sample.pdf' already uploaded"
}
```

400 file type not supported
```json
{
  "detail": "File type not supported {fileName}"
}
```


### 🧩 Tech Stack

 - LangGraph
 – Agent orchestration

 - ChromaDB
 – Vector database (Cloud Deployment)

 - FastAPI
 – API framework

 - MongoDB
 – Persistent memory storage

 - OpenAI
 – LLM for response generation

 