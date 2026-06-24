# Bug Report Template

Use this template to document issues found during the calls. Aim for quality over quantity. One clear, well-explained bug is better than ten vague observations.

## Bug: [Short title]

- **Severity:** High / Medium / Low
- **Call:** `calls/call_XX_.../conversation.wav` and `transcript.json`
- **Timestamp:** e.g., 0:45
- **What happened:** Describe exactly what the agent said or did.
- **Why it's a problem:** Explain the real-world impact on a patient or the practice.
- **What should have happened:** Describe the correct behavior.
- **Reproduction:** Which scenario triggers it? Can it be reproduced reliably?

## Example

**Bug:** Agent books appointment on Sunday when office is closed
- **Severity:** High
- **Call:** `calls/call_01_schedule_checkup/`
- **Timestamp:** 1:23
- **What happened:** When asked "Can I come in Sunday at 10am?", the agent said "I've scheduled you for Sunday at 10 am" without checking office hours.
- **Why it's a problem:** The patient will show up to a closed office, wasting their time and creating a bad experience.
- **What should have happened:** The agent should have said the office is closed on weekends and offered the next available weekday.
- **Reproduction:** Scenario `schedule_checkup`, request a Sunday appointment.
