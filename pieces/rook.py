from .base import Piece


class Rook(Piece):
    def get_valid_moves(self, board) -> list:
        valid_moves = []

        piece_x = ord(self.position[0]) - ord('a')  # 'a' -> 0, 'h' -> 7
        piece_y = 8 - int(self.position[1])  # '1' -> 7, '8' -> 0

        # Move right
        for i in range(piece_x + 1, 8):
            move_x = chr(i + ord('a'))
            move_pos = f"{move_x}{8 - piece_y}"

            if move_pos in board.pieces:  # Blocked by a piece
                if board.pieces[move_pos].color != self.color:  # Capture allowed
                    valid_moves.append(move_pos)
                break  # Stop moving in this direction
            valid_moves.append(move_pos)

        # Move left
        for i in range(piece_x - 1, -1, -1):
            move_x = chr(i + ord('a'))
            move_pos = f"{move_x}{8 - piece_y}"

            if move_pos in board.pieces:
                if board.pieces[move_pos].color != self.color:
                    valid_moves.append(move_pos)
                break
            valid_moves.append(move_pos)

        # Move up
        for i in range(piece_y - 1, -1, -1):
            move_y = 8 - i
            move_pos = f"{self.position[0]}{move_y}"

            if move_pos in board.pieces:
                if board.pieces[move_pos].color != self.color:
                    valid_moves.append(move_pos)
                break
            valid_moves.append(move_pos)

        # Move down
        for i in range(piece_y + 1, 8):
            move_y = 8 - i
            move_pos = f"{self.position[0]}{move_y}"

            if move_pos in board.pieces:
                if board.pieces[move_pos].color != self.color:
                    valid_moves.append(move_pos)
                break
            valid_moves.append(move_pos)

        return valid_moves
