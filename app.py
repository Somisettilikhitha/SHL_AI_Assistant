from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from pydantic import BaseModel
from typing import List

from retriever import retrieve_assessments
from intent_classifier import classify_intent
from context_parser import extract_context

# -----------------------------------
# FastAPI App
# -----------------------------------

app = FastAPI()

# -----------------------------------
# Static Files
# -----------------------------------

app.mount(

    "/static",

    StaticFiles(directory="static"),

    name="static"
)

# -----------------------------------
# Templates
# -----------------------------------

templates = Jinja2Templates(

    directory="templates"
)

# -----------------------------------
# CORS Middleware
# -----------------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# -----------------------------------
# Request Schema
# -----------------------------------

class Message(BaseModel):

    role: str
    content: str


class ChatRequest(BaseModel):

    messages: List[Message]

# -----------------------------------
# Frontend Route
# -----------------------------------

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(

        "index.html",

        {

            "request": request
        }
    )

# -----------------------------------
# Health Endpoint
# -----------------------------------

@app.get("/health")
def health():

    return {

        "status": "ok"
    }

# -----------------------------------
# Chat Endpoint
# -----------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    # -----------------------------------
    # Convert Messages
    # -----------------------------------

    messages = [

        msg.dict()

        for msg in request.messages
    ]

    # -----------------------------------
    # Latest User Message
    # -----------------------------------

    latest_message = (

        messages[-1]["content"]
    )

    latest_message_lower = (

        latest_message.lower()
    )

    # -----------------------------------
    # Intent Detection
    # -----------------------------------

    intent = classify_intent(

        latest_message
    )

    print("Intent:", intent)

    # -----------------------------------
    # Out of Scope
    # -----------------------------------

    if intent == "out_of_scope":

        return {

            "reply":

            (
                "I can only assist with "
                "SHL assessment "
                "recommendations and "
                "comparisons."
            ),

            "recommendations": [],

            "end_of_conversation": True
        }

    # -----------------------------------
    # Clarification Logic
    # -----------------------------------

    if intent == "clarification":

        return {

            "reply":

            (
                "Please provide the "
                "job role, required "
                "skills, or hiring "
                "requirements."
            ),

            "recommendations": [],

            "end_of_conversation": False
        }

    # -----------------------------------
    # Comparison Logic
    # -----------------------------------

    if (

        intent == "comparison"

        and

        "opq" in latest_message_lower

        and

        "gsa" in latest_message_lower

    ):

        return {

            "reply":

            (
                "OPQ32r is a Personality "
                "Assessment that evaluates "
                "behavioral traits such as "
                "leadership, teamwork, "
                "communication, and work style. "

                "GSA is a Cognitive Ability "
                "Assessment that measures "
                "problem-solving, logical reasoning, "
                "verbal reasoning, and numerical ability."
            ),

            "recommendations": [],

            "end_of_conversation": True
        }

    # -----------------------------------
    # Extract Conversation Context
    # -----------------------------------

    context = extract_context(
        messages
    )

    print("Context:", context)

    # -----------------------------------
    # Retrieve Recommendations
    # -----------------------------------

    results = retrieve_assessments(

        latest_message,

        top_k=5
    )

    recommendations = []

    for item in results:

        recommendations.append({

            "name":
            item["name"],

            "url":
            item["url"],

            "test_type":
            item["test_type"],

            "match_score":
            item.get(
                "match_score",
                0
            )
        })

    # -----------------------------------
    # No Results Found
    # -----------------------------------

    if len(recommendations) == 0:

        return {

            "reply":

            (
                "Sorry, I could not find "
                "suitable SHL assessments "
                "for this hiring request."
            ),

            "recommendations": [],

            "end_of_conversation": True
        }

    # -----------------------------------
    # Conversational Reply
    # -----------------------------------

    reply = (

        f"Based on your hiring "
        f"requirement for "
        f"'{latest_message}', "

        f"I have recommended "
        f"suitable SHL assessments."
    )

    # -----------------------------------
    # Final Response
    # -----------------------------------

    return {

        "reply": reply,

        "recommendations":
        recommendations,

        "end_of_conversation":
        True
    }