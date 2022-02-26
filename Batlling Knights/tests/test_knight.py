import pytest
from knights.knight import Knight
from items.item import Item
from items.magic_staff import MagicStaff
from items.axe import Axe

class TestKnight:
    @pytest.fixture
    def knight(self):
        def _create_knight(position:tuple) -> Knight:
            return Knight(start_position=position)
        return _create_knight

    @pytest.fixture
    def item(self):
        return MagicStaff()

    def test_attributes_initialize_values(self, knight):
        knight = knight(position=(0,0))
        assert knight.status == 'LIVE'
        assert knight.position == (0,0)
        assert not knight.prev_position
        assert knight.can_move == True
        assert knight.attack_score == 1
        assert knight.defense_score == 1
        assert not knight.item

    def test_knight_movement(self, knight):
        knight = knight(position=(0,0))
        knight.move(direction='S')
        assert knight.status == 'LIVE'
        assert knight.position == (1,0)
        assert knight.prev_position == (0,0)
        assert knight.can_move == True
        assert knight.attack_score == 1
        assert knight.defense_score == 1
        assert not knight.item

    def test_knight_more_movements(self, knight):
        knight = knight(position=(0,7))
        knight.move(direction='S')
        knight.move(direction='W')
        knight.move(direction='N')
        knight.move(direction='E')
        knight.move(direction='W')
        assert knight.status == 'LIVE'
        assert knight.position == (0,6)
        assert knight.prev_position == (0,7)
        assert knight.can_move == True
        assert knight.attack_score == 1
        assert knight.defense_score == 1
        assert not knight.item

    def test_drowned_knight(self, knight):
        knight = knight(position=(0,7))
        knight.move(direction='S')
        knight.move(direction='E')
        assert knight.status == 'DROWNED'
        assert not knight.position
        assert knight.prev_position == (1,7)
        assert knight.can_move == False
        assert knight.attack_score == 0
        assert knight.defense_score == 0
        assert not knight.item

    def test_drowned_knight_with_item(self, knight, item):
        knight = knight(position=(0,7))
        knight.item = item
        knight.move(direction='S')
        assert knight.item

        knight.move(direction='E')
        assert knight.status == 'DROWNED'
        # assert knight.item.equipped == False
        assert not knight.item
        
    def test_dead_knight(self, knight, item):
        knight = knight(position=(5,5))
        knight.item = item
        knight.move('S')
        assert knight.item

        knight.status = 'DEAD'
        assert knight.status == 'DEAD'
        assert knight.position == (6,5)
        assert knight.prev_position == (5,5)
        assert knight.can_move == False
        assert knight.attack_score == 0
        assert knight.defense_score == 0
        # assert knight.item.equipped == False
        assert not knight.item



