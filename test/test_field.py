import unittest

from markov_libs import FieldStateUnknownException
from markov_libs import FieldRequiresValueException
from markov_libs import EmptyUtilityHistoryException
from markov_libs import Field


class TestField(unittest.TestCase):
    def test_initialise_field(self):
        field = Field(Field.normal, x=0, y=1, reward=-0.04, utility=0)
        self.assertEqual(Field.normal, field.state)
        self.assertEqual(0, field.x)
        self.assertEqual(1, field.y)
        self.assertEqual(-0.04, field.reward)
        self.assertEqual(0, field.utility)

    def test_check_class_attributes(self):
        self.assertEqual(Field.terminal, "T")
        self.assertEqual(Field.forbidden, "F")
        self.assertEqual(Field.normal, "N")
        self.assertEqual(Field.start, "S")
        self.assertEqual(Field.special, "B")

    def test_terminal_field_without_value_should_raise_exception(self):
        self.assertRaises(FieldRequiresValueException, Field, Field.terminal, x=0, y=0)

    def test_unknown_state_raises_exception(self):
        self.assertRaises(FieldStateUnknownException, Field, "K", x=0, y=0)

    def test_has_utility_property(self):
        self.assertTrue(hasattr(Field, 'utility'))

    def test_utility_returns_last_utility_value(self):
        field = Field(Field.normal, x=0, y=1, reward=-0.04, utility=0)
        field.utility = 1
        self.assertEqual(1, field.utility)

    def test_utility_history_has_whole_history(self):
        field = Field(Field.normal, x=0, y=1, reward=-0.04, utility=0)
        field.utility = 1
        self.assertEqual([0, 1], field.utility_history)

    def test_utility_history_deleter_removes_last_record_from_history(self):
        field = Field(Field.normal, x=0, y=1, reward=-0.04, utility=0)
        field.utility = 1
        del field.utility
        self.assertEqual([0], field.utility_history)

    def test_utility_getter_raises_exception_if_empty(self):
        field = Field(Field.normal, x=0, y=1, reward=-0.04)
        with self.assertRaises(EmptyUtilityHistoryException):
            _ = field.utility

    def test_utility_deleter_raises_exception_if_empty(self):
        field = Field(Field.normal, x=0, y=1, reward=-0.04)
        with self.assertRaises(EmptyUtilityHistoryException):
            del field.utility

    def test_terminal_state_utility_is_reward(self):
        field = Field(Field.terminal, x=0, y=1, reward=1)
        self.assertEqual(1, field.utility)

    def test_has_str_policy_property(self):
        self.assertTrue(hasattr(Field, 'str_policy'))

    def test_str_policy_returns_correct_string(self):
        field = Field(Field.normal, x=0, y=1, reward=1)
        field.policy = '^'
        self.assertEqual('^', field.str_policy)
        field.policy = None
        self.assertEqual('x', field.str_policy)

    def test_has_str_utility_property(self):
        self.assertTrue(hasattr(Field, 'str_utility'))

    def test_str_uility_returns_constant_width_number(self):
        field = Field(Field.normal, x=0, y=1, reward=1)
        field.utility = 1.2345678
        self.assertEqual(7, len(field.str_utility))
        self.assertEqual(str(1.23456), field.str_utility)

    def test_str_uility_returns_constant_width_text_when_no_utility(self):
        field = Field(Field.normal, x=0, y=1, reward=1)
        self.assertEqual(7, len(field.str_utility))
        self.assertEqual("xxxxxxx", field.str_utility)
