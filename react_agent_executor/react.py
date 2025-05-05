from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain import hub
from langchain.agents import create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool


load_dotenv()

react_prompt: PromptTemplate = hub.pull("hwchase17/react")

@tool
def triple(num: float) -> float:
  """
  Triple a number
  :param num: The number to triple
  :return: The number tripled -> multiplied by 3
  """
  return float(num) * 3


tools = [TavilySearch(max_results=1), triple]


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

react_agent_runnable = create_react_agent(llm, tools, react_prompt)
