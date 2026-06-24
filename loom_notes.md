# Loom Notes

## Approach
- Twilio makes outbound calls to `+1-805-439-8008`
- Twilio handles speech recognition and text-to-speech
- OpenAI ChatGPT (`gpt-4o-mini`) generates patient responses
- FastAPI server coordinates the call flow

## main.py
- `/twiml` — returns Twilio instructions: patient greeting + listen for agent
- `/respond` — receives agent speech, sends to ChatGPT, returns patient response
- `/status` — handles call end, saves transcript
- `/recording` — downloads Twilio recording as WAV
- In-memory conversation history per call
- Saves transcript after every turn

## caller.py
- Loads 10 scenarios from `scenarios.py`
- Creates one outbound Twilio call per scenario
- Enables call recording
- Polls call status until complete
- Waits 5 seconds between calls

## scenarios.py
- 10 patient scenarios with goals and details
- Examples: schedule checkup, reschedule, cancel, refill, office hours, location, insurance, unclear speech, interruption, off-script request

## Key bugs found
- Agent cannot cancel appointments
- Agent hallucinates nonsensical question during refill
- Agent does not answer office hours, location, or insurance questions
- Agent does not handle unclear speech
- Agent mishears and confirms incorrect names
