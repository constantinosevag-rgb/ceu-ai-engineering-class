
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



import random
import datetime

@cl.on_message
async def on_message(message: cl.Message):
    user = message.author or "user"
    memory.add(user, message.content)

    text = message.content.strip().lower()

    # Greetings
    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
    if any(greet in text for greet in greetings):
        await cl.Message(content="Hello! How can I help you today?").send()
        return

    # Farewell
    farewells = ["bye", "goodbye", "see you", "later", "ciao"]
    if any(farewell in text for farewell in farewells):
        await cl.Message(content="Goodbye! Have a great day!").send()
        return

    # Fun fact
    if "fun fact" in text:
        facts = [
            "Honey never spoils and can last thousands of years.",
            "Bananas are berries, but strawberries are not.",
            "The Eiffel Tower was completed in 1889.",
            "Octopuses have three hearts.",
            "A group of flamingos is called a 'flamboyance.'"
        ]
        await cl.Message(content=f"Fun fact: {random.choice(facts)}").send()
        return

    # Date and time
    if "time" in text or "date" in text:
        now = datetime.datetime.now()
        await cl.Message(content=f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}").send()
        return

    # Memory: show conversation history if asked
    if "history" in text:
        hist = memory.get_history(user)
        formatted = "\n".join(hist) if hist else "No history yet."
        await cl.Message(content=f"[Memory] Your history:\n{formatted}").send()
        return

    # Try to detect and evaluate math expressions
    import re
    math_pattern = r"^[-+/*()\d\s\.]+$"
    if re.match(math_pattern, message.content.strip()):
        result = simple_calculator(message.content.strip())
        await cl.Message(content=f"[Tool] {result}").send()
        return

    # Try to answer from RAG (knowledge base)
    rag_result = rag_search(message.content.strip())
    if "RAG found:" in rag_result:
        await cl.Message(content=f"[RAG] {rag_result}").send()
        return

    # Motivational quote fallback
    quotes = [
        "Keep going, you're doing great!",
        "Every day is a new opportunity to learn.",
        "Success is the sum of small efforts repeated day in and day out.",
        "Believe in yourself and all that you are.",
        "Mistakes are proof that you are trying."
    ]
    await cl.Message(content=f"Sorry, I don't know the answer to that, but here's a motivational quote: {random.choice(quotes)}").send()
