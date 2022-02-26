import pytest
from arena import Arena
from items.helmet import Helmet
from knights.knight import Knight

class TestArena:
    @pytest.fixture
    def arena(self):
        def _create_arena(size:int) -> list:
            arena = Arena(size=size)
            arena.deploy_knights()
            return arena
        return _create_arena
    
    def move_to_direction(self, arena:Arena, knight:Knight, times:int, direction:str) -> None:
        for i in range(times):
            knight.move(direction)
            arena.position_knight_to_arena(knight)

    def test_attributes_initialize_values(self, arena):
        arena_field = arena(size=8)
        assert type(arena_field.arena) == list
        assert type(arena_field.arena[0]) == list
        assert len(arena_field.arena)  == 8
        assert len(arena_field.arena[0]) == 8
        assert len(arena_field.arena[7]) == 8
        assert arena_field.arena_size == 8

    def test_items_positions_in_arena(self, arena):
        arena_field = arena(size=8)
        assert arena_field.axe.position == (2,2)
        assert arena_field.dagger.position == (2,5)
        assert arena_field.helmet.position == (5,5)
        assert arena_field.magic_staff.position == (5,2)

    def test_items_equipped_status_in_arena(self, arena):
        arena_field = arena(size=8)
        assert arena_field.axe.equipped == False
        assert arena_field.dagger.equipped == False
        assert arena_field.helmet.equipped == False
        assert arena_field.magic_staff.equipped == False

    def test_items_str_representation(self, arena):
        arena_field = arena(size=8)
        assert arena_field.axe.__str__() == 'axe'
        assert arena_field.dagger.__str__() == 'dagger'
        assert arena_field.helmet.__str__() == 'helmet'
        assert arena_field.magic_staff.__str__() == 'magic_staff'

    def test_creating_knights_in_the_arena(self, arena):
        arena_field = arena(size=8)
        red_knight = arena_field.red_knight
        assert red_knight.position == (0,0)
        assert arena_field.arena[0][0].get('knights') == {red_knight:'LIVE'}

        blue_knight = arena_field.blue_knight
        assert blue_knight.position == (7,0)
        assert arena_field.arena[7][0].get('knights') == {blue_knight:'LIVE'}

        green_knight = arena_field.green_knight
        assert green_knight.position == (7,7)
        assert arena_field.arena[7][7].get('knights') == {green_knight:'LIVE'}

        yellow_knight = arena_field.yellow_knight
        assert yellow_knight.position == (0,7)
        assert arena_field.arena[0][7].get('knights') == {yellow_knight:'LIVE'}
        
    def test_knight_equipping_an_item(self, arena):
        arena_field = arena(size=8)
        red_knight = arena_field.red_knight

        red_knight.move('E')
        arena_field.position_knight_to_arena(red_knight)
        assert not arena_field.red_knight.item
        assert red_knight.position == (0,1)
        assert arena_field.arena[0][0] == {}
        assert arena_field.arena[0][1] == {'knights': {red_knight: 'LIVE'}}

        red_knight.move('E')
        arena_field.position_knight_to_arena(red_knight)
        assert not arena_field.red_knight.item
        assert red_knight.position == (0,2)
        assert arena_field.arena[0][1] == {}
        assert arena_field.arena[0][2] == {'knights': {red_knight: 'LIVE'}}

        red_knight.move('S')
        arena_field.position_knight_to_arena(red_knight)
        assert not arena_field.red_knight.item
        assert red_knight.position == (1,2)
        assert arena_field.arena[0][2] == {}
        assert arena_field.arena[1][2] == {'knights': {red_knight: 'LIVE'}}

        red_knight.move('S')
        arena_field.position_knight_to_arena(red_knight)
        assert str(arena_field.red_knight.item) == 'axe'
        assert red_knight.position == (2,2)
        assert arena_field.arena[1][2] == {}
        assert arena_field.arena[2][2] == {'items': [arena_field.red_knight.item], 'knights': {red_knight: 'LIVE'}}
    
    def test_knight_ignoring_an_item(self, arena):
        arena_field = arena(size=8)
        red_knight = arena_field.red_knight
        self.move_to_direction(arena=arena_field, knight=red_knight, times=2, direction='E')
        self.move_to_direction(arena=arena_field, knight=red_knight, times=2, direction='S')
        assert str(arena_field.red_knight.item) == 'axe'

        self.move_to_direction(arena=arena_field, knight=red_knight, times=3, direction='E')
        assert str(arena_field.red_knight.item) == 'axe'
        assert red_knight.position == (2,5)
        assert arena_field.arena[2][4] == {}
        assert arena_field.dagger in arena_field.arena[2][5].get('items')
        assert arena_field.axe in arena_field.arena[2][5].get('items')
        assert arena_field.red_knight in arena_field.arena[2][5].get('knights')

    def test_knight_battling_other_knight_without_equipped_item(self, arena):
        arena_field = arena(size=8)
        red_knight = arena_field.red_knight
        self.move_to_direction(arena=arena_field, knight=red_knight, times=7, direction='E')
        assert red_knight.status == 'LIVE'
        assert red_knight.position == (0,6) 
        assert not red_knight.item

    def test_knight_battling_other_knight_with_items(self, arena):
        arena_field = arena(size=8)
        red_knight = arena_field.red_knight
        blue_knight = arena_field.blue_knight
        self.move_to_direction(arena=arena_field, knight=red_knight, times=2, direction='E')
        self.move_to_direction(arena=arena_field, knight=red_knight, times=3, direction='S')
        assert str(red_knight.item) == 'axe'
        
        self.move_to_direction(arena=arena_field, knight=blue_knight, times=2, direction='E')
        self.move_to_direction(arena=arena_field, knight=blue_knight, times=4, direction='N')
        
        assert not red_knight.item
        assert red_knight.status == 'DEAD'
        assert red_knight.can_move == False
        assert red_knight.position == (3,2)

        assert blue_knight.position == (3,2)
        assert blue_knight.can_move == True
        assert str(blue_knight.item) == 'magic_staff'
        assert blue_knight.item.equipped == True
        assert blue_knight.item.position == (3,2)

        self.move_to_direction(arena=arena_field, knight=red_knight, times=2, direction='S')
        assert red_knight.position == (3,2)

        self.move_to_direction(arena=arena_field, knight=blue_knight, times=2, direction='S')
        assert blue_knight.position == (5,2)

    def test_knight_moving_outside_arena_to_drown(self, arena):
        arena_field = arena(size=8)
        red_knight = arena_field.red_knight
        self.move_to_direction(arena=arena_field, knight=red_knight, times=1, direction='W')
        assert red_knight.status == 'DROWNED'

    def test_knight_with_item_moving_outside_arena_to_drown(self, arena):
        arena_field = arena(size=8)
        yellow_knight = arena_field.yellow_knight
        self.move_to_direction(arena=arena_field, knight=yellow_knight, times=2, direction='W')
        self.move_to_direction(arena=arena_field, knight=yellow_knight, times=2, direction='S')
        assert str(yellow_knight.item) == 'dagger'
        
        self.move_to_direction(arena=arena_field, knight=yellow_knight, times=3, direction='N')
        assert yellow_knight.status == 'DROWNED'

        prev_position = yellow_knight.prev_position
        assert arena_field.arena[prev_position[0]][prev_position[1]].get('items') == [yellow_knight.unequipped_item]