import os
import re
import json
import urllib.request

GITHUB_REPO = "thanoojchokkakula-dev/Lab"
GITHUB_RAW = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/git/trees/main?recursive=1"

def _natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def _fetch_remote_list():
    """Fetch files list live from GitHub repository."""
    try:
        req = urllib.request.Request(GITHUB_API, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            valid_dirs = ("dva/", "ml/")
            files = [
                item["path"] for item in data.get("tree", [])
                if item.get("type") == "blob"
                and any(item["path"].startswith(vd) for vd in valid_dirs)
                and (item["path"].endswith(".py") or item["path"].endswith(".txt"))
            ]
            files.sort(key=_natural_sort_key)
            return files
    except Exception:
        return []

def list_programs(folder=None, dir_path="."):
    """Return list of program paths from dva/ and ml/ (locally if present, or live from GitHub)."""
    has_lab_dirs = os.path.isdir(os.path.join(dir_path, "dva")) or os.path.isdir(os.path.join(dir_path, "ml"))
    
    collected = []
    if has_lab_dirs:
        for cat in ("dva", "ml"):
            cat_dir = os.path.join(dir_path, cat)
            if os.path.isdir(cat_dir):
                for f in os.listdir(cat_dir):
                    if (f.endswith(".py") or f.endswith(".txt")) and not f.startswith("."):
                        collected.append(f"{cat}/{f}")
    else:
        collected = _fetch_remote_list()

    if folder:
        f_norm = folder.strip().rstrip("/\\").lower()
        collected = [p for p in collected if p.lower().startswith(f_norm + "/")]

    collected.sort(key=_natural_sort_key)
    return collected

def list_all(folder=None, dir_path="."):
    """Print a clean numbered list of all available programs and codes (.py and .txt) grouped by folder."""
    progs = list_programs(folder=folder, dir_path=dir_path)
    if not progs:
        # Fallback to remote if local was empty
        progs = _fetch_remote_list()
        if folder:
            f_norm = folder.strip().rstrip("/\\").lower()
            progs = [p for p in progs if p.lower().startswith(f_norm + "/")]

    if not progs:
        target = f" in '{folder}'" if folder else ""
        print(f"No programs found{target}.")
        return

    print(f"=== Available Codes ({len(progs)} total) ===")
    print("-" * 38)

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

list = list_all

def get_code(name, dir_path="."):
    """Read and return code for a program (by number e.g. 1, filename e.g. 'p1', or path e.g. 'ml/p1.py')."""
    progs = list_programs(dir_path=dir_path)
    if not progs:
        progs = _fetch_remote_list()

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

        # Check in programs list
        name_lower = name_str.lower()
        for p in progs:
            base = os.path.basename(p).lower()
            base_no_ext = os.path.splitext(base)[0]
            if name_lower in (p.lower(), base, base_no_ext):
                filename = p
                break

    if not filename:
        raise FileNotFoundError(
            f"Code '{name}' not found. Available codes: {progs}"
        )

    # First attempt: read local file if present
    filepath = os.path.join(dir_path, filename)
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return f.read(), filename

    # Second attempt: fetch directly from GitHub
    try:
        url = f"{GITHUB_RAW}/{filename}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            return content, filename
    except Exception as e:
        raise FileNotFoundError(f"Could not load '{filename}' locally or from GitHub: {e}")

def show(name, dir_path="."):
    """Print code with clean formatting in cell output."""
    code, filename = get_code(name, dir_path)
    print(f"--- {filename} ---")
    print(code)
    print("-" * (len(filename) + 8))

def load(name, replace=False):
    """Load code directly into a Jupyter Notebook cell so you can edit and run it."""
    try:
        from IPython import get_ipython
        ip = get_ipython()
        if ip is not None:
            code, filename = get_code(name)
            ip.set_next_input(code, replace=replace)
            print(f"Loaded '{filename}' into cell.")
            return
    except Exception:
        pass
    # If not in IPython, print code
    show(name)

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
