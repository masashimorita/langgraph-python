from dotenv import load_dotenv

from graph.graph import app

load_dotenv()


if __name__ == "__main__":
    print("Hello Agentic RAG Flow")

    print(app.invoke(input={"question": "What is agent memory?"}))
    # print(app.invoke(input={"question": "What is the weather in Tokyo?"}))
