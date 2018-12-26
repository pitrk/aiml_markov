from typing import List

from markov_libs import Field


class BoardEmptyException(Exception):
    pass


class BoardNoDefaultException(Exception):
    pass


class WorldFactory:
    def __init__(self, data: dict):
        self.data = data
        self.board = []

    def board_generator(self):
        size = self._get_board_size()
        self._generate_default_board(size['x'], size['y'])
        self._add_state_fields()

    def _get_default_reward(self):
        return self.data.get('reward')

    def _get_board_size(self):
        return {
            'x': self.data['size'][0],
            'y': self.data['size'][1]
        }

    def _generate_default_board(self, x: int, y: int) -> None:
        self.board = self._fill_board_with_default(self._generate_table_for_board(x, y))

    @staticmethod
    def _generate_table_for_board(x: int, y: int) -> List[List[None]]:
        return [[None] * x for _ in range(y)]

    def _fill_board_with_default(self, board: List[List[None]]) -> List[List[Field]]:
        if not board:
            raise BoardEmptyException("Board is empty, use _generate_table_for_board first.")
        reward = self._get_default_reward()
        for y in range(len(board)):
            for x in range(len(board[0])):
                board[y][x] = Field(Field.normal, x=x, y=y, reward=reward)
        return board

    def _add_state_fields(self):
        for state_field in self.data['state']:
            x = state_field['position'][0]
            y = state_field['position'][1]
            field_type = state_field.get('s_type')
            field_reward = self._get_reward_for_field(state_field)
            field = Field(
                state=field_type,
                x=x, y=y,
                reward=field_reward
            )
            self.board[y][x] = field

    def _get_reward_for_field(self, state_dict: dict) -> int or None:
        field_type = state_dict['s_type']
        default_reward = self.data['reward']
        if field_type is Field.start:
            return default_reward
        elif field_type is Field.special or field_type is Field.terminal:
            return state_dict['value']
        else:
            return None
