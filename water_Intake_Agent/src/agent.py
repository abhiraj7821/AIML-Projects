import os
from ai21 import AI21Client
from ai21.models.chat import ChatMessage
from dotenv import load_dotenv

load_dotenv()

class a121_ai_request:
    def __intit__(self):
        self.history = []

    def analyze_intake(self,intake_ml):
        a121_api_key=os.getenv("A121_API_KEY")
        client = AI21Client(api_key=a121_api_key)  
        response = client.chat.completions.create(
            model='jamba-large',
            messages=[ChatMessage(
                role='user', 
                content=f'''you are a hydration assistant. The user has consumed {intake_ml} ml of water today.
                    provide a hydration status and suggest if they need to drink more water'''
            )]
        )
        return response

if __name__ == "__main__":
    intake_ml=750  # You can change this number
    # response = WaterIntakeAgent.analyze_intake(intake_ml)
    obj=a121_ai_request()
    response=obj.analyze_intake(intake_ml)
    print(response.choices[0].message.content)