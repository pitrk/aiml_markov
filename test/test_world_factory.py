import unittest
import unittest.mock
import toml

from markov_libs import BoardEmptyException
from markov_libs import WorldFactory
from markov_libs import Field


class TestWorldFactory(unittest.TestCase):
    mock_file_content = """
        title = "default"
        size = [4, 3]
        reward = -0.04
        gamma = 1
        epsilon = 0
        probability = [0.8, 0.1, 0.1, 0.0]
        
        [states]
            [states.start]
                position = [0, 0]
        
            [[states.terminal]]
                position = [3, 2]
                value = 1
        
            [[states.terminal]]
                position = [3, 1]
                value = -1
        
            [[states.forbidden]]
                position = [1, 1]
    """

    mock_dict_content = toml.loads(mock_file_content)

    @unittest.mock.patch(
        'builtins.open',
        new=unittest.mock.mock_open(read_data=mock_file_content),
        create=True
    )
    def setUp(self):
        self.board_factory = WorldFactory(self.mock_dict_content)

    def test_world_has_fields(self):
        self.assertTrue(hasattr(self.board_factory, 'data'))

    def test_init_creates_dictionary_with_data_field(self):
        self.assertEqual(self.board_factory.data, self.mock_dict_content)

    def test_has_board_generator_method(self):
        self.assertTrue(hasattr(self.board_factory, 'board_generator'))

    def test_has__get_start_field_position_from_dict_method(self):
        self.assertTrue(hasattr(self.board_factory, '_get_start_field_position_from_dict'))

    def test__get_start_field_position_from_dict_returns_list_x_y(self):
        method_return = self.board_factory._get_start_field_position_from_dict(self.mock_dict_content)
        self.assertEqual(method_return, [0, 0])

    def test_has__generate_default_board_method(self):
        self.assertTrue(hasattr(self.board_factory, '_generate_default_board'))

    def test__generate_default_board_generates_board_x_y_normal(self):
        x = 2
        y = 3
        method_returns = self.board_factory._generate_default_board(x, y)
        for j in range(y):
            for i in range(x):
                self.assertEqual(Field(Field.normal), method_returns[j][i])

    def test_has__generate_table_for_board_method(self):
        self.assertTrue(hasattr(self.board_factory, '_generate_table_for_board'))

    def test__generate_table_for_board_creates_nonempty_list(self):
        method_returns = self.board_factory._generate_table_for_board(2, 2)
        self.assertIsInstance(method_returns, list)
        self.assertNotEqual(len(method_returns), 0)

    def test__generate_table_for_board_creates_table_x_y(self):
        x = 2
        y = 3
        method_returns = self.board_factory._generate_table_for_board(x, y)
        self.assertEqual(len(method_returns), y)
        self.assertEqual(len(method_returns[0]), x)

    def test__generate_table_for_board_is_not_working_like_wtf(self):
        method_returns = self.board_factory._generate_table_for_board(2, 2)
        method_returns[0][0] = "d"
        self.assertNotEqual(method_returns[1][0], "d")

    def test_has__fill_board_with_default_method(self):
        self.assertTrue(hasattr(self.board_factory, '_fill_board_with_default'))

    def test__fill_board_with_default_raises_exception_when_board_empty(self):
        self.assertRaises(BoardEmptyException, self.board_factory._fill_board_with_default, [])

    def test__fill_board_with_default_fills_whole_board_with_normal_fields(self):
        x = 2
        y = 3
        board = self.board_factory._generate_table_for_board(x, y)
        filled_board = self.board_factory._fill_board_with_default(board)
        for j in range(y):
            for i in range(x):
                self.assertEqual(Field(Field.normal), filled_board[j][i])

    def test_filled_board_fields_not_the_same_field(self):
        x = 2
        y = 3
        board = self.board_factory._generate_table_for_board(x, y)
        filled_board = self.board_factory._fill_board_with_default(board)
        filled_board[0][1] = Field(Field.start)
        self.assertNotEqual(filled_board[1][1], Field(Field.start))






