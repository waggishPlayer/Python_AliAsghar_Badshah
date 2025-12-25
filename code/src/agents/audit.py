import sys
import os
import logging
from datetime import datetime
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models import AgentInput, AgentOutput

logs_dir = Path(__file__).resolve().parent.parent.parent / "logs"
logs_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = logs_dir / f"audit_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AuditAgent:

    def process(self, agent_input: AgentInput, previous_output: AgentOutput) -> AgentOutput:
        input_details = []
        input_details.append(f"value={agent_input.value}")
        
        if agent_input.value2 is not None:
            input_details.append(f"value2={agent_input.value2}")
        
        if agent_input.percentage is not None:
            input_details.append(f"percentage={agent_input.percentage}")
        
        if agent_input.operation is not None:
            input_details.append(f"operation={agent_input.operation}")
        
        input_str = ", ".join(input_details)
        
        logger.info(
            f"Audit - Agent: {previous_output.agent} | "
            f"Inputs: [{input_str}] | "
            f"Output: {previous_output.value} | "
            f"Status: {previous_output.status}"
        )

        if previous_output.value < 0:
            logger.warning(f"Negative value detected: {previous_output.value}")
            return AgentOutput(
                value=previous_output.value,
                agent="AuditAgent",
                status="failed",
                details="Validation failed: negative value not allowed"
            )

        logger.info(f"Validation passed for output: {previous_output.value}")
        return AgentOutput(
            value=previous_output.value,
            agent="AuditAgent",
            status="success",
            details="Validation passed"
        )
