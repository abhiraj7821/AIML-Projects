import os
from dotenv import load_dotenv
import re
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.groq import Groq

# Step 1: Load API keys from .env
load_dotenv()  # Loads from .env file in your current directory

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Step 2: Load your document(s)
documents = SimpleDirectoryReader(input_dir="manim").load_data()  # PDF or text files

# Step 3: Setup OpenAI Embedding model for indexing
embed_model = OpenAIEmbedding(api_key=OPENAI_API_KEY)

# Step 5: Initialize Groq LLM for conversation
llm = Groq(model="llama3-70b-8192", api_key=GROQ_API_KEY)
# Step 4: Build the index using OpenAI embeddings
index = VectorStoreIndex.from_documents(documents,llm_predictor=llm,embed_model=embed_model)

# Step 6: Create a document-grounded chat engine
chat_engine = index.as_chat_engine(
    llm=llm,
    system_prompt=(
        "You are a Mathematical Animation Assistant that communicates in a precise, technical, and code-only manner. Your tone is strictly formal and functional. Avoid any explanation, greeting, or non-code commentary."
        "Your task is to generate valid, runnable Python code using the Manim library (preferably manimce) to visualize mathematical concepts, functions, or scenarios described in the user's input."
        "You will receive a natural language description of a mathematical animation or visualization. This may include functions, geometrical constructions, transformations, or coordinate-based scenes."
        "Return only the Manim Python code needed to create the described animation. Do not include any text, explanation, markdown, or additional commentary."
        "CONSTRAINTS:Output only Python code compatible with ManimCE. Use manim.Scene or its appropriate subclasses. Do not include explanatory comments unless required by the code logic. No import statements unless necessary beyond standard from manim import *. The code must be minimal, syntactically correct, and runnable in isolation. Do not wrap code in triple backticks (```)."
    ),
    chat_mode="context",
    verbose=True,
)

# Step 7: Start conversation
response = chat_engine.chat("write a program to Create Circle")
print(response.response)
result = re.search(r"```(.*?)```", response.response)

# You can continue the conversation:
# response = chat_engine.chat("Can I inherit from another class?")
# print(response.response)