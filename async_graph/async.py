import operator
import time
from typing import Annotated, Any, TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END, START


load_dotenv()


class State(TypedDict):
  aggregate: Annotated[list, operator.add]


class ReturnNodeValue:
  def __init__(self, node_secret: str):
    self._value = node_secret
  
  def __call__(self, state: State) -> Any:
    time.sleep(1)
    print(f"Adding {self._value} to {state['aggregate']}")
    return {"aggregate": [self._value]}


builder = StateGraph(State)
builder.add_node("a", ReturnNodeValue("I'm A"))
builder.add_node("b", ReturnNodeValue("I'm B"))
builder.add_node("b2", ReturnNodeValue("I'm B2"))
builder.add_node("c", ReturnNodeValue("I'm C"))
builder.add_node("d", ReturnNodeValue("I'm D"))


builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("a", "c")
builder.add_edge("b", "b2")
builder.add_edge(["b2", "c"], "d")
builder.add_edge("d", END)


app = builder.compile()

if __name__ == "__main__":
  print("Hello Async Graph");
  app.invoke({"aggregate": []}, {"configurable": {"thread_id": "async_graph"}})
