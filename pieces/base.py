class Piece:
    def __init__(self, color: str, position: str):
        self.color = color
        self.position = position

    def get_valid_moves(self, board):
        """Must be overridden by subclasses"""
        raise NotImplementedError

    def __repr__(self):
        """Returns a simple representation (e.g., 'wB' for white Bishop)."""
        return f"{self.color}{self.__class__.__name__[0]}"