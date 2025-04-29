import tkinter as tk

class RegionSelector:
    """
    Presents a transparent fullscreen overlay,
    lets the user drag to select a region,
    then returns (x, y, width, height).
    """
    def __init__(self, root):
        self.root = root
        self.start_x = self.start_y = 0
        self.rect_id = None
        self.selection = None

    def select_region(self):
        # Create a fullscreen overlay as a transient Toplevel
        overlay = tk.Toplevel(self.root)
        overlay.attributes('-fullscreen', True)
        overlay.attributes('-alpha', 0.25)
        overlay.configure(bg='black')
        overlay.focus_force()

        canvas = tk.Canvas(overlay, cursor='cross')
        canvas.pack(fill='both', expand=True)

        # Mouse events
        canvas.bind('<ButtonPress-1>', lambda e: self._on_press(e, canvas))
        canvas.bind('<B1-Motion>', lambda e: self._on_drag(e, canvas))
        canvas.bind('<ButtonRelease-1>', lambda e: self._on_release(e, canvas, overlay))

        # Block here until overlay.destroy() is called
        overlay.wait_window()
        return self.selection

    def _on_press(self, event, canvas):
        self.start_x, self.start_y = event.x, event.y
        # Remove old rectangle if any
        if self.rect_id:
            canvas.delete(self.rect_id)
        self.rect_id = canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline='red', width=2
        )

    def _on_drag(self, event, canvas):
        # Update rectangle as mouse moves
        canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

    def _on_release(self, event, canvas, overlay):
        end_x, end_y = event.x, event.y
        x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
        x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)
        self.selection = (x1, y1, x2 - x1, y2 - y1)
        overlay.destroy()  # only destroy the overlay, not the root
