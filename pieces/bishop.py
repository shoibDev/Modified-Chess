from .base import Piece

class Bishop(Piece):
    def get_valid_moves(self, board) -> list:
        valid_moves = []

        piece_x = ord(self.position[0]) - ord('a')  # 'a' -> 0, 'h' -> 7
        piece_y = 8 - int(self.position[1])  # '1' -> 7, '8' -> 0

        # Move diagonally up-right (↗)
        for i in range(1, 8):
            move_x, move_y = piece_x + i, piece_y - i
            if move_x > 7 or move_y < 0: break
            move_pos = f"{chr(move_x + ord('a'))}{8 - move_y}"
            if move_pos in board.pieces:
                if board.pieces[move_pos].color != self.color:
                    valid_moves.append(move_pos)
                break
            valid_moves.append(move_pos)

        # Move diagonally up-left (↖)
        for i in range(1, 8):
            move_x, move_y = piece_x - i, piece_y - i
            if move_x < 0 or move_y < 0: break
            move_pos = f"{chr(move_x + ord('a'))}{8 - move_y}"
            if move_pos in board.pieces:
                if board.pieces[move_pos].color != self.color:
                    valid_moves.append(move_pos)
                break
            valid_moves.append(move_pos)

        # Move diagonally down-right (↘)
        for i in range(1, 8):
            move_x, move_y = piece_x + i, piece_y + i
            if move_x > 7 or move_y > 7: break
            move_pos = f"{chr(move_x + ord('a'))}{8 - move_y}"
            if move_pos in board.pieces:
                if board.pieces[move_pos].color != self.color:
                    valid_moves.append(move_pos)
                break
            valid_moves.append(move_pos)

        # Move diagonally down-left (↙)
        for i in range(1, 8):
            move_x, move_y = piece_x - i, piece_y + i
            if move_x < 0 or move_y > 7: break
            move_pos = f"{chr(move_x + ord('a'))}{8 - move_y}"
            if move_pos in board.pieces:
                if board.pieces[move_pos].color != self.color:
                    valid_moves.append(move_pos)
                break
            valid_moves.append(move_pos)

        return valid_moves
