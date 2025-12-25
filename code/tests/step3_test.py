import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.main import run_compound_interest_app


def main():
    run_compound_interest_app()

if __name__ == "__main__":
    main()
