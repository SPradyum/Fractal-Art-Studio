import tkinter as tk
from tkinter import ttk
import math
import random

# ----------------- Fractal Drawing Functions ----------------- #

def draw_tree(canvas, x, y, length, angle_deg, depth, color):
    """Recursive binary tree."""
    if depth <= 0 or length < 2:
        return

    angle_rad = math.radians(angle_deg)
    x2 = x + length * math.cos(angle_rad)
    y2 = y - length * math.sin(angle_rad)

    width = max(1, int(2 * depth / 3))
    canvas.create_line(x, y, x2, y2, fill=color, width=width, capstyle=tk.ROUND)

    # Left and right branches
    draw_tree(canvas, x2, y2, length * 0.7, angle_deg + 20, depth - 1, color)
    draw_tree(canvas, x2, y2, length * 0.7, angle_deg - 20, depth - 1, color)


def draw_spiral(canvas, cx, cy, radius, depth, color):
    """Spiral made from arcs."""
    if depth <= 0 or radius < 3:
        return

    steps = 40
    angle_range = math.pi / 2  # quarter circle

    prev_x = cx + radius
    prev_y = cy

    for i in range(1, steps + 1):
        t = i / steps
        a = t * angle_range
        x = cx + radius * math.cos(a)
        y = cy + radius * math.sin(a)
        canvas.create_line(prev_x, prev_y, x, y, fill=color, width=2)
        prev_x, prev_y = x, y

    draw_spiral(canvas, cx, cy, radius * 0.75, depth - 1, color)


def koch_segment(canvas, x1, y1, x2, y2, depth, color):
    """Single segment of a Koch curve."""
    if depth == 0:
        canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
        return

    dx = (x2 - x1) / 3
    dy = (y2 - y1) / 3

    xA, yA = x1, y1
    xB, yB = x1 + dx, y1 + dy
    xD, yD = x1 + 2 * dx, y1 + 2 * dy
    xE, yE = x2, y2

    # Peak point
    angle = math.atan2(yD - yB, xD - xB) - math.pi / 3
    length = math.sqrt(dx * dx + dy * dy)
    xC = xB + length * math.cos(angle)
    yC = yB + length * math.sin(angle)

    koch_segment(canvas, xA, yA, xB, yB, depth - 1, color)
    koch_segment(canvas, xB, yB, xC, yC, depth - 1, color)
    koch_segment(canvas, xC, yC, xD, yD, depth - 1, color)
    koch_segment(canvas, xD, yD, xE, yE, depth - 1, color)


def draw_koch_snowflake(canvas, cx, cy, size, depth, color):
    """Koch snowflake centered at (cx, cy)."""
    h = size * math.sqrt(3) / 2

    x1, y1 = cx - size / 2, cy + h / 3
    x2, y2 = cx + size / 2, cy + h / 3
    x3, y3 = cx, cy - 2 * h / 3

    koch_segment(canvas, x1, y1, x2, y2, depth, color)
    koch_segment(canvas, x2, y2, x3, y3, depth, color)
    koch_segment(canvas, x3, y3, x1, y1, depth, color)


def draw_fern(canvas, x, y, length, angle_deg, depth, color):
    """Simple fern-like fractal."""
    if depth <= 0 or length < 2:
        return

    angle_rad = math.radians(angle_deg)
    x2 = x + length * math.cos(angle_rad)
    y2 = y - length * math.sin(angle_rad)

    width = max(1, depth // 2)
    canvas.create_line(x, y, x2, y2, fill=color, width=width)

    # main stem
    draw_fern(canvas, x2, y2, length * 0.8, angle_deg, depth - 1, color)
    # side leaves
    draw_fern(canvas, x2, y2, length * 0.4, angle_deg + 30, depth - 1, color)
    draw_fern(canvas, x2, y2, length * 0.4, angle_deg - 30, depth - 1, color)


# ----------------- Fractal Art Studio Class ----------------- #

class FractalArtStudio:
    def __init__(self, root):
        self.root = root
        root.title("Fractal Art Studio – Click to Paint")

        # Layout frames
        self.control_frame = tk.Frame(root, bg="#202020")
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas = tk.Canvas(root, bg="black", width=900, height=700)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.current_color = "#00ffcc"

        self._build_controls()

        # Bind mouse click on canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def _build_controls(self):
        f = self.control_frame

        title = tk.Label(f, text="Fractal Art Studio", fg="white",
                         bg="#202020", font=("Segoe UI", 16, "bold"))
        title.pack(pady=(10, 15))

        # Fractal type
        tk.Label(f, text="Fractal Type:", fg="white", bg="#202020")\
            .pack(anchor="w", padx=10)
        self.fractal_var = tk.StringVar(value="Tree")
        type_box = ttk.Combobox(
            f, textvariable=self.fractal_var,
            values=["Tree", "Spiral", "Koch Snowflake", "Fern"],
            state="readonly"
        )
        type_box.pack(fill="x", padx=10, pady=5)

        # Depth slider
        tk.Label(f, text="Depth:", fg="white", bg="#202020")\
            .pack(anchor="w", padx=10)
        self.depth_scale = tk.Scale(f, from_=1, to=9, orient="horizontal",
                                    bg="#202020", fg="white",
                                    troughcolor="#404040", highlightthickness=0)
        self.depth_scale.set(6)
        self.depth_scale.pack(fill="x", padx=10, pady=5)

        # Size slider
        tk.Label(f, text="Size:", fg="white", bg="#202020")\
            .pack(anchor="w", padx=10)
        self.size_scale = tk.Scale(f, from_=40, to=220, orient="horizontal",
                                   bg="#202020", fg="white",
                                   troughcolor="#404040", highlightthickness=0)
        self.size_scale.set(120)
        self.size_scale.pack(fill="x", padx=10, pady=5)

        # Color palette buttons
        tk.Label(f, text="Color Palette:", fg="white", bg="#202020")\
            .pack(anchor="w", padx=10, pady=(10, 0))

        palette_frame = tk.Frame(f, bg="#202020")
        palette_frame.pack(padx=10, pady=5, anchor="w")

        colors = ["#00ffcc", "#ff0066", "#00ff00", "#ffaa00", "#66aaff", "#ffffff"]
        for c in colors:
            btn = tk.Button(palette_frame, bg=c, width=2, relief=tk.FLAT,
                            command=lambda col=c: self.set_color(col))
            btn.pack(side=tk.LEFT, padx=3, pady=3)

        # Clear button
        tk.Button(f, text="Clear Canvas", command=self.clear_canvas)\
            .pack(fill="x", padx=10, pady=(20, 5))

        # Hint label
        hint = tk.Label(
            f,
            text="Click anywhere\non the black canvas\nto paint a fractal ✨",
            fg="lightgray", bg="#202020", justify="left"
        )
        hint.pack(anchor="w", padx=10, pady=10)

    def set_color(self, color):
        self.current_color = color

    def clear_canvas(self):
        self.canvas.delete("all")

    # ------------- Event: Canvas Click ------------- #

    def on_canvas_click(self, event):
        fractal = self.fractal_var.get()
        depth = self.depth_scale.get()
        size = self.size_scale.get()
        color = self.current_color

        x, y = event.x, event.y

        if fractal == "Tree":
            # Tree grows upwards
            draw_tree(self.canvas, x, y, size, -90, depth, color)

        elif fractal == "Spiral":
            draw_spiral(self.canvas, x, y, size, depth, color)

        elif fractal == "Koch Snowflake":
            draw_koch_snowflake(self.canvas, x, y, size, depth, color)

        elif fractal == "Fern":
            draw_fern(self.canvas, x, y, size, -90, depth, color)


# ----------------- Run App ----------------- #

if __name__ == "__main__":
    root = tk.Tk()
    app = FractalArtStudio(root)
    root.mainloop()
