from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil
from collections import defaultdict

from preprocess import preprocess
from similarity import semantic_similarity
from highlight import similarity_color, overall_color
from pdf_to_text import extract_with_source
from image_to_text import image_to_text
from ai_text_detector import ai_likelihood
from external_sources import external_similarity

app = FastAPI()

# ---------- PATH SETUP ----------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
REF_DIR = DATA_DIR / "reference_pdfs"
UPLOAD_DIR = DATA_DIR / "uploads"

REF_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

# ---------- LOAD REFERENCE DATA ----------
reference_data = []

def load_references():
    reference_data.clear()
    for pdf in REF_DIR.glob("*.pdf"):
        reference_data.extend(extract_with_source(pdf))

load_references()

# ---------- LOCAL PLAGIARISM ----------
def local_plagiarism(text, uploaded_filename):
    sentences = preprocess(text)
    scores = defaultdict(list)

    for s in sentences:
        for ref in reference_data:
            if ref["file"].lower() == uploaded_filename.lower():
                continue

            sim = float(semantic_similarity(s, ref["sentence"])) * 100

            if sim >= 25:
                scores[(ref["file"], ref["page"])].append(sim)

    sources = []
    for (file, page), vals in scores.items():
        avg = float(round(sum(vals) / len(vals), 2))
        sources.append({
            "file": file,
            "page": int(page),
            "similarity": avg,
            "color": similarity_color(avg)
        })

    local_score = float(round(
        sum(s["similarity"] for s in sources) / max(len(sources), 1),
        2
    ))

    return local_score, sources

# ---------- API ----------
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        upload_path = UPLOAD_DIR / file.filename
        with open(upload_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        ext = upload_path.suffix.lower()

        if ext == ".txt":
            text = upload_path.read_text(errors="ignore")

        elif ext == ".pdf":
            text = " ".join(x["sentence"] for x in extract_with_source(upload_path))

            # add uploaded PDF as future reference
            ref_copy = REF_DIR / file.filename
            if not ref_copy.exists():
                shutil.copy(upload_path, ref_copy)
                load_references()

        elif ext in [".jpg", ".jpeg", ".png"]:
            text = image_to_text(str(upload_path))

        else:
            return {"error": "Unsupported file type"}

        if not text or len(text.strip()) < 20:
            return {
                "report": {
                    "overall_plagiarism": 0.0,
                    "overall_color": "green",
                    "detected_sources": []
                },
                "ai_generated_likelihood": "Low"
            }

        # 🔹 LOCAL CHECK
        local_score, sources = local_plagiarism(text, file.filename)

        # 🔹 EXTERNAL CHECK
        external_score = external_similarity(text)

        # 🔹 AI CHECK
        ai_result = ai_likelihood(text)

        # 🔹 FINAL FUSION
        final_score = max(local_score, external_score)

        if ai_result == "High":
            final_score = min(100.0, final_score + 15)

        final_score = float(round(final_score, 2))

        return {
            "report": {
                "overall_plagiarism": final_score,
                "overall_color": overall_color(final_score),
                "detected_sources": sources
            },
            "ai_generated_likelihood": ai_result,
            "external_similarity": external_score
        }

    except Exception as e:
        return {
            "error": "Backend failed",
            "details": str(e)
        }
