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

    def test_has_front_probability_property(self):
        self.assertTrue(hasattr(self.world, 'front_probability'))

    def test_front_probability_returns_correct_value(self):
        self.assertEqual(
            self.mock_dict_content['probability'][0],
            self.world.front_probability
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

    def test_has_fields_around_method(self):
        self.assertTrue(hasattr(self.world, 'fields_around'))

    def test_fields_around_returns_tuple(self):
        field = self.world.field(x=0, y=0)
        self.assertTrue(isinstance(self.world.fields_around(field, action=World.up), tuple))

    def test_fields_around_returns_tuple_of_fields_around_in_order_f_l_r_b(self):
        field = self.world.field(x=2, y=0)
        self.assertTupleEqual(
            (self.world.field(2, 1), self.world.field(1, 0), self.world.field(3, 0), self.world.field(2, 0)),
            self.world.fields_around(field, World.up)
        )

    def test_has_position_front_method(self):
        self.assertTrue(hasattr(self.world, 'position_front'))

    def test_has_position_left_method(self):
        self.assertTrue(hasattr(self.world, 'position_left'))

    def test_has_position_right_method(self):
        self.assertTrue(hasattr(self.world, 'position_right'))

    def test_has_position_back_method(self):
        self.assertTrue(hasattr(self.world, 'position_back'))

    def check_position(self, direction_function, x, y, action):
        position = self.world.field(x, y)
        returned_position = direction_function(position, action)
        return returned_position.x, returned_position.y

    def test_position_front_where_position_is_reachable(self):
        self.assertTupleEqual((0, 1), self.check_position(self.world.position_front, 0, 0, World.up))
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_front, 1, 0, World.left))
        self.assertTupleEqual((1, 0), self.check_position(self.world.position_front, 0, 0, World.right))
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_front, 0, 1, World.down))

    def test_position_front_where_position_is_forbidden(self):
        self.assertTupleEqual((1, 0), self.check_position(self.world.position_front, 1, 0, World.up))
        self.assertTupleEqual((2, 1), self.check_position(self.world.position_front, 2, 1, World.left))
        self.assertTupleEqual((0, 1), self.check_position(self.world.position_front, 0, 1, World.right))
        self.assertTupleEqual((1, 2), self.check_position(self.world.position_front, 1, 2, World.down))

    def test_position_front_where_position_is_terminal(self):
        self.assertTupleEqual((3, 2), self.check_position(self.world.position_front, 3, 2, World.up))
        self.assertTupleEqual((3, 2), self.check_position(self.world.position_front, 3, 2, World.left))
        self.assertTupleEqual((3, 2), self.check_position(self.world.position_front, 3, 2, World.right))
        self.assertTupleEqual((3, 2), self.check_position(self.world.position_front, 3, 2, World.down))

    def test_position_front_where_position_is_outside(self):
        self.assertTupleEqual((0, 2), self.check_position(self.world.position_front, 0, 2, World.up))
        self.assertTupleEqual((0, 1), self.check_position(self.world.position_front, 0, 1, World.left))
        self.assertTupleEqual((3, 0), self.check_position(self.world.position_front, 3, 0, World.right))
        self.assertTupleEqual((1, 0), self.check_position(self.world.position_front, 1, 0, World.down))

    def test_position_left_where_position_is_reachable(self):
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_left, 1, 0, World.up))
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_left, 0, 1, World.left))
        self.assertTupleEqual((0, 1), self.check_position(self.world.position_left, 0, 0, World.right))
        self.assertTupleEqual((1, 0), self.check_position(self.world.position_left, 0, 0, World.down))

    def test_position_left_where_position_is_forbidden(self):
        self.assertTupleEqual((2, 1), self.check_position(self.world.position_left, 2, 1, World.up))
        self.assertTupleEqual((1, 2), self.check_position(self.world.position_left, 1, 2, World.left))
        self.assertTupleEqual((1, 0), self.check_position(self.world.position_left, 1, 0, World.right))
        self.assertTupleEqual((0, 1), self.check_position(self.world.position_left, 0, 1, World.down))

    def test_position_left_where_position_is_terminal(self):
        self.assertTupleEqual((3, 2), self.check_position(self.world.position_left, 3, 2, World.up))
        self.assertTupleEqual((3, 2), self.check_position(self.world.position_left, 3, 2, World.left))
        self.assertTupleEqual((3, 2), self.check_position(self.world.position_left, 3, 2, World.right))
        self.assertTupleEqual((3, 2), self.check_position(self.world.position_left, 3, 2, World.down))

    def test_position_left_where_position_is_outside(self):
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_left, 0, 0, World.up))
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_left, 0, 0, World.left))
        self.assertTupleEqual((0, 2), self.check_position(self.world.position_left, 0, 2, World.right))
        self.assertTupleEqual((3, 0), self.check_position(self.world.position_left, 3, 0, World.down))

    def test_position_right_where_position_is_reachable(self):
        self.assertTupleEqual((2, 0), self.check_position(self.world.position_right, 1, 0, World.up))
        self.assertTupleEqual((0, 1), self.check_position(self.world.position_right, 0, 0, World.left))
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_right, 0, 1, World.right))
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_right, 1, 0, World.down))

    def test_position_right_where_position_is_forbidden(self):
        self.assertTupleEqual((0, 1), self.check_position(self.world.position_right, 0, 1, World.up))
        self.assertTupleEqual((1, 0), self.check_position(self.world.position_right, 1, 0, World.left))
        self.assertTupleEqual((1, 2), self.check_position(self.world.position_right, 1, 2, World.right))
        self.assertTupleEqual((2, 1), self.check_position(self.world.position_right, 2, 1, World.down))

    def test_position_right_where_position_is_outside(self):
        self.assertTupleEqual((3, 0), self.check_position(self.world.position_right, 3, 0, World.up))
        self.assertTupleEqual((0, 2), self.check_position(self.world.position_right, 0, 2, World.left))
        self.assertTupleEqual((1, 0), self.check_position(self.world.position_right, 1, 0, World.right))
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_right, 0, 0, World.down))

    def test_position_right_where_position_is_terminal(self):
        self.assertTupleEqual((3, 2), self.check_position(self.world.position_right, 3, 2, World.up))
        self.assertTupleEqual((3, 2), self.check_position(self.world.position_right, 3, 2, World.left))
        self.assertTupleEqual((3, 2), self.check_position(self.world.position_right, 3, 2, World.right))
        self.assertTupleEqual((3, 2), self.check_position(self.world.position_right, 3, 2, World.down))

    def test_position_back_where_position_is_reachable(self):
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_back, 0, 1, World.up))
        self.assertTupleEqual((1, 0), self.check_position(self.world.position_back, 0, 0, World.left))
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_back, 1, 0, World.right))
        self.assertTupleEqual((0, 1), self.check_position(self.world.position_back, 0, 0, World.down))

    def test_position_back_where_position_is_forbidden(self):
        self.assertTupleEqual((1, 2), self.check_position(self.world.position_back, 1, 2, World.up))
        self.assertTupleEqual((0, 1), self.check_position(self.world.position_back, 0, 1, World.left))
        self.assertTupleEqual((2, 1), self.check_position(self.world.position_back, 2, 1, World.right))
        self.assertTupleEqual((1, 0), self.check_position(self.world.position_back, 1, 0, World.down))

    def test_position_back_where_position_is_outside(self):
        self.assertTupleEqual((0, 0), self.check_position(self.world.position_back, 0, 0, World.up))
        self.assertTupleEqual((3, 0), self.check_position(self.world.position_back, 3, 0, World.left))
        self.assertTupleEqual((0, 2), self.check_position(self.world.position_back, 0, 2, World.right))
        self.assertTupleEqual((0, 2), self.check_position(self.world.position_back, 0, 2, World.down))

    def test_position_back_where_position_is_terminal(self):
        self.assertTupleEqual((3, 2), self.check_position(self.world.position_back, 3, 2, World.up))
        self.assertTupleEqual((3, 2), self.check_position(self.world.position_back, 3, 2, World.left))
        self.assertTupleEqual((3, 2), self.check_position(self.world.position_back, 3, 2, World.right))
        self.assertTupleEqual((3, 2), self.check_position(self.world.position_back, 3, 2, World.down))

    def test_has_mdp_method(self):
        self.assertTrue(hasattr(self.world, 'mdp'))

    def test_mdp_calculates_mdp_correctly(self):
        self.world.mdp(n=30)
        expected_utilities = [0.705, 0.655, 0.611, 0.388, 0.762, 0.0, 0.660, -1, 0.812, 0.868, 0.918, 1]
        calculated_utilities = self.world._get_utilities_for_fields(self.world.all_fields())
        for calculated, expected in zip(calculated_utilities, expected_utilities):
            self.assertAlmostEqual(expected, calculated, places=3)

    def test_mdp_with_termination_value_calculates_mdp_correctly(self):
        self.world.mdp(termination_value=0.0001)
        expected_utilities = [0.705, 0.655, 0.611, 0.388, 0.762, 0.0, 0.660, -1, 0.812, 0.868, 0.918, 1]
        calculated_utilities = self.world._get_utilities_for_fields(self.world.all_fields())
        for calculated, expected in zip(calculated_utilities, expected_utilities):
            self.assertAlmostEqual(expected, calculated, places=3)

    def test_has__mdp_stop_method(self):
        self.assertTrue(hasattr(self.world, '_mdp_stop'))

    def test_has_all_fields_method(self):
        self.assertTrue(hasattr(self.world, 'all_fields'))

    def test_all_fields_returns_list_of_fields(self):
        all_fields = self.world.all_fields()
        expected_len = (self.world.max_x + 1) * (self.world.max_y + 1)
        self.assertIsInstance(all_fields, list)
        self.assertIsInstance(all_fields[0], Field)
        self.assertIs(all_fields[0], self.world.field(0, 0))
        self.assertIs(all_fields[3], self.world.field(3, 0))
        self.assertIs(all_fields[4], self.world.field(0, 1))
        self.assertEqual(expected_len, len(all_fields))

    def test_has_max_of_all_actions_method(self):
        self.assertTrue(hasattr(self.world, 'max_of_all_actions'))

    def test_max_of_all_actions_returns_float(self):
        field = self.world.field(0, 0)
        self.assertTrue(isinstance(self.world.max_of_all_actions(field), float))

    def test_max_of_all_actions_returns_correct_value(self):
        self.world.field(0, 0).utility = 0.1
        self.world.field(0, 1).utility = 0.2
        self.world.field(1, 0).utility = 0.3
        field = self.world.field(0, 0)
        pu_up = self.world.pu_sum_for_action(field, World.up)
        pu_left = self.world.pu_sum_for_action(field, World.left)
        pu_right = self.world.pu_sum_for_action(field, World.right)
        pu_down = self.world.pu_sum_for_action(field, World.down)
        expected_value = max(pu_up, pu_left, pu_right, pu_down)
        self.assertAlmostEqual(expected_value, self.world.max_of_all_actions(field), places=5)

    def test_has_pu_sum_for_action_method(self):
        self.assertTrue(hasattr(self.world, 'pu_sum_for_action'))

    def test_pu_sum_for_action_returns_float(self):
        field = self.world.field(0, 0)
        action = World.up
        self.assertIsInstance(self.world.pu_sum_for_action(field, action), float)

    def test_pu_sum_for_action_calculates_correct_value(self):
        utility_this_field = self.world.field(0, 0).utility = 0.1
        utility_field_up = self.world.field(0, 1).utility = 0.2
        utility_field_right = self.world.field(1, 0).utility = 0.3
        field = self.world.field(0, 0)
        action = World.up
        expected_value = sum([
            utility_field_up * self.world.front_probability,
            utility_this_field * self.world.left_probability,
            utility_field_right * self.world.right_probability,
            utility_this_field * self.world.backward_probability
        ])
        self.assertAlmostEqual(expected_value, self.world.pu_sum_for_action(field, action), places=5)

    def test_pu_sum_for_action_gives_0_for_terminal_field_because_agent_cannot_move_from_this_field(self):
        field = self.world.field(3, 2)
        self.assertIs(Field.terminal, field.state)
        action = World.up
        expected_value = 0.0
        self.assertAlmostEqual(expected_value, self.world.pu_sum_for_action(field, action), places=5)

    def test_has__get_utilities_for_fields_method(self):
        self.assertTrue(hasattr(self.world, '_get_utilities_for_fields'))

    def test__get_utilities_for_fields_returns_list(self):
        fields_list = self.world.fields_around(self.world.field(0, 0), World.up)
        self.assertTrue(isinstance(self.world._get_utilities_for_fields(fields_list), list))

    def test__get_utilities_for_fields_gets_utilities_for_fields(self):
        self.world.field(0, 0).utility = 0.1
        self.world.field(0, 1).utility = 0.2
        self.world.field(1, 0).utility = 0.3
        fields_list = self.world.fields_around(self.world.field(0, 0), World.up)
        expected_list = [0.2, 0.1, 0.3, 0.1]
        method_returns = self.world._get_utilities_for_fields(fields_list)
        self.assertEqual(expected_list, method_returns)

    def test__get_utilities_for_fields_gives_initial_utility_when_no_utility_history_for_field(self):
        self.world.field(1, 0).utility = 0.3
        initial_utility = self.world.initial_utility
        fields_list = self.world.fields_around(self.world.field(0, 0), World.up)
        expected_list = [initial_utility, initial_utility, 0.3, initial_utility]
        method_returns = self.world._get_utilities_for_fields(fields_list)
        self.assertEqual(expected_list, method_returns)


