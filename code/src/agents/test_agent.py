import sys

#doubles the input value
class TestAgent:
    def process_input(self, val: int) -> int:
        return val * 2

#takes input value and gives it to the above function, then shows the output
def main() -> None:
    agent = TestAgent()

    try:
        raw = input("Enter an integer: ").strip()
        input_val = int(raw)
    except ValueError:
        print("Error: Please enter a valid integer.")
        sys.exit(1)

    output_val = agent.process_input(input_val)

    print(f"Input:  {input_val}")
    print(f"Output: {output_val}")


if __name__ == "__main__":
    main()
