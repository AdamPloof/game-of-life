import tkinter as tk
from tkinter import ttk
from tkinter import N, W, S, E, SUNKEN, HORIZONTAL, VERTICAL
import numpy as np
import json

from board import Board

class UserInterface:
    BG_COLOR = '#edf2fa'
    GRID_COLOR = '#757678'
    LIVE_CELL_COLOR = '#2b7dff'

    def __init__(self, engine, dimensions: tuple) -> None:
        self.engine = engine
        self.root: tk.Tk = self.init_tk()
        self.running: bool = False
        self.refresh_rate = 400 # in ms
        self.zoom = tk.DoubleVar()
        self.zoom.set(1.0)
        self.last_zoom = 1.0

        self.build_ui(dimensions)

    def init_tk(self) -> tk.Tk:
        root = tk.Tk()
        # root.resizable(width=False, height=False)
        root.title('Game of Life')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        return root

    def build_ui(self, dimensions: tuple):
        mainframe = ttk.Frame(self.root, padding='12 12 12 24')
        mainframe.grid(column=0, row=0, sticky=''.join((N, W, E, S)))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        board_frame = ttk.Frame(mainframe, borderwidth=2, relief=SUNKEN)
        board_frame.grid(column=0, row=0, sticky=''.join((N, W, E, S)))
        board_frame.columnconfigure(0, weight=1)
        board_frame.rowconfigure(0, weight=1)

        board_props = {
            'is_running': self.is_running,
            'add_live_cell': self.add_live_cell,
            'remove_live_cell': self.remove_live_cell
        }
        self.board = Board(board_frame, dimensions, board_props)
        self.board.grid(column=0, row=0, sticky=''.join((N, W, E, S)))

        self.attach_scrollbars(mainframe)

        controls_frame = ttk.Frame(mainframe, padding=(25, 20))
        controls_frame.grid(column=0, row=2, sticky=''.join((S, W, E)))
        for i in range(5):
            controls_frame.columnconfigure(i, weight=1)
            controls_frame.rowconfigure(i, weight=1)

        self.activate_btn_text = tk.StringVar()
        self.activate_btn_text.set('Start')
        self.activate_btn = ttk.Button(controls_frame, textvariable=self.activate_btn_text, command=self.toggle_running)
        self.activate_btn.grid(column=1, row=0)

        self.next_btn = ttk.Button(controls_frame, text='Next', command=self.next_action)
        self.next_btn.grid(column=2, row=0)

        self.reset_btn_text = tk.StringVar()
        self.reset_btn_text.set('Clear')
        self.reset_btn = ttk.Button(controls_frame, textvariable=self.reset_btn_text, command=self.reset_or_clear)
        self.reset_btn.grid(column=3, row=0)

        self.attach_zoom(controls_frame)

    def draw_board(self, e):
        if self.board.ready():
            self.board.init_cells()
            self.board.set_live_cells(self.engine.live_cells)
            self.root.unbind('<Configure>')

    def attach_scrollbars(self, parent):
        self.scrollx = ttk.Scrollbar(parent, orient=HORIZONTAL, command=self.board.xview)
        self.scrollx.grid(column=0, row=1, sticky=''.join((W, E)))
        self.board['xscrollcommand'] = self.scrollx.set

        self.scrolly = ttk.Scrollbar(parent, orient=VERTICAL, command=self.board.yview)
        self.scrolly.grid(column=1, row=0, sticky=''.join((N, S)))
        self.board['yscrollcommand'] = self.scrolly.set

    def attach_zoom(self, parent):
        self.zoom_ctrl = ttk.Scale(
            parent,
            orient=HORIZONTAL,
            length=200,
            from_=-4.0,
            to=20.0,
            variable=self.zoom,
            command=self.zoom_board
        )
        self.zoom_ctrl.grid(column=1, row=1, columnspan=3, sticky=''.join((W, E)), padx=25, pady=25)

    def zoom_board(self, e):
        zoom = self.zoom.get()
        delta = zoom - self.last_zoom
        f = 1.1 ** delta
        self.board.zoom(f)
        self.last_zoom = zoom

    def reset_or_clear(self):
        if self.running:
            return
        
        if self.engine.is_first_gen and not self.engine.is_extinct():
            self.engine.clear()
            self.reset_btn_text.set('Reset')
        else:
            self.engine.reset()
            self.reset_btn_text.set('Clear')

        self.board.set_live_cells(self.engine.live_cells)
        
    def next_action(self):
        if self.running:
            return
        
        self.reset_btn_text.set('Reset')
        self.update(True)

    def toggle_running(self):
        self.reset_btn_text.set('Reset')

        if self.running:
            self.running = False
            self.board.show_active_cell(True)
            self.activate_btn_text.set('Start')
            self.next_btn.state(['!disabled'])
            self.reset_btn.state(['!disabled'])
        else:
            self.running = True
            self.board.show_active_cell(False)
            self.activate_btn_text.set('Stop')
            self.next_btn.state(['disabled'])
            self.reset_btn.state(['disabled'])
            self.update()

    def add_live_cell(self, cell_idx: tuple):
        self.engine.add_live_cell(cell_idx)
        self.board.set_live_cells(self.engine.live_cells)

    def remove_live_cell(self, cell_idx: tuple):
        self.engine.remove_live_cell(cell_idx)
        self.board.set_live_cells(self.engine.live_cells)

    def is_running(self):
        return self.running

    def update(self, force_update=False):
        if not self.running and not force_update:
            return

        next_gen = self.engine.get_next_gen()
        self.board.set_live_cells(next_gen)

        if self.running:
            self.board.after(self.refresh_rate, self.update)

    def run(self):
        self.root.bind('<Configure>', self.draw_board)
        self.root.mainloop()

    
def main():
    from gol import GameOfLife

    with open('./starting_positions/135-degree MWSS-to-G.json') as start_f:
        start_pos = json.load(start_f)

    starting_cells = np.asarray([(cell[0], cell[1]) for cell in start_pos])
    dimensions = (100, 100)
    game = GameOfLife(dimensions, starting_cells)

    dimensions = (100, 100)
    ui = UserInterface(game, dimensions)
    ui.run()

if __name__ == "__main__":
    main()
