from knights.knight import Knight

class Battle:
    def __init__(self, attacker:Knight, defender:Knight) -> None:
        self.element_of_surprise_score = 0.5
        self.attacker_knight = attacker
        self.defender_knight = defender
        self._winner = None
        self._loser = None

    @property
    def winner(self) -> Knight:
        return self._winner

    @winner.setter
    def winner(self, knight:Knight) -> None:
        self._winner = knight

    @property
    def loser(self) -> Knight:
        return self._loser

    @loser.setter
    def loser(self, knight:Knight) -> None:
        self._loser = knight

    def fight(self) -> None:
        if self._can_do_battle():
            damage_done_by_attacker = self.attack()
            if damage_done_by_attacker > 0:
                self.attacker_knight.status = 'LIVE'
                self.defender_knight.status = 'DEAD'
                self.winner = self.attacker_knight
                self.loser = self.defender_knight
            elif damage_done_by_attacker == 0:
                self.attacker_knight.status = 'DEAD'
                self.defender_knight.status = 'DEAD'
                self.winner = None
                self.loser = None
            else:
                self.defender_knight.status = 'LIVE'
                self.attacker_knight.status = 'DEAD'
                self.winner = self.defender_knight
                self.loser = self.attacker_knight
        else:
            print('Cannot do battle. One of the Knights has no equipped item.')
            self._revert_movement()
        
    def _can_do_battle(self) -> bool:
        attack_item = self.attacker_knight.item
        defend_item = self.defender_knight.item
        if attack_item and defend_item:
            return True
        return False

    def _revert_movement(self) -> None:
        self.attacker_knight.position = self.attacker_knight.prev_position
        if self.attacker_knight.item:
            self.attacker_knight.item.position = self.attacker_knight.prev_position

    def attack(self) -> int:
        if self.attacker_knight.item:
            damage = self.attack_score - self.defender_knight.defense_score
            return damage
        
    @property
    def attack_score(self) -> int:
        score = self.element_of_surprise_score
        score += self.attacker_knight.attack_score
        return score
