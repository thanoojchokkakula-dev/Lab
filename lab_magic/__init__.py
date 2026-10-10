import os
import glob
import re

def _natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def list_programs(dir_path="."):
    """Return a list of all Python program filenames."""
    files = glob.glob(os.path.join(dir_path, "*.py"))
    ignore = {"setup.py", "lab.py"}
    programs = [
        os.path.basename(f)
        for f in files
        if not os.path.basename(f).startswith("__") and os.path.basename(f) not in ignore
    ]
    programs.sort(key=_natural_sort_key)
    return programs

def list_all(dir_path="."):
    """Print a clean numbered list of all available programs."""
    progs = list_programs(dir_path)
    if not progs:
        print("No programs found in directory.")
        return
    print(f"=== Available Programs ({len(progs)} total) ===")
    print("-" * 35)
    for i, p in enumerate(progs, 1):
        print(f"  [{i}] {p}")
    print("-" * 35)

list = list_all

def get_code(name, dir_path="."):
    """Read and return code for a program (by name e.g. 'p1' or by number e.g. 1)."""
    progs = list_programs(dir_path)
    if isinstance(name, int) or (isinstance(name, str) and str(name).strip().isdigit()):
        idx = int(name) - 1
        if 0 <= idx < len(progs):
            filename = progs[idx]
        else:
            raise IndexError(f"Index {name} out of range (1 to {len(progs)} available).")
    else:
        name_str = str(name).strip()
        filename = name_str if name_str.endswith(".py") else f"{name_str}.py"

    filepath = os.path.join(dir_path, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Program '{filename}' not found. Available programs: {progs}"
        )
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read(), filename

def show(name, dir_path="."):
    """Print code with clean formatting."""
    code, filename = get_code(name, dir_path)
    print(f"--- {filename} ---")
    print(code)
    print("-" * (len(filename) + 8))

# IPython Magic registration
try:
    from IPython.core.magic import Magics, magics_class, line_magic

    @magics_class
    class LabMagics(Magics):
        @line_magic
        def print_code(self, line):
            """Usage: %print_code p1 or %print_code 1"""
            name = line.strip()
            if not name:
                list_all()
                print("Usage: %print_code <name_or_number> (e.g. %print_code p1)")
                return
            try:
                show(name)
            except Exception as e:
                print(f"Error: {e}")

        @line_magic
        def load_code(self, line):
            """Usage: %load_code p1 or %load_code 1 (loads code directly into Jupyter cell)"""
            name = line.strip()
            if not name:
                print("Usage: %load_code <name_or_number> (e.g. %load_code p1)")
                return
            try:
                code, _ = get_code(name)
                self.shell.set_next_input(code, replace=True)
            except Exception as e:
                print(f"Error: {e}")

        @line_magic
        def list_codes(self, line):
            """Usage: %list_codes"""
            list_all()

    def load_ipython_extension(ipython):
        ipython.register_magics(LabMagics)

except ImportError:
    pass
