import copy
import tkinter as tk

from rules import compute_attacks, in_bounds

BOARD_SIZE = 8
SQUARE = 80
PANEL_WIDTH = 320

LIGHT = "#FFFFFF"
DARK = "#B58863"
CHECK_RED = "#FF4C4C"

GREEN_SHADES = [
    "#C0EFC0", "#9BE09B", "#5CCD5C", "#2EBA2E",
]

ORANGE_SHADES = [
    "#FFB66E", "#FF9A42", "#F07F1F", "#DC6400",
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

        panel = tk.Frame(root, width=PANEL_WIDTH)
        panel.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        panel.pack_propagate(False)

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
            justify="left",
            wraplength=PANEL_WIDTH - 20,
        ).pack(anchor="w")

        self.coverage_summary_label = tk.Label(panel, text="", justify="left", wraplength=PANEL_WIDTH - 20)
        self.coverage_summary_label.pack(anchor="w", pady=(10, 0))

        self.hover_info_label = tk.Label(
            panel,
            text="Hover a square for details",
            justify="left",
            wraplength=PANEL_WIDTH - 20,
        )
        self.hover_info_label.pack(anchor="w", pady=(6, 0))

        self.drag_piece = None
        self.drag_from = None
        self.last_white_att = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.last_black_att = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        self.canvas.bind("<Button-1>", self.mouse_down)
        self.canvas.bind("<B1-Motion>", self.mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up)
        self.canvas.bind("<Motion>", self.mouse_hover)

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

    def mouse_hover(self, event):
        r, c = event.y // SQUARE, event.x // SQUARE
        if not in_bounds(r, c):
            self.hover_info_label.config(text="Hover a square for details")
            return

        w = self.last_white_att[r][c]
        b = self.last_black_att[r][c]
        diff = w - b

        if diff > 0:
            owner = "White"
        elif diff < 0:
            owner = "Black"
        elif w == 0 and b == 0:
            owner = "Unowned"
        else:
            owner = "Contested"

        self.hover_info_label.config(
            text=f"Square {chr(ord('a') + c)}{8 - r} | Coverage W:{w} B:{b} | Owner: {owner}"
        )

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
        self.last_white_att = white_att
        self.last_black_att = black_att

        white_covered = sum(1 for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if white_att[r][c] > 0)
        black_covered = sum(1 for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if black_att[r][c] > 0)
        self.coverage_summary_label.config(
            text=f"Covered squares\nWhite: {white_covered} / 64\nBlack: {black_covered} / 64"
        )

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
