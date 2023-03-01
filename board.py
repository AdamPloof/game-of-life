from PIL import Image
from PIL import ImageDraw
import cv2 as cv
import numpy as np
import sys


class Board:
    SIDE_SIZE = 800
    BG_COLOR = '#edf2fa'
    GRID_COLOR = '#757678'
    LIVE_CELL_COLOR = '#2b7dff'

    def __init__(self, cells: tuple) -> None:
        self.cells = cells
        self.board = self.draw_board()

    def draw_board(self):
        board = Image.new(
            'RGB', 
            (self.SIDE_SIZE, self.SIDE_SIZE),
            self.BG_COLOR
        )
        self.draw: ImageDraw.ImageDraw = ImageDraw.Draw(board)
        self.draw_grid()

        return board


    def draw_grid(self):
        x_cell_width = round(self.SIDE_SIZE / self.cells[0])
        y_cell_width = round(self.SIDE_SIZE / self.cells[1])

        x = 0
        while x < self.cells[0]:
            if x == 0:
                x += 1
                continue

            x_coord = x_cell_width * x
            self.draw.line(
                [(x_coord, 0), (x_coord, self.SIDE_SIZE)],
                fill=self.GRID_COLOR,
                width=1
            )
            x += 1

        y = 0
        while y < self.cells[0]:
            if y == 0:
                y += 1
                continue

            y_coord = y_cell_width * y
            self.draw.line(
                [(0, y_coord), (self.SIDE_SIZE, y_coord)],
                fill=self.GRID_COLOR,
                width=1
            )
            y += 1

    def draw_live_cells(self, live_cells):
        self.board = self.draw_board()

        x_cell_width = round(self.SIDE_SIZE / self.cells[0])
        y_cell_width = round(self.SIDE_SIZE / self.cells[1])

        for cell in live_cells:
            top_left = (
                cell[0] * x_cell_width + 1,
                cell[1] * y_cell_width + 1,
            )
            bottom_right = (
                cell[0] * x_cell_width + x_cell_width - 1,
                cell[1] * y_cell_width + y_cell_width - 1,
            )
            self.draw.rectangle(
                (top_left, bottom_right),
                fill=self.LIVE_CELL_COLOR
            )

    def show_board(self):
        # TODO: using opencv to show the image for now. Lets put this on a tkinter canvas later
        cv_img = cv.cvtColor(np.array(self.board), cv.COLOR_RGB2BGR)
        cv.imshow('Game of Life', cv_img)

        if cv.waitKey(0) == 27:
            cv.destroyAllWindows()
            sys.exit()
