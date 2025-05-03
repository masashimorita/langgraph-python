from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from pydantic import BaseModel, Field


load_dotenv()


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class GradeAnswer(BaseModel):
  """Binary score for correctness of an LLM generation."""
  binary_score: bool = Field(description="Answer addresses the question, 'yes' or 'no'")


structured_llm = llm.with_structured_output(GradeAnswer)

system_prompt = """\
You are a grader assistant whether an answer addresses / resolves a the question.
Give a binary score 'yes' or 'no'. 'Yes' means that the answer resolves the question.
"""


answer_prompt = ChatPromptTemplate.from_messages([
  ("system", system_prompt),
  ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
])

answer_grader: RunnableSequence = (
  answer_prompt
  | structured_llm
)
