BOARD_SIZE = 8


def in_bounds(r, c):
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE


def add_sliding(attacks, board, r, c, dirs, empty_square_code):
    for dr, dc in dirs:
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc):
            attacks[rr][cc] += 1
            if board[rr][cc] != empty_square_code:
                break
            rr += dr
            cc += dc


def compute_attacks(board, empty_square_code=""):
    white = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    black = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            p = board[r][c]
            if not p:
                continue

            is_white = p.isupper()
            target = white if is_white else black
            piece = p.lower()

            if piece == "p":
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

            elif piece == "n":
                jumps = [
                    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1),
                ]
                for dr, dc in jumps:
                    rr, cc = r + dr, c + dc
                    if in_bounds(rr, cc):
                        target[rr][cc] += 1

            elif piece == "b":
                add_sliding(target, board, r, c, [(-1, -1), (-1, 1), (1, -1), (1, 1)], empty_square_code)

            elif piece == "r":
                add_sliding(target, board, r, c, [(-1, 0), (1, 0), (0, -1), (0, 1)], empty_square_code)

            elif piece == "q":
                add_sliding(
                    target,
                    board,
                    r,
                    c,
                    [
                        (-1, -1), (-1, 1), (1, -1), (1, 1),
                        (-1, 0), (1, 0), (0, -1), (0, 1),
                    ],
                    empty_square_code,
                )

            elif piece == "k":
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        rr, cc = r + dr, c + dc
                        if in_bounds(rr, cc):
                            target[rr][cc] += 1

    return white, black
