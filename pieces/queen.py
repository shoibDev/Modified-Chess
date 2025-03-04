from .base import Piece

class Queen(Piece):
    def get_valid_moves(self, board) -> list:
        valid_moves = []

        piece_x = ord(self.position[0]) - ord('a')  # 'a' -> 0, 'h' -> 7
        piece_y = 8 - int(self.position[1])  # '1' -> 7, '8' -> 0

        # Horizontal & Vertical Moves (Rook Logic)
        # Move right
        for i in range(piece_x + 1, 8):
            move_x = chr(i + ord('a'))
            move_pos = f"{move_x}{8 - piece_y}"
            if move_pos in board.pieces:
                if board.pieces[move_pos].color != self.color:
                    valid_moves.append(move_pos)
                break
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

        # Diagonal Moves (Bishop Logic)
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            for i in range(1, 8):
                move_x, move_y = piece_x + dx * i, piece_y + dy * i
                if move_x < 0 or move_x > 7 or move_y < 0 or move_y > 7:
                    break
                move_pos = f"{chr(move_x + ord('a'))}{8 - move_y}"
                if move_pos in board.pieces:
                    if board.pieces[move_pos].color != self.color:
                        valid_moves.append(move_pos)
                    break
                valid_moves.append(move_pos)

        return valid_moves
