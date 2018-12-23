import unittest.mock

import toml

from markov_libs import BoardEmptyException
from markov_libs import Field
from markov_libs import WorldFactory


class TestWorldFactory(unittest.TestCase):
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
        self.world_factory = WorldFactory(self.mock_dict_content)

    def test_world_has_fields(self):
        self.assertTrue(hasattr(self.world_factory, 'data'))
        self.assertTrue(hasattr(self.world_factory, 'board'))

    def test_init_creates_dictionary_with_data_field(self):
        self.assertEqual(self.world_factory.data, self.mock_dict_content)

    def test_has__get_default_reward_method(self):
        self.assertTrue(hasattr(self.world_factory, '_get_default_reward'))

    def test__get_default_reward_returns_default_reward(self):
        self.assertEqual(self.world_factory._get_default_reward(), -0.04)

    def test_has__get_board_size_method(self):
        self.assertTrue(hasattr(self.world_factory, '_get_board_size'))

    def test__get_board_size_method_returns_dict_of_coordinates(self):
        self.assertEqual(
            {
                'x': 4,
                'y': 3
            },
            self.world_factory._get_board_size(),
        )

    def test_has_board_generator_method(self):
        self.assertTrue(hasattr(self.world_factory, 'board_generator'))

    def test_board_generator_generates_correct_board(self):
        self.world_factory.board_generator()

        self.assertEqual(Field.normal, self.world_factory.board[2][1].state)
        self.assertEqual(-0.04, self.world_factory.board[2][1].reward)
        self.assertEqual(1, self.world_factory.board[2][1].x)
        self.assertEqual(2, self.world_factory.board[2][1].y)

        self.assertEqual(Field.start, self.world_factory.board[0][0].state)
        self.assertEqual(-0.04, self.world_factory.board[0][0].reward)
        self.assertEqual(0, self.world_factory.board[0][0].x)
        self.assertEqual(0, self.world_factory.board[0][0].y)

        self.assertEqual(Field.terminal, self.world_factory.board[2][3].state)
        self.assertEqual(1, self.world_factory.board[2][3].reward)
        self.assertEqual(3, self.world_factory.board[2][3].x)
        self.assertEqual(2, self.world_factory.board[2][3].y)

        self.assertEqual(Field.terminal, self.world_factory.board[1][3].state)
        self.assertEqual(-1, self.world_factory.board[1][3].reward)
        self.assertEqual(3, self.world_factory.board[1][3].x)
        self.assertEqual(1, self.world_factory.board[1][3].y)

        self.assertEqual(Field.forbidden, self.world_factory.board[1][1].state)
        self.assertEqual(None, self.world_factory.board[1][1].reward)
        self.assertEqual(1, self.world_factory.board[1][1].x)
        self.assertEqual(1, self.world_factory.board[1][1].y)

        self.assertEqual(Field.special, self.world_factory.board[1][2].state)
        self.assertEqual(2, self.world_factory.board[1][2].reward)
        self.assertEqual(2, self.world_factory.board[1][2].x)
        self.assertEqual(1, self.world_factory.board[1][2].y)

    def test_has__generate_default_board_method(self):
        self.assertTrue(hasattr(self.world_factory, '_generate_default_board'))

    def test__generate_default_board_generates_board_x_y_normal(self):
        x = 2
        y = 3
        self.world_factory._generate_default_board(x, y)
        for j in range(y):
            for i in range(x):
                self.assertEqual(Field.normal, self.world_factory.board[j][i].state)
                self.assertEqual(-0.04, self.world_factory.board[j][i].reward)
                self.assertEqual(j, self.world_factory.board[j][i].y)
                self.assertEqual(i, self.world_factory.board[j][i].x)

    def test_has__generate_table_for_board_method(self):
        self.assertTrue(hasattr(self.world_factory, '_generate_table_for_board'))

    def test__generate_table_for_board_creates_nonempty_list(self):
        method_returns = self.world_factory._generate_table_for_board(2, 2)
        self.assertIsInstance(method_returns, list)
        self.assertNotEqual(len(method_returns), 0)

    def test__generate_table_for_board_creates_table_x_y(self):
        x = 2
        y = 3
        method_returns = self.world_factory._generate_table_for_board(x, y)
        self.assertEqual(len(method_returns), y)
        self.assertEqual(len(method_returns[0]), x)

    def test__generate_table_for_board_is_not_working_like_wtf(self):
        method_returns = self.world_factory._generate_table_for_board(2, 2)
        method_returns[0][0] = "d"
        self.assertNotEqual(method_returns[1][0], "d")

    def test_has__fill_board_with_default_method(self):
        self.assertTrue(hasattr(self.world_factory, '_fill_board_with_default'))

    def test__fill_board_with_default_raises_exception_when_board_empty(self):
        self.assertRaises(BoardEmptyException, self.world_factory._fill_board_with_default, [])

    def test__fill_board_with_default_fills_whole_board_with_normal_fields(self):
        x = 2
        y = 3
        board = self.world_factory._generate_table_for_board(x, y)
        filled_board = self.world_factory._fill_board_with_default(board)
        for j in range(y):
            for i in range(x):
                self.assertEqual(Field.normal, filled_board[j][i].state)
                self.assertEqual(-0.04, filled_board[j][i].reward)
                self.assertEqual(j, filled_board[j][i].y)
                self.assertEqual(i, filled_board[j][i].x)

    def test_filled_board_fields_not_the_same_field(self):
        x = 2
        y = 3
        board = self.world_factory._generate_table_for_board(x, y)
        filled_board = self.world_factory._fill_board_with_default(board)
        filled_board[0][1] = Field(Field.start, x=1, y=0, reward=-0.04)
        self.assertNotEqual(filled_board[1][1], filled_board[0][1])

    def test_has__add_state_fields_method(self):
        self.assertTrue(hasattr(self.world_factory, '_add_state_fields'))

    def test__add_state_fields_adds_state_fields(self):
        self.world_factory._generate_default_board(4, 3)
        self.world_factory._add_state_fields()

        self.assertEqual(Field.start, self.world_factory.board[0][0].state)
        self.assertEqual(0, self.world_factory.board[0][0].x)
        self.assertEqual(0, self.world_factory.board[0][0].y)
        self.assertEqual(-0.04, self.world_factory.board[0][0].reward)

        self.assertEqual(Field.terminal, self.world_factory.board[2][3].state)
        self.assertEqual(3, self.world_factory.board[2][3].x)
        self.assertEqual(2, self.world_factory.board[2][3].y)
        self.assertEqual(1, self.world_factory.board[2][3].reward)

        self.assertEqual(Field.terminal, self.world_factory.board[1][3].state)
        self.assertEqual(3, self.world_factory.board[1][3].x)
        self.assertEqual(1, self.world_factory.board[1][3].y)
        self.assertEqual(-1, self.world_factory.board[1][3].reward)

        self.assertEqual(Field.forbidden, self.world_factory.board[1][1].state)
        self.assertEqual(1, self.world_factory.board[1][1].x)
        self.assertEqual(1, self.world_factory.board[1][1].y)
        self.assertEqual(None, self.world_factory.board[1][1].reward)

        self.assertEqual(Field.special, self.world_factory.board[1][2].state)
        self.assertEqual(2, self.world_factory.board[1][2].reward)
        self.assertEqual(2, self.world_factory.board[1][2].x)
        self.assertEqual(1, self.world_factory.board[1][2].y)

    def test_has__get_reward_for_field_method(self):
        self.assertTrue(hasattr(self.world_factory, '_get_reward_for_field'))

    def test__get_reward_for_field_if_start(self):
        method_returns = self.world_factory._get_reward_for_field(self.world_factory.data['state'][0])
        self.assertEqual(self.world_factory.data['reward'], method_returns)

    def test__get_reward_for_field_if_forbidden(self):
        method_returns = self.world_factory._get_reward_for_field(self.world_factory.data['state'][3])
        self.assertIsNone(method_returns)

    def test__get_reward_for_field_if_special(self):
        method_returns = self.world_factory._get_reward_for_field(self.world_factory.data['state'][4])
        self.assertEqual(2, method_returns)

    def test__get_reward_for_field_if_terminal(self):
        method_returns = self.world_factory._get_reward_for_field(self.world_factory.data['state'][2])
        self.assertEqual(-1, method_returns)
