from arena import Arena
from knights.knight import Knight
import sys

class Main:
    def __init__(self, instruction_file) -> None:
        self.arena = Arena(size=8)
        self.arena.deploy_knights()
        self.contents = self._read_input_file(instruction_file)
        self.deploy_knights()
        # self.items = {
        #     'axe': self.arena.items.get('axe'),
        #     'dagger': self.arena.items.get('dagger'),
        #     'helmet': self.arena.items.get('helmet'),
        #     'magic_staff': self.arena.items.get('magic_staff')
        # }

        self.items = {
            'axe': self.arena.axe,
            'dagger': self.arena.dagger,
            'helmet': self.arena.helmet,
            'magic_staff': self.arena.magic_staff,
        }
        self.item_monitor = {}

    def deploy_knights(self):
        self.arena.deploy_knights()

    @property
    def leaderboard(self) -> dict:
        instructions = self._cleanup_instruction(self.contents)
        self._read_movements(instructions)    
        return self.finalized_results()

    def finalized_results(self) -> dict:
        results = {}
        results.update(self.finalize_knight_monitor())
        results.update(self.finalize_item_monitor())
        return results
        
    @staticmethod
    def _read_input_file(instruction_file):
        with open(instruction_file) as f:
            contents = f.readlines()
        return contents

    @staticmethod
    def _cleanup_instruction(contents:list) -> list:
        instructions = []
        for instruction in contents:
            line_text = instruction.split(':')
            knight = line_text[0].strip()
            direction = line_text[1].strip()
            instructions.append((knight, direction))
        return instructions

    def _read_movements(self, instructions):
        for move in instructions:
            key = move[0]
            direction = move[1]
            if self._is_invalid_key(key):
                self._execute_move(key=key, direction=direction)
            else:
                print(f'Cannot execute movement. Invalid instruction key: {key}')

    @staticmethod
    def _is_invalid_key(key) -> bool:
        return key in 'RBGY'

    def _execute_move(self, key:str, direction:str) -> None:
        results = {}
        if key == 'R':
            self.arena.red_knight.move(direction=direction)
            self.arena.position_knight_to_arena(self.arena.red_knight)
        elif key == 'B':
            self.arena.blue_knight.move(direction=direction)
            self.arena.position_knight_to_arena(self.arena.blue_knight)
        elif key == 'G':
            self.arena.green_knight.move(direction=direction)
            self.arena.position_knight_to_arena(self.arena.green_knight)
        elif key == 'Y':
            self.arena.yellow_knight.move(direction=direction)
            self.arena.position_knight_to_arena(self.arena.yellow_knight)
        
    @staticmethod
    def _finalize_result(knight:Knight) -> list:
        item = knight.item
        if item:
            item = str(item)
        return [knight.position, knight.status, item, knight.attack_score, knight.defense_score]

    def finalize_knight_monitor(self):
        results = {}
        results['red'] = self._finalize_result(self.arena.red_knight)
        results['blue'] = self._finalize_result(self.arena.blue_knight)
        results['green'] = self._finalize_result(self.arena.green_knight)
        results['yellow'] = self._finalize_result(self.arena.yellow_knight)
        return results

    def finalize_item_monitor(self) -> None:
        for item_str, item_obj in self.items.items():
            self.item_monitor[item_str] = [item_obj.position, item_obj.equipped]
        return self.item_monitor

if __name__ == '__main__':
    instruction_file = sys.argv[1]
    battle_knights = Main(instruction_file=instruction_file)
    for element, element_details in battle_knights.leaderboard.items():
        print(f'{element}: {element_details}')