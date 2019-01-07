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

    up = '^'
    left = '<'
    right = '>'
    down = 'v'

    actions = (up, left, right, down)

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
        self.policy = None
        if state is self.terminal:
            self.q_values = [reward, reward, reward, reward]
        else:
            self.q_values = [0.0, 0.0, 0.0, 0.0]
        self.actions_count = [0, 0, 0, 0]

    def __repr__(self):
        return "<Field state:{} x:{} y:{}, utility_history:{}".format(
            self.state,
            self.x,
            self.y,
            self.utility_history
        )

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

    @property
    def str_policy(self):
        if self.policy is None:
            return 'x'
        else:
            return self.policy

    @property
    def str_utility(self):
        try:
            return '{: >7}'.format(str(self.utility)[:7])
        except EmptyUtilityHistoryException:
            return 'xxxxxxx'

    def q_value(self, action: str) -> float:
        index = self.actions.index(action)
        return self.q_values[index]

    def set_q_value(self, action: str, q_value: float) -> None:
        index = self.actions.index(action)
        self.q_values[index] = q_value

    def str_q_value(self, action: str) -> str:
        if self.state is self.forbidden:
            return "xxxxx"
        return '{: >5}'.format(str(self.q_value(action))[:5])

    def is_terminal(self) -> bool:
        return self.state is self.terminal

    def increment_action_counter(self, action: str):
        index = self.actions.index(action)
        self.actions_count[index] += 1

    def get_action_counter_value(self, action: str) -> int:
        index = self.actions.index(action)
        return self.actions_count[index]

    def optimal_action(self) -> str:
        index = self.q_values.index(max(self.q_values))
        return self.actions[index]

    def str_optimal_action(self):
        if self.state in [self.terminal, self.forbidden]:
            return 'x'
        else:
            return self.optimal_action()
