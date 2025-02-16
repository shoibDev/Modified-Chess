from Board import Board
import utils
from pieces import Rook

def test():
    board = Board()
    _, piece_list = utils.parse_board('board.txt')

    for piece in piece_list:
        board.add_piece(piece)

    move_list = board.pieces['a8'].get_sling_moves(board)

    print(board)
    print(move_list)



if __name__ == "__main__":
    test()




