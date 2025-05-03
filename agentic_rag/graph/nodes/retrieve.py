from typing import Any, Dict


from graph.state import GraphState
from ingestion import retriever


def retrive(state: GraphState) -> Dict[str, Any]:
  """
  Retrieve documents from the vector store.
  """
  print("---------- RETRIEVE ----------")
  question = state["question"]

  documents = retriever.invoke(question)
  return {"documents": documents, "question": question}
