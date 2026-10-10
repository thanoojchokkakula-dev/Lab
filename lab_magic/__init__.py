import os
import glob
import re

def _natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def list_programs(dir_path="."):
    """Return a list of all Python (.py) and text (.txt) program filenames."""
    py_files = glob.glob(os.path.join(dir_path, "*.py"))
    txt_files = glob.glob(os.path.join(dir_path, "*.txt"))
    all_files = py_files + txt_files
    
    ignore = {"setup.py", "lab.py", "requirements.txt"}
    programs = [
        os.path.basename(f)
        for f in all_files
        if not os.path.basename(f).startswith(".")
        and not os.path.basename(f).startswith("__")
        and os.path.basename(f).lower() not in ignore
    ]
    programs.sort(key=_natural_sort_key)
    return programs

def list_all(dir_path="."):
    """Print a clean numbered list of all available programs and codes (.py and .txt)."""
    progs = list_programs(dir_path)
    if not progs:
        print("No .py or .txt programs found in directory.")
        return
    print(f"=== Available Codes ({len(progs)} total) ===")
    print("-" * 35)
    for i, p in enumerate(progs, 1):
        print(f"  [{i}] {p}")
    print("-" * 35)

list = list_all

def get_code(name, dir_path="."):
    """Read and return code for a program (by name e.g. 'p1', filename e.g. 'p1.txt', or number e.g. 1)."""
    progs = list_programs(dir_path)
    filename = None

    # 1. Number lookup (e.g. 1, '1', 2, '2')
    if isinstance(name, int) or (isinstance(name, str) and str(name).strip().isdigit()):
        idx = int(name) - 1
        if 0 <= idx < len(progs):
            filename = progs[idx]
        else:
            raise IndexError(f"Index {name} out of range (1 to {len(progs)} available).")
    else:
        name_str = str(name).strip()
        candidates = [
            name_str,
            f"{name_str}.py",
            f"{name_str}.txt"
        ]
        
        # Exact match check
        for cand in candidates:
            cand_path = os.path.join(dir_path, cand)
            if os.path.exists(cand_path) and os.path.isfile(cand_path):
                filename = cand
                break
        
        # Case-insensitive fallback
        if not filename:
            name_lower = name_str.lower()
            for p in progs:
                if p.lower() in (name_lower, f"{name_lower}.py", f"{name_lower}.txt"):
                    filename = p
                    break

    if not filename:
        raise FileNotFoundError(
            f"Code '{name}' not found. Available codes: {progs}"
        )

    filepath = os.path.join(dir_path, filename)
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
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
