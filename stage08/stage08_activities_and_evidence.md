# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [complete]
Members and UG/PG cohorts: [complete]
Record owner / contribution links for each member: [complete]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason: [complete]

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: 

- Expected behaviour: Following FR-07 and AC-05.2, a cancelled appointment must remain stored and retrievable using its original ID.
- Observed behaviour: After cancelling A001, store.find_appointment("A001") returned None instead of the original appointment.
- Minimal reproduction: Register patient P001 and practitioner D001, book A001 at 2026-11-01 10:30, cancel it and attempt to find A001 using the same datastore.
- Hypothesis: The appointment lookup method may be excluding cancelled appointments instead of returning all stored appointments by their ID.
- Evidence to inspect: Compare list_appointments() and find_appointment() after cancellation, inspect the datastore's lookup conditions and trace the service's call to the datastore.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: [complete]

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: [complete]

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: [complete]

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: [complete]


Classification responses (1–5, each with reason): [complete]
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: [complete]
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: [complete]

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: `ad1a79e6f7cb5e85c48a328b58012d17da59b176` SmartCare A3 Requirements Baseline 2026, revision 2.
- Baseline test command / working directory / observed result / evidence: [complete]
- Clean preparation SHA if a record-only commit followed Stage 7: [complete]
- Branch and preparer / how teammates obtained this branch: [complete]
- Downloaded tool version, source SHA256 and --check outcome: [complete]
- --apply and --verify output summaries / artefact references: [complete]
- Bounded diff inspected and recovery location (not committed): [complete]
- Prepared faulty-state commit SHA: 27445c702a5c32c3922f94f4239768e481b60d5c
- Preparation or recovery issues and resolution, if any: [complete]
- Initial prepared full-suite command / result / key failures: Ran python -m pytest -q from project/ on main at SHA d5bf17c1bf3b556c3339cbbf5e946ec13fcb32a5. Result: 42 passed, 5 failed in 0.32s. Two failures related to practitioner conflicts (F8-01), where a ValueError was expected but not raised. Three failures related to cancelled appointment history (F8-02), where cancelled records could not be retrieved and repeated cancellation raised LookupError instead of ValueError.

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: The system allowed a second appointment to be booked for the same practitioner at the same date and time. The existing tests expected ValueError, but no exception was raised.
- Expected behaviour and requirement: According to FR-05 and AC-04.1, a practitioner cannot have two scheduled appointments at the same time. AC-04.2 allows different practitioners to have appointments at the same time. Rejected bookings must not change existing stored appointments.
- Minimal synthetic reproduction steps: Create a fresh SmartCareDataStore and register patients P001 and P002 and practitioners D001 and D002. Book appointment A001 for P001 with D001 at 2026-11-01 10:30. Attempt to book A002 for P002 with D001 at the same time. The expected result is ValueError, but the faulty implementation allows the booking. In a separate fresh test setup, book appointments with D001 and D002 at the same time to check that different practitioners are allowed. Check that rejected bookings do not change the stored appointment records.
- Meaningful failing test path/name and exact relevant failure: `tests/test_services.py::test_booking_rejects_practitioner_time_conflict` failed at line 102 because the expected ValueError was not raised. The supplied starter test `tests/test_starter.py::test_conflict_rule_and_different_practitioner` also failed at line 127 because the conflicting booking was accepted.
- Human hypothesis and intended checks: See E, F8-01.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: After cancelling an appointment, the data store returned None when searching for its ID. Attempting to cancel the same appointment again raised LookupError rather than ValueError.
- Expected behaviour and requirement: According to FR-06, FR-07, AC-05.2 and AC-05.3, cancellation must change the appointment status to CANCELLED without removing its stored history. The same object must remain retrievable, and a repeated cancellation must raise ValueError without changing the record.
- Minimal synthetic reproduction steps: Register P001 and D001, book A001 at 2026-11-01 10:30 and cancel it. Search for A001 using the same SmartCareDataStore instance, then attempt a second cancellation. The current tests show that lookup returns None and repeated cancellation raises LookupError.
- Meaningful failing test path/name and exact relevant failure: `tests/test_services.py::test_cancel_appointment_retains_record_and_changes_status` failed at line 134 because `store.find_appointment("A001")` returned None instead of the original appointment. `test_cancelling_again_raises_value_error_and_preserves_state` failed because LookupError was raised instead of ValueError. `test_cancelled_slot_can_be_booked_again` also failed because the cancelled original appointment could not be retrieved.
- Human hypothesis and intended checks: See E, F8-02.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: The datastore's practitioner conflict check may be using the wrong comparison operator. The failed tests show that a second booking for the same practitioner is not recognised as a conflict.
Evidence intended to inspect / competing explanation / discriminating check: Compare the practitioner IDs used in has_practitioner_conflict() and check the call from AppointmentService.book_appointment(). An alternative explanation is that the service is failing to call the conflict check. Inspecting the call path can distinguish these causes.
Member and saved sequence/time or commit showing this preceded consultation: Alex. 1/11/2026: 4:15PM. `f552418d4aabab9f705bef9891b9650b20c150c9`

### F8-02 human entry
Likely cause and why plausible: Appointment lookup may be filtering out cancelled records rather than returning the stored appointment by ID. The failure occurs after cancellation even though the appointment object still exists in the workflow.
Evidence intended to inspect / competing explanation / discriminating check: Compare list_appointments() with find_appointment() after cancellation. Check whether the appointment remains stored but is filtered during lookup. Another possible cause is removal from the underlying appointment collection; the two observations distinguish them.
Member and saved sequence/time or commit showing this preceded consultation: Alex. 1/11/2026: 4:37PM. `f552418d4aabab9f705bef9891b9650b20c150c9`

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

### F8-02 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | [complete] | [complete] | [complete] |
| F8-02 after repair | [complete] | [complete] | [complete] |
| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [complete]

2. Where should expected behaviour come from during debugging?

Response: [complete]

3. What is a debugging hypothesis?

Response: [complete]

4. What is a regression test and why is it retained?

Response: [complete]

5. What is meant by root cause?

Response: [complete]

6. What is refactoring?

Response: [complete]

7. What is a swallowed exception?

Response: [complete]

8. What is a code smell?

Response: [complete]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [complete]

10. What is the Stage 8 engineering rule?

Response: [complete]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
