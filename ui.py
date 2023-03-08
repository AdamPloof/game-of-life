import tkinter as tk
from tkinter import ttk
from tkinter import N, W, S, E, SUNKEN

from board import Board

class GameOfLifeUI:
    BG_COLOR = '#edf2fa'
    GRID_COLOR = '#757678'
    LIVE_CELL_COLOR = '#2b7dff'

    def __init__(self, dimensions: tuple) -> None:
        self.root: tk.Tk = self.init_tk()
        self.build_ui(dimensions)

    def init_tk(self) -> tk.Tk:
        root = tk.Tk()
        root.resizable(width=False, height=False)
        root.title('Game of Life')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        return root

    def build_ui(self, dimensions: tuple):
        mainframe = ttk.Frame(self.root, padding='12 12 12 24')
        mainframe.grid(column=0, row=0, sticky=''.join((N, W, E, S)))
        mainframe.columnconfigure(1, weight=1)
        mainframe.rowconfigure(1, weight=1)

        board_frame = ttk.Frame(mainframe, borderwidth=2, relief=SUNKEN)
        board_frame.grid(column=0, row=0, sticky=''.join((N, W, E)))
        board_frame.columnconfigure(0, weight=1)
        board_frame.rowconfigure(0, weight=1)
        self.board = Board(board_frame, dimensions)
        self.board.grid(column=0, row=0, sticky=''.join((N, W, E)))
        # self.root.bind('<Configure>', lambda e: print((self.board.winfo_width(), self.board.winfo_height())))

        controls_frame = ttk.Frame(mainframe, padding=(25, 20))
        controls_frame.grid(column=0, row=1, sticky=''.join((S, W, E)))
        for i in range(5):
            controls_frame.columnconfigure(i, weight=1)
            controls_frame.rowconfigure(i, weight=1)

        self.activate_btn_text = tk.StringVar()
        self.activate_btn_text.set('Start')
        activate_btn = ttk.Button(controls_frame, textvariable=self.activate_btn_text)
        activate_btn.grid(column=1, row=0)

        self.reset_btn_text = tk.StringVar()
        self.reset_btn_text.set('Clear')
        next_btn = ttk.Button(controls_frame, text='Next')
        next_btn.grid(column=2, row=0)

        reset_btn = ttk.Button(controls_frame, textvariable=self.reset_btn_text)
        reset_btn.grid(column=3, row=0)

    def draw_board(self, e):
        grid_ready = self.board.draw_board()

        if grid_ready:
            self.board.init_cells()
            self.root.unbind('<Configure>')

    def run(self):
        self.root.bind('<Configure>', self.draw_board)
        self.root.mainloop()

    
def main():
    dimensions = (100, 100)
    ui = GameOfLifeUI(dimensions)
    ui.run()

if __name__ == "__main__":
    main()
