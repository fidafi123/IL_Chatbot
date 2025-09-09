import os
import json
from typing import List, Dict
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware

# Load env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("API key for Groq is missing. Please set the GROQ_API_KEY in the .env file.")

# Load FAQ data
with open("faq.json", "r") as f:
    FAQ_DATA = json.load(f)

# FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=GROQ_API_KEY)

class UserInput(BaseModel):
    message: str
    role: str = "user"
    conversation_id: str

class Conversation:
    def __init__(self):
        self.messages: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant for Iron Lady, a leadership and edtech company. "
                    "Always answer based on Iron Lady’s programs, FAQs, and values. "
                    "If the user asks about programs, duration, mode, certificates, mentors, pedagogy, or impact, "
                    "use the provided knowledge base. "
                    "If the answer is not in the knowledge base, use your AI reasoning but keep context about Iron Lady."
                )
            }
        ]
        self.active: bool = True

conversations: Dict[str, Conversation] = {}

def query_groq_api(conversation: Conversation) -> str:
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=conversation.messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with Groq API: {str(e)}")

def get_or_create_conversation(conversation_id: str) -> Conversation:
    if conversation_id not in conversations:
        conversations[conversation_id] = Conversation()
    return conversations[conversation_id]

def check_faq(message: str) -> str | None:
    """Simple keyword-based FAQ matching"""
    msg_lower = message.lower()
    for key, answer in FAQ_DATA.items():
        if key in msg_lower:
            return answer
    return None

@app.post("/chat/")
async def chat(input: UserInput):
    conversation = get_or_create_conversation(input.conversation_id)

    if not conversation.active:
        raise HTTPException(
            status_code=400,
            detail="The chat session has ended. Please start a new session."
        )

    try:
        # Append user message
        conversation.messages.append({
            "role": input.role,
            "content": input.message
        })

        # First check if answer exists in FAQ
        faq_answer = check_faq(input.message)
        if faq_answer:
            response = faq_answer
        else:
            # Otherwise query Groq AI
            response = query_groq_api(conversation)

        # Append assistant response
        conversation.messages.append({
            "role": "assistant",
            "content": response
        })

        return {
            "response": response,
            "conversation_id": input.conversation_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
