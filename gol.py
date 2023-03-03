import numpy as np
import time
from board import Board

class GameOfLife:
    def __init__(self, dimensions: tuple, live_cells: list[tuple]) -> None:
        self.cells = np.zeros(dimensions, np.bool_)
        self.live_cells = live_cells
        self.x_bound = dimensions[0] - 1
        self.y_bound = dimensions[1] - 1

        for y, x in live_cells:
            self.cells[y][x] = True
    
    def next_generation(self) -> None:
        # TODO: probably don't need to enumerat -- just get the dimensions.
        for y_idx, row in enumerate(self.cells):
            for x_idx, cell in enumerate(row):
                self.cells[y_idx][x_idx] = self.lives((y_idx, x_idx))

        self.live_cells = np.argwhere(self.cells)

    def get_neighbors(self, cell_idx: tuple):
        # TODO: Don't wrap indexes
        neighbor_positions = [
            # Previous row
            (cell_idx[0] - 1, cell_idx[1] - 1),
            (cell_idx[0] - 1, cell_idx[1]),
            (cell_idx[0] - 1, cell_idx[1] + 1),
            # Same row
            (cell_idx[0], cell_idx[1] - 1),
            (cell_idx[0], cell_idx[1] + 1),
            # Next row
            (cell_idx[0] + 1, cell_idx[1] - 1),
            (cell_idx[0] + 1, cell_idx[1]),
            (cell_idx[0] + 1, cell_idx[1] + 1),
        ]

        neighbors = []
        for pos in neighbor_positions:
            if self.cell_is_valid(pos):
                neighbors.append(self.cells[pos[0], pos[1]])

        return neighbors

    def cell_is_valid(self, cell_pos: tuple):
        if cell_pos[0] < 0 or cell_pos[1] < 0:
            return False
        
        if cell_pos[0] > self.x_bound:
            return False
        
        if cell_pos[1] > self.y_bound:
            return False
        
        return True

    def lives(self, cell: tuple) -> bool:
        neighbors = self.get_neighbors(cell)
        live_n_cnt = np.count_nonzero(neighbors)

        return live_n_cnt > 1 & live_n_cnt < 4
    

def main():
    starting_cells = [
        (1, 2),
        (1, 3),
        (2, 1),
        (5, 4),
        (6, 4),
        (6, 5),
        (7, 4),
    ]
    dimensions = (9, 9)
    game = GameOfLife(dimensions, starting_cells)
    board = Board(dimensions)
    board.draw_board(game.live_cells)
    board.show_board()

    # while True:
    #     game.next_generation()
    #     board.draw_board(game.live_cells)
    #     board.show_board()
    #     time.sleep(1)

if __name__ == "__main__":
    main()
