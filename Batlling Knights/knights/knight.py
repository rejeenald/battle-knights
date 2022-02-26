from items.item import Item

class Knight:
    def __init__(self, start_position:tuple, arena_size:int=8) -> None:
        self.arena_size = 8
        self.position = start_position
        self.prev_position = None
        self._status = 'LIVE'
        self.can_move = True
        self.attack_score = 1
        self.defense_score = 1
        self._item = None
        self.unequipped_item = None

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, found_item:Item) -> None:
        if found_item:
            # print(f'Equipping item {found_item}.')
            self._item = found_item
            self._item.equipped = True
            self._item.position = self.position
            self._increase_attribute_scores()
        else:
            self._item = None

    def move(self, direction:str) -> None:
        if self.can_move:
            ew_direction = {'E': 1, 'W': -1}
            sn_direction = {'S': 1, 'N': -1}
            self.prev_position = self.position
            # print(f'Moving to {direction}')
            self.position = self._update_position(direction, ew_direction, sn_direction)
            # print(f'Coordinate: {self.position}')
            if self._item:
                self._item.position = self.position
        else:
            print(f'Knight is {self.status}. Cannot move.')

    def _update_position(self, direction:str, ew_direction:dict, sn_direction:dict) -> tuple:
        position = list(self.position)
        if direction in ew_direction.keys():
            position[1] += ew_direction.get(direction.upper())
        if direction in sn_direction.keys():
            position[0] += sn_direction.get(direction.upper())

        return self._finalize_validity_of_position_coordinates(position)

    def _finalize_validity_of_position_coordinates(self, coordinate):
        final_coordinate = []
        for num in coordinate:
            if self._coordinate_num_inside_arena(num):
                final_coordinate.append(num)
            else:
                self.status = 'DROWNED'
                return

        # print(f'Final coordinate: {final_coordinate}')
        return tuple(final_coordinate)

    def _coordinate_num_inside_arena(self, num) -> bool:
        coordinate_numbers = [i for i in range(self.arena_size)]
        return num in coordinate_numbers

    def _increase_attribute_scores(self) -> None:
        if self._item.score_type == 'Attack':
            self.attack_score += self._item.score
        elif self._item.score_type == 'Defense':
            self.defense_score += self._item.score
        else:
            self.attack_score += self._item.score
            self.defense_score += self.item.score

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, status:str) -> None:
        self._status = status
        if status != 'LIVE':
            self._set_common_status_details_for_dead_and_drowned_knights()
            # print(f"Reset attack and defense scores to zero. Disabled movement. Status is {status}.")

    def _set_common_status_details_for_dead_and_drowned_knights(self) -> None:
        self._unequip_item()
        self.item = None
        self.attack_score = 0
        self.defense_score = 0
        self.can_move = False

    def _unequip_item(self):
        if self._item:
            self.unequipped_item = self._item
            self.unequipped_item.equipped = False

    def __str__(self) -> str:
        return 'Knight'



       