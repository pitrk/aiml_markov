import unittest.mock

import toml

from markov_libs import Field
from markov_libs import FieldForbiddenException
from markov_libs import FieldDoesNotExistException
from markov_libs import World


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


class TestWorldLoaded(unittest.TestCase):
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

    @unittest.mock.patch(
        'builtins.open',
        new=unittest.mock.mock_open(read_data=mock_file_content),
        create=True
    )
    def setUp(self):
        self.world = World()
        self.world.load('/dev/null')

    def test_has_forward_probability_property(self):
        self.assertTrue(hasattr(self.world, 'forward_probability'))

    def test_forward_probability_returns_correct_value(self):
        self.assertEqual(
            self.mock_dict_content['probability'][0],
            self.world.forward_probability
        )

    def test_has_left_probability_property(self):
        self.assertTrue(hasattr(self.world, 'left_probability'))

    def test_left_probability_returns_correct_value(self):
        self.assertEqual(
            self.mock_dict_content['probability'][1],
            self.world.left_probability
        )

    def test_has_right_probability_property(self):
        self.assertTrue(hasattr(self.world, 'right_probability'))

    def test_right_probability_returns_correct_value(self):
        self.assertEqual(
            self.mock_dict_content['probability'][2],
            self.world.right_probability
        )

    def test_has_backward_probability_property(self):
        self.assertTrue(hasattr(self.world, 'backward_probability'))

    def test_backward_probability_returns_correct_value(self):
        self.assertEqual(
            self.mock_dict_content['probability'][3],
            self.world.backward_probability
        )

    def test_has_field_method(self):
        self.assertTrue(hasattr(self.world, 'field'))

    def test_field_method_returns_correct_field_object(self):
        method_returns = self.world.field(x=3, y=2)
        self.assertEqual(self.world._board[2][3], method_returns)

    def test_field_method_allows_to_modify_field(self):
        self.assertEqual([], self.world._board[1][0].utility_history)
        self.world.field(0, 1).utility = 0.88
        self.assertEqual(0.88, self.world._board[1][0].utility)

    def test_has_field_allowed_method(self):
        self.assertTrue(hasattr(self.world, 'field_allowed'))

    def test_field_allowed_returns_field_if_exists_and_is_not_forbidden(self):
        method_returns = self.world.field_allowed(x=0, y=0)
        self.assertIs(self.world._board[0][0], method_returns)

    def test_field_allowed_raises_exception_when_field_forbidden(self):
        self.assertRaises(FieldForbiddenException, self.world.field_allowed, 1, 1)

    def test_field_allowed_raises_exception_when_field_does_not_exist(self):
        self.assertRaises(FieldDoesNotExistException, self.world.field_allowed, -1, 1)
        self.assertRaises(FieldDoesNotExistException, self.world.field_allowed, 4, 5)

    def test_has_max_x_property(self):
        self.assertTrue(hasattr(self.world, 'max_x'))

    def test_max_x_returns_maximum_x_index_of_world(self):
        self.assertEqual(3, self.world.max_x)

    def test_has_max_y_property(self):
        self.assertTrue(hasattr(self.world, 'max_y'))

    def test_max_y_returns_maximum_y_index_of_world(self):
        self.assertEqual(2, self.world.max_y)

    def test_has_position_in_front_method(self):
        self.assertTrue(hasattr(self.world, 'position_in_front'))

    def test_has_position_left_method(self):
        self.assertTrue(hasattr(self.world, 'position_left'))

    def test_has_position_right_method(self):
        self.assertTrue(hasattr(self.world, 'position_right'))

    def check_position(self, direction_function, x, y, action):
        position = self.world.field(x, y)
        returned_position = direction_function(position, action)
        return returned_position.x, returned_position.y

    def test_position_in_front_where_position_is_reachable(self):
        self.assertTupleEqual((0, 1), self.check_position(self.world.position_in_front, 0, 0, '^'))
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_in_front, 1, 0, '<'))
        self.assertTupleEqual((1, 0), self.check_position(self.world.position_in_front, 0, 0, '>'))
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_in_front, 0, 1, 'v'))

    def test_position_in_front_where_position_is_forbidden(self):
        self.assertTupleEqual((1, 0), self.check_position(self.world.position_in_front, 1, 0, '^'))
        self.assertTupleEqual((2, 1), self.check_position(self.world.position_in_front, 2, 1, '<'))
        self.assertTupleEqual((0, 1), self.check_position(self.world.position_in_front, 0, 1, '>'))
        self.assertTupleEqual((1, 2), self.check_position(self.world.position_in_front, 1, 2, 'v'))

    def test_position_in_front_where_position_is_outside(self):
        self.assertTupleEqual((0, 2), self.check_position(self.world.position_in_front, 0, 2, '^'))
        self.assertTupleEqual((0, 1), self.check_position(self.world.position_in_front, 0, 1, '<'))
        self.assertTupleEqual((3, 0), self.check_position(self.world.position_in_front, 3, 0, '>'))
        self.assertTupleEqual((1, 0), self.check_position(self.world.position_in_front, 1, 0, 'v'))

    def test_position_left_where_position_is_reachable(self):
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_left, 1, 0, '^'))
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_left, 0, 1, '<'))
        self.assertTupleEqual((0, 1), self.check_position(self.world.position_left, 0, 0, '>'))
        self.assertTupleEqual((1, 0), self.check_position(self.world.position_left, 0, 0, 'v'))

    def test_position_left_where_position_is_forbidden(self):
        self.assertTupleEqual((2, 1), self.check_position(self.world.position_left, 2, 1, '^'))
        self.assertTupleEqual((1, 2), self.check_position(self.world.position_left, 1, 2, '<'))
        self.assertTupleEqual((1, 0), self.check_position(self.world.position_left, 1, 0, '>'))
        self.assertTupleEqual((0, 1), self.check_position(self.world.position_left, 0, 1, 'v'))

    def test_position_left_where_position_is_outside(self):
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_left, 0, 0, '^'))
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_left, 0, 0, '<'))
        self.assertTupleEqual((0, 2), self.check_position(self.world.position_left, 0, 2, '>'))
        self.assertTupleEqual((3, 0), self.check_position(self.world.position_left, 3, 0, 'v'))

    def test_position_right_where_position_is_reachable(self):
        self.assertTupleEqual((2, 0), self.check_position(self.world.position_right, 1, 0, '^'))
        self.assertTupleEqual((0, 1), self.check_position(self.world.position_right, 0, 0, '<'))
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_right, 0, 1, '>'))
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_right, 1, 0, 'v'))

    def test_position_right_where_position_is_forbidden(self):
        self.assertTupleEqual((0, 1), self.check_position(self.world.position_right, 0, 1, '^'))
        self.assertTupleEqual((1, 0), self.check_position(self.world.position_right, 1, 0, '<'))
        self.assertTupleEqual((1, 2), self.check_position(self.world.position_right, 1, 2, '>'))
        self.assertTupleEqual((2, 1), self.check_position(self.world.position_right, 2, 1, 'v'))

    def test_position_right_where_position_is_outside(self):
        self.assertTupleEqual((3, 0), self.check_position(self.world.position_right, 3, 0, '^'))
        self.assertTupleEqual((0, 2), self.check_position(self.world.position_right, 0, 2, '<'))
        self.assertTupleEqual((1, 0), self.check_position(self.world.position_right, 1, 0, '>'))
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_right, 0, 0, 'v'))
