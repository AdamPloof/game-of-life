import numpy as np
import time
import json
from ui import UserInterface

# TODO: hang on to starting postion for resets, provide a clear method.
class GameOfLife:
    def __init__(self, dimensions: tuple, live_cells: np.ndarray) -> None:
        self.cells = np.zeros(dimensions, np.bool_)
        self.live_cells = live_cells
        self.first_gen = live_cells.copy()
        self.x_bound = dimensions[0] - 1
        self.y_bound = dimensions[1] - 1
        self.is_first_gen = True

        for y, x in live_cells:
            self.cells[y][x] = True

    def reset(self) -> np.ndarray:
        self.live_cells = self.first_gen.copy()
        self.cells = np.zeros(self.cells.shape, np.bool_)

        # TODO: there's probably a more numpy-y way to do this.
        for idx in self.live_cells:
            self.cells[idx[0], idx[1]] = True

        self.is_first_gen = True

        return self.live_cells
    
    def clear(self) -> np.ndarray:
        self.cells = np.zeros(self.cells.shape, np.bool_)
        self.live_cells = np.argwhere(self.cells) # Obviously empty.
        self.is_first_gen = True

        return self.live_cells

    def get_next_gen(self) -> np.ndarray:
        self.next_generation()
        return self.live_cells
    
    def next_generation(self) -> None:
        dimensions = self.cells.shape
        # Possible optimization here -- don't copy entire set of cells?
        next_generation = self.cells.copy()
        for y in range(dimensions[0] - 1):
            for x in range(dimensions[1] - 1):
                next_generation[y][x] = self.lives((y, x))

        self.cells = next_generation
        self.live_cells = np.argwhere(self.cells)
        self.is_first_gen = False

    def get_neighbors(self, cell_idx: tuple):
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

    def cell_is_valid(self, cell_idx: tuple):
        if cell_idx[0] < 0 or cell_idx[1] < 0:
            return False
        
        if cell_idx[0] > self.x_bound:
            return False
        
        if cell_idx[1] > self.y_bound:
            return False
        
        return True

    def lives(self, cell_idx: tuple) -> bool:
        neighbors = self.get_neighbors(cell_idx)
        live_n_cnt = np.count_nonzero(neighbors)

        if not self.cells[cell_idx[0], cell_idx[1]]:
            return live_n_cnt == 3
        
        return live_n_cnt > 1 and live_n_cnt < 4
    

def main():
    with open('./starting_positions/135-degree MWSS-to-G.json') as start_f:
        start_pos = json.load(start_f)

    # TODO: Should probably handle out of bounds errors if any starting cells are outside the board dimensions
    starting_cells = np.asarray([(cell[0], cell[1]) for cell in start_pos])
    dimensions = (100, 100)
    game = GameOfLife(dimensions, starting_cells)
    ui = UserInterface(game, dimensions)
    ui.run()

    # while True:
    #     game.next_generation()
    #     time.sleep(.25)

if __name__ == "__main__":
    main()
