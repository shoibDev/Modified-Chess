import numpy as np
from pieces import Flinger, Peon, Cannon, King, Zombie, Knight
from collections import defaultdict
from Board import Board

# Enhanced Aggressive Piece-Square Tables (8x8) for each piece type

# King PST – Encourage staying near corners and discourage central exposure
K_PST = np.array([
    [-2.00, -1.70, -1.80, -2.30, -2.30, -1.80, -1.70, -2.00],
    [-1.60, -1.30, -1.40, -1.90, -1.90, -1.40, -1.30, -1.60],
    [-1.20, -0.90, -1.00, -1.50, -1.50, -1.00, -0.90, -1.20],
    [-0.80, -0.50, -0.60, -1.10, -1.10, -0.60, -0.50, -0.80],
    [-0.40, -0.10, -0.20, -0.70, -0.70, -0.20, -0.10, -0.40],
    [0.00, 0.30, 0.20, -0.30, -0.30, 0.20, 0.30, 0.00],
    [0.20, 0.50, 0.40, -0.10, -0.10, 0.40, 0.50, 0.20],
    [0.30, 0.60, 0.50, 0.00, 0.00, 0.50, 0.60, 0.30]
], dtype=float)

# Queen PST – Favor central board control and forward placement
Q_PST = np.array([
    [0.00, 0.10, 0.20, 0.30, 0.30, 0.20, 0.10, 0.00],
    [0.10, 0.20, 0.30, 0.40, 0.40, 0.30, 0.20, 0.10],
    [0.05, 0.15, 0.25, 0.35, 0.35, 0.25, 0.15, 0.05],
    [0.00, 0.10, 0.20, 0.30, 0.30, 0.20, 0.10, 0.00],
    [-0.10, 0.00, 0.10, 0.20, 0.20, 0.10, 0.00, -0.10],
    [-0.20, -0.10, 0.00, 0.10, 0.10, 0.00, -0.10, -0.20],
    [-0.30, -0.20, -0.10, 0.00, 0.00, -0.10, -0.20, -0.30],
    [-0.40, -0.30, -0.20, -0.10, -0.10, -0.20, -0.30, -0.40]
], dtype=float)

# Rook PST – Encourage rooks to move off the back rank and onto open files/7th rank
R_PST = np.array([
    [0.15, 0.20, 0.25, 0.30, 0.30, 0.25, 0.20, 0.15],
    [0.20, 0.25, 0.30, 0.35, 0.35, 0.30, 0.25, 0.20],
    [0.10, 0.15, 0.20, 0.25, 0.25, 0.20, 0.15, 0.10],
    [0.05, 0.10, 0.15, 0.20, 0.20, 0.15, 0.10, 0.05],
    [0.00, 0.05, 0.10, 0.15, 0.15, 0.10, 0.05, 0.00],
    [-0.05, 0.00, 0.05, 0.10, 0.10, 0.05, 0.00, -0.05],
    [-0.10, -0.05, 0.00, 0.05, 0.05, 0.00, -0.05, -0.10],
    [-0.20, -0.15, -0.10, -0.05, -0.05, -0.10, -0.15, -0.20]
], dtype=float)

# Bishop PST – Favor long diagonals and central positioning
B_PST = np.array([
    [-0.10, -0.05, 0.00, 0.05, 0.05, 0.00, -0.05, -0.10],
    [0.00, 0.05, 0.10, 0.15, 0.15, 0.10, 0.05, 0.00],
    [0.05, 0.10, 0.15, 0.20, 0.20, 0.15, 0.10, 0.05],
    [0.10, 0.15, 0.20, 0.25, 0.25, 0.20, 0.15, 0.10],
    [0.05, 0.10, 0.15, 0.20, 0.20, 0.15, 0.10, 0.05],
    [0.00, 0.05, 0.10, 0.15, 0.15, 0.10, 0.05, 0.00],
    [-0.10, -0.05, 0.00, 0.05, 0.05, 0.00, -0.05, -0.10],
    [-0.30, -0.25, -0.20, -0.15, -0.15, -0.20, -0.25, -0.30]
], dtype=float)

# Knight PST – Strongly favor central and advanced outpost squares; penalize edges and corners
N_PST = np.array([
    [-0.90, -0.70, -0.40, -0.30, -0.30, -0.40, -0.70, -0.90],
    [-0.50, -0.30, 0.00, 0.10, 0.10, 0.00, -0.30, -0.50],
    [-0.30, -0.10, 0.20, 0.30, 0.30, 0.20, -0.10, -0.30],
    [-0.20, 0.00, 0.30, 0.40, 0.40, 0.30, 0.00, -0.20],
    [-0.30, -0.10, 0.20, 0.30, 0.30, 0.20, -0.10, -0.30],
    [-0.50, -0.30, 0.00, 0.10, 0.10, 0.00, -0.30, -0.50],
    [-0.70, -0.50, -0.20, -0.10, -0.10, -0.20, -0.50, -0.70],
    [-0.90, -0.70, -0.40, -0.30, -0.30, -0.40, -0.70, -0.90]
], dtype=float)

# Enhanced Peon (Pawn) PST – Significantly higher values to encourage pawn movement
P_PST = np.array([
    [2.00, 2.10, 2.20, 2.30, 2.30, 2.20, 2.10, 2.00],  # Promotion rank (highest value)
    [1.60, 1.70, 1.80, 1.90, 1.90, 1.80, 1.70, 1.60],
    [1.20, 1.30, 1.40, 1.50, 1.50, 1.40, 1.30, 1.20],
    [0.80, 0.90, 1.00, 1.10, 1.10, 1.00, 0.90, 0.80],
    [0.50, 0.60, 0.70, 0.80, 0.80, 0.70, 0.60, 0.50],
    [0.30, 0.40, 0.50, 0.60, 0.60, 0.50, 0.40, 0.30],
    [0.10, 0.20, 0.30, 0.40, 0.40, 0.30, 0.20, 0.10],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]  # Starting rank (lowest value)
], dtype=float)

# Enhanced Zombie PST – Much higher values to make zombies stronger and more central-aggressive
Z_PST = np.array([
    [1.80, 2.00, 2.20, 2.40, 2.40, 2.20, 2.00, 1.80],  # Highest value on opponent's side
    [1.50, 1.70, 1.90, 2.10, 2.10, 1.90, 1.70, 1.50],
    [1.20, 1.40, 1.60, 1.80, 1.80, 1.60, 1.40, 1.20],
    [0.90, 1.10, 1.30, 1.50, 1.50, 1.30, 1.10, 0.90],
    [0.60, 0.80, 1.00, 1.20, 1.20, 1.00, 0.80, 0.60],
    [0.30, 0.50, 0.70, 0.90, 0.90, 0.70, 0.50, 0.30],
    [0.10, 0.30, 0.50, 0.70, 0.70, 0.50, 0.30, 0.10],
    [0.00, 0.20, 0.40, 0.60, 0.60, 0.40, 0.20, 0.00]
], dtype=float)

# Flinger PST – Treat as a long-range piece; favor central files and advancing toward the 7th rank
F_PST = np.array([
    [0.30, 0.40, 0.50, 0.60, 0.60, 0.50, 0.40, 0.30],
    [0.40, 0.50, 0.60, 0.70, 0.70, 0.60, 0.50, 0.40],
    [0.30, 0.40, 0.50, 0.60, 0.60, 0.50, 0.40, 0.30],
    [0.20, 0.30, 0.40, 0.50, 0.50, 0.40, 0.30, 0.20],
    [0.10, 0.20, 0.30, 0.40, 0.40, 0.30, 0.20, 0.10],
    [0.00, 0.10, 0.20, 0.30, 0.30, 0.20, 0.10, 0.00],
    [-0.10, 0.00, 0.10, 0.20, 0.20, 0.10, 0.00, -0.10],
    [-0.15, -0.05, 0.05, 0.15, 0.15, 0.05, -0.05, -0.15]
], dtype=float)

# Cannon PST – Modeled after a Xiangqi cannon; favor mid-ranks and central files
C_PST = np.array([
    [-0.50, -0.30, -0.10, 0.00, 0.00, -0.10, -0.30, -0.50],
    [-0.40, -0.20, 0.00, 0.10, 0.10, 0.00, -0.20, -0.40],
    [-0.20, 0.00, 0.20, 0.30, 0.30, 0.20, 0.00, -0.20],
    [0.00, 0.20, 0.40, 0.50, 0.50, 0.40, 0.20, 0.00],
    [0.10, 0.30, 0.50, 0.60, 0.60, 0.50, 0.30, 0.10],
    [0.00, 0.20, 0.40, 0.50, 0.50, 0.40, 0.20, 0.00],
    [-0.20, 0.00, 0.20, 0.30, 0.30, 0.20, 0.00, -0.20],
    [-0.30, -0.10, 0.10, 0.20, 0.20, 0.10, -0.10, -0.30]
], dtype=float)

# Enhanced piece values to make certain pieces more valuable in captures
PIECE_VALUES = {
    'K': 10000,  # Extreme value for king
    'Q': 9.5,
    'R': 5,
    'B': 3.25,
    'N': 3,
    'P': 1.2,  # Increased pawn value to encourage pawn moves and captures
    'F': 4,
    'C': 11,
    'Z': 8  # Increased zombie value to make it stronger
}

PST = {
    'K': K_PST,
    'Q': Q_PST,
    'R': R_PST,
    'B': B_PST,
    'N': N_PST,
    'P': P_PST,
    'F': F_PST,
    'C': C_PST,
    'Z': Z_PST
}


class AI:
    def __init__(self, depth=4, ai_color='w'):
        self.depth = depth
        self.ai_color = ai_color
        self.opponent_color = 'b' if ai_color == 'w' else 'w'
        # Capture bonus - increased to encourage more captures
        self.capture_bonus = 0.3

    def evaluate(self, board: Board) -> int:
        ai_score = opp_score = 0
        kings = {'w': None, 'b': None}

        # Track pawns to ensure they're moving
        ai_pawns = []
        opp_pawns = []

        # Material and positional scoring
        for pos, piece in board.pieces.items():
            piece_type = "N" if isinstance(piece, Knight) else piece.__class__.__name__[0]
            value = PIECE_VALUES[piece_type]
            file = ord(pos[0]) - ord('a')
            rank = int(pos[1]) - 1

            # Apply piece square tables with color-specific orientation
            pst = PST[piece_type][7 - rank][file] if piece.color == 'b' else PST[piece_type][rank][file]

            if piece.color == self.ai_color:
                ai_score += value + pst
                if piece_type == 'P' or piece_type == 'Z':
                    ai_pawns.append((pos, rank))
            else:
                opp_score += value + pst
                if piece_type == 'P' or piece_type == 'Z':
                    opp_pawns.append((pos, rank))

            if piece_type == 'K':
                kings[piece.color] = pos  # Store position string

        # Terminal states
        if not kings.get(self.ai_color):
            return -100000
        if not kings.get(self.opponent_color):
            return 100000

        # Bonus for advanced pawns and zombies
        ai_score += self.evaluate_pawn_advancement(ai_pawns, self.ai_color)
        opp_score += self.evaluate_pawn_advancement(opp_pawns, self.opponent_color)

        # Color-specific evaluations
        ai_score += self.evaluate_king_safety(board, kings[self.ai_color], self.ai_color)
        ai_score += self.evaluate_mobility(board, self.ai_color)
        ai_score += self.evaluate_pawn_structure(board, self.ai_color)
        ai_score += self.evaluate_capture_opportunities(board, self.ai_color)

        opp_score += self.evaluate_king_safety(board, kings[self.opponent_color], self.opponent_color)
        opp_score += self.evaluate_mobility(board, self.opponent_color)
        opp_score += self.evaluate_pawn_structure(board, self.opponent_color)
        opp_score += self.evaluate_capture_opportunities(board, self.opponent_color)

        return ai_score - opp_score

    def evaluate_pawn_advancement(self, pawns, color):
        """Reward pawns and zombies that have advanced further toward promotion"""
        score = 0
        for pos, rank in pawns:
            # For white pawns, higher rank means more advanced
            if color == 'w':
                advancement = rank * 0.15  # Increased bonus for advancement
                # Extra bonus for pawns on 6th and 7th ranks
                if rank >= 5:  # 6th rank or higher
                    advancement += 0.3
                if rank >= 6:  # 7th rank
                    advancement += 0.5
            # For black pawns, lower rank means more advanced
            else:
                advancement = (7 - rank) * 0.15
                if rank <= 2:  # 3rd rank or lower
                    advancement += 0.3
                if rank <= 1:  # 2nd rank
                    advancement += 0.5

            score += advancement

        return score

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
        """Calculate mobility with bonuses for controlling center"""
        mobility = 0
        center_squares = ['d4', 'd5', 'e4', 'e5']

        for piece in board.pieces.values():
            if piece.color == color:
                moves = piece.get_valid_moves(board)

                # Basic mobility score
                mobility += len(moves) * 0.3

                # Bonus for controlling center
                center_control = sum(1 for move in moves if move in center_squares)
                mobility += center_control * 0.2

                # Extra mobility for pawns and zombies to encourage their movement
                if isinstance(piece, Peon) or isinstance(piece, Zombie):
                    mobility += len(moves) * 0.4

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

    def evaluate_capture_opportunities(self, board, color):
        """Evaluate potential captures to encourage aggressive play"""
        score = 0
        opponent_color = 'b' if color == 'w' else 'w'

        for piece in board.pieces.values():
            if piece.color == color:
                for move in piece.get_valid_moves(board):
                    # Check if move is a capture
                    if move in board.pieces and board.pieces[move].color == opponent_color:
                        captured_piece = board.pieces[move]
                        captured_type = "N" if isinstance(captured_piece, Knight) else \
                        captured_piece.__class__.__name__[0]
                        # Bonus for potential capture, weighted by the piece value
                        capture_value = PIECE_VALUES[captured_type]
                        score += capture_value * self.capture_bonus

        return score

    def alpha_beta_minimax(self, board, depth, alpha, beta, maximizing):
        if depth == 0 or board.is_checkmate():
            return self.evaluate(board)

        # Sort moves to improve pruning efficiency
        moves = self.sort_moves(board)

        if maximizing:
            max_eval = -float('inf')
            for move in moves:
                eval_score = self.alpha_beta_minimax(move, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                eval_score = self.alpha_beta_minimax(move, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def sort_moves(self, board):
        """Sort moves to improve alpha-beta pruning efficiency"""
        moves = board.generate_successors()
        scored_moves = []

        # First check if the board's turn matches the AI color
        maximizing = (board.turn == self.ai_color)

        for move in moves:
            # Quick evaluation of the move
            score = self.evaluate(move)

            # Prioritize capturing moves
            if hasattr(move, "last_move") and "captured" in move.last_move:
                score += 1000 if maximizing else -1000

            scored_moves.append((move, score))

        # Sort based on maximizing or minimizing
        if maximizing:
            scored_moves.sort(key=lambda x: x[1], reverse=True)
        else:
            scored_moves.sort(key=lambda x: x[1])

        return [move for move, _ in scored_moves]

    def choose_best_move(self, board):
        """
        Choose the best move with improved pawn movement and capture prioritization.
        First check for pawn moves that might be good, then look for captures,
        then fall back to the standard alpha-beta search.
        """
        # Generate all possible moves
        possible_moves = board.generate_successors()

        # Identify pawn/zombie moves and captures for potential prioritization
        pawn_moves = []
        capture_moves = []

        for move_board in possible_moves:
            if hasattr(move_board, "last_move"):
                # Check for pawn or zombie moves
                if any(piece_name in move_board.last_move for piece_name in ["Peon", "Zombie"]):
                    pawn_moves.append(move_board)

                # Check for captures
                if "captured" in move_board.last_move:
                    capture_moves.append(move_board)

        # For White, prioritize pawn development if in early game (pawn still on rank 2)
        if self.ai_color == 'w' and any(pos[1] == '2' for pos in board.pieces
                                        if pos in board.pieces and
                                           (isinstance(board.pieces[pos], Peon) or isinstance(board.pieces[pos],
                                                                                              Zombie)) and
                                           board.pieces[pos].color == 'w'):
            # Filter for forward pawn moves (especially e2-e4, d2-d4)
            central_pawn_moves = [move for move in pawn_moves
                                  if hasattr(move, "last_move") and
                                  any(start_pos + " to " + end_pos in move.last_move
                                      for start_pos, end_pos in
                                      [("e2", "e4"), ("d2", "d4"), ("e2", "e3"), ("d2", "d3")])]

            if central_pawn_moves:
                return central_pawn_moves[0]  # Return the first central pawn move

        # For Black, improve the zombie's play
        if self.ai_color == 'b':
            # Look for zombie moves that advance or capture
            zombie_moves = [move for move in possible_moves
                            if hasattr(move, "last_move") and
                            "Zombie" in move.last_move]

            # Sort zombie moves by preference:
            # 1. Captures
            # 2. Advancement toward opponent's side
            if zombie_moves:
                zombie_captures = [move for move in zombie_moves if "captured" in move.last_move]
                if zombie_captures:
                    return zombie_captures[0]  # Return a capturing zombie move

                # Otherwise, find the most advanced zombie move
                best_zombie_move = None
                best_rank = -1

                for move in zombie_moves:
                    # Extract the target position from the last_move attribute
                    if " to " in move.last_move:
                        target_pos = move.last_move.split(" to ")[1].split()[0]
                        target_rank = int(target_pos[1])

                        # For black, lower rank numbers are better (closer to white's side)
                        if target_rank < best_rank or best_rank == -1:
                            best_rank = target_rank
                            best_zombie_move = move

                if best_zombie_move:
                    return best_zombie_move

        # Prioritize captures if available (for both colors)
        if capture_moves:
            # Sort captures by value of captured piece
            best_capture = None
            highest_value = -1

            for move in capture_moves:
                # Extract the captured piece information
                captured_info = move.last_move.split("captured ")[1].split()[0]
                captured_type = captured_info[0]  # First letter indicates piece type

                # Convert to evaluation key if needed
                if captured_type == "K":
                    piece_value = PIECE_VALUES["K"]
                elif captured_type == "N" or captured_type == "n":
                    piece_value = PIECE_VALUES["N"]
                else:
                    piece_value = PIECE_VALUES.get(captured_type, 1)

                if piece_value > highest_value:
                    highest_value = piece_value
                    best_capture = move

            if best_capture:
                return best_capture

        # If no suitable pawn move or capture, use alpha-beta search
        best_move = None
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')
        is_maximizing = (board.turn == self.ai_color)

        # Use move ordering for better alpha-beta efficiency
        sorted_moves = self.sort_moves(board)

        for move in sorted_moves:
            score = self.alpha_beta_minimax(move, depth=self.depth - 1, alpha=alpha, beta=beta,
                                            maximizing=not is_maximizing)
            if score > best_score:
                best_score = score
                best_move = move
                alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        return best_move

    def extract_captured_pieces(self, previous_board: Board, current_board: Board) -> list:
        captured_pieces = []
        for pos, piece in previous_board.pieces.items():
            if pos not in current_board.pieces:
                captured_pieces.append(piece)
        return captured_pieces