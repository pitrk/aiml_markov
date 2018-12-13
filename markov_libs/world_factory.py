import toml

from markov_libs import Field


class BoardEmptyException(Exception):
    pass


class WorldFactory:
    def __init__(self, data: dict):
        self.data = data

    def board_generator(self):
        """
        Should take dictionary
        create board
        fill with default
        add special, terminal, forbidden and start fields
        add generated board to self._board
        :return: None
        """
        pass

    @staticmethod
    def _get_start_field_position_from_dict(dictionary):
        return dictionary['states']['start']['position']

    def _generate_default_board(self, x, y):
        return self._fill_board_with_default(self._generate_table_for_board(x, y))

    @staticmethod
    def _generate_table_for_board(x, y):
        return [[None]*x for _ in range(y)]

    @staticmethod
    def _fill_board_with_default(board):
        if not board:
            raise BoardEmptyException("Board is empty, use _generate_table_for_board first.")
        for y in range(len(board)):
            for x in range(len(board[0])):
                board[y][x] = Field(Field.normal)
        return board


