from langchain.chains import RetrievalQA
from langchain_ai21.chat_models import ChatAI21
from dotenv import load_dotenv
import os
from getpass import getpass

load_dotenv()
def a121_rag_chain(vector_store,query):
    # A121_API_KEY=os.getenv("A121_API_KEY")
    if "AI21_API_KEY" not in os.environ:
        os.environ["AI21_API_KEY"] = getpass()
    llm = ChatAI21(model="jamba-instruct", temperature=0)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    print("RETRIEVAL DEFINED")
    result = qa.invoke({"query": query})
    print(f"Answer: {result['result']}")
    return result