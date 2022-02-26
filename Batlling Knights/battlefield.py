import numpy as np
from item.item import Item
from item.axe import axe
from item.dagger import Dagger
from item.helmet import Helmet
from item.magicstaff import MagicStaff
from knight import Knight

class BattleField:
    def ___init__(self, movements={}, knights:list=[], items:list=[]) -> None:
        self.setup_knights(knights)
        self.setup_items()
        self._setup_arena()
        self._equipped_items = self._monitor_equipped_items()
        self.movements = movements

    def _setup_knights(self) -> None:
        self.red_knight = Knight(start_position=(0,0))
        self.blue_knight = Knight(start_position=(7,0))
        self.green_knight = Knight(start_position=(7,7))
        self.yellow_knight = Knight(start_position=(0,7))

    def _setup_items(self) -> None:
        self.axe = Axe()
        self.dagger = Dagger()
        self.helmet = Helmet()
        self.magicstaff = MagicStaff()

    def _setup_arena(self) -> None:
        matrix = np.empty((), dtype=object)
        matrix[()] = ()
        self.arena = np.empty((), dtype=object)
        self._position_objects_in_arena()

    def _position_objects_in_arena(self) -> None:
        self.arena[0,0] = (self.red_knight, 0)
        self.arena[7,0] = (self.blue_knight, 0)
        self.arena[7,7] = (self.green_knight, 0)
        self.arena[0,7] = (self.yellow_knight, 0)
    
    def _monitor_equipped_items(self) -> dict:
        return {
            'Axe': self.Axe.equipped,
            'Dagger': self.Dagger.equipped,
            'Helmet': self.Helmet.equipped,
            'MagicStaff': self.MagicStaff.equipped,
        }
    
    def begin_battle(self) -> dict:
        for knight, direction in self.movements.items():
            if knight == 'R':
                self.red_knight.move(direction=direction)
                item = self.get_item(self.red_knight.position)
                if item:
                    self.red_knight.item = item
            elif knight == 'B':
                self.blue_knight.move(direction=direction)
            elif knight == 'G':
                self.green_knight.move(direction=direction)
            elif knight == 'Y':
                self.yellow_knight.move(direction=direction)
            else:
                print(f"Invalid Knight object.")
                return None
            
    

    def update_arena(self, arena:np.ndarray) -> np.ndarray:
        # update position of knights, status
        # update items
        return self.area

    def _item_exists_in_tile(self, position:tuple) -> Boolean:
        return item_exists

    def _knight_exists_in_tile(self, position:tuple) -> Boolean:
        return knight_exists_in_tile

    def _is_tile_valid(self, position:tuple) -> Boolean:
        return valid


    
