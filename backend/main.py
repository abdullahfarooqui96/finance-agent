# Muhammad Abdullah Farooqui
# 62404051
 
import os
 
# Core
from dotenv import load_dotenv
from pydantic import BaseModel
 
# FastAPI imports
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
 
# LangChain imports
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import AIMessageChunk, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
 
# Finance imports
import yfinance as yf
 
# Workspace
load_dotenv()
 
app = FastAPI()
 
# Allow the Vite frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
model = ChatOpenAI(
    model="cl/openai/gpt-5/v-20250930",
    base_url="https://api.thesys.dev/v1/embed/",
    api_key=os.getenv("THESYS_API_KEY"),
)
 
 
@tool
def get_stock_price(ticker: str) -> str:
    """Get the latest price for a stock ticker symbol such as AAPL or TSLA."""
    try:
        info = yf.Ticker(ticker).fast_info
        return f"{ticker.upper()}: {info.last_price:.2f} {info.currency}"
    except Exception as e:
        return f"Could not get data for {ticker}: {e}"
 
 
checkpointer = InMemorySaver()
 
agent = create_agent(
    model=model,
    tools=[get_stock_price],
    system_prompt=(
        "You are a stock management assistant for Muhammad Abdullah Farooqui. "
        "Use the tools to get real time stock data from Yahoo Finance and "
        "give the user the best possible answer."
    ),
    checkpointer=checkpointer,
)
 
 
class PromptObject(BaseModel):
    content: str
    id: str | None = None
    role: str | None = None


class RequestObject(BaseModel):
    prompt: PromptObject
    threadId: str
    responseId: str | None = None
 
 
@app.post("/api/chat")
async def chat(request: RequestObject):
    config = {"configurable": {"thread_id": request.threadId}}
 
    def generate():
        for token, _ in agent.stream(
            {"messages": [HumanMessage(request.prompt.content)]},
            stream_mode="messages",
            config=config,
        ):
            # Only stream the model's text, skip tool output
            if isinstance(token, AIMessageChunk) and token.content:
                yield token.content
 
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
        },
    )
 
 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
 