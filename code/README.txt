Sequential Multi-Agent Financial System

This project uses LangGraph to coordinate multiple Python agents for financial calculations. Three agents work together: one calculates percentages, one does arithmetic operations, and one validates the results.


REQUIREMENTS

Python 3.9 or higher
Virtual environment (venv)


SETUP

1. Create and activate virtual environment

python3 -m venv venv
source venv/bin/activate

2. Install dependencies

pip install -r requirements.txt


PROJECT STRUCTURE

src/
  models.py - Data structures for agent inputs and outputs
  workflow.py - LangGraph coordinator that runs agents in sequence
  main.py - Compound interest calculator
  agents/
    arithmetic.py - Handles add, subtract, divide operations
    percentage.py - Calculates percentage values
    audit.py - Validates results and logs everything

tests/
  step1_test.py - Test individual agents interactively
  step2_test.py - Test the sequential workflow
  step3_test.py - Test compound interest calculation

logs/
  All audit logs are saved here with timestamps


HOW TO RUN

Step 1: Test individual agents

python tests/step1_test.py

Choose an agent, enter values, see the output and audit logs.


Step 2: Test sequential workflow

python tests/step2_test.py

Enter a value and percentage. The system runs percentage calculation, then adds the result to original value, then validates everything.


Step 3: Calculate compound interest

python tests/step3_test.py

Enter principal amount, interest rate, and time period. The system calculates compound interest year by year using the agent workflow.


WHAT HAPPENS INTERNALLY

For compound interest with 1000 principal at 10 percent for 3 years:

Year 1: Calculate 10 percent of 1000 = 100, then add 1000 + 100 = 1100
Year 2: Calculate 10 percent of 1100 = 110, then add 1100 + 110 = 1210
Year 3: Calculate 10 percent of 1210 = 121, then add 1210 + 121 = 1331

Every step is audited and logged to the logs folder.


NOTES

Audit logs include all inputs, outputs, agent names, and status
No formulas are used, everything goes through the agent workflow
All calculations are pure Python, no external APIs or LLMs
Negative values are rejected by the audit agent


TROUBLESHOOTING

If you see import errors, make sure venv is activated
If tests fail, check that all dependencies are installed
Check the logs folder for detailed audit trails of what went wrong
