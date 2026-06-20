import copy
import tkinter as tk

from rules import compute_attacks, in_bounds

BOARD_SIZE = 8
SQUARE = 80

LIGHT = "#FFFFFF"
DARK = "#B58863"
CHECK_RED = "#FF4C4C"

GREEN_SHADES = [
    "#E6FFE6", "#B8EDB8", "#78DC78", "#2EBA2E",
]

ORANGE_SHADES = [
    "#FFF0DC", "#FFC88C", "#FF9A42", "#DC6400",
]

PIECES = {
    "K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♟",
}


class ChessBoard:
    def __init__(self, root, board):
        self.root = root
        self.board = board
        self.initial_board = copy.deepcopy(board)

        self.canvas = tk.Canvas(root, width=BOARD_SIZE * SQUARE, height=BOARD_SIZE * SQUARE)
        self.canvas.pack(side=tk.LEFT)

        panel = tk.Frame(root)
        panel.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.highlight_on = tk.BooleanVar(value=False)

        tk.Checkbutton(
            panel,
            text="Highlight Squares",
            variable=self.highlight_on,
            command=self.draw,
        ).pack(anchor="w", pady=10)

        tk.Button(
            panel,
            text="Reset Board",
            command=self.reset_board,
        ).pack(anchor="w", pady=6)

        tk.Label(
            panel,
            text="Green = White attack\nOrange = Black attack",
        ).pack(anchor="w")

        self.drag_piece = None
        self.drag_from = None

        self.canvas.bind("<Button-1>", self.mouse_down)
        self.canvas.bind("<B1-Motion>", self.mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up)

        self.draw()

    def reset_board(self):
        self.board[:] = [row[:] for row in self.initial_board]
        self.drag_piece = None
        self.drag_from = None
        self.draw()

    def mouse_down(self, event):
        r, c = event.y // SQUARE, event.x // SQUARE
        if not in_bounds(r, c):
            return

        self.drag_piece = self.board[r][c]
        if self.drag_piece:
            self.drag_from = (r, c)
            self.board[r][c] = ""

    def mouse_move(self, event):
        self.draw()
        if self.drag_piece:
            self.canvas.create_text(
                event.x,
                event.y,
                text=PIECES[self.drag_piece],
                font=("Arial", 36),
            )

    def mouse_up(self, event):
        r, c = event.y // SQUARE, event.x // SQUARE

        if self.drag_piece:
            if in_bounds(r, c):
                self.board[r][c] = self.drag_piece
            elif self.drag_from:
                fr, fc = self.drag_from
                self.board[fr][fc] = self.drag_piece

        self.drag_piece = None
        self.drag_from = None
        self.draw()

    def find_kings(self):
        wk = bk = None
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == "K":
                    wk = (r, c)
                elif self.board[r][c] == "k":
                    bk = (r, c)
        return wk, bk

    def shade(self, count, palette):
        if count <= 0:
            return None
        return palette[min(count, 4) - 1]

    def draw(self):
        self.canvas.delete("all")

        white_att, black_att = compute_attacks(self.board)
        wking, bking = self.find_kings()

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                color = LIGHT if (r + c) % 2 == 0 else DARK

                if self.highlight_on.get():
                    w = white_att[r][c]
                    b = black_att[r][c]
                    diff = w - b

                    if diff > 0:
                        color = self.shade(diff, GREEN_SHADES)
                    elif diff < 0:
                        color = self.shade(-diff, ORANGE_SHADES)

                if wking == (r, c) and black_att[r][c] > 0:
                    color = CHECK_RED
                if bking == (r, c) and white_att[r][c] > 0:
                    color = CHECK_RED

                self.canvas.create_rectangle(
                    c * SQUARE,
                    r * SQUARE,
                    (c + 1) * SQUARE,
                    (r + 1) * SQUARE,
                    fill=color,
                    outline="black",
                )

                p = self.board[r][c]
                if p:
                    self.canvas.create_text(
                        c * SQUARE + SQUARE // 2,
                        r * SQUARE + SQUARE // 2,
                        text=PIECES[p],
                        font=("Arial", 36),
                    )
