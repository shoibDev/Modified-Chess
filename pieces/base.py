from abc import ABC

class Piece(ABC):
    def __init__(self, color: str, position: str):
        self.color = color
        self.position = position

    def get_valid_moves(self, board) -> list:
        """Must be overridden by subclasses"""
        raise NotImplementedError

    def __repr__(self):
        """Returns a simple representation ('wB' for white Bishop)."""
        symbol = "N" if self.__class__.__name__ == "Knight" else self.__class__.__name__[0]
        return f"{self.color}{symbol}"