import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.workflow import run_workflow


def prompt_float(label: str) -> float:
    while True:
        raw = input(f"{label}: ").strip()
        try:
            return float(raw)
        except ValueError:
            print("Invalid number. Try again.")


def main() -> None:
    while True:
        print("\nSequential Workflow Test")
        
        initial_value = prompt_float("Enter initial value")
        initial_percentage = prompt_float("Enter percentage")
        
        result = run_workflow(initial_value, initial_percentage)
        
        print(f"\nFinal Value: {result['final_result']}")
        print(f"Status: {result['final_status']}")
        
        again = input("\nContinue testing? (y/n): ").strip().lower()
        if again != "y":
            print("Exiting.")
            break


if __name__ == "__main__":
    main()
