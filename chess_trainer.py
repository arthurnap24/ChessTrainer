import tkinter as tk

BOARD_SIZE = 8
SQUARE = 80

LIGHT = "#FFFFFF"
DARK = "#B58863"

CHECK_RED = "#FF4C4C"

GREEN_SHADES = [
    "#E6FFE6", "#CCF5CC", "#A0EBA0",
    "#78DC78", "#50C850", "#1EAA1E"
]

ORANGE_SHADES = [
    "#FFF0DC", "#FFDCB4", "#FFC88C",
    "#FFAA5A", "#FF8C28", "#DC6400"
]

pieces = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
}

board = [
    ['r','n','b','q','k','b','n','r'],
    ['p','p','p','p','p','p','p','p'],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['P','P','P','P','P','P','P','P'],
    ['R','N','B','Q','K','B','N','R']
]


def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8


def add_sliding(attacks, r, c, dirs):
    for dr, dc in dirs:
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc):
            attacks[rr][cc] += 1
            if board[rr][cc] != '':
                break
            rr += dr
            cc += dc


def compute_attacks():
    white = [[0]*8 for _ in range(8)]
    black = [[0]*8 for _ in range(8)]

    for r in range(8):
        for c in range(8):

            p = board[r][c]
            if not p:
                continue

            is_white = p.isupper()
            target = white if is_white else black
            piece = p.lower()

            if piece == 'p':
                if is_white:
                    for dc in (-1, 1):
                        rr, cc = r - 1, c + dc
                        if in_bounds(rr, cc):
                            target[rr][cc] += 1
                else:
                    for dc in (-1, 1):
                        rr, cc = r + 1, c + dc
                        if in_bounds(rr, cc):
                            target[rr][cc] += 1

            elif piece == 'n':
                jumps = [
                    (-2,-1),(-2,1),(-1,-2),(-1,2),
                    (1,-2),(1,2),(2,-1),(2,1)
                ]
                for dr, dc in jumps:
                    rr, cc = r + dr, c + dc
                    if in_bounds(rr, cc):
                        target[rr][cc] += 1

            elif piece == 'b':
                add_sliding(target, r, c, [(-1,-1),(-1,1),(1,-1),(1,1)])

            elif piece == 'r':
                add_sliding(target, r, c, [(-1,0),(1,0),(0,-1),(0,1)])

            elif piece == 'q':
                add_sliding(target, r, c, [
                    (-1,-1),(-1,1),(1,-1),(1,1),
                    (-1,0),(1,0),(0,-1),(0,1)
                ])

            elif piece == 'k':
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        if dr == 0 and dc == 0:
                            continue
                        rr, cc = r + dr, c + dc
                        if in_bounds(rr, cc):
                            target[rr][cc] += 1

    return white, black


def shade(count, palette):
    if count <= 0:
        return None
    return palette[min(count, 6) - 1]


class ChessApp:

    def __init__(self, root):

        self.root = root
        self.canvas = tk.Canvas(root, width=640, height=640)
        self.canvas.pack(side=tk.LEFT)

        panel = tk.Frame(root)
        panel.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.highlight_on = tk.BooleanVar(value=False)

        tk.Checkbutton(
            panel,
            text="Highlight Squares",
            variable=self.highlight_on,
            command=self.draw
        ).pack(anchor="w", pady=10)

        tk.Label(
            panel,
            text="Green = White attack\nOrange = Black attack"
        ).pack(anchor="w")

        self.drag_piece = None
        self.drag_from = None

        self.canvas.bind("<Button-1>", self.mouse_down)
        self.canvas.bind("<B1-Motion>", self.mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up)

        self.draw()

    def mouse_down(self, event):
        r, c = event.y // SQUARE, event.x // SQUARE
        if not in_bounds(r, c):
            return

        self.drag_piece = board[r][c]
        if self.drag_piece:
            self.drag_from = (r, c)
            board[r][c] = ''

    def mouse_move(self, event):
        self.draw()
        if self.drag_piece:
            self.canvas.create_text(
                event.x, event.y,
                text=pieces[self.drag_piece],
                font=("Arial", 36)
            )

    def mouse_up(self, event):
        r, c = event.y // SQUARE, event.x // SQUARE

        if in_bounds(r, c):
            board[r][c] = self.drag_piece
        else:
            if self.drag_from:
                fr, fc = self.drag_from
                board[fr][fc] = self.drag_piece

        self.drag_piece = None
        self.drag_from = None

        self.draw()

    def find_kings(self):
        wk = bk = None
        for r in range(8):
            for c in range(8):
                if board[r][c] == 'K':
                    wk = (r,c)
                elif board[r][c] == 'k':
                    bk = (r,c)
        return wk, bk

    def draw(self):

        self.canvas.delete("all")

        white_att, black_att = compute_attacks()
        wking, bking = self.find_kings()

        for r in range(8):
            for c in range(8):

                color = LIGHT if (r+c)%2 == 0 else DARK

                if self.highlight_on.get():

                    w = white_att[r][c]
                    b = black_att[r][c]

                    if w > 0 and b == 0:
                        color = shade(w, GREEN_SHADES)

                    elif b > 0 and w == 0:
                        color = shade(b, ORANGE_SHADES)

                    elif w > 0 and b > 0:
                        g = shade(w, GREEN_SHADES)
                        o = shade(b, ORANGE_SHADES)
                        if g and o:
                            color = (
                                (int(g[1:3],16)+int(o[1:3],16))//2,
                                (int(g[3:5],16)+int(o[3:5],16))//2,
                                (int(g[5:7],16)+int(o[5:7],16))//2
                            )
                            color = f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"

                # check highlight
                if wking == (r,c) and black_att[r][c] > 0:
                    color = CHECK_RED
                if bking == (r,c) and white_att[r][c] > 0:
                    color = CHECK_RED

                self.canvas.create_rectangle(
                    c*SQUARE, r*SQUARE,
                    (c+1)*SQUARE, (r+1)*SQUARE,
                    fill=color,
                    outline="black"
                )

                p = board[r][c]
                if p:
                    self.canvas.create_text(
                        c*SQUARE + SQUARE//2,
                        r*SQUARE + SQUARE//2,
                        text=pieces[p],
                        font=("Arial", 36)
                    )


root = tk.Tk()
root.title("Chess Drag + Heatmap + Check Toggle")

ChessApp(root)

root.mainloop()