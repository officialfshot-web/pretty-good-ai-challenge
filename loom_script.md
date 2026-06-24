# Loom Recording Script

Use this as a teleprompter while recording your 5-minute walkthrough.

## 1. Intro (30 sec)

"Hi, I'm [your name], and this is my submission for the Pretty Good AI engineering challenge. I built a voice bot that calls the Pretty Good AI test line and acts as a patient to test their AI receptionist."

"The approach is simple: I use Twilio to make the phone calls, Twilio's built-in speech recognition and text-to-speech, and OpenAI's ChatGPT to generate the patient responses. This keeps the cost low and avoids needing access to OpenAI's Realtime API."

## 2. README and architecture (45 sec)

Show the GitHub repo.

"The README explains the setup. You need a Twilio account, an OpenAI API key, and ngrok to expose the local server. The cost estimate is around $2 for 10 calls."

Open `architecture.md`.

"The architecture doc shows the flow: Twilio calls the test number, fetches a TwiML document from our FastAPI server, which speaks the patient greeting and listens for the agent. When the agent speaks, Twilio sends the transcript to our server, we send it to ChatGPT, and ChatGPT returns the patient response."

## 3. main.py (1 min 30 sec)

Scroll to the top.

"`main.py` is the FastAPI server. It handles four webhooks from Twilio."

"`/twiml` is the first webhook. It returns Twilio instructions: say the patient's opening line, then gather the agent's speech."

Point to the `Gather` block.

"This `Gather` tells Twilio to listen for speech, transcribe it, and send it to the `/respond` endpoint."

Scroll to `/respond`.

"`/respond` gets the agent's speech, sends the conversation history to ChatGPT, and gets back the patient response. Then it builds new TwiML that says the response and gathers the next agent reply."

Scroll to the system prompt.

"The system prompt tells ChatGPT to act as a patient with a specific goal and details. We also save the transcript after every turn so we don't lose data."

## 4. caller.py (45 sec)

Open `caller.py`.

"`caller.py` makes the actual calls. It loops through the 10 scenarios in `scenarios.py` and creates one outbound Twilio call per scenario. It also enables call recording and status callbacks."

"Each call runs up to 2 minutes, then we poll the status until it completes."

## 5. scenarios.py (30 sec)

Open `scenarios.py`.

"`scenarios.py` defines the 10 test cases: scheduling, rescheduling, canceling, medication refills, office hours, location, insurance, unclear speech, interruptions, and off-script requests. Each has a goal and patient details so ChatGPT knows how to respond."

## 6. Bug report and results (1 min 30 sec)

Open `bug_report.md`.

"After the calls, I reviewed the transcripts and wrote a bug report. Here are the most important bugs I found."

"First, the agent cannot cancel appointments. It just says it will transfer to patient support."

"Second, the agent hallucinates a nonsensical question during a medication refill: it asks 'How many days of life in a pearl?' This is clearly broken."

"Third, the agent does not answer simple factual questions like office hours or insurance acceptance. It gets stuck asking for identity verification instead."

"Fourth, the agent does not handle unclear speech or name mispronunciations well. It confidently confirms wrong names like 'Noen' instead of 'Nguyen'."

"I included call references and timestamps in the bug report so these can be reproduced."

## 7. Outro (30 sec)

"Overall, the Pretty Good AI agent handles identity verification well but fails when it needs to actually complete tasks or answer questions. The code is in the repo, along with all the transcripts and the full bug report. Thanks for reviewing my submission."

---

Tip: Keep the Loom tab or this file open on a second screen while you record.
