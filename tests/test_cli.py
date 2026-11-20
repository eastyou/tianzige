"""测试命令行入口。"""

from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from tianzige.cli import main


def run_cli(args: list) -> tuple:
    stdout, stderr = io.StringIO(), io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        code = main(args)
    return code, stdout.getvalue(), stderr.getvalue()


class CliTests(unittest.TestCase):
    def test_text_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "zitie.html"
            code, stdout, _ = run_cli(["--text", "春眠不觉晓", "-o", str(output)])
            self.assertEqual(code, 0)
            content = output.read_text(encoding="utf-8")
            self.assertIn("春", content)
            self.assertIn("已生成", stdout)
            self.assertIn("5 个字", stdout)

    def test_file_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "words.txt"
            source.write_text("春眠\n不觉晓\n", encoding="utf-8")
            output = Path(tmp) / "zitie.html"
            code, _, _ = run_cli(["-i", str(source), "-o", str(output)])
            self.assertEqual(code, 0)
            self.assertIn("春", output.read_text(encoding="utf-8"))

    def test_comment_lines_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "words.txt"
            source.write_text("# 说明文字\n春\n", encoding="utf-8")
            output = Path(tmp) / "zitie.html"
            code, stdout, _ = run_cli(["-i", str(source), "-o", str(output)])
            self.assertEqual(code, 0)
            self.assertIn("1 个字", stdout)

    def test_blank_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, _, stderr = run_cli(
                ["--text", "   ", "-o", str(Path(tmp) / "z.html")]
            )
            self.assertEqual(code, 2)
            self.assertIn("没有可练习的字", stderr)

    def test_missing_file(self) -> None:
        code, _, stderr = run_cli(["-i", "/tmp/none.txt"])
        self.assertEqual(code, 2)
        self.assertIn("文件不存在", stderr)

    def test_invalid_trace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, _, stderr = run_cli(
                ["--text", "春", "--repeat", "5", "--trace", "6", "-o", str(Path(tmp) / "z.html")]
            )
            self.assertEqual(code, 2)
            self.assertIn("描红", stderr)

    def test_grid_choice(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "z.html"
            run_cli(["--text", "春", "--grid", "mi", "-o", str(output)])
            self.assertIn('class="grid mi"', output.read_text(encoding="utf-8"))

    def test_write_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, _, stderr = run_cli(["--text", "春", "-o", tmp])
            self.assertEqual(code, 1)
            self.assertIn("写入文件失败", stderr)

    def test_pagination_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "z.html"
            _, stdout, _ = run_cli(
                [
                    "--text",
                    "春夏秋冬",
                    "--rows-per-char",
                    "2",
                    "--page-rows",
                    "4",
                    "-o",
                    str(output),
                ]
            )
            self.assertIn("8 行", stdout)
            self.assertIn("2 页", stdout)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
