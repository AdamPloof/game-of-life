import tkinter as tk
from tkinter import Canvas
from tkinter import ttk
from tkinter import N, W, S, E
import numpy as np

class Board(Canvas):
    BOARD_SIZE = 700
    BG_COLOR = '#edf2fa'
    GRID_COLOR = '#757678'
    LIVE_CELL_COLOR = '#2b7dff'
    LIVE_TAG = 'alive'
    DEAD_TAG = 'dead'

    def __init__(self, parent: ttk.Frame, cell_dim: tuple, **kwargs) -> None:
        self.cell_dim: tuple = cell_dim
        self.cells = []

        kwargs['height'] = self.BOARD_SIZE
        kwargs['width'] = self.BOARD_SIZE
        kwargs['background'] = self.BG_COLOR
        kwargs['borderwidth'] = 0
        kwargs['highlightthickness'] = 0

        super().__init__(parent, **kwargs)
        self.grid(column=0, row=0, sticky=''.join((N, W, E)))

    # Return True on successfully drawing the grid, False otherwise.
    # The reason this may return false is because the canvas hasn't been rendered yet and
    # doesn't have an actual size which we need to calculate where to put the grid lines.
    def draw_board(self) -> bool:
        computed_w = self.winfo_width()
        computed_h = self.winfo_height()

        if computed_w == 1 or computed_h == 1:
            return False
        
        cell_width = round(computed_w / self.cell_dim[0])
        cell_height = round(computed_h / self.cell_dim[1])

        x = 0
        while x < self.cell_dim[0]:
            if x == 0:
                x += 1
                continue

            x_coord = (cell_width * x)
            self.create_line(
                [(x_coord, 0), (x_coord, computed_w)],
                fill=self.GRID_COLOR,
                width=1
            )
            x += 1

        y = 0
        while y < self.cell_dim[0]:
            if y == 0:
                y += 1
                continue

            y_coord = (cell_height * y)
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
    
    def init_cells(self) -> None:
        computed_w = self.winfo_width()
        computed_h = self.winfo_height()
        cell_width = round(computed_w / self.cell_dim[0])
        cell_height = round(computed_h / self.cell_dim[1])

        for x in range(self.cell_dim[0]):
            # Subtract 1 pixel from each dimension for the grid lines
            cell_x1 = (x * cell_width) + 1
            cell_x2 = ((x * cell_width) + cell_width) - 1

            cell_row = []
            for y in range(self.cell_dim[1]):
                cell_y1 = (y * cell_height) + 1
                cell_y2 = ((y * cell_height) + cell_height) - 1
                cell = self.add_cell((cell_x1, cell_y1, cell_x2, cell_y2))
                cell_row.append(cell)
            
            self.cells.append(cell_row)

    def add_cell(self, coords: tuple) -> int:
        # TODO: Remove the pink fill once we've got the living and dying thing going on.
        cell = self.create_rectangle(*coords, width=0, fill='pink', tags=self.DEAD_TAG)
        return cell
    
    def cell_live(self, cell_idx: tuple):
        pass

    def cell_die(self, cell_idx: tuple):
        pass
