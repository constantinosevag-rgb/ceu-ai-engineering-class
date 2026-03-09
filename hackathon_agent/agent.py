
import dotenv
dotenv.load_dotenv()

import chainlit as cl
import os
from memory_store import MemoryStore
from tools import simple_calculator

# Initialize memory
memory = MemoryStore()

# Load RAG data
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.txt")
with open(DATA_PATH, "r") as f:
    KB = f.read().splitlines()

def rag_search(query: str) -> str:
    # Simple keyword search in KB
    for line in KB:
        if query.lower() in line.lower():
            return f"RAG found: {line}"
    return "No relevant info found in knowledge base."

@cl.on_message
async def on_message(message: cl.Message):
    user = message.author or "user"
    memory.add(user, message.content)

    # Tool: calculator if message starts with 'calc:'
    if message.content.strip().lower().startswith("calc:"):
        expr = message.content[5:].strip()
        result = simple_calculator(expr)
        await cl.Message(content=f"[Tool] {result}").send()
        return

    # RAG: search KB if message contains 'search:'
    if message.content.strip().lower().startswith("search:"):
        query = message.content[7:].strip()
        result = rag_search(query)
        await cl.Message(content=f"[RAG] {result}").send()
        return

    # Memory: show conversation history if asked
    if "history" in message.content.lower():
        hist = memory.get_history(user)
        formatted = "\n".join(hist) if hist else "No history yet."
        await cl.Message(content=f"[Memory] Your history:\n{formatted}").send()
        return

    # Default reply
    await cl.Message(content=f"[Hackathon Agent] Received: {message.content}").send()
