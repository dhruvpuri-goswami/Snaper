import pytesseract
from PIL import Image

class OCREngine:
    def __init__(self, tesseract_cmd=None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def image_to_text(self, image: Image.Image) -> str:
        return pytesseract.image_to_string(image)
