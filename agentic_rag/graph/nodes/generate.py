from typing import Dict, Any

from graph.state import GraphState
from graph.chains.generation import generation_chain


def generate(state: GraphState) -> GraphState:
  print("---------- GENERATE ----------")
  question = state["question"]
  documents = state["documents"]
  context = "\n\n".join([doc.page_content for doc in documents])
  generation = generation_chain.invoke({"question": question, "context": context})
  
  return {"generation": generation, "documents": documents, "question": question}
