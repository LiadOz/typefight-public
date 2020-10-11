import unittest
from unittest.mock import MagicMock
from backend.register import Register, RegisterData


class TestRegister(unittest.TestCase):
    def setUp(self):
        self.reg = Register(None, 't')

    def test_child(self):
        self.assertEqual('t/a', self.reg.child_register('/a').endpoint)

    def test_out(self):
        class Change:
            first = True

            def func(x):
                if Change.first:
                    Change.first = False
                    return 1
                else:
                    return 2

        self.reg._out_function = MagicMock()
        data = RegisterData('a')
        new_func = self.reg.register_out(Change.func, data)
        new_func(None)
        self.reg._out_function.assert_called_with(data)
        self.assertEqual(data.event, 'a')
        self.assertEqual(data.data, 1)

        new_func(None)
        self.reg._out_function.assert_called_with(data)
        self.assertEqual(data.event, 'a')
        self.assertEqual(data.data, 2)

    def test_notify(self):
        wrapped = MagicMock()
        self.reg._notify_function = MagicMock()
        data = RegisterData('a', lambda: 1)
        self.reg.register_notify(wrapped, data)()
        wrapped.assert_called()
        self.reg._notify_function.assert_called()
