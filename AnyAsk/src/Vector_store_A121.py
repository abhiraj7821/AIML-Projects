import getpass
import os
import torch
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.text_splitter import CharacterTextSplitter
from langchain_ai21 import AI21Embeddings


if not os.getenv("AI21_API_KEY"):
    os.environ["AI21_API_KEY"] = getpass.getpass("Enter your AI21 API key: ")



def create_vector_store(texts):
    embeddings = AI21Embeddings()
    print("EMBEDDING MODEL CREATED")

    sample_embedding = torch.tensor(embeddings.embed_query(texts[0]))
    print("SAMPLE EMBEDDING CREATED")
    dimention = sample_embedding.shape[0]
    index=faiss.IndexFlatL2(dimention)

    #FAISS VECTOR STORE
    vector_store = FAISS(
        embeddings.embed_query,
        index,
        InMemoryDocstore(),{},
    )
    vector_store.add_texts(texts)
    print("VECTOR STORE CREATED")
    return vector_store


documents='''
Nvidia's fourth-quarter results, released on February 26, 2025, showed a record revenue of $39.3 billion, up 12% from the previous quarter and 78% from the previous year. This performance beat Wall Street expectations on both revenue and earnings per share. The company's Data Center revenue also reached a record $35.6 billion, up 16% quarter-over-quarter and 93% year-over-year.
Key Highlights:
Revenue: $39.3 billion, up 12% QoQ and 78% YoY.
Data Center Revenue: $35.6 billion, up 16% QoQ and 93% YoY.
Earnings per Share: $0.89 (beat expectations of $0.84).
Full-year Revenue: $130.5 billion, up 114%.
These results reflect a strong performance driven by the growing demand for NVIDIA's products, particularly in the AI and data center sectors. The company's Blackwell platform is also seeing strong demand and rapid ramp-up.
'''

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(documents)
vector_store=create_vector_store(texts)