import unittest
import unittest.mock
import toml

from markov_libs import World
from markov_libs import Field


class TestWorld(unittest.TestCase):
    mock_file_content = """
        title = "default"
        size = [4, 3]
        reward = -0.04
        gamma = 1
        epsilon = 0
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

        [[state]]
            s_type = 'B'
            position = [2, 1]
            value = 2
        """

    mock_dict_content = toml.loads(mock_file_content)

    def setUp(self):
        self.world = World()

    def test_world_has_fields(self):
        self.assertTrue(hasattr(self.world, 'data'))
        self.assertTrue(hasattr(self.world, '_board'))
        self.assertTrue(hasattr(self.world, 'title'))
        self.assertTrue(hasattr(self.world, 'gamma'))
        self.assertTrue(hasattr(self.world, 'epsilon'))
        self.assertTrue(hasattr(self.world, 'probability'))

    def test_has__parse_toml_method(self):
        self.assertTrue(hasattr(self.world, '_parse_toml'))

    @unittest.mock.patch(
        'builtins.open',
        new=unittest.mock.mock_open(read_data=mock_file_content),
        create=True
    )
    def test__parse_toml_saves_to_data(self):
        self.world._parse_toml('/dev/null')
        self.assertIsInstance(self.world.data, dict)

    @unittest.mock.patch(
        'builtins.open',
        new=unittest.mock.mock_open(read_data=mock_file_content),
        create=True
    )
    def test__parse_toml_returns_correct_dict(self):
        correct_dict = toml.loads(self.mock_file_content)
        self.world._parse_toml('/dev/null')
        self.assertEqual(correct_dict, self.world.data)

    def test_has_set_values_method(self):
        self.assertTrue(hasattr(self.world, '_set_values'))

    @unittest.mock.patch(
        'builtins.open',
        new=unittest.mock.mock_open(read_data=mock_file_content),
        create=True
    )
    def test_set_values_sets_values(self):
        self.world._parse_toml('/dev/null')
        self.world._set_values()
        self.assertEqual("default", self.world.title)
        self.assertEqual(1, self.world.gamma)
        self.assertEqual(0, self.world.epsilon)
        self.assertEqual([0.8, 0.1, 0.1, 0.0], self.world.probability)

        self.assertEqual(Field.normal, self.world._board[2][1].state)
        self.assertEqual(-0.04, self.world._board[2][1].reward)
        self.assertEqual(1, self.world._board[2][1].x)
        self.assertEqual(2, self.world._board[2][1].y)

        self.assertEqual(Field.start, self.world._board[0][0].state)
        self.assertEqual(-0.04, self.world._board[0][0].reward)
        self.assertEqual(0, self.world._board[0][0].x)
        self.assertEqual(0, self.world._board[0][0].y)

        self.assertEqual(Field.terminal, self.world._board[2][3].state)
        self.assertEqual(1, self.world._board[2][3].reward)
        self.assertEqual(3, self.world._board[2][3].x)
        self.assertEqual(2, self.world._board[2][3].y)

        self.assertEqual(Field.terminal, self.world._board[1][3].state)
        self.assertEqual(-1, self.world._board[1][3].reward)
        self.assertEqual(3, self.world._board[1][3].x)
        self.assertEqual(1, self.world._board[1][3].y)

        self.assertEqual(Field.forbidden, self.world._board[1][1].state)
        self.assertEqual(None, self.world._board[1][1].reward)
        self.assertEqual(1, self.world._board[1][1].x)
        self.assertEqual(1, self.world._board[1][1].y)

        self.assertEqual(Field.special, self.world._board[1][2].state)
        self.assertEqual(2, self.world._board[1][2].reward)
        self.assertEqual(2, self.world._board[1][2].x)
        self.assertEqual(1, self.world._board[1][2].y)

    def test_has_load_method(self):
        self.assertTrue(hasattr(self.world, 'load'))
