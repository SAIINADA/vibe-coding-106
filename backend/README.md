# Backend – AI Plagiarism Detection System

This directory contains the backend implementation of the AI Plagiarism Detection System built using FastAPI.

## Purpose
The backend handles document ingestion, text extraction, plagiarism analysis, and AI-generated content detection. It exposes REST APIs consumed by the Streamlit frontend.

## Core Responsibilities
- Accept uploaded documents (TXT, PDF, JPG, JPEG, PNG)
- Extract text from PDFs and images (OCR support)
- Clean and preprocess text data
- Perform semantic plagiarism detection against reference documents
- Identify source documents with page-level similarity
- Estimate likelihood of AI-generated content
- Return structured, explainable results

## Main Files
- `main.py` – FastAPI application entry point and API routes
- `preprocess.py` – Text extraction, OCR handling, and preprocessing
- `similarity.py` – Semantic similarity computation using embeddings
- `ai_detector.py` – AI-generated content likelihood analysis
- `utils.py` – Utility and helper functions
- `requirements.txt` – Backend dependencies

## API Endpoint
- `POST /analyze`  
  Upload a document and receive a plagiarism analysis report in JSON format.

## Dependencies
Major libraries used:
- FastAPI
- Uvicorn
- Sentence Transformers
- NLTK
- PyMuPDF
- Tesseract OCR
- NumPy
- Scikit-learn

## Notes
- Tesseract OCR must be installed and available in the system PATH for image and handwritten document support.
- Virtual environments (`venv/`) are intentionally excluded from version control.
- Reference documents should be placed in the `data/` directory.

## Execution
To run the backend server:
```bash
python -m uvicorn main:app --reload

