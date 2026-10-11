import os
import glob
import re

def _natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def list_programs(folder=None, dir_path="."):
    """Return a list of all program relative paths (.py and .txt), optionally filtered by folder."""
    ignore_dirs = {".git", "lab_magic", "__pycache__", ".ipynb_checkpoints", "build", "dist"}
    ignore_files = {"setup.py", "lab.py", "requirements.txt", "pyproject.toml"}

    collected = []
    for root, dirs, files in os.walk(dir_path):
        # Filter out ignored dirs in-place
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith(".")]

        rel_dir = os.path.relpath(root, dir_path).replace("\\", "/")
        if rel_dir == ".":
            rel_dir = ""

        # If a specific folder is requested, filter
        if folder:
            f_norm = folder.strip().rstrip("/\\").lower()
            if rel_dir.lower() != f_norm and not rel_dir.lower().startswith(f_norm + "/"):
                continue

        for f in files:
            if f.startswith(".") or f.startswith("__") or f.lower() in ignore_files:
                continue
            if f.endswith(".py") or f.endswith(".txt"):
                rel_path = f"{rel_dir}/{f}" if rel_dir else f
                collected.append(rel_path)

    collected.sort(key=_natural_sort_key)
    return collected

def list_all(folder=None, dir_path="."):
    """Print a clean numbered list of all available programs and codes (.py and .txt) grouped by folder."""
    progs = list_programs(folder=folder, dir_path=dir_path)
    if not progs:
        target = f" in '{folder}'" if folder else ""
        print(f"No .py or .txt programs found{target}.")
        return

    print(f"=== Available Codes ({len(progs)} total) ===")
    print("-" * 38)

    # Group by directory using standard dict to avoid shadowing builtins
    groups = {}
    for idx, p in enumerate(progs, 1):
        parts = p.split("/")
        category = parts[0] if len(parts) > 1 else "root"
        if category not in groups:
            groups[category] = []
        groups[category].append((idx, p))

    for cat in sorted(groups.keys(), key=_natural_sort_key):
        print(f"[{cat}]")
        for idx, p in groups[cat]:
            print(f"  [{idx}] {p}")
        print()
    print("-" * 38)

# Expose list alias
list = list_all

def get_code(name, dir_path="."):
    """Read and return code for a program (by number e.g. 1, filename e.g. 'p1', or path e.g. 'ml/p1.py')."""
    progs = list_programs(dir_path=dir_path)
    filename = None

    # 1. Number lookup (e.g. 1, '1', 2, '2')
    if isinstance(name, int) or (isinstance(name, str) and str(name).strip().isdigit()):
        idx = int(name) - 1
        if 0 <= idx < len(progs):
            filename = progs[idx]
        else:
            raise IndexError(f"Index {name} out of range (1 to {len(progs)} available).")
    else:
        name_str = str(name).strip().replace("\\", "/")

        # Direct path check
        candidates = [
            name_str,
            f"{name_str}.py",
            f"{name_str}.txt"
        ]

        for cand in candidates:
            cand_path = os.path.join(dir_path, cand)
            if os.path.exists(cand_path) and os.path.isfile(cand_path):
                filename = cand
                break

        # Search by basename across all folders
        if not filename:
            name_lower = name_str.lower()
            for p in progs:
                base = os.path.basename(p).lower()
                base_no_ext = os.path.splitext(base)[0]
                if name_lower in (base, base_no_ext, p.lower()):
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
            """Usage: %list_codes [folder]"""
            folder = line.strip() if line.strip() else None
            list_all(folder=folder)

    def load_ipython_extension(ipython):
        ipython.register_magics(LabMagics)

except ImportError:
    pass
