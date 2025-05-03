from pprint import pprint
from dotenv import load_dotenv
from graph.chains.retrieval_grader import retrieval_grader, GradeDocuments
from graph.chains.generation import generation_chain
from graph.chains.hallucination_grader import hallucination_grader, GradeHallucinations
from ingestion import retriever


load_dotenv()


def test_retrieval_grader_answer_yes() -> None:
  question = "agent memory"
  docs = retriever.invoke(question)
  doc_text = docs[0].page_content

  res: GradeDocuments = retrieval_grader.invoke({"question": question,"document": doc_text,})

  assert res.binary_score == "yes"
  

def test_retrieval_grader_answer_no() -> None:
  question = "agent memory"
  docs = retriever.invoke(question)
  doc_text = docs[0].page_content

  res: GradeDocuments = retrieval_grader.invoke({"question": "how to make pizza","document": doc_text,})

  assert res.binary_score == "no"


def test_generation_chain() -> None:
  question = "agent memory"
  docs = retriever.invoke(question)
  generation = generation_chain.invoke({"question": question, "context": docs})
  pprint(generation)


def test_hallucination_grader_answer_yes() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)

    generation = generation_chain.invoke({"context": docs, "question": question})
    res: GradeHallucinations = hallucination_grader.invoke(
        {"documents": docs, "generation": generation}
    )
    assert res.binary_score


def test_hallucination_grader_answer_no() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)

    res: GradeHallucinations = hallucination_grader.invoke(
        {
            "documents": docs,
            "generation": "In order to make pizza we need to first start with the dough",
        }
    )
    assert not res.binary_score