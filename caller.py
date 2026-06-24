"""Make outbound test calls to the Pretty Good AI assessment line."""

# WALKTHROUGH NARRATION:
# This file makes the actual phone calls.
# It loads 10 patient scenarios from scenarios.py and calls the Pretty Good AI test number once per scenario.
# For each call, it asks Twilio to record the conversation and send webhooks to our FastAPI server.
# Then it waits for the call to finish and moves on to the next scenario.

import os
import time

from dotenv import load_dotenv
from twilio.rest import Client

from scenarios import SCENARIOS

# Load credentials from .env
load_dotenv()

# Twilio credentials and phone numbers
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_PHONE = os.getenv("FROM_PHONE")
TO_PHONE = os.getenv("TO_PHONE", "+18054398008")
PUBLIC_URL = os.getenv("PUBLIC_URL")

# Each call runs up to 2 minutes; 5 second pause between calls
CALL_TIMEOUT_SECONDS = 120
DELAY_BETWEEN_CALLS = 5


def validate_env():
    # Make sure we have the required environment variables before starting
    missing = []
    for key in ["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "FROM_PHONE", "PUBLIC_URL"]:
        if not os.getenv(key):
            missing.append(key)
    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")


def make_call(client: Client, scenario: dict, call_index: int) -> str:
    """Create an outbound Twilio call and point it to our FastAPI server."""
    # Unique ID for this call, used to save transcripts and recordings
    call_id = f"call_{call_index:02d}_{scenario['key']}"
    # The Twilio webhook URL that serves the initial TwiML
    twiml_url = f"https://{PUBLIC_URL}/twiml?scenario={scenario['key']}&call_id={call_id}"

    print(f"\n[{call_id}] Calling {TO_PHONE} for scenario: {scenario['title']}")

    # Create the actual Twilio call with recording and callbacks enabled
    call = client.calls.create(
        to=TO_PHONE,
        from_=FROM_PHONE,
        url=twiml_url,
        method="POST",
        record=True,
        recording_channels="dual",
        recording_status_callback=f"https://{PUBLIC_URL}/recording?call_id={call_id}",
        recording_status_callback_event=["completed"],
        recording_status_callback_method="POST",
        status_callback=f"https://{PUBLIC_URL}/status?call_id={call_id}",
        status_callback_event=["completed"],
        status_callback_method="POST",
    )
    return call.sid


def wait_for_call(client: Client, call_sid: str, call_id: str, timeout: int = CALL_TIMEOUT_SECONDS):
    """Poll Twilio every 5 seconds until the call ends or hits the timeout."""
    start = time.time()
    while time.time() - start < timeout:
        call = client.calls(call_sid).fetch()
        status = call.status
        print(f"[{call_id}] Call status: {status}")

        if status in ("completed", "failed", "busy", "no-answer", "canceled"):
            return status

        time.sleep(5)

    # If the call is still going after the timeout, force it to end
    print(f"[{call_id}] Timeout reached, hanging up")
    try:
        client.calls(call_sid).update(status="completed")
    except Exception as e:
        print(f"[{call_id}] Error hanging up: {e}")
    return "completed"


def run_test_call(client: Client, scenario_key: str = "schedule_checkup"):
    """Make a single short test call to verify everything works before the full run."""
    scenario = next((s for s in SCENARIOS if s["key"] == scenario_key), SCENARIOS[0])
    call_id = f"test_{scenario['key']}"
    print(f"\n=== TEST CALL: {scenario['title']} ===")
    call_sid = make_call(client, scenario, 0)
    status = wait_for_call(client, call_sid, call_id, timeout=60)
    print(f"Test call ended with status: {status}")


def run_all_calls(client: Client):
    """Run through all 10 scenarios and make one call per scenario."""
    print(f"Starting {len(SCENARIOS)} test calls to {TO_PHONE}")
    print(f"From: {FROM_PHONE}")
    print(f"Webhook URL: https://{PUBLIC_URL}")

    for i, scenario in enumerate(SCENARIOS, 1):
        try:
            call_sid = make_call(client, scenario, i)
            final_status = wait_for_call(client, call_sid, f"call_{i:02d}_{scenario['key']}")
            print(f"Call {i} ended with status: {final_status}")
        except Exception as e:
            print(f"Call {i} failed: {e}")

        # Pause between calls to avoid overwhelming the test line
        if i < len(SCENARIOS):
            print(f"Waiting {DELAY_BETWEEN_CALLS}s before next call...")
            time.sleep(DELAY_BETWEEN_CALLS)

    print("\nAll calls completed. Recordings and transcripts are in the /calls directory.")


def main():
    # Validate environment, then run all 10 test calls
    validate_env()
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    run_all_calls(client)


if __name__ == "__main__":
    main()
