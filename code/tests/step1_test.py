import sys
from pathlib import Path
from typing import Optional, Tuple

from pydantic import ValidationError

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.models import AgentInput, AgentOutput
from src.agents.arithmetic import ArithmeticAgent
from src.agents.percentage import PercentageAgent
from src.agents.audit import AuditAgent


def prompt_float(label: str) -> float:
    while True:
        raw = input(f"{label}: ").strip()
        try:
            return float(raw)
        except ValueError:
            print("Invalid number. Try again.")


def prompt_operation() -> str:
    print("Select operation:")
    print("  1) add")
    print("  2) subtract")
    print("  3) divide")
    choice = input("Enter choice: ").strip()
    mapping = {"1": "add", "2": "subtract", "3": "divide"}
    return mapping.get(choice, "")


def run_arithmetic() -> Tuple[AgentInput, AgentOutput]:
    print("\nArithmeticAgent - performs add, subtract, or divide operations")
    operation = prompt_operation()
    if not operation:
        print("Invalid operation selection.")
        dummy_input = AgentInput(value=0, operation="")
        dummy_output = AgentOutput(value=0, agent="ArithmeticAgent", status="failed", details="Invalid operation selection")
        return dummy_input, dummy_output
    
    print(f"You selected: {operation}")
    value1 = prompt_float("Enter first value")
    value2 = prompt_float("Enter second value")
    
    try:
        agent_input = AgentInput(value=value1, value2=value2, operation=operation)
    except ValidationError as exc:
        print(f"Input validation failed: {exc}")
        dummy_output = AgentOutput(value=value1, agent="ArithmeticAgent", status="failed", details="Validation error")
        return AgentInput(value=value1), dummy_output
    agent = ArithmeticAgent()
    output = agent.process(agent_input)
    return agent_input, output


def run_percentage() -> Tuple[AgentInput, AgentOutput]:
    print("\nPercentageAgent - calculates percentage of a value")
    print("Input format: numeric value, percentage (e.g., 10 for 10%)")
    value = prompt_float("Enter value")
    percentage = prompt_float("Enter percentage")
    try:
        agent_input = AgentInput(value=value, percentage=percentage)
    except ValidationError as exc:
        print(f"Input validation failed: {exc}")
        dummy_output = AgentOutput(value=value, agent="PercentageAgent", status="failed", details="Validation error")
        return AgentInput(value=value), dummy_output
    agent = PercentageAgent()
    output = agent.process(agent_input)
    return agent_input, output


def run_audit() -> AgentOutput:
    print("\nAuditAgent - validates that values are not negative")
    print("Input format: numeric value to validate")
    value_to_validate = prompt_float("Enter value to validate")
    agent_name = input("Enter source agent name (default=UserProvided): ").strip() or "UserProvided"
    try:
        agent_input = AgentInput(value=value_to_validate)
        previous_output = AgentOutput(
            value=value_to_validate,
            agent=agent_name,
            status="success",
            details="Provided by user"
        )
    except ValidationError as exc:
        print(f"Input validation failed: {exc}")
        return AgentOutput(value=value_to_validate, agent="AuditAgent", status="failed", details="Validation error")
    agent = AuditAgent()
    return agent.process(agent_input, previous_output)


def run_sequential() -> None:
    print("\nSequential Flow - runs an agent then validates with AuditAgent")
    print("Choose which agent to run first:")
    print("  1) ArithmeticAgent")
    print("  2) PercentageAgent")
    choice = input("Enter choice: ").strip()
    
    if choice == "1":
        agent_input, first_output = run_arithmetic()
    elif choice == "2":
        agent_input, first_output = run_percentage()
    else:
        print("Invalid choice.")
        return
    
    print("\n--- First Agent Output ---")
    print_output(first_output)
    
    print("\n--- Running AuditAgent ---")
    audit_agent = AuditAgent()
    audit_output = audit_agent.process(agent_input, first_output)
    
    print("\n--- Audit Result ---")
    print_output(audit_output)


def print_output(output: AgentOutput) -> None:
    print("agent:   {0}".format(output.agent))
    print("status:  {0}".format(output.status))
    print("value:   {0}".format(output.value))
    print("details: {0}".format(output.details))


def main() -> None:
    agents = {
        "1": ("ArithmeticAgent", run_arithmetic),
        "2": ("PercentageAgent", run_percentage),
        "0": ("Exit", None),
    }

    while True:
        print("\nSelect agent to test:")
        print("  1) ArithmeticAgent")
        print("  2) PercentageAgent")
        print("  0) Exit")
        choice = input("Enter choice: ").strip()

        if choice == "0":
            print("Exiting.")
            break

        agent_entry = agents.get(choice)
        if not agent_entry or not agent_entry[1]:
            print("Invalid selection. Try again.")
            continue

        _, runner = agent_entry
        agent_input, output = runner()
        print("\n--- Agent Output ---")
        print_output(output)
        
        audit_agent = AuditAgent()
        audit_agent.process(agent_input, output)

        print()
        again = input("Continue testing? (y/n): ").strip().lower()
        if again != "y":
            print("Exiting.")
            break


if __name__ == "__main__":
    main()
