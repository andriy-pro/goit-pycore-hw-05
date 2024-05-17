from typing import Callable

import unittest
import time
import tracemalloc
import sys
import os

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.caching_fibonacci import caching_fibonacci


def measure_performance(func):
    def wrapper(*args, **kwargs):
        # Measure time
        start_time = time.time()

        # Measure memory usage
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Calculate execution time
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # convert to milliseconds

        # Convert memory usage to kilobytes
        current_kb = current / 1024
        peak_kb = peak / 1024

        # Print performance results
        print(
            f"\n{func.__name__.replace('test_', '').ljust(35, '.')}: Duration: {duration:>7.3f} ms;  Mem.Curr.: {current_kb:>7.3f} KB, Peak: {peak_kb:>7.3f} KB",
            end="",
        )

        return result

    return wrapper


class TestCachingFibonacci(unittest.TestCase):
    def setUp(self):
        """Initialize the Fibonacci function."""
        self.fib: Callable[[int], int] = caching_fibonacci()

    @measure_performance
    def test_a1_base_case_zero(self):
        """Test the base case when n = 0."""
        self.assertEqual(self.fib(0), 0)

    @measure_performance
    def test_a2_base_case_one(self):
        """Test the base case when n = 1."""
        self.assertEqual(self.fib(1), 1)

    @measure_performance
    def test_a3_small_positive_number(self):
        """Test with a small positive number."""
        self.assertEqual(self.fib(5), 5)

    @measure_performance
    def test_b1_consecutive_calls(self):
        """Test consecutive calls."""
        self.assertEqual(self.fib(16), 987)
        self.assertEqual(self.fib(17), 1597)
        self.assertEqual(self.fib(18), 2584)
        self.assertEqual(self.fib(19), 4181)
        self.assertEqual(self.fib(20), 6765)
        self.assertEqual(self.fib(19), 4181)
        self.assertEqual(self.fib(18), 2584)
        self.assertEqual(self.fib(15), 610)
        self.assertEqual(self.fib(10), 55)
        self.assertEqual(self.fib(5), 5)

    @measure_performance
    def test_b2_repeated_calls_same_value(self):
        """Test repeated calls for the same Fibonacci number."""
        for _ in range(20):
            self.assertEqual(self.fib(20), 6765)

    @measure_performance
    def test_c1_large_input_100(self):
        """Test the function with a large input."""
        self.assertEqual(self.fib(100), 354224848179261915075)

    @measure_performance
    def test_c2_large_input_978(self):
        """Test the function with a large input."""
        self.assertEqual(
            self.fib(978),
            1097557198057001938453841363644415006374573595389643436520255061711780089392489003778952798974711705543381888276590315395738796138788161499726039945177057123749403326820574003343599955000130556475552464664,
        )

    @measure_performance
    def test_d1_negative_input(self):
        """Validate the function's behavior with a negative input."""
        with self.assertRaises(ValueError):
            self.fib(-5)

    @measure_performance
    def test_d2_float_input(self):
        """Check the function's response to non-integer input."""
        with self.assertRaises(ValueError):
            self.fib(5.5)

    @measure_performance
    def test_d3_string_input(self):
        """Check the function's response to string input."""
        with self.assertRaises(TypeError):
            self.fib("abc")


if __name__ == "__main__":
    unittest.main()
