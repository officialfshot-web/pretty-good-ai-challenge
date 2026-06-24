# Architecture

The system is built around three components: Twilio for telephony and speech services, OpenAI's ChatGPT API for the patient conversation logic, and a FastAPI server that orchestrates the call flow.

## Call Flow

1. `caller.py` creates an outbound Twilio call to `+1-805-439-8008` and points it to the `/twiml` endpoint.
2. The `/twiml` endpoint returns a TwiML document that uses Twilio's `<Say>` to speak the patient's initial greeting and `<Gather>` to listen for the agent's response.
3. When the agent speaks, Twilio sends the transcribed speech to the `/respond` endpoint as a `SpeechResult` parameter.
4. The `/respond` endpoint sends the conversation history to OpenAI's `gpt-4o-mini` API and receives a patient response.
5. The response is returned to Twilio as TwiML with `<Say>` for the patient and a new `<Gather>` for the next agent turn.
6. This loop continues until the bot says goodbye, the goal is complete, or the turn limit is reached.

## Recording

Twilio records each call automatically. When the recording is ready, Twilio hits the `/recording` endpoint with the recording URL, and the server downloads the WAV file into the call's `calls/` directory.

## Transcripts

The server maintains an in-memory conversation history for each call. After every turn and when the call ends, the transcript is saved as `transcript.json` and `conversation.json` in the call's directory.

## Why this approach

We originally planned to use OpenAI's Realtime API for end-to-end voice, but the provided API key did not have access to that model. This architecture uses stable, accessible Twilio speech features and the standard OpenAI ChatGPT API, making it cheaper and more reliable while still producing natural patient conversations.
