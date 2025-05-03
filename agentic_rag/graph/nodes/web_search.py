from typing import Any, Dict
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_tavily import TavilySearch

from graph.state import GraphState


load_dotenv()


web_search_tool = TavilySearch(max_results=3)


def web_search(state: GraphState) -> Dict[str, Any]:
  print("---------- WEB SEARCH ----------")
  question = state["question"]
  documents = state["documents"]

  tavily_results = web_search_tool.invoke({"query": question})
  joined_tavily_results = "\n".join([result["content"] for result in tavily_results['results']])
  web_results = Document(page_conetnt=joined_tavily_results)
  if documents is not None:
    documents.append(web_results)
  else:
    documents = [web_results]

  return {"documents": documents, "question": question}
