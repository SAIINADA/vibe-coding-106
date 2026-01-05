import fitz, cv2, pytesseract, numpy as np, re

def clean(text):
    return re.sub(r"\s+", " ", text).strip()

def ocr_page(page):
    pix = page.get_pixmap(dpi=300)
    img = np.frombuffer(pix.samples, dtype=np.uint8)
    img = img.reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray)

def extract_with_source(pdf_path):
    doc = fitz.open(pdf_path)
    data = []

    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if len(text) < 50:
            text = ocr_page(page)
        text = clean(text)

        for s in text.split("."):
            if len(s.strip()) > 10:
                data.append({
                    "sentence": s.strip(),
                    "file": pdf_path.name,
                    "page": i + 1
                })
    return data
