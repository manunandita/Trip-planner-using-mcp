from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from langsmith import BaseModel
from pydantic import Field
from response import run_travel_agent
from typing import Annotated

app=FastAPI()

class TripRequest(BaseModel):
    query: Annotated[str, Field(..., description="The user's travel request.")]

@app.post("/plan")
def plan_trip(request:TripRequest):
    try:
        result = run_travel_agent(request.query)
        return JSONResponse(content=result["answer"], status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))