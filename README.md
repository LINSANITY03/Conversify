# CONVERSIFY

## Overview
Document Analyzer & Chat is a microservice-oriented application that enables users to upload documents, extract their content, and interact with them through natural language queries.
The core idea is to turn static documents into interactive knowledge sources.

## Features (Planned & In Progress)
- File Upload: Upload documents (PDF, DOCX, TXT, etc.) with secure user association.
- Document Storage: Metadata and file management handled in Django REST Framework.
- Content Extraction: Parse and extract relevant information from uploaded files.
- Language Detection & Translation: Identify document language and translate to English for consistency.
- Conversational Interface: Ask questions about the document in English, with continuous conversation support.
- Multimodal Input (future): Start with text input; expand to audio queries later.
- Download Chat History: Export conversations for offline use.
- Scalable Microservices: Separate services for file management and AI workloads, enabling independent scaling.

## Architecture

### Frontend: 
- Next.js (UI, document selection, chat interface)

### Backend:
- Django REST Framework for authentication, file upload, metadata APIs
- FastAPI for AI endpoints (analysis, embeddings, chat)

### AI/ML: 
- PreTrained HuggingFace Model for document understanding, embeddings, and chat models

### Database: 
- PostgreSQL (metadata + users)
- MongoDB (chat history)
- Vector Database (planned): For semantic search and conversational context retrieval

### Workflow Orchestration: 
n8n for chaining tasks like:

1. File ingestion
2. Document parsing
3. Language detection & translation
4. Embedding & storage
5. Generating responses to user queries

## Roadmap

- ✅ File upload API (Django DRF)
- 🔄 Document storage & metadata association
- 🔲 Content parsing service (FastAPI + PyTorch)
- 🔲 LLM-based chat with documents
- 🔲 Translation & language detection
- 🔲 Continuous conversation with memory (vector DB integration)
- 🔲 Audio input support
- 🔲 Downloadable chat logs

## Why this project?

- Combines traditional file storage with modern AI + orchestration workflows
- Explores PyTorch, FastAPI, Django DRF, vector databases, and n8n in a real-world pipeline
- Shows how microservices + automation tools can work together for scalable AI products