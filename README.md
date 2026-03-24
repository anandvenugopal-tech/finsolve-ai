# FinSolve AI — RAG Based Role-Specific Insights Chatbot

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38-red)
![LangChain](https://img.shields.io/badge/LangChain-0.3-orange)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5-purple)
![Gemini](https://img.shields.io/badge/Gemini-2.0--flash-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Overview

**FinSolve AI** is a RAG-based (Retrieval Augmented Generation) chatbot built for **FinSolve Technologies**, a fintech company facing data silos and communication delays across departments.

The chatbot enables employees to access **role-specific insights** securely. Each user gets answers only from data their role is permitted to see — enforced through a **Role-Based Access Control (RBAC)** system backed by JWT authentication.

Built as part of the **Codebasics Resume Project Challenge**.

---

## Problem Statement

FinSolve Technologies was facing:

- Delays in communication between departments
- Difficulty accessing the right data at the right time
- Data silos between Finance, Marketing, HR, Engineering, and C-Level teams
- Inefficiencies in decision-making and strategic planning

**Solution:** A secure, department-specific AI chatbot that retrieves answers only from data the user is authorized to access.

---

## Architecture

```
User (Streamlit UI)
        ↓
    Login → JWT Token issued
        ↓
    Ask Question
        ↓
FastAPI Backend
        ↓
RBAC Check → Allowed Collections Identified
        ↓
ChromaDB Vector Search (department-specific)
        ↓
Retrieved Document Chunks (context)
        ↓
Gemini 2.0 Flash → Answer + Source References
        ↓
Response displayed in Streamlit Chat UI
```

---

## Roles and Permissions

| Role | Access |
|---|---|
| `c_level` | Full access to all departments |
| `finance` | Finance reports, budgets, expenses, reimbursements |
| `marketing` | Campaign data, customer feedback, sales metrics |
| `hr` | Employee records, payroll, attendance, performance |
| `engineering` | Architecture docs, dev guidelines, technical specs |
| `employee` | General company policies, FAQs, events only |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Backend API | FastAPI |
| Frontend UI | Streamlit |
| LLM | Google Gemini 2.0 Flash |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Store | ChromaDB |
| RAG Framework | LangChain |
| Authentication | JWT (python-jose) + bcrypt (passlib) |

---

## Project Structure

```
rag-rbac-chatbot/
│
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI app, routes, auth endpoints
│   ├── auth.py          # JWT creation, bcrypt password hashing
│   ├── rbac.py          # Role to collection mapping
│   ├── rag_engine.py    # RAG pipeline (retrieve + augment + generate)
│   └── ingest.py        # Document ingestion into ChromaDB
│
├── frontend/
│   └── app.py           # Streamlit chat UI
│
├── data/
│   ├── finance/         # Financial reports, budgets
│   ├── marketing/       # Campaign data, customer feedback
│   ├── hr/              # Employee data, payroll, attendance
│   ├── engineering/     # Architecture docs, dev guidelines
│   └── general/         # Company policies, FAQs, events
│
├── chroma_db/           # Persisted vector store (auto-created)
├── .env                 # API keys and config (never commit this)
├── .env.example         # Template for environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- Google Gemini API key (free at [aistudio.google.com](https://aistudio.google.com))

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/rag-rbac-chatbot.git
cd rag-rbac-chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SECRET_KEY=your-random-32-character-secret-key
CHROMA_PERSIST_DIR=./chroma_db
```

To generate a SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Add Your Data

Place your documents inside the appropriate department folders:

```
data/finance/     → PDF, CSV, TXT, MD files
data/marketing/   → PDF, CSV, TXT, MD files
data/hr/          → PDF, CSV, TXT, MD files
data/engineering/ → PDF, CSV, TXT, MD files
data/general/     → PDF, CSV, TXT, MD files
```

### 6. Ingest Documents into ChromaDB

```bash
python -m backend.ingest
```

You will see output like:
```
Ingesting: finance     → 12 chunks stored
Ingesting: marketing   → 8 chunks stored
Ingesting: hr          → 15 chunks stored
Ingesting: engineering → 10 chunks stored
Ingesting: general     → 6 chunks stored
```

### 7. Start the Backend

```bash
uvicorn backend.main:app --reload --port 8000
```

### 8. Start the Frontend

Open a new terminal:

```bash
streamlit run frontend/app.py
```

### 9. Open in Browser

```
Frontend: http://localhost:8501
API Docs: http://localhost:8000/docs
```

---

## Test Users

| Username | Password | Role |
|---|---|---|
| tony | tony123 | c_level |
| alice | alice123 | finance |
| bob | bob123 | marketing |
| carol | carol123 | hr |
| dave | dave123 | engineering |
| eve | eve123 | employee |

---

## How It Works

### 1. Authentication
User logs in with username and password. FastAPI verifies credentials using bcrypt and issues a signed JWT token containing the user's role.

### 2. Role-Based Access Control
When a query is made, the system checks the JWT token and maps the role to allowed ChromaDB collections. A finance user only searches the `finance` and `general` collections — never HR or Marketing data.

### 3. RAG Pipeline
- The query is converted to a vector using HuggingFace embeddings
- ChromaDB performs similarity search on allowed collections
- Top relevant document chunks are retrieved
- Chunks are passed as context to Gemini 2.0 Flash
- Gemini generates a grounded answer citing source documents

### 4. Response
The answer is displayed in the Streamlit chat UI along with the source document names so users can verify where the information came from.

---

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/login` | Authenticate and get JWT token | No |
| POST | `/query` | Ask a question, get RAG response | Yes |
| GET | `/me` | Get current user info | Yes |

---

## Environment Variables

| Variable | Description | Where to Get |
|---|---|---|
| `GEMINI_API_KEY` | Google Gemini API key | [aistudio.google.com](https://aistudio.google.com) |
| `SECRET_KEY` | JWT signing secret | Generate yourself |
| `CHROMA_PERSIST_DIR` | ChromaDB storage path | Set to `./chroma_db` |

---

## Key Features

- **Secure Authentication** — JWT tokens with bcrypt password hashing
- **Role-Based Access Control** — 6 roles with department-specific data access
- **RAG Pipeline** — Retrieves from vector store, augments with context, generates grounded answers
- **Source Citations** — Every answer references the source document
- **Multi-format Support** — Reads PDF, CSV, TXT, and Markdown files
- **Department Isolation** — Each department's data stored in separate ChromaDB collections
- **Free LLM** — Uses Google Gemini 2.0 Flash (no paid API needed)

---

## Security Notes

- Passwords are hashed with bcrypt — never stored in plain text
- JWT tokens expire after 60 minutes
- RBAC is enforced at the retrieval layer — users cannot access unauthorized collections even through direct API calls
- `.env` file is gitignored — never commit API keys

---
