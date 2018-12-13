import toml


from markov_libs import Field


class BoardEmptyException(Exception):
    pass


class World:
    def __init__(self):
        self._board = []
        self._reward = None
        self.title = None
        self.gamma = None
        self.epsilon = None
        self.probability = []

    @staticmethod
    def _parse_toml(filename):
        with open(filename, 'r') as f:
            data = toml.loads(f.read())
        return data
