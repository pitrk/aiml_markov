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

    def __init__(self, state: str, reward: int = None):
        if state not in self.possible_states:
            raise FieldStateUnknownException("State {} is unknown. Use one of states: {}".format(
                state, self.possible_states)
            )
        if state in [self.terminal, self.special] and reward is None:
            raise FieldRequiresValueException("Field type {} has to have a reward value.".format(state))
        self.state = state
        self.reward = reward
