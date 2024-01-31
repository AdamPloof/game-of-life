import json
import numpy as np

from game import GameOfLife
from ui import UserInterface

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
