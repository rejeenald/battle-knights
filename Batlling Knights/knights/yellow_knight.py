from .knight import Knight

class YellowKnight(Knight):
    def __init__(self, start_position=(0,7)) -> None:
        super().__init__(start_position=start_position)
        
    def __repr__(self) -> str:
        return 'Yellow'

    def __str__(self) -> str:
        return 'Yellow'