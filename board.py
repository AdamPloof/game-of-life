import tkinter as tk
from tkinter import Canvas
from tkinter import ttk
from tkinter import N, W, S, E, ALL
import numpy as np

from typing import Callable

class Board(Canvas):
    BOARD_SIZE = 700
    BG_COLOR = '#edf2fa'
    GRID_COLOR = '#757678'
    LIVE_CELL_COLOR = '#2b7dff'
    DEAD_CELL_COLOR = '#f6ccda'
    ACTIVE_CELL_COLOR = '#de4e7c'
    CELL_TAG = 'cell'
    LIVE_TAG = 'alive'

    def __init__(self, parent: ttk.Frame, cell_dim: tuple, props: dict, **kwargs) -> None:
        self.cells: np.ndarray = np.zeros(cell_dim, dtype=int)
        self.add_live_cell: Callable = props['add_live_cell']
        self.remove_live_cell: Callable = props['remove_live_cell']
        self.is_running: Callable = props['is_running']
        self.cell_size = 10 # in pixels
        self.cell_dim = cell_dim

        w, h = self.get_board_dimensions()

        kwargs['height'] = self.BOARD_SIZE
        kwargs['width'] = self.BOARD_SIZE
        kwargs['background'] = self.BG_COLOR
        kwargs['borderwidth'] = 0
        kwargs['highlightthickness'] = 0
        kwargs['scrollregion'] = (0, 0, w, h)

        super().__init__(parent, **kwargs)

    def ready(self):
        return self.winfo_width() != 1
    
    def init_cells(self) -> None:
        x = 0
        for x, row in enumerate(self.cells):
            cell_x1 = (x * self.cell_size)
            cell_x2 = ((x * self.cell_size) + self.cell_size)

            y = 0
            for y, cell in enumerate(row):
                cell_y1 = (y * self.cell_size)
                cell_y2 = ((y * self.cell_size) + self.cell_size)
                self.cells[x, y] = self.add_cell((cell_x1, cell_y1, cell_x2, cell_y2))                
                y += 1

            x += 1
        
        # Don't ask my why, but the order that cells are inserted here mirrors the starting position order.
        # So just transpose the cells and call it a day.
        self.cells = self.cells.T

    # TODO: clicking on a live cell should kill it.
    def add_cell(self, coords: tuple) -> int:
        cell = self.create_rectangle(
            *coords,
            width=1,
            fill=self.DEAD_CELL_COLOR,
            activefill=self.ACTIVE_CELL_COLOR,
            tags=self.CELL_TAG,
            outline='black'
        )
        self.tag_bind(cell, "<Button-1>", self.toggle_cell)

        return cell
    
    def toggle_cell(self, e: tk.Event) -> None:
        if self.is_running() == True:
            return

        cell_id = e.widget.find_withtag('current')[0]
        cell_idx = np.argwhere(self.cells == cell_id)

        if self.LIVE_TAG not in self.gettags(cell_id):
            # Cell is dead, bring to life
            self.add_live_cell(cell_idx[0])
        else:
            # Cell is alive, now it dies.
            self.remove_live_cell(cell_idx[0])
        
    def set_live_cells(self, cells: np.ndarray):
        last_gen: tuple = self.find_withtag(self.LIVE_TAG)
        live_cells: dict = {}
        for cell in cells:
            id = self.cell_live(cell)
            live_cells[id] = cell

        died = [id for id in last_gen if id not in live_cells.keys()]
        for died_id in died:
            self.cell_die(died_id)

        self.itemconfigure(self.LIVE_TAG, fill=self.LIVE_CELL_COLOR)

    # return the id of the cell brought to life.
    def cell_live(self, cell_idx: tuple[int, int]) -> int:
        cell_id: int = self.cells[cell_idx[0], cell_idx[1]]
        if self.LIVE_TAG not in self.gettags(cell_id):
            self.addtag(self.LIVE_TAG, 'withtag', cell_id)

        return cell_id

    def cell_die(self, cell_id: int):
        self.dtag(cell_id, self.LIVE_TAG)
        # Note, you can make a cool "Live Cells were here" path by using a different color here.
        self.itemconfigure(cell_id, fill=self.DEAD_CELL_COLOR)

    def show_active_cell(self, show: bool) -> None:
        if show:
            self.itemconfigure(self.CELL_TAG, activefill=self.ACTIVE_CELL_COLOR)
        else:
            self.itemconfigure(self.CELL_TAG, activefill='')

    def get_board_dimensions(self) -> tuple:
        board_width = self.cell_size * self.cell_dim[1]
        board_height = self.cell_size * self.cell_dim[0]

        return (board_width, board_height)

    def zoom(self, factor):
        self.scale(ALL, 0, 0, factor, factor)
        # Recalculate scroll region of board based on scaled size of cells
        cell_bbox = self.bbox(self.cells[0, 0])

        # Subtract 1 pixel from bound box since the box *contains* the element
        self.cell_size = cell_bbox[2] - 1
        w, h = self.get_board_dimensions()
        self.configure(scrollregion=(0, 0 , w, h))
