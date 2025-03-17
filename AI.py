import numpy as np
from pieces import Flinger, Peon, Cannon, King, Zombie, Knight
from collections import defaultdict
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
    [ 0.30,  0.60,  0.80,  1.00,  1.00,  1.00,  0.80,  0.50],
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

PIECE_VALUES = {
    'K': 10000,  # Extreme value for king
    'Q': 9.5, 'R': 5, 'B': 3.25, 'N': 3,
    'P': 1, 'F': 4, 'C': 11, 'Z': 7
}

PST = {
    'K': K_PST, 'Q': Q_PST, 'R': R_PST, 'B': B_PST,
    'N': N_PST, 'P': P_PST, 'F': F_PST, 'C': C_PST, 'Z': Z_PST
}


class AI:
    def __init__(self, depth=4, ai_color='w'):
        self.depth = depth
        self.ai_color = ai_color
        self.opponent_color = 'b' if ai_color == 'w' else 'w'


    def evaluate(self, board: Board) -> int:
        ai_score = opp_score = 0
        kings = {'w': None, 'b': None}

        # Material and positional scoring
        for pos, piece in board.pieces.items():
            piece_type = "N" if isinstance(piece, Knight) else piece.__class__.__name__[0]
            value = PIECE_VALUES[piece_type]
            file = ord(pos[0]) - ord('a')
            rank = int(pos[1]) - 1
            pst = PST[piece_type][7 - rank][file] if piece.color == 'b' else PST[piece_type][rank][file]

            if piece.color == self.ai_color:
                ai_score += value + pst
            else:
                opp_score += value + pst

            if piece_type == 'K':
                kings[piece.color] = pos  # Store position string

        # Terminal states
        if not kings.get(self.ai_color):
            return -100000
        if not kings.get(self.opponent_color):
            return 100000

        # Color-specific evaluations
        ai_score += self.evaluate_king_safety(board, kings[self.ai_color], self.ai_color)
        ai_score += self.evaluate_mobility(board, self.ai_color)
        ai_score += self.evaluate_pawn_structure(board, self.ai_color)

        opp_score += self.evaluate_king_safety(board, kings[self.opponent_color], self.opponent_color)
        opp_score += self.evaluate_mobility(board, self.opponent_color)
        opp_score += self.evaluate_pawn_structure(board, self.opponent_color)

        return ai_score - opp_score

    def evaluate_king_safety(self, board, king_pos, color):
        if not king_pos:
            return 0

        k_file = ord(king_pos[0]) - ord('a')
        k_rank = int(king_pos[1]) - 1
        score = 0
        pawn_shield = 0
        enemy_threats = 0

        # Adjacent squares calculation
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            af = k_file + dx
            ar = k_rank + dy
            if 0 <= af < 8 and 0 <= ar < 8:
                pos = f"{chr(af + ord('a'))}{ar + 1}"
                if pos in board.pieces and board.pieces[pos].color == color:
                    pawn_shield += 1

        # Pawn shield penalty
        if pawn_shield < 2:
            score -= (2 - pawn_shield) * 5

        # Enemy threats with piece value weighting
        enemy_color = 'b' if color == 'w' else 'w'
        for piece in board.pieces.values():
            if piece.color == enemy_color:
                if king_pos in piece.get_valid_moves(board):
                    enemy_threats += PIECE_VALUES.get(piece.__class__.__name__[0], 1)
                if isinstance(piece, Cannon):
                    for _, targets in piece.get_cannonball_moves(board):
                        if king_pos in targets:
                            enemy_threats += PIECE_VALUES['C']

        score -= enemy_threats * 2  # Reduced multiplier for better balance

        # Open file check
        king_file = king_pos[0]
        if not any(p.position[0] == king_file for p in board.pieces.values()
                   if isinstance(p, Peon) and p.color == color):
            score -= 5

        return score

    def evaluate_mobility(self, board, color):
        """Calculate mobility for specified color"""
        mobility = 0
        for piece in board.pieces.values():
            if piece.color == color and not isinstance(piece, King):
                moves = piece.get_valid_moves(board)
                mobility += len(moves) * 0.3
        return mobility

    def evaluate_pawn_structure(self, board, color):
        """Evaluate pawn structure for specified color"""
        score = 0
        pawns = defaultdict(list)
        enemy_pawns = defaultdict(list)

        for pos, piece in board.pieces.items():
            if isinstance(piece, Peon):
                if piece.color == color:
                    pawns[pos[0]].append(int(pos[1]))
                else:
                    enemy_pawns[pos[0]].append(int(pos[1]))

        for file, ranks in pawns.items():
            ranks.sort()
            # Doubled pawns
            if len(ranks) > 1:
                score -= (len(ranks) - 1) * 2

            # Isolation check
            left = chr(ord(file) - 1)
            right = chr(ord(file) + 1)
            isolated = not (pawns.get(left) or pawns.get(right))
            if isolated:
                score -= 3

            # Passed pawn detection
            front_rank = max(ranks) if color == 'w' else min(ranks)
            blocked = False
            for f in [file, left, right]:
                if f in enemy_pawns:
                    if color == 'w':
                        if any(r >= front_rank for r in enemy_pawns[f]):
                            blocked = True
                    else:
                        if any(r <= front_rank for r in enemy_pawns[f]):
                            blocked = True
            if not blocked:
                score += 4 + abs(front_rank - (4 if color == 'w' else 5))

        return score

    def alpha_beta_minimax(self, board, depth, alpha, beta, maximizing):
        if depth == 0 or board.is_checkmate():
            return self.evaluate(board)

        if maximizing:
            max_eval = -float('inf')
            for move in board.generate_successors():
                eval_score = self.alpha_beta_minimax(move, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.generate_successors():
                eval_score = self.alpha_beta_minimax(move, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def choose_best_move(self, board):
        """
        First, check if an opening move is still available by verifying whether
        the piece is still on its initial square. If so, iterate through the generated
        successors to find the board state that reflects the opening move.
        Otherwise, fall back to alpha-beta search.
        """
        # For White (Ruy López opening: 1. e4, 2. Nf3, 3. Bb5)
        if self.ai_color == 'w':
            # Move 1: e2 -> e3 (Zombie)
            if 'e2' in board.pieces and isinstance(board.pieces['e2'], Zombie):
                for new_board in board.generate_successors():
                    # Assuming new_board.last_move is set as "Piece moved from e2 to e4"
                    if hasattr(new_board, "last_move") and "e2 to e4" in new_board.last_move:
                        return new_board
            # Move 2: g1 -> f3 (Knight)
            elif 'g1' in board.pieces and isinstance(board.pieces['g1'], Knight):
                for new_board in board.generate_successors():
                    if hasattr(new_board, "last_move") and "g1 to f3" in new_board.last_move:
                        return new_board
            # Move 3: f1 -> b5 (Bishop)
            elif 'f1' in board.pieces and board.pieces['f1'].__class__.__name__[0] == 'B':
                for new_board in board.generate_successors():
                    if hasattr(new_board, "last_move") and "f1 to b5" in new_board.last_move:
                        return new_board

        # For Black (Queen's Indian Defense: 1. ... Nf6, 2. ... e6, 3. ... b6)
        else:
            # Move 1: g8 -> f6 (Knight)
            if 'g8' in board.pieces and isinstance(board.pieces['g8'], Knight):
                for new_board in board.generate_successors():
                    if hasattr(new_board, "last_move") and "g8 to f6" in new_board.last_move:
                        return new_board
            # Move 2: c7 -> e6 (Peon)
            elif 'c7' in board.pieces and isinstance(board.pieces['c7'], Peon):
                for new_board in board.generate_successors():
                    if hasattr(new_board, "last_move") and "c7 to e6" in new_board.last_move:
                        return new_board
            # Move 3: b7 -> b6 (Peon)
            elif 'b7' in board.pieces and isinstance(board.pieces['b7'], Peon):
                for new_board in board.generate_successors():
                    if hasattr(new_board, "last_move") and "b7 to b6" in new_board.last_move:
                        return new_board

        # If none of the opening moves are applicable, fall back to alpha-beta search.
        best_move = None
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')
        is_maximizing = (board.turn == self.ai_color)
        for move in board.generate_successors():
            score = self.alpha_beta_minimax(move, depth=self.depth - 1, alpha=alpha, beta=beta,
                                            maximizing=not is_maximizing)
            if score > best_score:
                best_score = score
                best_move = move
                alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_move
