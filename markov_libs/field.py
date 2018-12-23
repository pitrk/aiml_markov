class FieldStateUnknownException(Exception):
    pass


class FieldRequiresValueException(Exception):
    pass


class EmptyUtilityHistoryException(Exception):
    pass


class Field:
    terminal = "T"
    forbidden = "F"
    normal = "N"
    start = "S"
    special = "B"
    possible_states = [terminal, special, forbidden, normal, start]

    def __init__(self, state: str, x: int, y: int, reward: float = None, utility: float = None):
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
        self.utility_history = [utility] if utility is not None else []

    @property
    def utility(self):
        try:
            if self.state is self.terminal:
                return self.reward
            return self.utility_history[-1]
        except IndexError:
            raise EmptyUtilityHistoryException

    @utility.setter
    def utility(self, value):
        if value is not None:
            self.utility_history.append(value)

    @utility.deleter
    def utility(self):
        try:
            self.utility_history.pop()
        except IndexError:
            raise EmptyUtilityHistoryException
