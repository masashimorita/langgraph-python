import operator
import time
from typing import Annotated, Any, TypedDict, Sequence
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END, START


load_dotenv()


class State(TypedDict):
  aggregate: Annotated[list, operator.add]
  which: str


class ReturnNodeValue:
  def __init__(self, node_secret: str):
    self._value = node_secret
  
  def __call__(self, state: State) -> Any:
    time.sleep(1)
    print(f"Adding {self._value} to {state['aggregate']}")
    return {"aggregate": [self._value]}


def route_bc_or_cd(state: State) -> Sequence[str]:
  if state["which"] == "cd":
    return ["c", "d"]
  return ["b", "c"]


intermediates = ["b", "c", "d"]


builder = StateGraph(State)
builder.add_node("a", ReturnNodeValue("I'm A"))
builder.add_node("b", ReturnNodeValue("I'm B"))
builder.add_node("c", ReturnNodeValue("I'm C"))
builder.add_node("d", ReturnNodeValue("I'm D"))
builder.add_node("e", ReturnNodeValue("I'm E"))


builder.add_edge(START, "a")
builder.add_conditional_edges("a", route_bc_or_cd, intermediates)
for node in intermediates:
  builder.add_edge(node, "e")
builder.add_edge("e", END)
app = builder.compile()

print(app.get_graph().draw_ascii())

if __name__ == "__main__":
  print("Hello Async Graph");
  app.invoke({"aggregate": [], "which": "cd"}, {"configurable": {"thread_id": "async_graph"}})
