"""
Step 0: Simple Test Agent
Baseline implementation for testing and validation.
"""


class SimpleTestAgent:
    """Basic test agent for Step 0."""

    def process_input(self, val: int) -> int:
        """
        Process input by doubling the value.
        
        Args:
            val: Input integer value
            
        Returns:
            Doubled input value
        """
        return val * 2


def main() -> None:
    """Test the SimpleTestAgent."""
    agent = SimpleTestAgent()
    
    input_val = 5
    output_val = agent.process_input(input_val)
    
    print(f"Input:  {input_val}")
    print(f"Output: {output_val}")
    
    assert output_val == 10, f"Expected 10, got {output_val}"
    print("Test passed.")


if __name__ == "__main__":
    main()
