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


class UtilitiesNotCalculated(Exception):
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
        if field.state is Field.terminal:
            return field
        try:
            x_in_front = field.x + self.x_modifier_front[action]
            y_in_front = field.y + self.y_modifier_front[action]
            return self.field_allowed(x=x_in_front, y=y_in_front)
        except (FieldDoesNotExistException, FieldForbiddenException):
            return field

    def position_left(self, field: Field, action: str) -> Field:
        if field.state is Field.terminal:
            return field
        try:
            x_on_left = field.x + self.x_modifier_left[action]
            y_on_left = field.y + self.y_modifier_left[action]
            return self.field_allowed(x=x_on_left, y=y_on_left)
        except (FieldDoesNotExistException, FieldForbiddenException):
            return field

    def position_right(self, field: Field, action: str) -> Field:
        if field.state is Field.terminal:
            return field
        try:
            x_on_right = field.x + self.x_modifier_right[action]
            y_on_right = field.y + self.y_modifier_right[action]
            return self.field_allowed(x=x_on_right, y=y_on_right)
        except (FieldDoesNotExistException, FieldForbiddenException):
            return field

    def position_back(self, field: Field, action: str) -> Field:
        if field.state is Field.terminal:
            return field
        try:
            x_in_back = field.x + self.x_modifier_back[action]
            y_in_back = field.y + self.y_modifier_back[action]
            return self.field_allowed(x=x_in_back, y=y_in_back)
        except (FieldDoesNotExistException, FieldForbiddenException):
            return field

    def mdp(self, n: int = None, termination_value: float = None):
        if n is not None:
            for _ in range(n):
                for field in self.all_fields():
                    if field.state is not Field.forbidden:
                        field.utility = field.reward + self.gamma * self.max_of_all_actions(field)
        elif termination_value is not None:
            while not self._mdp_stop(termination_value):
                for field in self.all_fields():
                    if field.state is not Field.forbidden:
                        field.utility = field.reward + self.gamma * self.max_of_all_actions(field)
        else:
            raise AttributeError("Provide either maximum iterations or difference termination value")

    def _mdp_stop(self, termination_value: float) -> bool:
        differences = []
        for field in self.all_fields():
            if field.state not in [Field.terminal, Field.forbidden]:
                try:
                    differences.append(abs(field.utility_history[-2] - field.utility_history[-1]))
                except IndexError:
                    differences.append(float('inf'))
        return max(differences) < termination_value

    def all_fields(self) -> List[Field]:
        return functools.reduce(operator.iconcat, self._board, [])

    def max_of_all_actions(self, field: Field) -> float:
        results = []
        for action in self.actions:
            results.append(self.pu_sum_for_action(field, action))
        return max(results)

    def pu_sum_for_action(self, field: Field, action: str) -> float:
        if field.state is Field.terminal:
            return 0.0
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
                field.utility = self.initial_utility
        return return_list

    def calculate_policy(self):
        fields = self.all_fields()
        for field in fields:
            if field.state not in [Field.terminal, Field.forbidden]:
                field.policy = self._calculate_policy_for_field(field)

    def _calculate_policy_for_field(self, field) -> str:
        utilities = []
        for action in self.actions:
            utilities.append(self.pu_sum_for_action(field, action))
        max_value = max(utilities)
        return self.actions[utilities.index(max_value)]

    def generate_gnuplot_file(self, filename: str):
        fields = self.all_fields()
        utilities_length = len(fields[0].utility_history)-1
        with open(filename, 'w') as f:
            f.write('iteration ')
            for field in fields:
                if field.state is not Field.forbidden:
                    f.write('({x},{y}) '.format(x=field.x+1, y=field.y+1))
            f.write('\n')
            for i in range(utilities_length):
                line = "{} ".format(str(i))
                for field in fields:
                    if field.state is not Field.forbidden:
                        line += "{} ".format(field.utility_history[i])
                line += '\n'
                f.write(line)

    def __str__(self):
        return_string = ""
        for j in range(self.max_y, -1, -1):
            return_string += ("-------"*(self.max_x+1) + "-\n")
            for i in range(0, self.max_x+1):
                return_string += ("|{}    {}".format(self._board[j][i].str_policy, self._board[j][i].state))
            return_string += "|\n"
            for i in range(0, self.max_x+1):
                return_string += ("|{}".format(self._board[j][i].str_utility))
            return_string += "|\n"
        return_string += ("-------" * (self.max_x + 1) + "-\n")
        return return_string

