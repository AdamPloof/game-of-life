import numpy as np
import time
import json
from ui import UserInterface
from p_timer import p_timer

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

    def add_live_cell(self, idx: tuple) -> None:
        self.cells[*idx] = True
        live_cell = np.array([idx])
        self.live_cells = np.concatenate((self.live_cells, live_cell), axis=0)

        if self.is_first_gen or self.is_extinct():
            self.first_gen = self.live_cells.copy()

    # TODO: Bugfix, if all cells are removed manually, adding a new one results in an error:
    # ValueError: all the input arrays must have same number of dimensions, but the array 
    # at index 0 has 1 dimension(s) and the array at index 1 has 2 dimension(s)
    def remove_live_cell(self, idx: np.ndarray) -> None:
        self.cells[*idx] = False

        # TODO: It's a bit annoying to have to convert the ndarrays to lists
        # in order to remove the dead cell. Figure out a more numpy-y way to do this.
        lc_list: list = self.live_cells.tolist()
        lc_list.remove(idx.tolist())
        self.live_cells = np.array(lc_list)

        if self.is_first_gen or self.is_extinct():
            self.first_gen = self.live_cells.copy()

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

    # @p_timer
    def next_generation(self) -> None:
        next_generation = self.cells.copy()
        for y, x in self.cells_to_check():
            next_generation[y][x] = self.lives((y, x))

        self.cells = next_generation
        self.live_cells = np.argwhere(self.cells)
        self.is_first_gen = False

    def cells_to_check(self) -> list:
        live_cells = [tuple(c) for c in self.live_cells]
        cells_to_check = [*live_cells]
        for cell in live_cells:
            neighbors = self.cell_neighbors(cell)

            for neighbor in neighbors:
                if neighbor not in cells_to_check:
                    cells_to_check.append(neighbor)

        return cells_to_check
    
    def cell_neighbors(self, cell: tuple) -> list:
        possible_neighbors = [
            # Previous row
            (cell[0] - 1, cell[1] - 1),
            (cell[0] - 1, cell[1]),
            (cell[0] - 1, cell[1] + 1),
            # Same row
            (cell[0], cell[1] - 1),
            (cell[0], cell[1] + 1),
            # Next row
            (cell[0] + 1, cell[1] - 1),
            (cell[0] + 1, cell[1]),
            (cell[0] + 1, cell[1] + 1),
        ]
        neighbors = [n for n in possible_neighbors if self.cell_is_valid(n)]

        return neighbors

    def live_neighbor_count(self, cell: tuple) -> int:
        neighbors = self.cell_neighbors(cell)
        neighbor_statuses = [self.cells[n[0], n[1]] for n in neighbors]

        return np.count_nonzero(neighbor_statuses)

    def cell_is_valid(self, cell_idx: tuple):
        if cell_idx[0] < 0 or cell_idx[1] < 0:
            return False
        
        if cell_idx[0] > self.x_bound:
            return False
        
        if cell_idx[1] > self.y_bound:
            return False
        
        return True

    def lives(self, cell_idx: tuple) -> bool:
        live_n_count = self.live_neighbor_count(cell_idx)
        if not self.cells[cell_idx[0], cell_idx[1]]:
            return live_n_count == 3
        
        return live_n_count > 1 and live_n_count < 4
    
    def is_extinct(self) -> bool:
        return self.live_cells.size == 0

def main():
    # with open('./starting_positions/135-degree MWSS-to-G.json') as start_f:
    with open('./starting_positions/simple_oscillator.json') as start_f:
        start_pos = json.load(start_f)

    # TODO: Should probably handle out of bounds errors if any starting cells are outside the board dimensions
    starting_cells = np.asarray([(cell[0], cell[1]) for cell in start_pos])
    dimensions = (250, 250)
    game = GameOfLife(dimensions, starting_cells)
    ui = UserInterface(game, dimensions)
    ui.run()


if __name__ == "__main__":
    main()
