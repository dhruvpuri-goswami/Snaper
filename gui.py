from __future__ import annotations

import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

import pyautogui
import keyboard
import pyperclip
from PIL import Image, ImageTk

from region_selector import RegionSelector
from ocr_engine import OCREngine

class SnaperApp:
    BASE_DIR = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))
    ICON_PATH = BASE_DIR / "assets" / "capture.png"
    LOGO_PATH = BASE_DIR / "assets" / "snaper.ico"
    ACCENT   = "#ffffff"  # blue‑600
    BG       = "#FFFFFF"  # full white
    PLACE_BG = "#F3F4F6"  # gray‑100
    PLACE_FG = "#6B7280"  # gray‑500

    def __init__(self, tesseract_cmd: str | None = None) -> None:
        
        self.root = tk.Tk()
        self.root.title("Snaper")
        self.root.geometry("420x110")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG)
        self.root.attributes("-topmost", True)

        self._load_icons()
        self._init_styles()

        self.root.iconbitmap(self.LOGO_PATH)
        
        self.ocr_engine = OCREngine(tesseract_cmd)
        self.selector   = RegionSelector(self.root)

        self._build_ui()
        keyboard.add_hotkey("ctrl+shift+t", self.capture_and_ocr)

    def _load_icons(self):
        self.btn_img: ImageTk.PhotoImage | None = None
        if self.ICON_PATH.exists():
            try:
                img = Image.open(self.ICON_PATH)
                self.root.iconphoto(True, ImageTk.PhotoImage(img))
                self.btn_img = ImageTk.PhotoImage(img.resize((20, 20), Image.Resampling.LANCZOS))
            except Exception as exc:
                print(f"[Snaper] Icon load failed – {exc}", file=sys.stderr)
        
        if self.LOGO_PATH.exists():
            try:
                logo_img = Image.open(self.LOGO_PATH)
                self.logo_img = ImageTk.PhotoImage(logo_img)
                self.root.iconphoto(True, self.logo_img)  
            except Exception as exc:
                print(f"[Snaper] Logo icon load failed – {exc}", file=sys.stderr)
                

    def _init_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background=self.BG)

        style.configure(
            "Primary.TButton",
            background=self.ACCENT,
            foreground="black",
            font=("Segoe UI", 10),
            radius=4,
            bordercolor=self.ACCENT,
            borderwidth=0.5,
            padding=(12, 8),
        )
        style.map(
            "Primary.TButton",
            background=[("active", self.PLACE_BG)],
        )

    def _build_ui(self):
        wrapper = ttk.Frame(self.root)
        wrapper.pack(fill="both", expand=True, padx=16, pady=16)

        # row ---------------------------------------------------------------
        row = ttk.Frame(wrapper)
        row.pack(fill="x")

        # Select‑area button
        capture_btn = ttk.Button(
            row,
            text=" Select Area",
            image=self.btn_img,
            compound="left",
            style="Primary.TButton",
            command=self.capture_and_ocr,
        )
        capture_btn.image = self.btn_img
        capture_btn.pack(side="left")

        # Status label
        self.status = ttk.Label(
            wrapper,
            text="Hot-key: Ctrl + Shift + T",
            background=self.BG,
            foreground="#4B5563",  # gray‑600
            font=("Segoe UI", 9),
        )
        self.status.pack(anchor="w", pady=(12, 0))

    def capture_and_ocr(self):
        region = self.selector.select_region()
        if not region:
            return
        try:
            img = pyautogui.screenshot(region=region)
            text = self.ocr_engine.image_to_text(img)
            pyperclip.copy(text)
            self.status.config(text="✔ Text copied to clipboard")
        except Exception as exc:
            messagebox.showerror("Snaper Error", str(exc))
            self.status.config(text="Error – see details")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    SnaperApp().run()