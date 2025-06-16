"""reusable canvas configuration module"""

import tkinter as tk

def create_canvas(root, width=600, height=500, bg='white', **kwargs):
    """
    Create a canvas with specified dimensions and background color.
    Additional Canvas options can be passed via kwargs.
    """
    canvas = tk.Canvas(root, width=width, height=height, bg=bg, **kwargs)
    canvas.pack()
    return canvas