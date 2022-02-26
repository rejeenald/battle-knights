from .knight import Knight

class RedKnight(Knight):
    def __init__(self, start_position=(0,0)) -> None:
        super().__init__(start_position=start_position)

    def __repr__(self) -> str:
        return 'Red'

    def __str__(self) -> str:
        return 'Red'