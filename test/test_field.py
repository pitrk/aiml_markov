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

    def test_has_q_value_method(self):
        self.assertTrue(hasattr(Field, 'q_value'))

    def test_q_val_method_returns_q_value(self):
        field = Field(Field.normal, x=0, y=1, reward=1)
        field.q_values = [-0.1, -0.2, -0.3, -0.4]
        self.assertEqual(-0.1, field.q_value('^'))
        self.assertEqual(-0.2, field.q_value('<'))
        self.assertEqual(-0.3, field.q_value('>'))
        self.assertEqual(-0.4, field.q_value('v'))

    def test_set_q_value_method_sets_value_for_action(self):
        field = Field(Field.normal, x=0, y=0, reward=-0.04)
        field.set_q_value(Field.up, -0.02)
        self.assertEqual(-0.02, field.q_value(Field.up))

    def test_str_q_value_returns_constant_width_number(self):
        field = Field(Field.normal, x=0, y=1, reward=1)
        field.q_values = [0.0012, 0.1010, 0.2345, 0.1234]
        self.assertEqual(5, len(field.str_q_value(Field.up)))
        self.assertEqual(str(0.123), field.str_q_value(Field.down))

    def test_str_q_value_returns_constant_width_text_when_field_forbidden(self):
        field = Field(Field.forbidden, x=0, y=1, reward=1)
        self.assertEqual(5, len(field.str_q_value(Field.up)))
        self.assertEqual("xxxxx", field.str_q_value(Field.up))

    def test_has_is_terminal_method(self):
        self.assertTrue(Field, 'is_terminal')

    def test_is_terminal_returns_true_when_terminal(self):
        field = Field(Field.terminal, x=0, y=0, reward=1)
        self.assertTrue(field.is_terminal())

    def test_is_terminal_returns_false_when_not_terminal(self):
        field = Field(Field.normal, x=0, y=0, reward=-0.04)
        self.assertFalse(field.is_terminal())

    def test_increment_action_counter_up_and_nothing_else(self):
        field = Field(Field.normal, x=0, y=0, reward=-0.04)
        self.assertEqual([0, 0, 0, 0], field.actions_count)
        field.increment_action_counter(Field.up)
        self.assertEqual(1, field.actions_count[0])
        self.assertEqual(0, field.actions_count[1])
        self.assertEqual(0, field.actions_count[2])
        self.assertEqual(0, field.actions_count[3])

    def test_increment_action_counter_directions(self):
        field = Field(Field.normal, x=0, y=0, reward=-0.04)
        field.increment_action_counter(Field.up)
        self.assertEqual(1, field.actions_count[0])
        field.increment_action_counter(Field.left)
        self.assertEqual(1, field.actions_count[1])
        field.increment_action_counter(Field.right)
        self.assertEqual(1, field.actions_count[2])
        field.increment_action_counter(Field.down)
        self.assertEqual(1, field.actions_count[3])

    def test_get_action_counter_value(self):
        field = Field(Field.normal, x=0, y=0, reward=-0.04)
        field.increment_action_counter(Field.up)
        self.assertEqual(1, field.get_action_counter_value(Field.up))

    def test_optimal_action(self):
        field = Field(Field.normal, x=0, y=0, reward=-0.04)
        field.q_values = [-0.02, -0.04, -0.06, -0.08]
        self.assertEqual(Field.up, field.optimal_action())

    def test_str_optimal_action(self):
        field = Field(Field.normal, x=0, y=0, reward=-0.04)
        field.q_values = [-0.02, -0.04, -0.06, -0.08]
        self.assertEqual(Field.up, field.str_optimal_action())

    def test_str_optimal_action_when_forbidden(self):
        field = Field(Field.forbidden, x=0, y=0,)
        field.q_values = [-0.02, -0.04, -0.06, -0.08]
        self.assertEqual('x', field.str_optimal_action())
