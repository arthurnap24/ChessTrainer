import tkinter as tk

from chess_board import BOARD_SIZE, PANEL_WIDTH, SQUARE, ChessBoard, Piece


board = [
    [Piece.BLACK_ROOK.code, Piece.BLACK_KNIGHT.code, Piece.BLACK_BISHOP.code, Piece.BLACK_QUEEN.code, Piece.BLACK_KING.code, Piece.BLACK_BISHOP.code, Piece.BLACK_KNIGHT.code, Piece.BLACK_ROOK.code],
    [Piece.BLACK_PAWN.code, Piece.BLACK_PAWN.code, Piece.BLACK_PAWN.code, Piece.BLACK_PAWN.code, Piece.BLACK_PAWN.code, Piece.BLACK_PAWN.code, Piece.BLACK_PAWN.code, Piece.BLACK_PAWN.code],
    [Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code],
    [Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code],
    [Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code],
    [Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code, Piece.EMPTY_SQUARE.code],
    [Piece.WHITE_PAWN.code, Piece.WHITE_PAWN.code, Piece.WHITE_PAWN.code, Piece.WHITE_PAWN.code, Piece.WHITE_PAWN.code, Piece.WHITE_PAWN.code, Piece.WHITE_PAWN.code, Piece.WHITE_PAWN.code],
    [Piece.WHITE_ROOK.code, Piece.WHITE_KNIGHT.code, Piece.WHITE_BISHOP.code, Piece.WHITE_QUEEN.code, Piece.WHITE_KING.code, Piece.WHITE_BISHOP.code, Piece.WHITE_KNIGHT.code, Piece.WHITE_ROOK.code],
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