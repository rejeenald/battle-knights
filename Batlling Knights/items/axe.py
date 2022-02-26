from .item import Item

class Axe(Item):
    def __init__(self) -> None:
        super().__init__(start_position=(2,2))
        self.score_type = 'Attack'
        self.score = 2

    def __str__(self) -> str:
        return 'axe'

    def __repr__(self) -> str:
        return 'axe'