from .item import Item

class Helmet(Item):
    def __init__(self) -> None:
        super().__init__(start_position=(5,5))
        self.score_type = 'Defense'
        self.score = 1

    def __str__(self) -> str:
        return 'helmet'

    def __repr__(self) -> str:
        return 'helmet'