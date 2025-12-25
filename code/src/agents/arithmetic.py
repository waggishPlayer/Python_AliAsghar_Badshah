import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models import AgentInput, AgentOutput

# function for addition, subtraction, division operations
class ArithmeticAgent:

    def process(self, agent_input: AgentInput) -> AgentOutput:
        value1 = agent_input.value
        value2 = agent_input.value2 if agent_input.value2 is not None else value1
        operation = agent_input.operation

        if operation == "add":
            result = value1 + value2
            return AgentOutput(
                value=result,
                agent="ArithmeticAgent",
                status="success",
                details=f"Added {value1} + {value2}"
            )

        elif operation == "subtract":
            result = value1 - value2
            return AgentOutput(
                value=result,
                agent="ArithmeticAgent",
                status="success",
                details=f"Subtracted {value1} - {value2}"
            )

        elif operation == "divide":
            try:
                if value2 == 0:
                    raise ZeroDivisionError("Cannot divide by zero")
                result = value1 / value2
                return AgentOutput(
                    value=result,
                    agent="ArithmeticAgent",
                    status="success",
                    details=f"Divided {value1} / {value2}"
                )
            except ZeroDivisionError as e:
                return AgentOutput(
                    value=value1,
                    agent="ArithmeticAgent",
                    status="failed",
                    details=f"Division error: {str(e)}"
                )

        else:
            return AgentOutput(
                value=value,
                agent="ArithmeticAgent",
                status="failed",
                details=f"Unknown operation: {operation}"
            )
