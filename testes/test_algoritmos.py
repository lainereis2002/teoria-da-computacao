import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from python.algoritmos import merge_sort, quick_sort


class SortingTests(unittest.TestCase):
    def check_case(self, values: list[float]) -> None:
        expected = sorted(values)
        quick_values = values.copy()
        merge_values = values.copy()
        quick_sort(quick_values)
        merge_sort(merge_values)
        self.assertEqual(expected, quick_values)
        self.assertEqual(expected, merge_values)
        self.assertEqual(quick_values, merge_values)

    def test_edge_cases(self) -> None:
        cases = [
            [],
            [1.0],
            [1.0, 2.0],
            [2.0, 1.0],
            [1.0, 2.0, 3.0, 4.0],
            [4.0, 3.0, 2.0, 1.0],
            [3.5, -1.25, 3.5, 0.0, -9.75],
            [7.0] * 20,
        ]
        for values in cases:
            with self.subTest(values=values):
                self.check_case(values)

    def test_deterministic_random_cases(self) -> None:
        generator = random.Random(42)
        for length in range(2, 201):
            values = [generator.uniform(-100.0, 100.0) for _ in range(length)]
            self.check_case(values)

    def test_merge_rejects_small_auxiliary(self) -> None:
        with self.assertRaises(ValueError):
            merge_sort([2.0, 1.0], [0.0])


if __name__ == "__main__":
    unittest.main()
