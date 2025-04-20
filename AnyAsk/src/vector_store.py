from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import torch
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
import numpy as np
# from agent import answer_question
from agent import a121_rag_chain

import warnings
# Displaying a warning message
warnings.warn('Error: A warning just appeared')

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model_name="sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': DEVICE}
encode_kwargs = {'normalize_embeddings': True}

hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
if(hf):
    print("EMBEDDING MODEL CREATED")

def create_vector_store(texts):

    sample_embedding = torch.tensor(hf.embed_query(texts[0]))
    print("SAMPLE EMBEDDING CREATED")
    dimention = sample_embedding.shape[0]
    index=faiss.IndexFlatL2(dimention)

    #FAISS VECTOR STORE
    vector_store = FAISS(
        hf.embed_query,
        index,
        InMemoryDocstore(),{},
    )
    vector_store.add_texts(texts)
    print("VECTOR STORE CREATED")
    return vector_store
    


# documents='''
# Nvidia's fourth-quarter results, released on February 26, 2025, showed a record revenue of $39.3 billion, up 12% from the previous quarter and 78% from the previous year. This performance beat Wall Street expectations on both revenue and earnings per share. The company's Data Center revenue also reached a record $35.6 billion, up 16% quarter-over-quarter and 93% year-over-year.
# Key Highlights:
# Revenue: $39.3 billion, up 12% QoQ and 78% YoY.
# Data Center Revenue: $35.6 billion, up 16% QoQ and 93% YoY.
# Earnings per Share: $0.89 (beat expectations of $0.84).
# Full-year Revenue: $130.5 billion, up 114%.
# These results reflect a strong performance driven by the growing demand for NVIDIA's products, particularly in the AI and data center sectors. The company's Blackwell platform is also seeing strong demand and rapid ramp-up.
# '''

# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# texts = text_splitter.split_text(documents)
# vector_store=create_vector_store(texts)

# a121_rag_chain(vector_store,"What is Nvidia result for 2025?")