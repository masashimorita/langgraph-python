from typing import List
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langgraph.graph import END, MessageGraph

from chains import revisor, first_responder
from tool_executor import execute_tools


load_dotenv()

MAX_ITERATIONS = 2


def event_loop(state: List[BaseMessage]):
  count_tool_visits = sum(isinstance(m, ToolMessage) for m in state)
  if count_tool_visits > MAX_ITERATIONS:
    return END
  return "execute_tools"


builder = MessageGraph()
builder.add_node("draft", first_responder)
builder.add_node("execute_tools", execute_tools)
builder.add_node("revise", revisor)
builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools", "revise")
builder.add_conditional_edges("revise", event_loop)
builder.set_entry_point("draft")

graph = builder.compile()
# print(graph.get_graph().draw_ascii())
# graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


if __name__ == "__main__":
  print("HELLO Reflexion Agent")

  inputs = HumanMessage(content="""\
    Write about AI-Powered SOC / autonomous soc problem domain,
    list startups that do that and raised capital. 
  """)

  res = graph.invoke(inputs)
  # print(res)
  print(res[-1].tool_calls[0]["args"]["answer"])
