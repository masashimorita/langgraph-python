from dotenv import load_dotenv
from langgraph.graph import END, StateGraph

from graph.consts import RETRIEVE, GRADE_DOCUMENTS, WEBSEARCH, GENERATE
from graph.nodes import retrieve, grade_documents, web_search, generate
from graph.state import GraphState
from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.answer_grader import answer_grader
from graph.chains.router import question_router, RouteQuery


load_dotenv()


def route_question(state: GraphState) -> str:
  print("---------- ROUTE QUESTION ----------")
  question = state["question"]
  source: RouteQuery = question_router.invoke({"question": question})
  if source.datasource == "vectorstore":
    print("---------- ROUTE QUESTION TO VECTORSTORE ----------")
    return RETRIEVE
  elif source.datasource == "websearch":
    print("---------- ROUTE QUESTION TO WEB SEARCH ----------")
    return WEBSEARCH
  else:
    raise ValueError(f"Invalid datasource: {source.datasource}")


def decide_to_generate(state: GraphState) -> str:
  print("---------- ASSESS GRADED DOCUMENTS ----------")
  if state["web_search"] == True:
    print("---------- DECISION: WEB SEARCH ----------")
    return WEBSEARCH
  else:
    print("---------- DECISION: GENERATE ----------")
    return GENERATE


def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
  print("---------- ASSESS HALLUCINATION ----------")
  question = state["question"]
  documents = state["documents"]
  generation = state["generation"]

  score = hallucination_grader.invoke({"documents": documents, "generation": generation})
  if hallucination_grade := score.binary_score:
    print("---------- DECISION: GENERATION IS GROUNDED IN DOCUMENTS ----------")
    print("---------- GRADE GENERATION VS QUESTION ----------")
    score = answer_grader.invoke({"question": question, "generation": generation})
    if answer_grade := score.binary_score:
      print("---------- DECISION: GENERATION ADDRESSES QUESTION ----------")
      return "useful"
    else:
      print("---------- DECISION: GENERATION DOES NOT ADDRESS QUESTION ----------")
      return "not useful"
  else:
    print("---------- DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS ----------")
    return "not supported"


builder = StateGraph(GraphState)

builder.add_node(RETRIEVE, retrieve)
builder.add_node(GRADE_DOCUMENTS, grade_documents)
builder.add_node(WEBSEARCH, web_search)
builder.add_node(GENERATE, generate)

builder.set_conditional_entry_point(
  route_question,
  {
    RETRIEVE: RETRIEVE,
    WEBSEARCH: WEBSEARCH,
  },
)
builder.add_edge(RETRIEVE, GRADE_DOCUMENTS)
builder.add_conditional_edges(
  GRADE_DOCUMENTS, 
  decide_to_generate,
  {
    WEBSEARCH: WEBSEARCH,
    GENERATE: GENERATE
  },
)
builder.add_edge(WEBSEARCH, GENERATE)
builder.add_conditional_edges(
  GENERATE,
  grade_generation_grounded_in_documents_and_question,
  {
    "not supported": GENERATE,
    "not useful": WEBSEARCH,
    "useful": END,
  }
)
# builder.add_edge(GENERATE, END)

app = builder.compile()
