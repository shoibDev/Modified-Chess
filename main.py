from Board import Board
from pieces.bishop import Bishop
from pieces.knight import Knight

# Initialize the board
board = Board()

# Add a white Bishop at c1 and a black Knight at g8
board.add_piece(Bishop('w', 'c1'))
board.add_piece(Knight('b', 'g8'))

# Print the board
print(board)
