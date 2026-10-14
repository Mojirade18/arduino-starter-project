"""Everything about compiling Arduino code with arduino-cli."""
import subprocess
import tempfile
from pathlib import Path

BOARD = "arduino:avr:uno"


def compile_code(code):
    """Compile Arduino code with arduino-cli. Returns (worked?, error messages)."""
    with tempfile.TemporaryDirectory() as tmp:
        sketch_dir = Path(tmp) / "sketch"
        sketch_dir.mkdir()
        sketch_file = sketch_dir / "sketch.ino"
        sketch_file.write_text(code)
        result = subprocess.run(
            ["arduino-cli", "compile", "--fqbn", BOARD, str(sketch_dir)],
            capture_output=True, text=True,
        )
        output = (result.stdout + result.stderr).replace(str(sketch_file), "sketch.ino")
        return result.returncode == 0, output


def only_error_lines(errors):
    """Keep just the lines that say 'error:', so the AI isn't distracted by the rest."""
    return "\n".join(line for line in errors.splitlines() if "error:" in line)