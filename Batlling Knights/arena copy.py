from battle import Battle
from items.item import Item
from items.axe import Axe
from items.dagger import Dagger
from items.helmet import Helmet
from items.magic_staff import MagicStaff
from knights.knight import Knight
from knights.red_knight import RedKnight
from knights.blue_knight import BlueKnight
from knights.green_knight import GreenKnight
from knights.yellow_knight import YellowKnight

class Arena:
    def __init__(self, size:int=8) -> None:
        self.arena_size = size
        self.arena = [[{} for i in range(size)] for j in range(size)]
        self._forge_items()
  
    def deploy_knights(self) -> Knight:
        self.red_knight = RedKnight()
        self.blue_knight = BlueKnight()
        self.green_knight = GreenKnight()
        self.yellow_knight = YellowKnight()
        self._position_knights_set_to_arena()

    def _position_knights_set_to_arena(self) -> None:
        self._position_knight_to_arena(self.red_knight)
        self._position_knight_to_arena(self.blue_knight)
        self._position_knight_to_arena(self.green_knight)
        self._position_knight_to_arena(self.yellow_knight)

    def _position_knight_to_arena(self, knight:Knight) -> None:
        coordinate = knight.position
        self.arena[coordinate[0]][coordinate[1]] = {'knights': {knight:knight.status}}

    def _forge_items(self) -> None:
        self.axe = Axe()
        self.dagger = Dagger()
        self.helmet = Helmet()
        self.magic_staff = MagicStaff()
        self._position_item_set_to_arena()

    def _position_item_set_to_arena(self) -> None:
        self._position_item_to_arena(self.axe)
        self._position_item_to_arena(self.dagger)
        self._position_item_to_arena(self.helmet)
        self._position_item_to_arena(self.magic_staff)

    def _position_item_to_arena(self, item:Item) -> None:
        coordinate = item.position
        self.arena[coordinate[0]][coordinate[1]] = {'items': [item]}

    def position_knight_to_arena(self, knight: Knight, from_attempted_battle:bool=False) -> None:
        if knight.status != 'DROWNED':
            new_position = knight.position
            occupant = self.arena[new_position[0]][new_position[1]]
            
            if not from_attempted_battle and knight.can_move:
                self._remove_from_previous_tile(knight)

            if occupant:
                occupant_knights = occupant.get('knights')
                if occupant_knights:
                    occupant_knights[knight] = knight.status
                    self._engage_battle(knight, occupant_knights)
                else:
                    occupant['knights'] = {knight:knight.status}
                    if not knight.item:
                        self._equip_item(knight, occupant.get('items'))
                    else:
                        occupant['items'].append(knight.item)
            else:
                self.arena[new_position[0]][new_position[1]] = {'knights': {knight:knight.status}}
        else:
            print(f'Knight drowned.')
            item = knight.unequipped_item
            self._remove_from_previous_tile(knight)
            if item:
                self._position_item_to_arena(item)
            
        self._print_arena()

    def _remove_from_previous_tile(self, knight:Knight) -> None:
        prev_position = knight.prev_position
        if prev_position:
            content = self.arena[prev_position[0]][prev_position[1]]
            self._remove_knight_from_tile(knight, content)
            self._remove_item_from_tile(knight, content)

    @staticmethod
    def _remove_knight_from_tile(knight, content) -> None:
        k = content.get('knights')
        if len(k.keys()) > 1:
            content.get('knights').pop(knight)
        else:
            content.pop('knights')

    @staticmethod
    def _remove_item_from_tile(knight, content) -> None:
        items = content.get('items')
        if items:
            if len(items) > 1:
                items.remove(knight.item)
            else:
                content.pop('items')
        
    def _engage_battle(self, knight, occupant):
        occupant_knight = list(occupant.keys())[0]
        if occupant_knight.status == 'LIVE':
            battle = Battle(attacker=knight, defender=occupant_knight)
            battle.fight()
            if battle.loser:
                self.position_knight_to_arena(battle.loser, from_attempted_battle=True)
            if battle.attacker_knight.status == 'LIVE' and not battle.winner:
                self.position_knight_to_arena(battle.attacker_knight, from_attempted_battle=True)
           
    def _equip_item(self, knight, items:list) -> Item:
        max_score = 1
        item_with_better_score = None
        if len(items) > 1:
            for item in items:
                if item.score > max_score:
                    max_score = item.score
                    item_with_better_score = item
            knight.item = item_with_better_score
        else:
            knight.item = items[0]

    @staticmethod
    def _list_down_items(knight_item, occupant_item) -> list:

        items = []
        if type(occupant_item) == list:
            items.append(knight_item)
            items += occupant_item
        else:
            items = [knight_item, occupant_item]
        return items

    def _print_arena(self):
        for row in self.arena:
            print(row)
        print('\n')