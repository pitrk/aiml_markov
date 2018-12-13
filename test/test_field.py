import unittest

from markov_libs import FieldStateUnknownException
from markov_libs import FieldRequiresValueException
from markov_libs import Field


class TestField(unittest.TestCase):
    def test_initialise_field(self):
        field = Field(Field.normal)
        self.assertEqual(field.state, Field.normal)
        self.assertEqual(field.reward, None)

    def test_initialise_field_with_value(self):
        field = Field(Field.special, 50)
        self.assertEqual(field.reward, 50)

    def test_check_class_attributes(self):
        self.assertEqual(Field.terminal, "T")
        self.assertEqual(Field.forbidden, "F")
        self.assertEqual(Field.normal, "N")
        self.assertEqual(Field.start, "S")
        self.assertEqual(Field.special, "B")

    def test_terminal_field_without_value_should_raise_exception(self):
        self.assertRaises(FieldRequiresValueException, Field, Field.terminal)

    def test_unknown_state_raises_exception(self):
        self.assertRaises(FieldStateUnknownException, Field, "K")
