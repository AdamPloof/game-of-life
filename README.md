# Conway's Game of Life in Python & tkinter
Just another implementation of Conway's game of a life. Since I had never done a version of this
before, I thought it'd make a fun weekend project, which it was.

Uses tkinter's Canvas to draw the cells and provide a way to draw in living cells. Probably not the most
optimized implementation you'll find, but it gets the job done pretty decently at small board sizes.

## Possible improvements for the future
It'd be nice to save custom starting positions to replay them later. There's already a starting postiions
directory, so just saving the current position on the board as a JSON file and loading it dynamically
ought to be pretty straightforward.
