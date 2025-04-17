import torch
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_huggingface import HuggingFaceEndpoint
import numpy as np
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from transformers import AutoModelForSeq2SeqLM 
from langchain.chains import RetrievalQA




def answer_question(vector_store,query):
    
    MODEL_NAME = "google/flan-t5-large"  # Even smaller alternative

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(  # Changed class
        MODEL_NAME,
        device_map="auto",
        torch_dtype=torch.float16
    )
    print("MODEL CREATED")
    
    pipe = pipeline(
        "text2text-generation",  
        model=model,
        tokenizer=tokenizer,
        max_length=200,
        do_sample=True,
        temperature=0.3
    )

    hf_pipeline = HuggingFacePipeline(pipeline=pipe)
    print("PIPELINE DEFINED")

    qa = RetrievalQA.from_chain_type(
    llm=hf_pipeline,
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)
    print("RETRIEVAL DEFINED")
    result = qa.invoke({"query": query})
    return result