# F8-01 GitHub Copilot Diagnosis

- Member: Alex Marek
- Tool: GitHub Copilot Chat (PyCharm)
- Date: 3 November 2026
- Defect: F8-01 - Practitioner Booking Conflict
- Human-first hypothesis: See Section E of stage08_activities_and_evidence.md.

## Actual Prompt

I'm working on Stage 8 of our SmartCare assignment and trying to figure out why the practitioner booking conflict test is failing.

According to FR-05 and AC-04.1, a practitioner shouldn't be able to have two scheduled appointments at the same date and time. However, different practitioners should still be allowed to have appointments at the same time under AC-04.2. If a booking is rejected, the existing appointments should remain unchanged.

The problem I'm getting is that when I book A001 for practitioner D001 at 2026-11-01 10:30, the system still allows me to book A002 for D001 at the exact same time. The test expects a `ValueError`, but it doesn't raise one.

These tests are currently failing:

- `test_booking_rejects_practitioner_time_conflict`
- `test_conflict_rule_and_different_practitioner`
- `test_f8_01_practitioner_conflict_regression`

The regression test fails at line 37 with `Failed: DID NOT RAISE ValueError`.

I looked through `has_practitioner_conflict()` in `data_store.py` and noticed this condition:

appointment.appointment_id != exclude_appointment_id
and appointment.practitioner.practitioner_id != practitioner_id
and appointment.date_time == date_time
and appointment.status.value == "scheduled"

I also checked `book_appointment()` in `services.py`, and it appears to pass `practitioner.practitioner_id` and `date_time` correctly to the conflict-checking method.

My original hypothesis was that the practitioner ID comparison might be using the wrong operator, although I also considered whether the service was calling the method incorrectly. The Git diff shows the comparison was changed during the Stage 8 fault injection.

Can you give me the three most likely causes of this issue, ranked from most to least likely? For each one, explain why it might be causing the problem, what evidence supports or contradicts it, and how I could check whether it's actually the cause.

Then explain which cause you think is most likely, what the smallest fix would be, and what existing behaviour I need to make sure doesn't change.

Please don't edit any files or rewrite the program. I only want help diagnosing the issue for now, without adding new features, dependencies, or requirements.

## Actual Copilot Response

1.
Wrong practitioner-ID operator — most likely. The current condition uses !=, so an existing D001 appointment does not match a D001 booking. It can also make an appointment for a different practitioner look like a conflict. The service’s call and arguments appear correct, and the Stage 8 diff showing this operator changed strongly supports an injected comparison fault. Check: with A001 stored, call has_practitioner_conflict("D001", when); it should return True but currently returns False.
2.
The service skips the check or passes incorrect arguments — less likely. That could explain why no ValueError is raised, but the inspected book_appointment() calls the check with the practitioner ID and requested time, then raises if it returns True. Check: trace or instrument the call during the second booking and verify it is reached with "D001" and the exact when.
3.
The stored appointment’s time or status fails to match — least likely. The conflict check requires an exact datetime match and a scheduled appointment. The test uses the same datetime for both bookings, and newly created appointments are scheduled by default. Check: before the second booking, inspect A001’s date_time and status.value and compare them to the requested values.
Most likely diagnosis and smallest fix: Change the practitioner-ID comparison from != to == in has_practitioner_conflict(). Keep the appointment-ID exclusion, datetime equality, and scheduled-status check intact. Verify the fix still allows a different practitioner at the same time and the same practitioner at a different time. A rejected booking must still raise before insertion, leaving A001 and its status unchanged.