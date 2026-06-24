# Bug Report: Pretty Good AI Receptionist Assessment

## Summary

We tested the Pretty Good AI receptionist (`+1-805-439-8008`) with 10 patient scenarios. The system handles simple identity verification and appointment scheduling well, but fails in several important ways: it does not answer simple factual questions, hallucinates nonsensical questions, fails to cancel appointments, and mishears names. The most severe issues block the patient from completing their goal.

## Bug 1: Agent cannot cancel appointments

- **Severity:** High
- **Call:** `calls/call_03_cancel_appointment/`
- **What happened:** The patient asks to cancel their appointment. After identity verification, the agent says: "I can't cancel the appointment right now, but I can connect you to our patient support team for help."
- **Why it's a problem:** A receptionist that cannot handle cancellations forces patients to wait on hold or call back, creating a poor experience and extra work for the practice.
- **What should have happened:** The agent should cancel the appointment or schedule a follow-up to confirm the cancellation.
- **Reproduction:** Scenario `cancel_appointment`.

## Bug 2: Agent hallucinates nonsensical questions during medication refill

- **Severity:** High
- **Call:** `calls/call_04_medication_refill/`
- **What happened:** After confirming the refill request for Lisinopril, the agent asks: "How many days of life in a pearl? Do you have left right now?"
- **Why it's a problem:** The patient has no idea what the agent is asking. This breaks trust and makes the practice sound broken or incompetent.
- **What should have happened:** The agent should ask how many days of medication are left or confirm the pharmacy details.
- **Reproduction:** Scenario `medication_refill`.

## Bug 3: Agent does not answer office hours questions directly

- **Severity:** Medium
- **Call:** `calls/call_05_office_hours/`
- **What happened:** In the first call, the agent said "We're open Monday through Friday, but closed on Saturday" but never gave the actual opening and closing times. In the replay call, the agent did provide times, but the inconsistency shows it does not reliably answer the question.
- **Why it's a problem:** Patients need specific times to plan their visit. Vague answers lead to missed appointments or calls back to the office.
- **What should have happened:** The agent should consistently state the weekday hours and weekend status.
- **Reproduction:** Scenario `office_hours`.

## Bug 4: Agent does not give location or parking details

- **Severity:** Medium
- **Call:** `calls/call_06_location_directions/`
- **What happened:** The patient asks for the office address and parking information. The agent keeps asking for identity verification (name, DOB, spelling) but never provides the address or parking details.
- **Why it's a problem:** A new or visiting patient needs this information to arrive on time. The agent gets stuck in an identity loop instead of helping.
- **What should have happened:** The agent should provide the address and parking information after a simple identity check or even without it for general information.
- **Reproduction:** Scenario `location_directions`.

## Bug 5: Agent does not answer insurance acceptance questions

- **Severity:** Medium
- **Call:** `calls/call_07_insurance_question/`
- **What happened:** The patient asks if the practice accepts Aetna insurance. The agent asks for full name and date of birth instead of answering the insurance question.
- **Why it's a problem:** Insurance is often a deciding factor before booking. Forcing identity verification before answering a simple yes/no question creates friction.
- **What should have happened:** The agent should answer the insurance question directly, then optionally offer to book an appointment.
- **Reproduction:** Scenario `insurance_question`.

## Bug 6: Agent does not handle unclear speech

- **Severity:** Medium
- **Call:** `calls/call_08_unclear_speech/`
- **What happened:** The patient mumbles and asks for an appointment. The agent does not respond or ask for clarification. The transcript is empty after the greeting.
- **Why it's a problem:** Patients with colds, accents, or speech difficulties will be ignored or dropped.
- **What should have happened:** The agent should say something like "I'm sorry, I didn't catch that. Could you please repeat that?"
- **Reproduction:** Scenario `unclear_speech`.

## Bug 7: Agent mishears names and confidently confirms incorrect spellings

- **Severity:** Medium
- **Call:** `calls/call_02_reschedule_appointment/`, `calls/call_00_interruption/`
- **What happened:** The agent mishears "Jordan" and "Nguyen" as "Noen" and confidently confirms the incorrect spelling. The patient has to correct the agent.
- **Why it's a problem:** Incorrect patient records lead to scheduling errors, missed reminders, and billing problems.
- **What should have happened:** The agent should ask for clarification when it is unsure of a name or spelling, especially for uncommon names.
- **Reproduction:** Scenarios `reschedule_appointment` and `interruption`.

## Bug 8: Agent does not reschedule the appointment

- **Severity:** Medium
- **Call:** `calls/call_02_reschedule_appointment/`
- **What happened:** The patient asks to reschedule from Friday to Monday. The agent only collects identity information and never offers available times or completes the reschedule.
- **Why it's a problem:** The patient's goal is not accomplished. They still need to call back or wait for help.
- **What should have happened:** The agent should look up the appointment and propose a new time.
- **Reproduction:** Scenario `reschedule_appointment`.

## Bug 9: Agent does not handle off-script requests

- **Severity:** Low
- **Call:** `calls/call_10_off_script_request/`
- **What happened:** The patient asks if they can bring their emotional support dog. The agent mishears "Quinn" as "Gwen" and continues with identity verification without addressing the question.
- **Why it's a problem:** Patients with special needs or accessibility questions may not get answers. The name mishearing also contributes to record errors.
- **What should have happened:** The agent should answer the question or transfer to a human if it cannot handle it.
- **Reproduction:** Scenario `off_script_request`.

## Notes

- The agent often starts calls with phrases like "Thanks for calling Pivot Point Orthopedics. Part of pretty good. AI." or "Training purposes." This sounds unprofessional and can confuse callers.
- The agent is good at collecting identity information (name, DOB, phone number) but frequently gets stuck in verification loops instead of solving the caller's problem.
- Speech recognition errors are common with names and some words, but the agent does not gracefully ask for clarification.
