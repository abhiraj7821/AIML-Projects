from fastapi import FastAPI
from pydantic import BaseModel
# from src.agent import WaterIntakeAgent
from agent import a121_ai_request

from database import log_intake,get_intake_history
from logger import log_message

app=FastAPI()
agent=a121_ai_request()


class WaterIntakeRequest(BaseModel):
    user_id:str
    intake_ml:int


@app.post("/log-intake")
async def log_water_intake(request:WaterIntakeRequest):
    log_intake(request.user_id,request.intake_ml)
    analysis=agent.analyze_intake(request.intake_ml)
    log_message(f"User {request.user_id} logged {request.intake_ml}ml")
    return {"message":"Water intake logged successfully","analysis":analysis.choices[0].message.content}

@app.get("/history/{user_id}")
async def get_water_history(user_id:str):
    history=get_intake_history(user_id)
    return {"user_id":user_id,"history":history}