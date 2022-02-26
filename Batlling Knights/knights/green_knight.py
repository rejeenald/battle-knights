from .knight import Knight

class GreenKnight(Knight):
    def __init__(self, start_position=(7,7)) -> None:
        super().__init__(start_position=start_position)
        
    def __repr__(self) -> str:
        return 'Green'

    def __str__(self) -> str:
        return 'Green'