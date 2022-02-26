from .item import Item

class Dagger(Item):
    def __init__(self) -> None:
        super().__init__(start_position=(2,5))
        self.score_type = 'Attack'
        self.score = 1

    def __str__(self) -> str:
        return 'dagger'

    def __repr__(self) -> str:
        return 'dagger'