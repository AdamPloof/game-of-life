# Py Game of Life

## Rules
- A live cell dies if it has fewer than two live neighbors.
- A live cell with two or three live neighbors lives on to the next generation.
- A live cell with more than three live neighbors dies.
- A dead cell will be brought back to live if it has exactly three live neighbors


**Not enough live neighbors; middle cell dies**
|   |   |   |
|   | X |   |
| X |   |   |

**Too many live neighbors; middle cell dies**
| O |   | O |
|   | X |   |
| O | O |   |

**3 live neighbors; middle cells lives**
|   |   | O |
|   | O |   |
| O |   | O |

**3 live neighbors; middles cells becomes live on next round**
|   |   | O |
|   |   |   |
| O |   | O |

### Boundry condition used in this version
Cells outside of boundry area are just considered dead -- no wrapping/toroidal topology.

## Design
To generate the graphics for the game, we'll draw an image to a window and update it on each tick.

The cells will be represented by a two dimensional numpy array.

Each tick, evaluate the state of each cell.

We'll worry about optimization after we've got a basic version working.
