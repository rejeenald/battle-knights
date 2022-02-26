from .item import Item

class MagicStaff(Item):
    def __init__(self) -> None:
        super().__init__(start_position = (5,2))
        self.score_type = 'Attack and Defense'
        self.score = 1

    def __str__(self) -> str:
        return 'magic_staff'

    def __repr__(self) -> str:
        return 'magic_staff'