''' Unit tests for calculator functions using unittest framework. '''

import sys
import os
import unittest

# Get the path to the project's root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from src.calculator import fun1, fun2, fun3, fun4, check_type

class TestCalculator(unittest.TestCase):
    def test_fun1(self):
        self.assertEqual(fun1(2, 3), 5)
        self.assertEqual(fun1(-1, 1), 0)
        self.assertEqual(fun1(0, 0), 0)
        self.assertEqual(fun1(2.5, 3.5), 6.0)
        self.assertEqual(fun1(-2.5, 4), 1.5)

    def test_fun2(self):
        self.assertEqual(fun2(2, 3), -1)
        self.assertEqual(fun2(-1, 1), -2)
        self.assertEqual(fun2(0, 0), 0)
        self.assertEqual(fun2(2.5, 3.5), -1.0)
        self.assertEqual(fun2(-2.5, 4), -6.5)

    def test_fun3(self):
        self.assertEqual(fun3(2, 3), 6)
        self.assertEqual(fun3(-1, 1), -1)
        self.assertEqual(fun3(0, 0), 0)
        self.assertEqual(fun3(2.5, 3.5), 8.75)
        self.assertEqual(fun3(-2.5, 4), -10.0)

    def test_fun4(self):
        self.assertEqual(fun4(2, 3), 10)
        self.assertEqual(fun4(-1, 1), -3)
        self.assertEqual(fun4(0, 0), 0)
        self.assertEqual(fun4(2.5, 3.5), 13.75)
        self.assertEqual(fun4(-2.5, 4), -15.0)

    def test_check_type(self):
        with self.assertRaises(TypeError):
            check_type("a", 1)
        with self.assertRaises(TypeError):
            check_type(1, "b")
        with self.assertRaises(TypeError):
            check_type("a", "b")
        # Valid types should not raise an error
        try:
            check_type(1, 2)
            check_type(1.5, 2.5)
            check_type(-1, -2)
        except TypeError:
            self.fail("check_type raised TypeError unexpectedly!")

if __name__ == '__main__':
    unittest.main()
