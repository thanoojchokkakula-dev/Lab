"""Browse the DVA text files included in this package."""

from pathlib import Path
import re
from typing import List, Union


_PROGRAM_DIR = Path(__file__).parent


def _programs() -> List[Path]:
    return sorted(
        _PROGRAM_DIR.glob("*.txt"),
        key=lambda path: [
            int(part) if part.isdigit() else part.lower()
            for part in re.split(r"(\d+)", path.name)
        ],
    )


def list() -> None:
    """Print the numbered list of available DVA files."""
    programs = _programs()
    if not programs:
        print("No DVA files are available.")
        return

    print(f"=== Available DVA Codes ({len(programs)} total) ===")
    for index, program in enumerate(programs, 1):
        print(f"[{index}] {program.name}")


def show(program: Union[int, str]) -> None:
    """Print a DVA file by its number from list() or by its filename."""
    programs = _programs()

    if isinstance(program, int):
        if program < 1 or program > len(programs):
            raise IndexError(
                f"Program number {program} is out of range "
                f"(1 to {len(programs)} available)."
            )
        selected = programs[program - 1]
    elif isinstance(program, str):
        requested = Path(program).name.lower()
        if not requested.endswith(".txt"):
            requested += ".txt"
        selected = next(
            (path for path in programs if path.name.lower() == requested),
            None,
        )
        if selected is None:
            available = ", ".join(path.name for path in programs)
            raise FileNotFoundError(
                f"DVA file '{program}' was not found. Available files: {available}"
            )
    else:
        raise TypeError("program must be a program number or filename")

    print(f"--- {selected.name} ---")
    print(selected.read_text(encoding="utf-8"))
    print("-" * (len(selected.name) + 8))
