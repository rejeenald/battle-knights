import pytest
from main import Main

class TestMain:
    @pytest.fixture
    def main(self):
        def _initialize_main(instruction_file):
            sample_path = "/".join(['samples', instruction_file])
            battle_knights = Main(instruction_file=sample_path)
            return battle_knights

        return _initialize_main

    def test_battle_knights(self, main):
        battle_knights = main(instruction_file='moves.txt')
        leaderboard = battle_knights.leaderboard
        keys = list(leaderboard.keys())
        assert 'red' in keys
        assert 'blue' in keys
        assert 'green' in keys
        assert 'yellow' in keys
        assert 'axe' in keys
        assert 'dagger' in keys
        assert 'helmet' in keys
        assert 'magic_staff' in keys
        assert leaderboard['red'] == [(2,2), 'LIVE', 'axe', 3, 1]
        assert leaderboard['blue'] == [(5,2), 'LIVE', 'magic_staff', 2, 2]
        assert leaderboard['green'] == [(5,5), 'LIVE', 'helmet', 1, 2]
        assert leaderboard['yellow'] == [(2,5), 'LIVE', 'dagger', 2, 1]
        assert leaderboard['axe'] == [(2,2), True]
        assert leaderboard['dagger'] == [(2,5), True]
        assert leaderboard['helmet'] == [(5,5), True]
        assert leaderboard['magic_staff'] == [(5,2), True]

    def test_battle_knights_with_dead_and_drowned_knights_equipped_with_item(self, main):
        battle_knights = main(instruction_file='moves_with_dead_knights.txt')
        leaderboard = battle_knights.leaderboard
        assert leaderboard['red'] == [(2,4), 'DEAD', None, 0, 0]
        assert leaderboard['yellow'] == [(2,4), 'LIVE', 'dagger', 2, 1]
        assert leaderboard['blue'] == [(5,2), 'LIVE', 'magic_staff', 2, 2]
        assert leaderboard['green'] == [None, 'DROWNED', None, 0, 0]
        assert leaderboard['axe'] == [(2,4), False]
        assert leaderboard['dagger'] == [(2,4), True]
        assert leaderboard['helmet'] == [(5,5), False]
        assert leaderboard['magic_staff'] == [(5,2), True]

    def test_battle_knights_with_drowned_knights_dropping_item_to_last_valid_tile(self, main):
        battle_knights = main(instruction_file='moves_dropping_item_to_last_valid_tile.txt')
        leaderboard = battle_knights.leaderboard
        assert leaderboard['red'] == [(0,0), 'LIVE', None, 1, 1]
        assert leaderboard['yellow'] == [(0,7), 'LIVE', None, 1, 1]
        assert leaderboard['blue'] == [(5,4), 'LIVE', 'magic_staff', 2, 2]
        assert leaderboard['green'] == [None, 'DROWNED', None, 0, 0]
        assert leaderboard['axe'] == [(2,2), False]
        assert leaderboard['dagger'] == [(2,5), False]
        assert leaderboard['helmet'] == [(5,7), False]
        assert leaderboard['magic_staff'] == [(5,4), True]
