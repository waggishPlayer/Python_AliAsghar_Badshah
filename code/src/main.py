import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.workflow import run_workflow

#to calculate the compund interest
def run_compound_interest_app():
    def get_positive_float(prompt: str) -> float:
        while True:
            try:
                value = float(input(prompt))
                if value <= 0:
                    print("ERROR: Value must be positive.")
                    continue
                return value
            except ValueError:
                print("ERROR: Invalid input. Please enter a number.")
    
    def get_positive_int(prompt: str) -> int:
        while True:
            try:
                value = int(input(prompt))
                if value <= 0:
                    print("ERROR: Value must be positive.")
                    continue
                return value
            except ValueError:
                print("ERROR: Invalid input. Please enter an integer.")
    
    principal = get_positive_float("Enter Principal Amount (P): ")
    rate = get_positive_float("Enter Annual Interest Rate (R in %): ")
    time = get_positive_int("Enter Time Period (T in years): ")
    
    current_balance = principal
    
    #year wise calculation
    for year in range(1, time + 1):
        
        result_state = run_workflow(
            initial_value=current_balance,
            initial_percentage=rate
        )
        
        if result_state["final_status"] == "failed":
            print(f"ERROR: Audit failed at Year {year}")
            print(f"Details: {result_state['final_details']}")
            return
        
        current_balance = result_state["final_result"]
        print(f"Year {year} -> {current_balance:.0f}")
    
    print(f"\nFinal Amount: {current_balance:.0f}")
    print(f"Interest Amount: {current_balance - principal:.0f}")


if __name__ == "__main__":
    run_compound_interest_app()
