# F8-02 GitHub Copilot Diagnosis

- Member: Alex Marek
- Tool: GitHub Copilot Chat (PyCharm)
- Date: 3 November 2026
- Defect: F8-02 - Cancelled Appointment History
- Human-first hypothesis: See Section E of stage08_activities_and_evidence.md.

## Actual Prompt

I'm working on the second debugging issue (F8-02) for Stage 8 of our SmartCare assignment. The problem is that cancelled appointments aren't being found properly, even though they're still stored in the system.

According to FR-07 and AC-05.2, cancelling an appointment should change its status to CANCELLED, but the appointment should still be stored and retrievable using its original ID. AC-05.3 also requires invalid state transitions, such as cancelling the same appointment twice, to raise ValueError without changing the appointment.

The problem I'm getting is that after booking A001 for practitioner D001 at 2026-11-01 10:30 and cancelling it, `store.find_appointment("A001")` returns None instead of the original appointment. When I try cancelling it again, the service raises LookupError instead of ValueError.

These tests are currently failing:
- `test_cancel_appointment_retains_record_and_changes_status`
- `test_cancelling_again_raises_value_error_and_preserves_state`
- `test_cancelled_slot_can_be_booked_again`
- `test_f8_02_cancelled_history_regression`

My new regression test fails at line 64 with `AssertionError: assert None is original`.

I looked through `find_appointment()` in `data_store.py` and found this code:

def find_appointment(self, appointment_id: str) -> Appointment | None:
    if not isinstance(appointment_id, str) or not appointment_id.strip():
        raise ValueError("Appointment ID cannot be blank")
    for appointment in self.list_appointments():
        if (appointment.appointment_id == appointment_id.strip()
                and appointment.status.value != "cancelled"):
            return appointment
    return None

The cancellation service first uses `self.data_store.find_appointment(appointment_id)` to retrieve the appointment. If it returns None, the service raises `LookupError("Appointment not found")`.

My original hypothesis, which I recorded before consulting Copilot, was that the lookup method might be filtering out cancelled appointments rather than returning all stored appointments by their ID. I also considered whether cancellation was removing the appointment from the datastore.

The regression test shows that the appointment has CANCELLED status and is still present in `store.list_appointments()`, but looking it up by ID returns None.

Can you give me the three most likely causes of this issue, ranked from most to least likely? For each one, explain why it might be causing the problem, what evidence supports or contradicts it, and how I could check whether it's actually the cause.

Then explain which cause you think is most likely, what the smallest fix would be, and what existing behaviour I need to make sure doesn't change.

Please don't edit any files or rewrite the program. I only want help diagnosing the issue for now, without adding new features, dependencies, or requirements.

## Actual Copilot Response

1.
find_appointment() filters out cancelled records — overwhelmingly most likely. Its condition explicitly requires appointment.status.value != "cancelled". That explains both symptoms: lookup returns None, and cancel_appointment() raises LookupError before it can attempt the second cancellation. The regression evidence that A001 is still in list_appointments() supports this cause and contradicts removal. Check: inspect the stored A001’s ID and status, then evaluate the lookup condition; the matching ID is excluded solely because its status is cancelled.
2.
Cancellation removes or replaces the stored appointment — possible generally, but contradicted here. If the record were removed, lookup would fail too. However, the regression test finds the cancelled appointment in list_appointments(), so removal is not the observed cause. Check: compare the object in list_appointments() after cancellation with the original A001 object, and confirm the ID and status.
3.
The requested ID does not match the stored ID — possible, but unlikely. A mismatch would also make lookup return None; however, the reported call uses "A001", and the method trims the lookup argument before comparing it. Check: inspect the stored appointment IDs and the exact lookup argument (including whitespace) after cancellation; confirm one stored ID equals "A001".
Most likely diagnosis and smallest fix: remove the cancelled-status condition from find_appointment() so it returns a matching appointment by ID regardless of status. Preserve blank-ID validation and the existing status transition: the first cancellation should retain the record and set it to CANCELLED; a second cancellation should find that same record and raise ValueError without changing it. Keep the conflict check’s scheduled-only rule so a cancelled appointment’s time slot can be booked again.