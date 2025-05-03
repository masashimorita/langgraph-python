from typing import Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from pydantic import BaseModel, Field


load_dotenv()


class RouteQuery(BaseModel):
  """Route a user query to the most relevant datasource."""
  datasource: Literal["vectorstore", "websearch"] = Field(
    ...,
    description="Given a user question choose to route it to web search or a vectorstore."
  )


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm = llm.with_structured_output(RouteQuery)


system_prompt = """\
You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
Use a vectorstore for questions on these topics. For all else, use web-search.
"""

router_prompt = ChatPromptTemplate.from_messages([
  ("system", system_prompt),
  ("human", "{question}"),
])

question_router: RunnableSequence = (
  router_prompt
  | structured_llm
)
