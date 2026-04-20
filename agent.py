from dotenv import load_dotenv
import os
from typing import TypedDict, List
from sentence_transformers import SentenceTransformer
import chromadb
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

documents = [
    {
        "id": "doc_001",
        "topic": "Resume Tips",
        "text": "A good resume should be one page, highlight key projects, include measurable achievements, and avoid spelling mistakes. Use action verbs and keep formatting clean and professional."
    },
    {
        "id": "doc_002",
        "topic": "Aptitude Preparation",
        "text": "Aptitude preparation includes topics like percentages, probability, time and work, and speed-distance. Daily practice and mock tests are essential for improving speed and accuracy."
    },
    {
        "id": "doc_003",
        "topic": "Technical Interview",
        "text": "Technical interviews focus on DSA, OOPS, DBMS, and OS. Candidates should understand concepts clearly and be able to apply them in problem-solving scenarios."
    },
    {
        "id": "doc_004",
        "topic": "HR Interview",
        "text": "HR interviews include questions like tell me about yourself, strengths, weaknesses, and career goals. Answers should be honest, structured, and aligned with the company role."
    },
    {
        "id": "doc_005",
        "topic": "Group Discussion",
        "text": "Group discussions test communication skills. Speak clearly, add value to the discussion, and avoid interrupting others. Structure your points logically."
    },
    {
        "id": "doc_006",
        "topic": "Coding Round",
        "text": "Coding rounds require practice in arrays, strings, recursion, and problem-solving. Platforms like LeetCode help improve coding skills."
    },
    {
        "id": "doc_007",
        "topic": "Project Explanation",
        "text": "While explaining projects, clearly state the problem, your solution, technologies used, and the impact. Be confident and concise."
    },
    {
        "id": "doc_008",
        "topic": "Company Research",
        "text": "Before interviews, research the company’s background, recent developments, and job role expectations. This shows interest and preparation."
    },
    {
        "id": "doc_009",
        "topic": "Email Etiquette",
        "text": "Professional emails should have a clear subject, formal tone, and no slang. Keep messages concise and respectful."
    },
    {
        "id": "doc_010",
        "topic": "Placement Timeline",
        "text": "A proper placement timeline includes 2 months of concept learning, 1 month of mock practice, and final revision before interviews."
    }
]

embedder = SentenceTransformer('all-MiniLM-L6-v2')

texts = [doc["text"] for doc in documents]
embeddings = embedder.encode(texts).tolist()

client = chromadb.Client()
collection = client.create_collection(name="placement_kb")

collection.add(
    documents=texts,
    embeddings=embeddings,
    ids=[doc["id"] for doc in documents],
    metadatas=[{"topic": doc["topic"]} for doc in documents]
)

load_dotenv()
print(os.getenv("GROQ_API_KEY")) 

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

class CapstoneState(TypedDict):
    question: str
    messages: List[str]
    route: str
    retrieved: str
    sources: List[str]
    tool_result: str
    answer: str
    faithfulness: float
    eval_retries: int
    user_name: str
    goal: str

def study_planner_tool(days: int) -> str:
    try:
        if days <= 0:
            return "Invalid number of days."

        plan = f"{days}-day study plan:\n"

        for i in range(1, days + 1):
            plan += f"Day {i}: Aptitude + Coding + Revision\n"

        return plan

    except Exception as e:
        return f"Error: {str(e)}"

def memory_node(state: CapstoneState):
    messages = state.get("messages", [])
    question = state["question"]

    messages.append(question)

    messages = messages[-6:]

    user_name = state.get("user_name", "")

    if "my name is" in question.lower():
        user_name = question.split("my name is")[-1].strip()

    return {
        "messages": messages,
        "user_name": user_name
    }

def router_node(state: CapstoneState):

    prompt = f"""
    Decide the route for the question.

    Options:
    - retrieve → if question needs knowledge base
    - tool → if question asks for plan, days, calculation
    - skip → if it's just personal info

    Question: {state["question"]}

    Answer ONLY one word: retrieve / tool / skip
    """

    response = llm.invoke(prompt).content.strip().lower()

    return {"route": response}
    
def retrieval_node(state: CapstoneState):
    query = state["question"]

    query_embedding = embedder.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    docs = results["documents"][0]
    sources = results["metadatas"][0]

    context = ""
    for i, doc in enumerate(docs):
        context += f"[{sources[i]['topic']}] {doc}\n"

    return {
        "retrieved": context,
        "sources": [s["topic"] for s in sources]
    }

def tool_node(state: CapstoneState):
    q = state["question"]

    try:
        # extract number from question
        days = int([word for word in q.split() if word.isdigit()][0])
        result = study_planner_tool(days)
    except:
        result = "I couldn't understand the number of days."

    return {
        "tool_result": result
    }

def answer_node(state: CapstoneState):

    # if tool was used
    if state["route"] == "tool":
        return {"answer": state["tool_result"]}

    context = state.get("retrieved", "")
    history = state.get("messages", [])

    prompt = f"""
    You are a placement assistant.

    Answer ONLY using the provided context.
    If the answer is not in the context, say "I don't know".

    Context:
    {context}

    Conversation:
    {history}

    Question:
    {state["question"]}
    """

    response = llm.invoke(prompt).content

    return {"answer": response}

def eval_node(state: CapstoneState):
    return {
        "faithfulness": 1.0,
        "eval_retries": 0
    }

def save_node(state: CapstoneState):
    messages = state.get("messages", [])
    messages.append(state["answer"])

    return {
        "messages": messages
    }

def ask(question, thread_id="1"):
    result = app.invoke(
        {"question": question},
        config={"configurable": {"thread_id": thread_id}}
    )
    return result["answer"]

def route_decision(state):
    return state["route"]

def eval_decision(state):
    return "save"


graph = StateGraph(CapstoneState)
graph.add_node("memory", memory_node)
graph.add_node("router", router_node)
graph.add_node("retrieve", retrieval_node)
graph.add_node("tool", tool_node)
graph.add_node("answer", answer_node)
graph.add_node("eval", eval_node)
graph.add_node("save", save_node)
graph.set_entry_point("memory")
graph.add_edge("memory", "router")
graph.add_conditional_edges(
    "router",
    route_decision,
    {
        "retrieve": "retrieve",
        "tool": "tool",
        "skip": "answer"
    }
)
graph.add_edge("retrieve", "answer")
graph.add_edge("tool", "answer")
graph.add_edge("answer", "eval")
graph.add_conditional_edges(
    "eval",
    eval_decision,
    {
        "save": "save"
    }
)

graph.add_edge("save", END)

app = graph.compile(checkpointer=MemorySaver())

if __name__ == "__main__":
    print(ask("How to prepare for coding round?"))
    print(ask("Give me a 5 day plan"))