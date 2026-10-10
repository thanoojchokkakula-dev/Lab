import sys
from lab_magic import list_programs, get_code, show

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prog = sys.argv[1]
        try:
            show(prog)
        except Exception as err:
            print(f"Error: {err}")
    else:
        programs = list_programs()
        print("Available programs:")
        for p in programs:
            print(f"  - {p}")
        print("\nUsage:")
        print("  python lab.py <program_name>   (e.g., python lab.py p1)")
