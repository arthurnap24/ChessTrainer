Prompt 1:
create a python program that:
* displays an interactive chess board with black and white pieces, use brown for dark squares and white for white squares.
* has a button that shows a toggle button called "highlight squares"
* when highlight squares is selected:
    - each chess square that the white pieces cover (can move to or attack including squares with pieces to take) must take a shade of green.
    - each chess square that the black pieces cover must take a shade of orange.
    - plan to have 6 shades of orange (you pick what rgb values to use)

Prompt 2:
add feature to drag and drop and move the pieces:
* if a piece is dragged and dropped on a square, remove the piece on that square
* add check feature, (highlight the king square red)
* do not add any legal move verification

Prompt 3:
break chess_trainer.py into 3 source files:
* rules.py - add in_bounds, add_sliding, and compute_attacks
* chess_board.py - add chess board rendering, drag and drop, and buttons
* chess_trainer.py - where everything is tied together