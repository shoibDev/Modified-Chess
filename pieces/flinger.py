from .base import Piece

class Flinger(Piece):
    def get_valid_moves(self, board) -> list:
        valid_moves = []

        piece_x = ord(self.position[0]) - ord('a')
        piece_y = 8 - int(self.position[1])

        # Flinger moves like a King (1 step in any direction)
        flinger_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # Horizontal & Vertical
            (1, 1), (-1, -1), (1, -1), (-1, 1)  # Diagonal
        ]

        for dx, dy in flinger_moves:
            move_x, move_y = piece_x + dx, piece_y + dy
            if 0 <= move_x < 8 and 0 <= move_y < 8:
                move_pos = f"{chr(move_x + ord('a'))}{8 - move_y}"
                if move_pos not in board.pieces:  # Can only move to empty squares
                    valid_moves.append(move_pos)

        return valid_moves

    def get_sling_moves(self, board) -> list:
        sling_moves = []

        piece_x = ord(self.position[0]) - ord('a')
        piece_y = 8 - int(self.position[1])

        # Look for adjacent friendly pieces
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            adj_x, adj_y = piece_x + dx, piece_y + dy
            if 0 <= adj_x < 8 and 0 <= adj_y < 8:
                adj_pos = f"{chr(adj_x + ord('a'))}{8 - adj_y}"

                if adj_pos in board.pieces and board.pieces[adj_pos].color == self.color:
                    # Sling direction
                    sling_x, sling_y = dx, dy

                    # Keep moving in the sling direction
                    new_x, new_y = adj_x + sling_x, adj_y + sling_y
                    while 0 <= new_x < 8 and 0 <= new_y < 8:
                        sling_pos = f"{chr(new_x + ord('a'))}{8 - new_y}"

                        if sling_pos in board.pieces:
                            # If it lands on an enemy, it's a capture (but also destroys the slung piece)
                            if board.pieces[sling_pos].color != self.color:
                                sling_moves.append((adj_pos, sling_pos))  # (slung piece, landing spot)
                            break  # Stop slinging further
                        else:
                            sling_moves.append((adj_pos, sling_pos))  # (slung piece, landing spot)

                        new_x += sling_x
                        new_y += sling_y

        return sling_moves
