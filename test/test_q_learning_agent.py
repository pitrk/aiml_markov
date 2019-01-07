import unittest
from unittest import mock

from markov_libs import world, QLearningAgent, World


class TestQLearningAgent(unittest.TestCase):
    mock_file_content = """
           title = "default"
           size = [4, 3]
           reward = -0.04
           gamma = 1
           epsilon = 0.2
           probability = [0.8, 0.1, 0.1, 0.0]

           [[state]]
               s_type = 'S'
               position = [0, 0]

           [[state]]
               s_type = 'T'
               position = [3, 2]
               value = 1

           [[state]]
               s_type = 'T'
               position = [3, 1]
               value = -1

           [[state]]
               s_type = 'F'
               position = [1, 1]
           """

    @unittest.mock.patch(
        'builtins.open',
        new=unittest.mock.mock_open(read_data=mock_file_content),
        create=True
    )
    def setUp(self):
        self.world = world.World()
        self.world.load('/dev/null')
        self.agent = QLearningAgent(self.world)

    @mock.patch('markov_libs.q_learning_agent.QLearningAgent.random_action')
    def test_select_exploration_or_exploitation(self, random_action_mock):
        for _ in range(1000):
            self.agent.select_exploration_or_exploitation(World.up)
        self.assertAlmostEqual(200, random_action_mock.call_count, delta=40)


