"""FastAPI server for Pretty Good AI voice bot challenge.

Uses Twilio's built-in speech recognition and text-to-speech, plus OpenAI
ChatGPT, to simulate a patient calling the Pretty Good AI test line.
Twilio records the entire call automatically.
"""

import json
import os
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Query
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather

from scenarios import SCENARIOS

load_dotenv()

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_PHONE = os.getenv("FROM_PHONE")
TO_PHONE = os.getenv("TO_PHONE")
PUBLIC_URL = os.getenv("PUBLIC_URL", "localhost")

CALL_DIR = Path("calls")
CALL_DIR.mkdir(exist_ok=True)

if not all([OPENAI_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, FROM_PHONE, TO_PHONE, PUBLIC_URL]):
    print("Warning: Missing required environment variables. Check .env.example")

# In-memory conversation state
conversations = {}
recording_urls = {}


def get_scenario(key: str):
    return next((s for s in SCENARIOS if s["key"] == key), SCENARIOS[0])


def build_system_prompt(scenario: dict) -> str:
    return f"""You are a PATIENT calling a medical practice. You are the caller, not the receptionist.

SCENARIO: {scenario['title']}
YOUR GOAL: {scenario['goal']}
YOUR DETAILS: {scenario['patient']}

CRITICAL RULES:
- You are the patient. NEVER say "Thank you for calling" or "How can I help you today?" or anything that sounds like a receptionist.
- Speak naturally and concisely, like a real patient on the phone.
- Keep responses to 1-2 sentences.
- Provide realistic fake information when asked (name, DOB, phone, etc.).
- If the agent says something confusing or incomplete, just restate your goal or ask a simple question.
- If the agent makes a mistake, correct them politely.
- Do not be aggressive or rude.
- If the agent says goodbye or the goal is complete, say goodbye and end.
- Do not repeat yourself unless the agent asks.
"""


def initial_greeting(scenario: dict) -> str:
    """Generate the first thing the patient says."""
    key = scenario["key"]
    if "checkup" in key:
        return "Hi, I'd like to schedule a checkup appointment."
    elif "reschedule" in key:
        return "Hi, I need to reschedule my appointment from Friday to Monday."
    elif "cancel" in key:
        return "Hi, I need to cancel my appointment tomorrow."
    elif "refill" in key:
        return "Hi, I need a refill on my Lisinopril prescription."
    elif "office_hours" in key:
        return "Hi, what are your office hours?"
    elif "location" in key:
        return "Hi, I have an appointment tomorrow. Can you give me the address and parking info?"
    elif "insurance" in key:
        return "Hi, do you accept Aetna insurance?"
    elif "unclear" in key:
        return "Uh... hi... I wanna make appointment... I got a cold..."
    elif "interruption" in key:
        return "Hi, I need to check on my prescription refill."
    elif "off_script" in key:
        return "Hi, I want to book a checkup. Can I bring my emotional support dog?"
    else:
        return "Hi, I'd like to schedule an appointment."


def chatgpt_response(call_id: str, agent_text: str, scenario: dict) -> str:
    """Get a response from ChatGPT for the patient bot."""
    history = conversations.setdefault(call_id, [])

    if not history:
        history.append({"role": "system", "content": build_system_prompt(scenario)})

    history.append({"role": "user", "content": agent_text})

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "gpt-4o-mini",
                "messages": history,
                "temperature": 0.7,
                "max_tokens": 120
            },
            timeout=15
        )
        response.raise_for_status()
        data = response.json()
        bot_text = data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[Call {call_id}] ChatGPT error: {e}")
        bot_text = "Sorry, I'm having trouble understanding. Can you repeat that?"

    history.append({"role": "assistant", "content": bot_text})
    return bot_text


def should_end_call(bot_text: str, turn_count: int) -> bool:
    """Decide if the bot should hang up."""
    if turn_count >= 8:
        return True
    text_lower = bot_text.lower()
    if "goodbye" in text_lower or "bye" in text_lower or "thank you" in text_lower:
        return True
    return False


def build_response_twiml(scenario: str, call_id: str, bot_text: str, end_call: bool = False) -> str:
    """Build TwiML with the bot's response and a gather for the next turn."""
    response = VoiceResponse()
    response.say(bot_text, voice="Polly.Joanna")

    if end_call:
        response.hangup()
    else:
        gather = Gather(
            input="speech",
            speech_timeout="auto",
            speech_model="phone_call",
            action=f"/respond?scenario={scenario}&call_id={call_id}",
            method="POST",
            language="en-US"
        )
        response.append(gather)
        response.say("I didn't catch that. I'll call back later. Goodbye.", voice="Polly.Joanna")
        response.hangup()

    return str(response)


@app.get("/twiml")
@app.post("/twiml")
def twiml(scenario: str, call_id: str):
    """Serve initial TwiML: greet and gather agent's response."""
    response = VoiceResponse()
    scenario_obj = get_scenario(scenario)
    greeting = initial_greeting(scenario_obj)

    # Initialize conversation
    conversations[call_id] = [{"role": "system", "content": build_system_prompt(scenario_obj)}]

    response.say(greeting, voice="Polly.Joanna")

    gather = Gather(
        input="speech",
        speech_timeout="auto",
        speech_model="phone_call",
        action=f"/respond?scenario={scenario}&call_id={call_id}",
        method="POST",
        language="en-US"
    )
    response.append(gather)
    response.say("Hello? I think we got disconnected. Goodbye.", voice="Polly.Joanna")
    response.hangup()

    return Response(content=str(response), media_type="application/xml")


@app.post("/respond")
def respond(scenario: str, call_id: str, SpeechResult: Optional[str] = Form(None)):
    """Handle agent's speech, generate bot response, return TwiML."""
    scenario_obj = get_scenario(scenario)
    agent_text = SpeechResult or ""

    print(f"[Call {call_id}] Agent said: {agent_text}")

    bot_text = chatgpt_response(call_id, agent_text, scenario_obj)
    print(f"[Call {call_id}] Bot says: {bot_text}")

    # Save transcript after each turn so we don't lose data if callback fails
    save_transcript(call_id)

    turn_count = len([m for m in conversations.get(call_id, []) if m["role"] == "assistant"])
    end_call = should_end_call(bot_text, turn_count)

    return Response(content=build_response_twiml(scenario, call_id, bot_text, end_call), media_type="application/xml")


@app.post("/status")
def status(call_id: Optional[str] = Query(None), CallStatus: Optional[str] = Form(None)):
    """Handle call status callbacks. Save transcript when call ends."""
    if call_id and CallStatus in ("completed", "failed", "busy", "no-answer"):
        save_transcript(call_id)
        print(f"[Call {call_id}] Call ended with status: {CallStatus}")
    return {"status": "ok"}


@app.post("/recording")
def recording(call_id: Optional[str] = Query(None), RecordingUrl: Optional[str] = Form(None), RecordingDuration: Optional[str] = Form(None)):
    """Handle recording callback and download the recording."""
    if call_id and RecordingUrl:
        recording_urls[call_id] = RecordingUrl
        download_recording(call_id, RecordingUrl, RecordingDuration)
    return {"status": "ok"}


def download_recording(call_id: str, url: str, duration: Optional[str] = None):
    """Download the Twilio recording as WAV."""
    call_dir = CALL_DIR / call_id
    call_dir.mkdir(parents=True, exist_ok=True)

    try:
        response = requests.get(
            f"{url}.wav",
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            timeout=30
        )
        response.raise_for_status()

        recording_path = call_dir / "recording.wav"
        recording_path.write_bytes(response.content)
        print(f"[Call {call_id}] Downloaded recording: {recording_path} ({len(response.content)} bytes)")

        meta_path = call_dir / "recording_meta.json"
        with open(meta_path, "w") as f:
            json.dump({
                "recording_url": url,
                "duration": duration,
                "downloaded_at": datetime.now().isoformat()
            }, f, indent=2)
    except Exception as e:
        print(f"[Call {call_id}] Error downloading recording: {e}")


def save_transcript(call_id: str):
    """Save the conversation transcript to a file."""
    call_dir = CALL_DIR / call_id
    call_dir.mkdir(parents=True, exist_ok=True)

    history = conversations.get(call_id, [])
    transcript = []
    for msg in history:
        if msg["role"] == "user":
            transcript.append({"role": "agent", "text": msg["content"]})
        elif msg["role"] == "assistant":
            transcript.append({"role": "patient", "text": msg["content"]})

    with open(call_dir / "transcript.json", "w") as f:
        json.dump(transcript, f, indent=2)

    with open(call_dir / "conversation.json", "w") as f:
        json.dump(history, f, indent=2)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
