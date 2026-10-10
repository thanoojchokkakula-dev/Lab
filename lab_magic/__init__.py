import os
import glob

def list_programs(dir_path="."):
    """List all Python program files in the directory."""
    files = sorted(glob.glob(os.path.join(dir_path, "*.py")))
    ignore = {"setup.py", "lab.py"}
    programs = [
        os.path.basename(f)
        for f in files
        if not os.path.basename(f).startswith("__") and os.path.basename(f) not in ignore
    ]
    return programs

def get_code(name, dir_path="."):
    """Read and return code for a program (e.g. 'p1' or 'p1.py')."""
    filename = name if name.endswith(".py") else f"{name}.py"
    filepath = os.path.join(dir_path, filename)
    if not os.path.exists(filepath):
        available = list_programs(dir_path)
        raise FileNotFoundError(
            f"Program '{filename}' not found. Available programs: {available}"
        )
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def show(name, dir_path="."):
    """Print code with clean formatting."""
    code = get_code(name, dir_path)
    filename = name if name.endswith(".py") else f"{name}.py"
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
            """Usage: %print_code p1"""
            name = line.strip()
            if not name:
                progs = list_programs()
                print("Usage: %print_code <filename> (e.g. %print_code p1)")
                print(f"Available: {', '.join(progs) if progs else 'None'}")
                return
            try:
                show(name)
            except Exception as e:
                print(f"Error: {e}")

        @line_magic
        def load_code(self, line):
            """Usage: %load_code p1 (loads code directly into Jupyter cell)"""
            name = line.strip()
            if not name:
                print("Usage: %load_code <filename> (e.g. %load_code p1)")
                return
            try:
                code = get_code(name)
                self.shell.set_next_input(code, replace=True)
            except Exception as e:
                print(f"Error: {e}")

        @line_magic
        def list_codes(self, line):
            """Usage: %list_codes"""
            progs = list_programs()
            print("Available programs:")
            for p in progs:
                print(f"  - {p}")

    def load_ipython_extension(ipython):
        ipython.register_magics(LabMagics)

except ImportError:
    pass
