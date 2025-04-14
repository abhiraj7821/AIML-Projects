import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
from transformers import pipeline, set_seed
from transformers import pipeline

load_dotenv()
class open_ai_request:
    ...
    # OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
    # llm = ChatOpenAI(api_key=OPENAI_API_KEY,model="gpt-4",temperature=0.5)
    # class WaterIntakeAgent:
    #     def __intit__(self):
    #         self.history = []
    #     def analyze_intake(self,intake_ml):
    #         prompt = f"""
    #         you are a hydration assistant. The user has consumed {intake_ml} ml of water today.
    #         provide a hydration status and suggest if they need to drink more water
    #         """
    #         generator = pipeline('text-generation', model='gpt2')
    #         set_seed(42)
    #         response=generator(prompt, max_length=30, num_return_sequences=1)
    #         return response.content

class WaterIntakeAgent:
    def __init__(self):
        self.history=[]
    
    def analyze_intake(self,intake_ml):
        prompt=f'''
                    you are a hydration assistant. The user has consumed {intake_ml} ml of water today.
                    provide a hydration status and suggest if they need to drink more water 
                '''
        generator=pipeline("text-generation",model="HuggingFaceH4/zephyr-7b-beta")
        return generator(prompt,max_length=30,num_return_sequences=3)



if __name__ == "__main__":
    intake_ml=750  # You can change this number
    response = WaterIntakeAgent.analyze_intake(intake_ml)
    print(response)