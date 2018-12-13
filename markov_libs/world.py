import toml


class World:
    def __init__(self):
        pass

    def load_from_file(self):
        pass

    def _parse_toml(self, filename):
        with open(filename, 'r') as f:
            data = toml.loads(f.read())
        return data
