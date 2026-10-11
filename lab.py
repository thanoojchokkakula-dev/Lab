import sys
from lab_magic import list_programs, list_all, get_code, show, list, load

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].strip()
        if arg.lower() in ("dva", "ml"):
            list_all(folder=arg)
        else:
            try:
                show(arg)
            except Exception as err:
                print(f"Error: {err}")
    else:
        list_all()
        print("\nUsage:")
        print("  python lab.py <name_or_number>   (e.g., python lab.py p1  or  python lab.py 1)")
        print("  python lab.py dva                (list only files in dva/)")
        print("  python lab.py ml                 (list only files in ml/)")
