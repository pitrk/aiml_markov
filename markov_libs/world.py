import toml

from markov_libs import WorldFactory


class BoardEmptyException(Exception):
    pass


class World:
    actions = ['^', '<', '>', 'v']

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

    def field(self, x: int, y: int):
        return self._board[y][x]
