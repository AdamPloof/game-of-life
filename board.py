import tkinter as tk
from tkinter import Canvas
from tkinter import ttk
from tkinter import N, W, S, E, SUNKEN
import numpy as np

class Board(Canvas):
    BOARD_SIZE = 700
    BG_COLOR = '#edf2fa'
    BORDER_WIDTH = 2
    GRID_COLOR = '#757678'
    LIVE_CELL_COLOR = '#2b7dff'

    def __init__(self, parent: ttk.Frame, dimensions: tuple, **kwargs) -> None:
        self.dimensions: tuple = dimensions
        kwargs['height'] = self.BOARD_SIZE
        kwargs['width'] = self.BOARD_SIZE
        kwargs['background'] = self.BG_COLOR
        kwargs['borderwidth'] = self.BORDER_WIDTH
        kwargs['relief'] = SUNKEN

        super().__init__(parent, **kwargs)
        self.grid(column=0, row=0, sticky=''.join((N, W, E)))
        self.draw_grid()

    # Return True on successfully drawing the grid, False otherwise.
    # The reason this may return false is because the canvas hasn't been rendered yet and
    # doesn't have an actual size which we need to calculate where to put the grid lines.
    def draw_grid(self) -> bool:
        computed_w = self.winfo_width()
        computed_h = self.winfo_height()

        if computed_w == 1 or computed_h == 1:
            return False
        
        x_cell_width = round(computed_w / self.dimensions[0])
        y_cell_width = round(computed_h / self.dimensions[1])

        x = 0
        while x < self.dimensions[0]:
            if x == 0:
                x += 1
                continue

            x_coord = (x_cell_width * x) + (self.BORDER_WIDTH * 2)
            self.create_line(
                [(x_coord, 0), (x_coord, computed_w)],
                fill=self.GRID_COLOR,
                width=1
            )
            x += 1

        y = 0
        while y < self.dimensions[0]:
            if y == 0:
                y += 1
                continue

            y_coord = (y_cell_width * y) + (self.BORDER_WIDTH * 2)
            self.create_line(
                [(0, y_coord), (computed_w, y_coord)],
                fill=self.GRID_COLOR,
                width=1
            )
            y += 1

        # Drawing outer border lines
        self.create_line([(0, 0), (computed_w, 0)]) # Top
        self.create_line([(0, computed_h), (computed_w, computed_h)]) # Bottom
        self.create_line([(0, 0), (0, computed_h)]) # Left
        self.create_line([(computed_w, 0), (computed_w, computed_h)]) # Right

        return True
