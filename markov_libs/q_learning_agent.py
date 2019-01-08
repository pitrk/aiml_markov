import numpy as np

from markov_libs import World


class QLearningAgent:
    initial_action = World.up

    def __init__(self, world_to_learn: World):
        self.world = world_to_learn
        self.start_position = world_to_learn.start_field()

    def learning(self, iterations: int):
        for i in range(iterations):
            optimal_action = self.initial_action
            previous_position = self.start_position
            while not previous_position.is_terminal():
                selected_action = self.select_exploration_or_exploitation(optimal_action)
                current_position = self.world.agent_move(previous_position, selected_action)
                alpha = 1 / previous_position.get_action_counter_value(selected_action)
                new_q_value = previous_position.q_value(selected_action) \
                              + alpha \
                              * (
                                      previous_position.reward
                                      + self.world.gamma * max(current_position.q_values)
                                      - previous_position.q_value(selected_action)
                              )
                previous_position.set_q_value(selected_action, new_q_value)

                previous_position = current_position
                optimal_action = current_position.optimal_action()

    def select_exploration_or_exploitation(self, optimal_action: str) -> str:
        random_number = np.random.random()
        if random_number < self.world.epsilon:
            return self.random_action()
        return optimal_action

    def random_action(self) -> str:
        return np.random.choice(self.world.actions)

    def __str__(self):
        return_string = ""
        for j in range(self.world.max_y, -1, -1):
            return_string += ("-------" * (self.world.max_x + 1) + "-\n")
            for action in self.world.actions:
                for i in range(0, self.world.max_x + 1):
                    return_string += ("|{}{}".format(action, self.world.field(i, j).str_q_value(action)))
                return_string += "|\n"
            for i in range(0, self.world.max_x + 1):
                return_string += ("|  {}   ".format(self.world.field(i, j).str_optimal_action()))
            return_string += "|\n"
        return_string += ("-------" * (self.world.max_x + 1) + "-\n")
        return return_string
