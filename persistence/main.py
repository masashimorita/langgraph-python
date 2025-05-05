from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver


load_dotenv()


STEP_1 = "step_1"
HUMAN_FEEDBACK = "human_feedback"
STEP_3 = "step_3"


class State(TypedDict):
    input: str
    user_feedback: str


def step_1(state: State) -> None:
    print("---------- Step 1 ----------")


def human_feedback(state: State) -> None:
    print("---------- Human Feedback ----------")


def step_3(state: State) -> None:
    print("---------- Step 3 ----------")


builder = StateGraph(State)

builder.add_node(STEP_1, step_1)
builder.add_node(HUMAN_FEEDBACK, human_feedback)
builder.add_node(STEP_3, step_3)

builder.add_edge(START, STEP_1)
builder.add_edge(STEP_1, HUMAN_FEEDBACK)
builder.add_edge(HUMAN_FEEDBACK, STEP_3)
builder.add_edge(STEP_3, END)


memory = MemorySaver()


app = builder.compile(checkpointer=memory, interrupt_before=[HUMAN_FEEDBACK])


if __name__ == "__main__":
    print("Hello Persistence Flow")

    config = {"configurable": {"thread_id": "1"}}
    for event in app.stream(input={"input": "Hello, world!"}, config=config, stream_mode="values"):
        print(event)
      
    print(app.get_state(config=config).next)

    user_input = input("Tell me how you want to update the state: ")
    app.update_state(config, {"user_feedback": user_input}, as_node=HUMAN_FEEDBACK)

    print("---------- State after update ----------")
    print(app.get_state(config=config))

    for event in app.stream(input=None, config=config, stream_mode="values"):
        print(event)
