import numpy as np

live_cells = {
    1: (0, 0),
    12: (3, 2),
    53: (1, 1),
    42: (4, 3),
}

cells = [
    (0, 0),
    (1, 4),
    (9, 0)
]

for k, c in live_cells.items():
    print(f'checking: {k}')

    if c in cells:
        print(f'still alive: {k}')
