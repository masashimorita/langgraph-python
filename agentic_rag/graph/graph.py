from dotenv import load_dotenv
from langgraph.graph import END, StateGraph

from graph.consts import RETRIEVE, GRADE_DOCUMENTS, WEB_SEARCH, GENERATE
from graph.nodes import retrieve, grade_documents, web_search, generate
from graph.state import GraphState

load_dotenv()


def decide_to_generate(state: GraphState) -> str:
  print("---------- ASSESS GRADED DOCUMENTS ----------")
  if state["web_search"] == True:
    print("---------- DECISION: WEB SEARCH ----------")
    return WEB_SEARCH
  else:
    print("---------- DECISION: GENERATE ----------")
    return GENERATE


builder = StateGraph(GraphState)

builder.add_node(RETRIEVE, retrieve)
builder.add_node(GRADE_DOCUMENTS, grade_documents)
builder.add_node(WEB_SEARCH, web_search)
builder.add_node(GENERATE, generate)

builder.set_entry_point(RETRIEVE)
builder.add_edge(RETRIEVE, GRADE_DOCUMENTS)
builder.add_conditional_edges(
  GRADE_DOCUMENTS, 
  decide_to_generate,
  {
    WEB_SEARCH: WEB_SEARCH,
    GENERATE: GENERATE
  },
)
builder.add_edge(WEB_SEARCH, GENERATE)
builder.add_edge(GENERATE, END)

app = builder.compile()
