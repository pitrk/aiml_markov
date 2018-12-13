import unittest
import unittest.mock
import toml

from markov_libs import World


class TestWorld(unittest.TestCase):
    mock_file_content = """
        title = "default"
        size = [4, 3]
        reward = -0.04
        gamma = 1
        epsilon = 0
        probability = [0.8, 0.1, 0.1, 0.0]
        
        [states]
            [states.start]
                position = [1, 1]
        
            [[states.terminal]]
                position = [4, 3]
                value = 1
        
            [[states.terminal]]
                position = [4, 2]
                value = -1
        
            [[states.forbidden]]
                position = [2, 2]
    """

    def setUp(self):
        self.world = World()

    def test_has_load_from_file_method(self):
        self.assertTrue(hasattr(self.world, 'load_from_file'))

    def test_has__parse_toml_method(self):
        self.assertTrue(hasattr(self.world, '_parse_toml'))

    @unittest.mock.patch(
        'builtins.open',
        new=unittest.mock.mock_open(read_data=mock_file_content),
        create=True
    )
    def test__parse_toml_returns_dict(self):
        method_return = self.world._parse_toml('/dev/null')
        self.assertIsInstance(method_return, dict)

    @unittest.mock.patch(
        'builtins.open',
        new=unittest.mock.mock_open(read_data=mock_file_content),
        create=True
    )
    def test__parse_toml_returns_correct_dict(self):
        correct_dict = toml.loads(self.mock_file_content)
        self.assertEqual(self.world._parse_toml('/dev/null'), correct_dict)

