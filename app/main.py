import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from agents.orchestrator_agent import root_agent

load_dotenv()

app = FastAPI()

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="jarvis-investment",
    session_service=session_service
)

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

@app.post("/chat")
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        session = await session_service.get_session(
            app_name="jarvis-investment",
            session_id=request.session_id,
            user_id="user"
        )
        if not session:
            session = await session_service.create_session(
                app_name="jarvis-investment",
                session_id=request.session_id,
                user_id="user"
            )

        response_text = ""
        async for event in runner.run_async(
            user_id="user",
            session_id=request.session_id,
            new_message=Content(role="user", parts=[Part(text=request.message)])
        ):
            if hasattr(event, "text") and event.text:
                response_text += event.text
            elif hasattr(event, "content") and event.content:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        response_text += part.text

        return {"response": response_text.strip() or "Jarvis is thinking... please try again."}
    
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {"response": f"Error: {str(e)}"}

app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

@app.get("/")
def read_root():
    return FileResponse("app/static/index.html")