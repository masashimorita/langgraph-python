from dotenv import load_dotenv
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = hub.pull("rlm/rag-prompt")

generation_chain = (
  prompt
  | llm
  | StrOutputParser()
)
