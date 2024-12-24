from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse, JSONResponse
from gpt import _BaseGPTAgent

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
agent = _BaseGPTAgent("The system runs on the collection of tools")


class Question(BaseModel):
    message: str


@app.post("/vibescope_ai/v1/ask", tags=["ask"])
async def ask_question(question: Question):
    response = agent.run(question.message)
    if response["status"] == 200:
        return JSONResponse(content={"data": response["answer"]}, status_code=200)
    else:
        return JSONResponse(content={"data": response["answer"]}, status_code=500)
