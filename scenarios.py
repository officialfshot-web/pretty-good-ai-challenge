"""Patient scenarios for testing the Pretty Good AI voice agent."""

SCENARIOS = [
    {
        "key": "schedule_checkup",
        "title": "Schedule a routine checkup",
        "goal": "Schedule an annual checkup appointment for next week, preferably in the morning.",
        "patient": "You are Alex Rivera, DOB 03/12/1988. You have been a patient at the practice for 2 years. You want a morning slot if available.",
    },
    {
        "key": "reschedule_appointment",
        "title": "Reschedule an existing appointment",
        "goal": "Reschedule your appointment from this Friday to next Monday at the same time.",
        "patient": "You are Jordan Smith, DOB 11/04/1995. You have an appointment this Friday at 2pm but something came up. You want to move it to Monday.",
    },
    {
        "key": "cancel_appointment",
        "title": "Cancel an appointment",
        "goal": "Cancel your upcoming appointment and ask if you need to call back to reschedule.",
        "patient": "You are Taylor Brown, DOB 07/22/1976. You have an appointment tomorrow but you need to cancel. You may reschedule later.",
    },
    {
        "key": "medication_refill",
        "title": "Request a medication refill",
        "goal": "Request a refill for your blood pressure medication, Lisinopril.",
        "patient": "You are Morgan Lee, DOB 09/30/1992. You take Lisinopril 10mg daily and need a 90-day refill. Your pharmacy is CVS on Main Street.",
    },
    {
        "key": "office_hours",
        "title": "Ask about office hours",
        "goal": "Ask what time the office opens and closes, and whether they are open on Saturday.",
        "patient": "You are a new patient, Sam Wilson, DOB 01/15/2000. You are thinking about scheduling a visit but need to know the hours first.",
    },
    {
        "key": "location_directions",
        "title": "Ask about location and parking",
        "goal": "Ask for the office address and where to park.",
        "patient": "You are Casey Kim, DOB 05/08/1983. You have an appointment tomorrow but have never been to the office. You need directions and parking info.",
    },
    {
        "key": "insurance_question",
        "title": "Ask about insurance accepted",
        "goal": "Ask if the practice accepts your insurance, Aetna.",
        "patient": "You are Riley Patel, DOB 12/19/1990. You recently switched to Aetna insurance and want to confirm the practice accepts it before booking.",
    },
    {
        "key": "unclear_speech",
        "title": "Caller speaks unclearly",
        "goal": "Mumble slightly and ask about an appointment. See if the agent asks for clarification politely.",
        "patient": "You are Jamie Carter, DOB 04/25/1987. You have a bit of a cold and are speaking quietly. You want to book an appointment but are hard to understand.",
    },
    {
        "key": "interruption",
        "title": "Interrupt the agent",
        "goal": "Start the call, then interrupt the agent mid-sentence to ask a different question. See how it handles barge-in.",
        "patient": "You are Drew Nguyen, DOB 10/03/1979. You are in a hurry. Interrupt the agent while they are speaking and ask about your prescription refill instead.",
    },
    {
        "key": "off_script_request",
        "title": "Off-script request",
        "goal": "Ask something unusual: whether you can bring your emotional support animal to the appointment.",
        "patient": "You are Quinn Miller, DOB 06/17/1994. You want to book a checkup but need to bring your emotional support dog. Ask if that is allowed.",
    },
]
