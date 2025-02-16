from .base import Piece
from .zombie import Zombie  # Needed for promotion


class Peon(Piece):
    def get_valid_moves(self, board) -> list:
        valid_moves = []

        piece_x = ord(self.position[0]) - ord('a')  # 'a' -> 0, 'h' -> 7
        piece_y = 8 - int(self.position[1])  # '1' -> 7, '8' -> 0

        # Direction (White moves UP, Black moves DOWN)
        direction = -1 if self.color == 'w' else 1

        # Move forward 1 square
        move_y = piece_y + direction
        if 0 <= move_y < 8:
            move_pos = f"{self.position[0]}{8 - move_y}"
            if move_pos not in board.pieces:  # Can only move to an empty square
                valid_moves.append(move_pos)

        # Capture diagonally (left & right)
        for dx in [-1, 1]:  # Try both diagonal directions
            move_x = piece_x + dx
            move_y = piece_y + direction
            if 0 <= move_x < 8 and 0 <= move_y < 8:
                move_pos = f"{chr(move_x + ord('a'))}{8 - move_y}"
                if move_pos in board.pieces and board.pieces[move_pos].color != self.color:
                    valid_moves.append(move_pos)  # Capture enemy piece

        return valid_moves

    def promote_if_needed(self, board):
        """If the Peon reaches the last rank, promote it to a Zombie."""
        last_rank = 8 if self.color == 'w' else 1  # White promotes at rank 8, Black at rank 1
        if int(self.position[1]) == last_rank:
            board.pieces[self.position] = Zombie(self.color, self.position)  # Convert to Zombie
