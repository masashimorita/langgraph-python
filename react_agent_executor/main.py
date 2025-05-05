from dotenv import load_dotenv
from langchain_core.agents import AgentFinish
from langgraph.graph import END, StateGraph

from state import AgentState
from nodes import run_agent_reasoning_engine, execute_tools

AGENT_REASON = 'agent_reason'
ACT = 'act'


load_dotenv()


def should_continue(state: AgentState) -> str:
  """
  Should continue the agent loop?
  """
  if isinstance(state["agent_outcome"], AgentFinish):
    return END
  else:
    return ACT


builder = StateGraph(AgentState)
builder.add_node(AGENT_REASON, run_agent_reasoning_engine)
builder.add_node(ACT, execute_tools)

builder.set_entry_point(AGENT_REASON)
builder.add_conditional_edges(
  AGENT_REASON,
  should_continue,
)
builder.add_edge(ACT, AGENT_REASON)


graph = builder.compile()


if __name__ == "__main__":
  print("Hello ReAct Agent Executor!")

  # res = graph.invoke(input={"input": "What is the weather in Tokyo? Write it and then Triple it."})
  res = graph.invoke(input={"input": "How to become AI driven developer?"})
  print(res["agent_outcome"].return_values["output"])
