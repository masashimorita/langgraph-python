import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


load_dotenv()

chroma_collection_name = "rag-chroma"
chroma_persist_directory = f"{os.getenv('ROOT_DIR')}/.chroma"


urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

def ingest_docs_to_chroma() -> None:
  docs = [WebBaseLoader(url).load() for url in urls]
  doc_list = [item for sublist in docs for item in sublist]


  text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250,
    chunk_overlap=0,
  )

  doc_splits = text_splitter.split_documents(doc_list)


  vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name=chroma_collection_name,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    persist_directory=chroma_persist_directory,
  )



retriever = Chroma(
  collection_name=chroma_collection_name,
  persist_directory=chroma_persist_directory,
  embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
).as_retriever()


if __name__ == "__main__":
  ingest_docs_to_chroma()
