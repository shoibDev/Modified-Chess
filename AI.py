import numpy as np

from pieces import Flinger, Peon, Cannon, King, Zombie
from Board import Board

# Aggressive Piece-Square Tables (8x8) for each piece type

# King PST – Encourage staying near corners and discourage central exposure
K_PST = np.array([
    [-2.00, -1.70, -1.80, -2.30, -2.30, -1.80, -1.70, -2.00],
    [-1.60, -1.30, -1.40, -1.90, -1.90, -1.40, -1.30, -1.60],
    [-1.20, -0.90, -1.00, -1.50, -1.50, -1.00, -0.90, -1.20],
    [-0.80, -0.50, -0.60, -1.10, -1.10, -0.60, -0.50, -0.80],
    [-0.40, -0.10, -0.20, -0.70, -0.70, -0.20, -0.10, -0.40],
    [ 0.00,  0.30,  0.20, -0.30, -0.30,  0.20,  0.30,  0.00],
    [ 0.20,  0.50,  0.40, -0.10, -0.10,  0.40,  0.50,  0.20],
    [ 0.30,  0.60,  0.50,  0.00,  0.00,  0.50,  0.60,  0.30]
], dtype=float)

# Queen PST – Favor central board control and forward placement
Q_PST = np.array([
    [ 0.00,  0.10,  0.20,  0.30,  0.30,  0.20,  0.10,  0.00],
    [ 0.10,  0.20,  0.30,  0.40,  0.40,  0.30,  0.20,  0.10],
    [ 0.05,  0.15,  0.25,  0.35,  0.35,  0.25,  0.15,  0.05],
    [ 0.00,  0.10,  0.20,  0.30,  0.30,  0.20,  0.10,  0.00],
    [-0.10,  0.00,  0.10,  0.20,  0.20,  0.10,  0.00, -0.10],
    [-0.20, -0.10,  0.00,  0.10,  0.10,  0.00, -0.10, -0.20],
    [-0.30, -0.20, -0.10,  0.00,  0.00, -0.10, -0.20, -0.30],
    [-0.40, -0.30, -0.20, -0.10, -0.10, -0.20, -0.30, -0.40]
], dtype=float)

# Rook PST – Encourage rooks to move off the back rank and onto open files/7th rank
R_PST = np.array([
    [ 0.15,  0.20,  0.25,  0.30,  0.30,  0.25,  0.20,  0.15],
    [ 0.20,  0.25,  0.30,  0.35,  0.35,  0.30,  0.25,  0.20],
    [ 0.10,  0.15,  0.20,  0.25,  0.25,  0.20,  0.15,  0.10],
    [ 0.05,  0.10,  0.15,  0.20,  0.20,  0.15,  0.10,  0.05],
    [ 0.00,  0.05,  0.10,  0.15,  0.15,  0.10,  0.05,  0.00],
    [-0.05,  0.00,  0.05,  0.10,  0.10,  0.05,  0.00, -0.05],
    [-0.10, -0.05,  0.00,  0.05,  0.05,  0.00, -0.05, -0.10],
    [-0.20, -0.15, -0.10, -0.05, -0.05, -0.10, -0.15, -0.20]
], dtype=float)

# Bishop PST – Favor long diagonals and central positioning
B_PST = np.array([
    [-0.10, -0.05,  0.00,  0.05,  0.05,  0.00, -0.05, -0.10],
    [ 0.00,  0.05,  0.10,  0.15,  0.15,  0.10,  0.05,  0.00],
    [ 0.05,  0.10,  0.15,  0.20,  0.20,  0.15,  0.10,  0.05],
    [ 0.10,  0.15,  0.20,  0.25,  0.25,  0.20,  0.15,  0.10],
    [ 0.05,  0.10,  0.15,  0.20,  0.20,  0.15,  0.10,  0.05],
    [ 0.00,  0.05,  0.10,  0.15,  0.15,  0.10,  0.05,  0.00],
    [-0.10, -0.05,  0.00,  0.05,  0.05,  0.00, -0.05, -0.10],
    [-0.30, -0.25, -0.20, -0.15, -0.15, -0.20, -0.25, -0.30]
], dtype=float)

# Knight PST – Strongly favor central and advanced outpost squares; penalize edges and corners
N_PST = np.array([
    [-0.90, -0.70, -0.40, -0.30, -0.30, -0.40, -0.70, -0.90],
    [-0.50, -0.30,  0.00,  0.10,  0.10,  0.00, -0.30, -0.50],
    [-0.30, -0.10,  0.20,  0.30,  0.30,  0.20, -0.10, -0.30],
    [-0.20,  0.00,  0.30,  0.40,  0.40,  0.30,  0.00, -0.20],
    [-0.30, -0.10,  0.20,  0.30,  0.30,  0.20, -0.10, -0.30],
    [-0.50, -0.30,  0.00,  0.10,  0.10,  0.00, -0.30, -0.50],
    [-0.70, -0.50, -0.20, -0.10, -0.10, -0.20, -0.50, -0.70],
    [-0.90, -0.70, -0.40, -0.30, -0.30, -0.40, -0.70, -0.90]
], dtype=float)

# Peon (Pawn) PST – Encourage pawns to advance and control the center
P_PST = np.array([
    [ 0.80,  0.85,  0.90,  1.00,  1.00,  0.90,  0.85,  0.80],
    [ 0.80,  0.85,  0.90,  1.00,  1.00,  0.90,  0.85,  0.80],
    [ 0.60,  0.65,  0.70,  0.80,  0.80,  0.70,  0.65,  0.60],
    [ 0.30,  0.35,  0.40,  0.50,  0.50,  0.40,  0.35,  0.30],
    [ 0.10,  0.15,  0.20,  0.30,  0.30,  0.20,  0.15,  0.10],
    [ 0.00,  0.05,  0.10,  0.20,  0.20,  0.10,  0.05,  0.00],
    [-0.10, -0.05,  0.00,  0.10,  0.10,  0.00, -0.05, -0.10],
    [-0.10, -0.05,  0.00,  0.10,  0.10,  0.00, -0.05, -0.10]
], dtype=float)

# Zombie PST – Favor advancing into opponent’s side and centralizing
Z_PST = np.array([
    [ 0.50,  0.80,  1.00,  1.20,  1.20,  1.00,  0.80,  0.50],
    [ 0.50,  0.80,  1.00,  1.20,  1.20,  1.00,  0.80,  0.50],
    [ 0.30,  0.60,  0.80,  1.00,  1.00,  0.80,  0.60,  0.30],
    [ 0.10,  0.40,  0.60,  0.80,  0.80,  0.60,  0.40,  0.10],
    [-0.10,  0.20,  0.40,  0.60,  1.20,  0.40,  0.20, -0.10],
    [-0.30,  0.00,  0.20,  0.40,  0.40,  0.20,  0.00, -0.30],
    [-0.40, -0.10,  0.10,  0.30,  0.30,  0.10, -0.10, -0.40],
    [-0.50, -0.20,  0.00,  0.20,  0.20,  0.00, -0.20, -0.50]
], dtype=float)

# Flinger PST – Treat as a long-range piece; favor central files and advancing toward the 7th rank
F_PST = np.array([
    [ 0.30,  0.40,  0.50,  0.60,  0.60,  0.50,  0.40,  0.30],
    [ 0.40,  0.50,  0.60,  0.70,  0.70,  0.60,  0.50,  0.40],
    [ 0.30,  0.40,  0.50,  0.60,  0.60,  0.50,  0.40,  0.30],
    [ 0.20,  0.30,  0.40,  0.50,  0.50,  0.40,  0.30,  0.20],
    [ 0.10,  0.20,  0.30,  0.40,  0.40,  0.30,  0.20,  0.10],
    [ 0.00,  0.10,  0.20,  0.30,  0.30,  0.20,  0.10,  0.00],
    [-0.10,  0.00,  0.10,  0.20,  0.20,  0.10,  0.00, -0.10],
    [-0.15, -0.05,  0.05,  0.15,  0.15,  0.05, -0.05, -0.15]
], dtype=float)

# Cannon PST – Modeled after a Xiangqi cannon; favor mid-ranks and central files
C_PST = np.array([
    [-0.50, -0.30, -0.10,  0.00,  0.00, -0.10, -0.30, -0.50],
    [-0.40, -0.20,  0.00,  0.10,  0.10,  0.00, -0.20, -0.40],
    [-0.20,  0.00,  0.20,  0.30,  0.30,  0.20,  0.00, -0.20],
    [ 0.00,  0.20,  0.40,  0.50,  0.50,  0.40,  0.20,  0.00],
    [ 0.10,  0.30,  0.50,  0.60,  0.60,  0.50,  0.30,  0.10],
    [ 0.00,  0.20,  0.40,  0.50,  0.50,  0.40,  0.20,  0.00],
    [-0.20,  0.00,  0.20,  0.30,  0.30,  0.20,  0.00, -0.20],
    [-0.30, -0.10,  0.10,  0.20,  0.20,  0.10, -0.10, -0.30]
], dtype=float)


class AI:
    def __init__(self, depth=4, ai_color='w'):
        self.depth = depth
        self.ai_color = ai_color  # 'w' or 'b'

    @staticmethod
    def evaluate(board: Board) -> int:
        PIECE_VALUES = {
            'K': 20, 'Q': 9, 'R': 5, 'B': 3, 'N': 3,
            'P': 1, 'F': 4, 'C': 11
        }

        PST = {
            'K': K_PST, 'Q': Q_PST, 'R': R_PST, 'B': B_PST, 'N': N_PST,
            'P': P_PST, 'F': F_PST, 'C': C_PST
        }
        score = 0
        king_positions = {'w': None, 'b': None}  # Store king locations for both sides

        for piece in board.pieces.values():
            # Use "N" for Knight; for all others, use first letter of class name.
            piece_type = "N" if piece.__class__.__name__ == "Knight" else piece.__class__.__name__[0]
            piece_value = PIECE_VALUES.get(piece_type, 0)
            file = ord(piece.position[0]) - ord('a')
            rank = int(piece.position[1]) - 1

            if piece_type == "K":
                king_positions[piece.color] = (file, rank)  # Save King's location

            # Access PST (mirror for Black)
            pst_bonus = PST[piece_type][7 - rank][file] if piece.color == 'b' else PST[piece_type][rank][file]

            # Add piece value and PST bonus; subtract for opponent's pieces.
            score += (piece_value + pst_bonus) if piece.color == board.turn else -1 * (piece_value + pst_bonus)

        # Check for missing kings: if the king for the current side is missing, that's a loss.
        if king_positions[board.turn] is None:
            return -100000

        # If the opponent's king is missing, that's a win.
        opponent = 'b' if board.turn == 'w' else 'w'
        if king_positions[opponent] is None:
            return 100000

        # Only evaluate king safety for the AI's turn if the king is found.
        score += AI.evaluate_king_safety(board, king_positions[board.turn], board.turn)
        score += AI.evaluate_mobility(board)
        score += AI.evaluate_pawn_structure(board)

        return score

    @staticmethod
    def evaluate_king_safety(board, king_pos, color):
        if king_pos is None:
            return 0  # No King found (shouldn't happen in a valid game)

        k_file, k_rank = king_pos
        king_square = f"{chr(k_file + ord('a'))}{k_rank + 1}"
        enemy_color = 'b' if color == 'w' else 'w'
        king_safety_score = 0
        pawn_protection = 0
        enemy_threats = 0

        adjacent_deltas = [(-1, -1), (-1, 0), (-1, 1),
                           (0, -1),           (0, 1),
                           (1, -1),  (1, 0),  (1, 1)]

        # 1: Friendly Piece Protection (check all adjacent squares)
        for dx, dy in adjacent_deltas:
            adj_file = k_file + dx
            adj_rank = k_rank + dy
            if 0 <= adj_file < 8 and 0 <= adj_rank < 8:
                adj_pos = f"{chr(adj_file + ord('a'))}{adj_rank + 1}"
                if adj_pos in board.pieces:
                    piece = board.pieces[adj_pos]
                    if piece.color == color:
                        pawn_protection += 1

        if pawn_protection < 2:
            king_safety_score -= (2 - pawn_protection) * 5

        # 2: Check for Enemy Attacks
        for enemy_pos, enemy_piece in board.pieces.items():
            if enemy_piece.color == enemy_color:
                enemy_moves = enemy_piece.get_valid_moves(board)
                for move in enemy_moves:
                    if move == king_square:
                        enemy_threats += 3  # Direct attack penalty

                if isinstance(enemy_piece, Cannon):
                    cannonball_moves = enemy_piece.get_cannonball_moves(board)
                    for _, hit_pieces in cannonball_moves:
                        if king_square in hit_pieces:
                            enemy_threats += 5  # Higher penalty for a Cannon threat

        king_safety_score -= enemy_threats * 10

        # 3: Open File Penalty – if no friendly pawn is on the King's file.
        friendly_pawns = [p for p in board.pieces.values() if p.color == color and p.position[0] == f"{chr(k_file + ord('a'))}"]
        if not friendly_pawns:
            king_safety_score -= 8

        return king_safety_score

    @staticmethod
    def evaluate_mobility(board):
        mobility_score = 0
        for piece in board.pieces.values():
            if isinstance(piece, King):
                continue
            legal_moves = piece.get_valid_moves(board)
            move_count = len(legal_moves)
            mobility_score += move_count * 0.5
            if move_count < 2:
                mobility_score -= 2
        return mobility_score

    @staticmethod
    def evaluate_pawn_structure(board):
        pawn_structure_score = 0
        pawn_positions = {'w': {}, 'b': {}}

        for piece in board.pieces.values():
            if isinstance(piece, Peon):
                file = piece.position[0]
                rank = int(piece.position[1])
                pawn_positions[piece.color].setdefault(file, []).append(rank)

        for color, pawns in pawn_positions.items():
            for file, ranks in pawns.items():
                ranks.sort()
                if len(ranks) > 1:
                    pawn_structure_score -= (len(ranks) - 1) * 2
                left_file = chr(ord(file) - 1) if file > 'a' else None
                right_file = chr(ord(file) + 1) if file < 'h' else None
                has_neighbor = ((left_file in pawns) or (right_file in pawn_positions[color]))
                if not has_neighbor:
                    pawn_structure_score -= 3
                if color == 'w':
                    enemy_pawns = pawn_positions['b']
                    blocked = any(
                        f in enemy_pawns and any(r > min(ranks) for r in enemy_pawns[f])
                        for f in [file, left_file, right_file] if f
                    )
                else:
                    enemy_pawns = pawn_positions['w']
                    blocked = any(
                        f in enemy_pawns and any(r < max(ranks) for r in enemy_pawns[f])
                        for f in [file, left_file, right_file] if f
                    )
                if not blocked:
                    pawn_structure_score += 6
                if file in ['d', 'e'] and (color == 'w' and max(ranks) >= 4 or color == 'b' and min(ranks) <= 5):
                    pawn_structure_score += 4
        return pawn_structure_score

    def alpha_beta_minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_checkmate():
            return self.evaluate(board)

        if maximizing_player:
            max_eval = -float('inf')
            for move in self.order_moves(board.generate_successors()):
                eval_score = self.alpha_beta_minimax(move, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.order_moves(board.generate_successors()):
                eval_score = self.alpha_beta_minimax(move, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def choose_best_move(self, board):
        best_move = None
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        # Determine if we're maximizing based on AI color
        is_maximizing = (board.turn == self.ai_color)

        for move in self.order_moves(board.generate_successors()):
            current_score = self.alpha_beta_minimax(
                move,
                depth=self.depth - 1,  # Use full depth
                alpha=alpha,
                beta=beta,
                maximizing_player=not is_maximizing  # Switch sides after root move
            )

            if current_score > best_score:
                best_score = current_score
                best_move = move
                alpha = max(alpha, best_score)

            if beta <= alpha:
                break

        return best_move

    def order_moves(self, moves):
        # Basic move ordering - sort moves based on move priority.
        return sorted(moves, key=lambda m: self.move_priority(m), reverse=True)

    def move_priority(self, move):
        """
        Calculate a priority score for a move.
        The higher the score, the sooner the move will be examined.
        Priorities are based on:
          1. Captures (MVV-LVA): capturing high-value pieces with low-value pieces.
          2. Checks: moves that put the enemy king in check.
          3. Promotions: moves that promote a pawn.
          4. Threats: moves that threaten high-value enemy pieces.
          5. Defensive moves: moves that protect the king or prevent mate.
          6. Positional improvements: improvements according to piece-square tables.
          7. Quiet moves: least priority.
        """
        score = 0
        # If the move has a last_move attribute, we use its text to decide priorities.
        if hasattr(move, "last_move") and move.last_move:
            text = move.last_move.lower()
            # Promotion moves: highest priority.
            if "promote" in text:
                score += 9000
            # Captures: look for keywords (assume 'capture' appears in the description).
            if "capture" in text:
                score += 1000
            # Cannon firing moves (usually capture multiple pieces)
            if "fires" in text:
                score += 1200
            # Flinger sling moves that may capture pieces.
            if "sling" in text:
                score += 800
            # Moves that give check.
            if "check" in text:
                score += 500
            # Threats to high-value pieces (if the description mentions attacking a queen, rook, etc.)
            if "queen" in text:
                score += 300
            if "rook" in text:
                score += 200
            # Defensive moves: if the move description indicates blocking or defending.
            if "defend" in text or "block" in text:
                score += 400
        return score
