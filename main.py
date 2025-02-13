from Board import Board
import utils

if __name__ == "__main__":
    turn, pieces = utils.parse_board("board.txt")
    board = Board()

    for piece in pieces:
        board.add_piece(piece)

    print(board)


