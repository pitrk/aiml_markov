class FieldRequiresValueException(Exception):
    pass


class Field:
    terminal = "T"
    forbidden = "F"
    normal = "N"
    start = "S"
    special = "B"

    def __init__(self, state: str, reward: int = None):
        if state in [self.terminal, self.special] and reward is None:
            raise FieldRequiresValueException("Field type {} has to have a reward value".format(state))
        self.state = state
        self.reward = reward
