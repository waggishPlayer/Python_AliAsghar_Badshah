"""
Percentage Agent: Calculates percentage values.

Single responsibility:
- Applies percentage calculation to input values using pure Python logic.
- Formula: value * percentage / 100
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models import AgentInput, AgentOutput

#function to calculate the percentage of given value and return the output
class PercentageAgent:

    def process(self, agent_input: AgentInput) -> AgentOutput:
        value = agent_input.value
        percentage = agent_input.percentage

        if percentage is None:
            return AgentOutput(
                value=value,
                agent="PercentageAgent",
                status="failed",
                details="Missing percentage parameter"
            )

        result = value * percentage / 100

        return AgentOutput(
            value=result,
            agent="PercentageAgent",
            status="success",
            details=f"Calculated {percentage}% of {value}"
        )
