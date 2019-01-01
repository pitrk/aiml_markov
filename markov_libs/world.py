import functools
import operator
from typing import List, Tuple, Iterable

import toml

from markov_libs import WorldFactory, Field, EmptyUtilityHistoryException


class BoardEmptyException(Exception):
    pass


class FieldForbiddenException(Exception):
    pass


class FieldDoesNotExistException(Exception):
    pass


class World:
    up = '^'
    left = '<'
    right = '>'
    down = 'v'

    actions = (up, left, right, down)

    x_modifier_front = {up: 0, left: -1, right: 1, down: 0}
    y_modifier_front = {up: 1, left: 0, right: 0, down: -1}

    x_modifier_left = {up: -1, left: 0, right: 0, down: 1}
    y_modifier_left = {up: 0, left: -1, right: 1, down: 0}

    x_modifier_right = {up: 1, left: 0, right: 0, down: -1}
    y_modifier_right = {up: 0, left: 1, right: -1, down: 0}

    x_modifier_back = {up: 0, left: 1, right: -1, down: 0}
    y_modifier_back = {up: -1, left: 0, right: 0, down: 1}

    def __init__(self):
        self.data = None
        self._board = []
        self.title = None
        self.gamma = None
        self.epsilon = None
        self.probability = []
        self.initial_utility = 0.0

    @property
    def front_probability(self):
        return self.probability[0]

    @property
    def left_probability(self):
        return self.probability[1]

    @property
    def right_probability(self):
        return self.probability[2]

    @property
    def backward_probability(self):
        return self.probability[3]

    def load(self, filename: str):
        self._parse_toml(filename)
        self._set_values()

    def _parse_toml(self, filename):
        with open(filename, 'r') as f:
            data = toml.loads(f.read())
        self.data = data

    def _set_values(self):
        self.title = self.data['title']
        self.gamma = self.data['gamma']
        self.epsilon = self.data['epsilon']
        self.probability = self.data['probability']
        world_factory = WorldFactory(self.data)
        world_factory.board_generator()
        self._board = world_factory.board

    def field(self, x: int, y: int) -> Field:
        return self._board[y][x]

    def field_allowed(self, x: int, y: int) -> Field:
        if x < 0 or y < 0 or x > self.max_x or y > self.max_y:
            raise FieldDoesNotExistException
        field = self._board[y][x]
        if field.state is Field.forbidden:
            raise FieldForbiddenException
        return field

    @property
    def max_x(self) -> int:
        return len(self._board[0]) - 1

    @property
    def max_y(self) -> int:
        return len(self._board) - 1

    def fields_around(self, field: Field, action: str) -> Tuple[Field, Field, Field, Field]:
        return (
            self.position_front(field, action),
            self.position_left(field, action),
            self.position_right(field, action),
            self.position_back(field, action)
        )

    def position_front(self, field: Field, action: str) -> Field:
        try:
            x_in_front = field.x + self.x_modifier_front[action]
            y_in_front = field.y + self.y_modifier_front[action]
            return self.field_allowed(x=x_in_front, y=y_in_front)
        except (FieldDoesNotExistException, FieldForbiddenException):
            return field

    def position_left(self, field: Field, action: str) -> Field:
        try:
            x_on_left = field.x + self.x_modifier_left[action]
            y_on_left = field.y + self.y_modifier_left[action]
            return self.field_allowed(x=x_on_left, y=y_on_left)
        except (FieldDoesNotExistException, FieldForbiddenException):
            return field

    def position_right(self, field: Field, action: str) -> Field:
        try:
            x_on_right = field.x + self.x_modifier_right[action]
            y_on_right = field.y + self.y_modifier_right[action]
            return self.field_allowed(x=x_on_right, y=y_on_right)
        except (FieldDoesNotExistException, FieldForbiddenException):
            return field

    def position_back(self, field: Field, action: str) -> Field:
        try:
            x_in_back = field.x + self.x_modifier_back[action]
            y_in_back = field.y + self.y_modifier_back[action]
            return self.field_allowed(x=x_in_back, y=y_in_back)
        except (FieldDoesNotExistException, FieldForbiddenException):
            return field

    def mdf(self):
        pass

    def all_fields(self):
        return functools.reduce(operator.iconcat, self._board, [])

    def max_of_all_actions(self, field: Field) -> float:
        results = []
        for action in self.actions:
            results.append(self.pu_sum_for_action(field, action))
        return max(results)

    def pu_sum_for_action(self, field: Field, action: str) -> float:
        fields_around = self.fields_around(field, action)
        fields_utilities = self._get_utilities_for_fields(fields_around)
        return sum(p * u for p, u in zip(self.probability, fields_utilities))

    def _get_utilities_for_fields(self, fields_list: Iterable[Field]) -> List[float]:
        return_list = []
        for field in fields_list:
            try:
                return_list.append(field.utility)
            except EmptyUtilityHistoryException:
                return_list.append(self.initial_utility)
        return return_list
