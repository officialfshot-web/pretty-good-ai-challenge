"""Make outbound test calls to the Pretty Good AI assessment line."""

import os
import time

from dotenv import load_dotenv
from twilio.rest import Client

from scenarios import SCENARIOS

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_PHONE = os.getenv("FROM_PHONE")
TO_PHONE = os.getenv("TO_PHONE", "+18054398008")
PUBLIC_URL = os.getenv("PUBLIC_URL")

CALL_TIMEOUT_SECONDS = 120  # Max 2 minutes per call
DELAY_BETWEEN_CALLS = 5     # Seconds between calls


def validate_env():
    missing = []
    for key in ["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "FROM_PHONE", "PUBLIC_URL"]:
        if not os.getenv(key):
            missing.append(key)
    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")


def make_call(client: Client, scenario: dict, call_index: int) -> str:
    """Create an outbound Twilio call for a specific scenario."""
    call_id = f"call_{call_index:02d}_{scenario['key']}"
    twiml_url = f"https://{PUBLIC_URL}/twiml?scenario={scenario['key']}&call_id={call_id}"

    print(f"\n[{call_id}] Calling {TO_PHONE} for scenario: {scenario['title']}")

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
    """Poll call status until it completes or timeout."""
    start = time.time()
    while time.time() - start < timeout:
        call = client.calls(call_sid).fetch()
        status = call.status
        print(f"[{call_id}] Call status: {status}")

        if status in ("completed", "failed", "busy", "no-answer", "canceled"):
            return status

        time.sleep(5)

    print(f"[{call_id}] Timeout reached, hanging up")
    try:
        client.calls(call_sid).update(status="completed")
    except Exception as e:
        print(f"[{call_id}] Error hanging up: {e}")
    return "completed"


def run_test_call(client: Client, scenario_key: str = "schedule_checkup"):
    """Make a single cheap test call to verify the setup."""
    scenario = next((s for s in SCENARIOS if s["key"] == scenario_key), SCENARIOS[0])
    call_id = f"test_{scenario['key']}"
    print(f"\n=== TEST CALL: {scenario['title']} ===")
    call_sid = make_call(client, scenario, 0)
    status = wait_for_call(client, call_sid, call_id, timeout=60)
    print(f"Test call ended with status: {status}")
    print("Check calls/test_schedule_checkup/ for transcript and recording.")


def run_all_calls(client: Client):
    """Make all 10 test calls."""
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

        if i < len(SCENARIOS):
            print(f"Waiting {DELAY_BETWEEN_CALLS}s before next call...")
            time.sleep(DELAY_BETWEEN_CALLS)

    print("\nAll calls completed. Recordings and transcripts are in the /calls directory.")


def main():
    validate_env()
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    run_all_calls(client)


if __name__ == "__main__":
    main()
