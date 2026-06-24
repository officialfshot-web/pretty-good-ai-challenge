# Pretty Good AI - AI Engineering Challenge

This repo contains a Python voice bot that calls the Pretty Good AI assessment line (`+1-805-439-8008`) and acts as a realistic patient to test their AI receptionist.

## What it does

- Makes 10 outbound phone calls, one per scenario.
- Uses Twilio for telephony, speech recognition, and text-to-speech.
- Uses OpenAI ChatGPT (`gpt-4o-mini`) to generate natural patient responses.
- Records every call automatically.
- Saves transcripts and full conversation history.

## Cost estimate

Typical cost for 10 calls of ~1-2 minutes each:

| Service | Rate | ~20 min total |
|---|---|---|
| Twilio phone number | ~$1.15/month | $1.15 |
| Twilio outbound calls | ~$0.013/min | $0.26 |
| Twilio recording | ~$0.0025/min | $0.05 |
| OpenAI ChatGPT (`gpt-4o-mini`) | ~$0.0006/turn | ~$0.50 |
| **Total** | | **~$2.00** |

Actual cost depends on call length and number of turns.

## Prerequisites

- Python 3.10+
- A Twilio account with a phone number
- An OpenAI API key with billing enabled
- ngrok (free tier) or another public tunnel

## Setup

1. Clone the repo and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

3. Get your Twilio credentials from the [Twilio Console](https://console.twilio.com):
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `FROM_PHONE`: a Twilio number in E.164 format (e.g., `+15551234567`)

4. Get your OpenAI API key from the [OpenAI Platform](https://platform.openai.com/) and make sure billing is enabled.

## Run the server

Start the FastAPI server locally:

```bash
python main.py
```

The server listens on port `8000`.

## Expose the server with ngrok

In a new terminal:

```bash
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://1234-56-78-90.ngrok-free.app`) and set it in your `.env`:

```bash
PUBLIC_URL=1234-56-78-90.ngrok-free.app
```

Restart the server so it picks up the new `PUBLIC_URL`.

## Make the test calls

```bash
python caller.py
```

This will call the 10 scenarios in `scenarios.py` one at a time. Each call runs up to 2 minutes, then hangs up. Wait for all calls to finish.

To run a single test call:

```bash
python test_call.py
```

## Review outputs

Each call has its own directory under `calls/`:

- `recording.wav` — full call recording
- `recording_meta.json` — recording metadata
- `transcript.json` — conversation transcript
- `conversation.json` — full chat history

## Scenarios covered

1. Schedule a routine checkup
2. Reschedule an existing appointment
3. Cancel an appointment
4. Request a medication refill
5. Ask about office hours
6. Ask about location and parking
7. Ask about insurance accepted
8. Caller speaks unclearly
9. Interrupt the agent
10. Off-script request (emotional support animal)

## Notes

- Do not call the number outside the assessment. Only call `+1-805-439-8008`.
- The bot uses `gpt-4o-mini` for cheap, fast responses.
- Speech recognition uses Twilio's `phone_call` model for better accuracy.

## Submitting

1. Push this repo to GitHub (public).
2. Record a 5-minute Loom walkthrough of your approach and the code.
3. Record a 5-minute screen recording of you using an AI tool (Cursor/Claude) to debug and iterate on the code.
4. Fill out the Pretty Good AI submission form with the GitHub link, Loom link, and the `FROM_PHONE` number you used.
