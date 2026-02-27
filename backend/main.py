from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import ChatRequest, ChatResponse
from backend.agent import TitanicAgent

app = FastAPI(title="Titanic AI Chat Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = TitanicAgent()


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    result = agent.run(request.message)
    return ChatResponse(**result)