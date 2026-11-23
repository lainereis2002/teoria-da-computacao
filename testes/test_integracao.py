import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from python.algoritmos import merge_sort, quick_sort


class CrossLanguageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.executable = ROOT / "c" / "executar.exe"
        if not cls.executable.exists():
            raise unittest.SkipTest("Compile c/executar.exe antes do teste de integracao.")

    def test_four_implementations_match(self) -> None:
        cases = [
            [],
            [1.0],
            [2.0, 1.0],
            [3.5, -1.25, 3.5, 0.0, -9.75],
            [float(index % 17) for index in range(100, -1, -1)],
        ]
        for case_index, values in enumerate(cases):
            expected = sorted(values)
            python_quick = values.copy()
            python_merge = values.copy()
            quick_sort(python_quick)
            merge_sort(python_merge)
            self.assertEqual(expected, python_quick)
            self.assertEqual(expected, python_merge)
            with tempfile.TemporaryDirectory() as directory_name:
                directory = Path(directory_name)
                input_path = directory / f"entrada_{case_index}.txt"
                input_path.write_text(
                    "".join(f"{value:.17g}\n" for value in values),
                    encoding="ascii",
                )
                outputs = []
                for algorithm in ("quick", "merge"):
                    output_path = directory / f"{algorithm}.txt"
                    subprocess.run(
                        [
                            str(self.executable),
                            algorithm,
                            str(input_path),
                            str(output_path),
                        ],
                        check=True,
                    )
                    outputs.append(
                        [
                            float(line)
                            for line in output_path.read_text(encoding="ascii").splitlines()
                        ]
                    )
                self.assertEqual(expected, outputs[0])
                self.assertEqual(expected, outputs[1])


if __name__ == "__main__":
    unittest.main()
