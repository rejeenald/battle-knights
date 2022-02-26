from .knight import Knight

class BlueKnight(Knight):
    def __init__(self, start_position=(7,0)) -> None:
        super().__init__(start_position=start_position)

    def __repr__(self) -> str:
        return 'Blue'

    def __str__(self) -> str:
        return 'Blue'