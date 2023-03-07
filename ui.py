from tkinter import *
from tkinter import ttk

class GameOfLifeUI:
    BG_COLOR = '#edf2fa'
    GRID_COLOR = '#757678'
    LIVE_CELL_COLOR = '#2b7dff'

    def __init__(self) -> None:
        self.root: Tk = self.init_tk()
        self.build_ui()

    def init_tk(self) -> Tk:
        root = Tk()
        root.resizable(width=False, height=False)
        root.title('Game of Life')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        return root

    def build_ui(self):
        mainframe = ttk.Frame(self.root, padding='12 12 12 24')
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(1, weight=1)
        mainframe.rowconfigure(1, weight=1)

        # TODO: manage canvas as separate class?
        self.canvas = Canvas(mainframe, height=700, width=700, background=self.BG_COLOR, borderwidth=2, relief=SUNKEN)
        self.canvas.grid(column=0, row=0, sticky=(N, W, E))
        self.root.bind('<Configure>', lambda e: print((self.canvas.winfo_width(), self.canvas.winfo_height())))

        controls_frame = ttk.Frame(mainframe, padding=(25, 20))
        controls_frame.grid(column=0, row=1, sticky=(S, W, E))
        for i in range(5):
            controls_frame.columnconfigure(i, weight=1)
            controls_frame.rowconfigure(i, weight=1)

        self.activate_btn_text = StringVar()
        self.activate_btn_text.set('Start')
        activate_btn = ttk.Button(controls_frame, textvariable=self.activate_btn_text)
        activate_btn.grid(column=1, row=0)

        self.reset_btn_text = StringVar()
        self.reset_btn_text.set('Clear')
        next_btn = ttk.Button(controls_frame, text='Next')
        next_btn.grid(column=2, row=0)

        reset_btn = ttk.Button(controls_frame, textvariable=self.reset_btn_text)
        reset_btn.grid(column=3, row=0)

    def run(self):
        self.root.mainloop()

    
def main():
    ui = GameOfLifeUI()
    ui.run()

if __name__ == "__main__":
    main()
