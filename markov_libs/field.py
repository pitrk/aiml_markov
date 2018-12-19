class FieldStateUnknownException(Exception):
    pass


class FieldRequiresValueException(Exception):
    pass


class Field:
    terminal = "T"
    forbidden = "F"
    normal = "N"
    start = "S"
    special = "B"
    possible_states = [terminal, special, forbidden, normal, start]

    def __init__(self, state: str, x: int, y: int, reward: float = None):
        if state not in self.possible_states:
            raise FieldStateUnknownException("State {} is unknown. Use one of states: {}".format(
                state, self.possible_states)
            )
        if state in [self.terminal, self.special, self.normal, self.start] and reward is None:
            raise FieldRequiresValueException("Field type {} has to have a reward value.".format(state))
        self.state = state
        self.reward = reward
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.state == other.state and self.reward == other.reward
