import pytest
from items.item import Item

class TestItem:
    @pytest.fixture
    def item(self):
        return Item(start_position=(0,0))

    def test_item_position(self, item):
        previous_position = item.position
        item.position = (0,1)
        assert previous_position == (0,0)
        assert item.position == (0,1)

    def test_item_equipped(self, item):
        previous_equipped_status = item.equipped
        item.equipped = True
        assert previous_equipped_status == False
        assert item.equipped == True

    def test_item_str_represention(self, item):
        assert item.__str__() == 'Item'