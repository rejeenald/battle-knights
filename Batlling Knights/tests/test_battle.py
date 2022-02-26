import pytest
from knights.knight import Knight
from items.magic_staff import MagicStaff
from items.axe import Axe
from items.helmet import Helmet
from items.item import Item
from battle import Battle

class TestBattle:
    @pytest.fixture
    def knight(self):
        def _create_knight(position:tuple) -> Knight:
            return Knight(start_position=position)
        return _create_knight

    @pytest.fixture
    def battle(self):
        def _initiate_battle(attacker:Knight, defender:Knight) -> None:
            battle = Battle(attacker=attacker, defender=defender)
            battle.fight()
            return battle
        return _initiate_battle
    
    @pytest.fixture
    def battle_match(self, knight, battle):
        def _create_battle_case(attacker_item:Item, defender_item: Item) -> Battle:
            battle_field_tile = defender_item.position
            attacker = knight(position=battle_field_tile)
            attacker.prev_position = (5,1)
            defender = knight(position=battle_field_tile)
            attacker.item = attacker_item
            defender.item = defender_item
            return battle(attacker=attacker, defender=defender)
        return _create_battle_case

    @pytest.fixture
    def invalid_battle_match(self, knight, battle):
        def _create_battle_case(item:Item, no_item:str) -> Item:
            attacker = knight(position=(item.position))
            attacker.prev_position = (4,2)
            defender = knight(position=(item.position))
            if no_item == 'attacker':
                defender.item = item
                attacker.item = None
            else:
                attacker.item = item
                defender.item = None
            battle_match = battle(attacker=attacker, defender=defender)
            battle_match.fight()
            return battle_match
        return _create_battle_case

    def test_attributes_initialize_values(self, battle_match):
        attack_item = MagicStaff()
        defend_item = Axe()
        battle = battle_match(attacker_item=attack_item, defender_item=defend_item)
        assert battle.element_of_surprise_score == 0.5
        assert battle.attacker_knight
        assert battle.defender_knight

    def test_battle_match(self, battle_match):
        defend_item = MagicStaff()
        attack_item = Axe()
        battle = battle_match(attacker_item=attack_item, defender_item=defend_item)
        defender_loser = battle.loser 
        attacker_winner = battle.winner

        assert defender_loser.status == 'DEAD'
        assert not defender_loser.item
        assert defender_loser.attack_score == 0
        assert defender_loser.defense_score == 0
        assert defender_loser.position == (5,2)
        assert defender_loser.position == defend_item.position
        assert defender_loser.position == attacker_winner.position

        assert attacker_winner.status == 'LIVE'
        assert str(attacker_winner.item) == 'axe'
        assert attacker_winner.attack_score == 3
        assert attacker_winner.defense_score == 1
        assert attacker_winner.position == (5,2)
        assert attacker_winner.position == defend_item.position
        assert attacker_winner.position == defender_loser.position
        
    def test_battle_match_defender_knight_winner(self, battle_match):
        defend_item = MagicStaff()
        attack_item = Helmet()
        battle = battle_match(attacker_item=attack_item, defender_item=defend_item)
        attacker_loser = battle.loser 
        defender_winner = battle.winner
        
        assert attacker_loser.status == 'DEAD'
        assert not attacker_loser.item
        assert attacker_loser.attack_score == 0
        assert attacker_loser.defense_score == 0
        assert attacker_loser.position == (5,2)
        assert attacker_loser.position == defend_item.position
        assert attacker_loser.position == defender_winner.position

        assert defender_winner.status == 'LIVE'
        assert str(defender_winner.item) == 'magic_staff'
        assert defender_winner.attack_score == 2
        assert defender_winner.defense_score == 2
        assert defender_winner.position == (5,2)
        assert defender_winner.position == defend_item.position
        assert defender_winner.position == attacker_loser.position

    def test_battle_invalid_attacker_no_item(self, invalid_battle_match):
        battle = invalid_battle_match(item=MagicStaff(), no_item='attacker')
        assert not battle.winner
        assert not battle.loser
        assert battle.attacker_knight.position == (4,2)
        assert not battle.attacker_knight.item