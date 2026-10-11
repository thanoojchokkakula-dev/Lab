import sys
from lab_magic import list_programs, list_all, get_code, show, list, load, dva, ml

if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        if len(args) == 1 and args[0].lower() in ("dva", "ml"):
            list_all(folder=args[0])
        else:
            try:
                show(*args)
            except Exception as err:
                print(f"Error: {err}")
    else:
        list_all()
        print("\nUsage:")
        print("  python lab.py <number_or_name>   (e.g., python lab.py 1  or  python lab.py p1)")
        print("  python lab.py dva                (list only files in dva/)")
        print("  python lab.py ml                 (list only files in ml/)")
