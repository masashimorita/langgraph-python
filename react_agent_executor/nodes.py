from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode
from react import react_agent_runnable, tools
from state import AgentState


load_dotenv()

tool_executor = ToolNode(tools)


def run_agent_reasoning_engine(state: AgentState) -> AgentState:
  """
  Run the agent reasoning engine
  """
  agent_outcome = react_agent_runnable.invoke(state)
  return {"agent_outcome": agent_outcome}


def execute_tools(state: AgentState) -> AgentState:
  """
  Execute the tools
  """
  agent_action = state["agent_outcome"]
  output = tool_executor.invoke(agent_action)

