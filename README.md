# AI Plagiarism Detection System

An AI-based system to detect plagiarism in academic documents with explainable results and AI-generated content analysis.

## Features
- Text, PDF, and image plagiarism detection
- Semantic similarity analysis
- AI-generated content likelihood detection
- Modern Streamlit frontend
- FastAPI backend

## Tech Stack
- FastAPI
- Streamlit
- Sentence Transformers
- OCR (Tesseract)

## How to Run

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
