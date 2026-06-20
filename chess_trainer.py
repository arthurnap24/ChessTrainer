import tkinter as tk

from chess_board import BOARD_SIZE, PANEL_WIDTH, SQUARE, ChessBoard


board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]


def main():
    root = tk.Tk()
    root.title("Chess Drag + Heatmap + Check Toggle")
    root.geometry(f"{BOARD_SIZE * SQUARE + PANEL_WIDTH + 20}x{BOARD_SIZE * SQUARE}")
    root.resizable(False, False)

    ChessBoard(root, board)

    root.mainloop()


if __name__ == "__main__":
    main()