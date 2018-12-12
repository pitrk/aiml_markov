import unittest
from markov_libs import World


class TestWorld(unittest.TestCase):
    def setUp(self):
        self.world = World()

    def test_has_load_from_file_method(self):
        self.assertTrue(hasattr(self.world, 'load_from_file'))
