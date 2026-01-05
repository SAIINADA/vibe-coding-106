import cv2, pytesseract, re

def image_to_text(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return re.sub(r"\s+", " ", text).strip()
