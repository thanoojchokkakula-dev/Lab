import sys
from lab_magic import list_programs, list_all, get_code, show, list

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prog = sys.argv[1]
        try:
            show(prog)
        except Exception as err:
            print(f"Error: {err}")
    else:
        list_all()
        print("\nUsage:")
        print("  python lab.py <name_or_number>   (e.g., python lab.py p1  or  python lab.py 1)")
