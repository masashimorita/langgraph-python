from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from pydantic import BaseModel, Field

load_dotenv()


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class GradeHallucinations(BaseModel):
  """Binary score for hallucination present in generated answer."""
  binary_score: bool = Field(description="Answer is grounded in the facts, 'yes' or 'no'")


structured_llm = llm.with_structured_output(GradeHallucinations)

system_prompt = """\
You are a grader assistant whether an LLM generation is grounded in / supported by a set of retrieved facts.
Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts.
"""

hallucination_prompt = ChatPromptTemplate.from_messages([
  ("system", system_prompt),
  ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
])

hallucination_grader: RunnableSequence = (
  hallucination_prompt
  | structured_llm
)

