#Coordinate the worklfow in a sequential manner
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from src.models import AgentInput, AgentOutput
from src.agents.percentage import PercentageAgent
from src.agents.arithmetic import ArithmeticAgent
from src.agents.audit import AuditAgent


class WorkflowState(TypedDict):
    initial_value: float
    initial_percentage: float
    percentage_result: Optional[float]
    arithmetic_result: Optional[float]
    final_result: Optional[float]
    final_status: Optional[str]
    final_details: Optional[str]
    should_stop: bool

#percentage agent
def percentage_node(state: WorkflowState) -> WorkflowState:
    agent = PercentageAgent()
    agent_input = AgentInput(
        value=state["initial_value"],
        percentage=state["initial_percentage"]
    )
    output = agent.process(agent_input)
    
    state["percentage_result"] = output.value
    
    audit_agent = AuditAgent()
    audit_agent.process(agent_input, output)
    
    return state

#arithmatic agent
def arithmetic_node(state: WorkflowState) -> WorkflowState:
    agent = ArithmeticAgent()
    agent_input = AgentInput(
        value=state["initial_value"],
        value2=state["percentage_result"],
        operation="add"
    )
    output = agent.process(agent_input)
    
    state["arithmetic_result"] = output.value
    
    audit_agent = AuditAgent()
    audit_agent.process(agent_input, output)
    
    return state

def audit_node(state: WorkflowState) -> WorkflowState:
    agent = AuditAgent()
    
    agent_input = AgentInput(
        value=state["initial_value"],
        value2=state["percentage_result"],
        operation="add"
    )
    
    previous_output = AgentOutput(
        value=state["arithmetic_result"],
        agent="WorkflowFinalValidation",
        status="success",
        details=f"Final workflow result: {state['arithmetic_result']}"
    )
    
    output = agent.process(agent_input, previous_output)
    
    state["final_result"] = output.value
    state["final_status"] = output.status
    state["final_details"] = output.details
    
    if output.status == "failed":
        state["should_stop"] = True
    
    return state


def should_continue(state: WorkflowState) -> str:
    if state.get("should_stop", False):
        return "end"
    return "continue"


def create_workflow() -> StateGraph:
    workflow = StateGraph(WorkflowState)
    
    workflow.add_node("percentage", percentage_node)
    workflow.add_node("arithmetic", arithmetic_node)
    workflow.add_node("audit", audit_node)
    
    workflow.set_entry_point("percentage")
    workflow.add_edge("percentage", "arithmetic")
    workflow.add_edge("arithmetic", "audit")
    workflow.add_edge("audit", END)
    
    return workflow.compile()


def run_workflow(initial_value: float, initial_percentage: float) -> WorkflowState:
    graph = create_workflow()
    
    initial_state: WorkflowState = {
        "initial_value": initial_value,
        "initial_percentage": initial_percentage,
        "percentage_result": None,
        "arithmetic_result": None,
        "final_result": None,
        "final_status": None,
        "final_details": None,
        "should_stop": False
    }
    
    final_state = graph.invoke(initial_state)
    return final_state
