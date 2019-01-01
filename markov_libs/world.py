import toml

from markov_libs import WorldFactory, Field


class BoardEmptyException(Exception):
    pass


class FieldForbiddenException(Exception):
    pass


class FieldDoesNotExistException(Exception):
    pass


class World:
    forward = '^'
    left = '<'
    right = '>'
    backward = 'v'

    x_modifier = {
        forward: 0,
        left: -1,
        right: 1,
        backward: 0
    }

    y_modifier = {
        forward: 1,
        left: 0,
        right: 0,
        backward: -1
    }

    def __init__(self):
        self.data = None
        self._board = []
        self.title = None
        self.gamma = None
        self.epsilon = None
        self.probability = []

    @property
    def forward_probability(self):
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
    def max_x(self):
        return len(self._board[0]) - 1

    @property
    def max_y(self):
        return len(self._board) - 1

    def position_in_front(self, field, action):
        try:
            x_in_front = field.x + self.x_modifier[action]
            y_in_front = field.y + self.y_modifier[action]
            return self.field_allowed(x=x_in_front, y=y_in_front)
        except (FieldDoesNotExistException, FieldForbiddenException):
            return field

