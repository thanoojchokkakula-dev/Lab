import os
import re
import json
import urllib.request
import urllib.parse

GITHUB_REPO = "thanoojchokkakula-dev/Lab"
GITHUB_RAW = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/git/trees/main?recursive=1"

_CURRENT_VIEW = []

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
    """Print a clean numbered list of programs. Can filter by 'dva' or 'ml'."""
    global _CURRENT_VIEW
    progs = list_programs(folder=folder, dir_path=dir_path)
    if not progs and not folder:
        progs = _fetch_remote_list()
    elif not progs and folder:
        remote = _fetch_remote_list()
        f_norm = folder.strip().rstrip("/\\").lower()
        progs = [p for p in remote if p.lower().startswith(f_norm + "/")]

    _CURRENT_VIEW = progs

    if not progs:
        target = f" in '{folder}'" if folder else ""
        print(f"No programs found{target}.")
        return

    title_target = f" in [{folder}]" if folder else ""
    print(f"=== Available Codes{title_target} ({len(progs)} total) ===")
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

def dva():
    """List only codes in dva folder."""
    return list_all(folder="dva")

def ml():
    """List only codes in ml folder."""
    return list_all(folder="ml")

def get_code(*args, dir_path="."):
    """
    Read code for a program.
    Supports:
      get_code(1)                  -> uses last listed view or all codes
      get_code('dva', 1)           -> 1st code in dva
      get_code('ml', 1)            -> 1st code in ml
      get_code('experment-1')      -> by name
    """
    global _CURRENT_VIEW
    folder = None
    name = None

    if len(args) == 2:
        folder, name = args
    elif len(args) == 1:
        name = args[0]
    else:
        raise ValueError("Usage: get_code(name_or_number) or get_code(folder, number)")

    # If folder is specified (e.g. get_code('dva', 1))
    if folder:
        target_progs = list_programs(folder=folder, dir_path=dir_path)
        if not target_progs:
            remote = _fetch_remote_list()
            f_norm = str(folder).strip().rstrip("/\\").lower()
            target_progs = [p for p in remote if p.lower().startswith(f_norm + "/")]
    elif _CURRENT_VIEW:
        target_progs = _CURRENT_VIEW
    else:
        target_progs = list_programs(dir_path=dir_path)
        if not target_progs:
            target_progs = _fetch_remote_list()

    filename = None

    # 1. Number lookup (e.g. 1, '1', 2, '2')
    if isinstance(name, int) or (isinstance(name, str) and str(name).strip().isdigit()):
        idx = int(name) - 1
        if 0 <= idx < len(target_progs):
            filename = target_progs[idx]
        else:
            raise IndexError(f"Index {name} out of range (1 to {len(target_progs)} available).")
    else:
        name_str = str(name).strip().replace("\\", "/")

        # Check in target_progs or all programs
        all_progs = list_programs(dir_path=dir_path) or _fetch_remote_list()
        name_lower = name_str.lower()
        for p in all_progs:
            base = os.path.basename(p).lower()
            base_no_ext = os.path.splitext(base)[0]
            if name_lower in (p.lower(), base, base_no_ext):
                filename = p
                break

    if not filename:
        raise FileNotFoundError(
            f"Code '{name}' not found. Available codes: {target_progs}"
        )

    # First attempt: read local file if present
    filepath = os.path.join(dir_path, filename)
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return f.read(), filename

    # Second attempt: fetch directly from GitHub
    try:
        encoded_filename = urllib.parse.quote(filename, safe="/")
        url = f"{GITHUB_RAW}/{encoded_filename}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            return content, filename
    except Exception as e:
        raise FileNotFoundError(f"Could not load '{filename}' locally or from GitHub: {e}")

def show(*args, dir_path="."):
    """Print code with clean formatting in cell output."""
    code, filename = get_code(*args, dir_path=dir_path)
    print(f"--- {filename} ---")
    print(code)
    print("-" * (len(filename) + 8))

def load(*args, replace=False):
    """Load code directly into a Jupyter Notebook cell so you can edit and run it."""
    try:
        from IPython import get_ipython
        ip = get_ipython()
        if ip is not None:
            code, filename = get_code(*args)
            ip.set_next_input(code, replace=replace)
            print(f"Loaded '{filename}' into cell.")
            return
    except Exception:
        pass
    # Fallback to show
    show(*args)

# IPython Magic registration
try:
    from IPython.core.magic import Magics, magics_class, line_magic

    @magics_class
    class LabMagics(Magics):
        @line_magic
        def print_code(self, line):
            """Usage: %print_code 1 or %print_code dva 1"""
            parts = line.strip().split()
            if not parts:
                list_all()
                return
            try:
                show(*parts)
            except Exception as e:
                print(f"Error: {e}")

        @line_magic
        def load_code(self, line):
            """Usage: %load_code 1 or %load_code ml 1"""
            parts = line.strip().split()
            if not parts:
                return
            try:
                code, _ = get_code(*parts)
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
