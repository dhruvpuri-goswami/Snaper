import os
import sys
from gui import SnaperApp

def main():
    """
    Start the app and point pytesseract to the correct Tesseract executable.
    """
    # Detect if we're running inside a PyInstaller-built .exe
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__)

    # Build the path to the bundled tesseract
    tesseract_cmd = os.path.join(base_path, 'Tesseract-OCR', 'tesseract.exe')

    app = SnaperApp(tesseract_cmd)
    app.run()

if __name__ == '__main__':
    main()
