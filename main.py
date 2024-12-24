from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from gpt import _BaseGPTAgent

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    "https://vibescope.ai",
    "http://localhost:5177",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
