import copy
import tkinter as tk
from enum import Enum

from rules import compute_attacks, in_bounds

BOARD_SIZE = 8
SQUARE = 80
PANEL_WIDTH = 320

LIGHT = "#FFFFFF"
DARK = "#B58863"
CHECK_RED = "#FF4C4C"
TIE_YELLOW = "#F2DD4A"

class GreenShade(Enum):
    LEVEL_1 = "#C0EFC0"
    LEVEL_2 = "#9BE09B"
    LEVEL_3 = "#5CCD5C"
    LEVEL_4 = "#2EBA2E"


class OrangeShade(Enum):
    LEVEL_1 = "#FFB66E"
    LEVEL_2 = "#FF9A42"
    LEVEL_3 = "#F07F1F"
    LEVEL_4 = "#DC6400"


class Piece(Enum):
    EMPTY_SQUARE = ("", "")
    WHITE_PAWN = ("P", "♙")
    WHITE_ROOK = ("R", "♖")
    WHITE_KNIGHT = ("N", "♘")
    WHITE_BISHOP = ("B", "♗")
    WHITE_KING = ("K", "♔")
    WHITE_QUEEN = ("Q", "♕")
    BLACK_PAWN = ("p", "♟")
    BLACK_ROOK = ("r", "♜")
    BLACK_KNIGHT = ("n", "♞")
    BLACK_BISHOP = ("b", "♝")
    BLACK_KING = ("k", "♚")
    BLACK_QUEEN = ("q", "♛")

    @property
    def code(self):
        return self.value[0]

    @property
    def glyph(self):
        return self.value[1]

    @classmethod
    def from_code(cls, code):
        for piece in cls:
            if piece.code == code:
                return piece
        return cls.EMPTY_SQUARE


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
            text="Enable Heatmap",
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

        self.help_label = tk.Label(
            panel,
            text=(
                "Help\n"
                "- Drag + drop: move piece\n"
                "- Right click: remove piece\n"
                "- Ctrl+Z: undo last change"
            ),
            justify="left",
            wraplength=PANEL_WIDTH - 20,
        )
        self.help_label.pack(anchor="w", pady=(10, 0))

        self.drag_piece = None
        self.drag_from = None
        self.pending_undo_state = None
        self.history = []
        self.last_white_att = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.last_black_att = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        self.canvas.bind("<Button-1>", self.mouse_down)
        self.canvas.bind("<Button-3>", self.mouse_right_click)
        self.canvas.bind("<B1-Motion>", self.mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up)
        self.canvas.bind("<Motion>", self.mouse_hover)
        self.root.bind_all("<Control-z>", self.undo_shortcut)
        self.root.bind_all("<Control-Z>", self.undo_shortcut)

        self.draw()

    def snapshot_board(self):
        return [row[:] for row in self.board]

    def push_history(self, board_state=None):
        state = self.snapshot_board() if board_state is None else [row[:] for row in board_state]
        self.history.append(state)
        if len(self.history) > 200:
            self.history.pop(0)

    def undo_shortcut(self, _event=None):
        if not self.history:
            return "break"

        previous_state = self.history.pop()
        self.board[:] = [row[:] for row in previous_state]
        self.drag_piece = None
        self.drag_from = None
        self.pending_undo_state = None
        self.draw()
        return "break"

    def reset_board(self):
        if self.board != self.initial_board:
            self.push_history()
        self.board[:] = [row[:] for row in self.initial_board]
        self.drag_piece = None
        self.drag_from = None
        self.pending_undo_state = None
        self.draw()

    def mouse_down(self, event):
        r, c = event.y // SQUARE, event.x // SQUARE
        if not in_bounds(r, c):
            return

        self.drag_piece = self.board[r][c]
        if self.drag_piece:
            self.pending_undo_state = self.snapshot_board()
            self.drag_from = (r, c)
            self.board[r][c] = Piece.EMPTY_SQUARE.code

    def mouse_move(self, event):
        self.draw()
        if self.drag_piece:
            self.canvas.create_text(
                event.x,
                event.y,
                text=Piece.from_code(self.drag_piece).glyph,
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

        if self.pending_undo_state is not None and self.board != self.pending_undo_state:
            self.push_history(self.pending_undo_state)

        self.drag_piece = None
        self.drag_from = None
        self.pending_undo_state = None
        self.draw()

    def mouse_right_click(self, event):
        r, c = event.y // SQUARE, event.x // SQUARE
        if not in_bounds(r, c):
            return

        if self.board[r][c] == Piece.EMPTY_SQUARE.code:
            return

        self.push_history()
        self.board[r][c] = Piece.EMPTY_SQUARE.code
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

    def shade(self, count, palette_enum):
        if count <= 0:
            return None
        return palette_enum[f"LEVEL_{min(count, 4)}"].value

    def draw(self):
        self.canvas.delete("all")

        white_att, black_att = compute_attacks(self.board, Piece.EMPTY_SQUARE.code)
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
                        color = self.shade(diff, GreenShade)
                    elif diff < 0:
                        color = self.shade(-diff, OrangeShade)
                    elif w > 0:
                        color = TIE_YELLOW

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
                    piece = Piece.from_code(p)
                    self.canvas.create_text(
                        c * SQUARE + SQUARE // 2,
                        r * SQUARE + SQUARE // 2,
                        text=piece.glyph,
                        font=("Arial", 36),
                    )
