# Chat with Your Docs

A full-stack AI-powered document QA app where users upload PDFs and ask grounded questions about their content.

## Stack
- Frontend: React + TypeScript (Vite)
- Backend: FastAPI
- Database: PostgreSQL + pgvector
- AI: OpenAI Embeddings + Chat
- Orchestration: LangChain
- Containerization: Docker / Docker Compose

## Project Layout
- `frontend` - React client for uploads, chat, and source display
- `backend` - FastAPI API for ingestion, retrieval, and generation
- `infra` - DB initialization scripts and local infrastructure assets

## Prerequisites
- Docker Desktop (or Docker Engine + Compose plugin)
- (Optional for later commits) OpenAI API key

## Quick Start (Run the Whole App)
1. Copy environment templates:
   - `cp .env.example .env`
   - `cp backend/.env.example backend/.env`
   - `cp frontend/.env.example frontend/.env`
2. Start all services:
   - `docker compose up --build`
3. Open:
   - Frontend: http://localhost:5173
   - Backend docs: http://localhost:8000/docs

