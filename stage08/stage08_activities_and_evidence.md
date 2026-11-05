# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Tue 1:30 - 3:30 Group 2
Members and UG/PG cohorts: Alex Marek (UG), Kreesha Singh (UG), CoolCoder49, kreesha-12
Record owner / contribution links for each member: Alex

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

Response and reason:

- "Appointment disappears after cancellation." (Symptom): This describes unexpected behaviour observed in the system, but does not explain what caused it. The appointment may still be stored but no longer accessible through lookup.
- "The data-store removal path is probably being called." (Hypothesis): This suggests a possible cause, but there is no evidence that the appointment was removed. You would need to inspect the datastore to determine whether the appointment was deleted or excluded from lookup.
- "The failing test shows store.find_appointment('A1') returns None." (Evidence): This describes a specific result obtained from testing. It shows that the appointment lookup returned None instead of the expected appointment, but it doesn't explain why.
- "The service layer is badly designed." (Opinion): This is a general judgement rather than a specific observation or testable explanation. More evidence is needed to identify an actual design issue.
- "Traceback points to smartcare/services.py line 42 in the example." (Evidence): A traceback identifies where an error occurred during execution, which can help with debugging. However, the example line number does not establish the root cause and should be checked against the actual code and traceback.

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

Response and reason: 

A test that expects cancelled appointments to be deleted is a test defect because it violates FR-07, which states that appointment history should be retained after cancellation. The test should be fixed to ensure that the appointment is retained and can be retrieved via its original ID, with its status being CANCELLED. The production code should not be altered to meet the incorrect test expectation.

Similarly, a test that expects appointments with different practitioners on the same date and time to conflict is incorrect under AC-04.2. The conflict rule only stops the same practitioner having multiple appointments scheduled at the same time. The test should check that appointments with different practitioners can be booked at the same time, and that only the same practitioner cannot have overlapping appointments.

In both instances, the requirements should be checked before making any changes. A failing test doesn't necessarily mean that the production code is wrong, as the issue could be with the test itself and its expected behaviour.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason:

- Rename `appt` to `appointment` (Refactoring): This improves readability by making the variable name more descriptive without changing the program's functionality.
- Extract a repeated conflict helper (Refactoring): Moving duplicated conflict-checking logic into a focused helper method reduces repetition and makes the code easier to maintain, provided the same conflict rules and outcomes are preserved.
- Add rescheduling (New feature): This introduces functionality that does not currently exist in the required Stage 8 behaviour, so it is not considered refactoring.
- Restore retained cancellation lookup (Defect repair): This corrects existing behaviour that contradicts FR-07 and AC-05.2, which require cancelled appointments to remain stored and retrievable using their original ID.
- Replace a magic status string with the existing enum (Refactoring): Using `AppointmentStatus.SCHEDULED` instead of a hardcoded string improves readability and consistency while preserving the same status comparison.


### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: 

The failing test, tests/test_services.py::test_booking_rejects_practitioner_time_conflict, checks whether the system correctly rejects two appointments for the same practitioner on the same date and time.

Exception/assertion: The test failed at line 102 because pytest.raises(ValueError) expected a ValueError, but no exception was raised.

Expected behaviour: Following FR-05 and AC-04.1, attempting to book a second scheduled appointment for practitioner D001 at 2026-11-01 10:30 should raise ValueError. The original appointment should remain unchanged.

Observed behaviour: The system allowed the conflicting appointment to be booked instead of rejecting it.

Application call path: The test calls AppointmentService.book_appointment(), which calls SmartCareDataStore.has_practitioner_conflict(). If the conflict check incorrectly returns False, the service continues and stores the second appointment.

Three possible causes:

Incorrect practitioner comparison operator (Most likely): The conflict-checking condition may be comparing practitioner IDs incorrectly. This is consistent with the system allowing two appointments for the same practitioner. To check, inspect the comparison in has_practitioner_conflict() and check whether identical practitioner IDs are recognised as a conflict.

Conflict-checking method not called correctly (Less likely): The booking service may be skipping the conflict check or passing incorrect arguments. To check, trace book_appointment() and confirm that it calls has_practitioner_conflict() with the correct practitioner ID and appointment time.

Incorrect date, time or appointment status comparison (Least likely): The existing appointment may not be recognised as a conflict because its date, time or status does not match the expected values. To check, inspect the stored appointment and confirm that both bookings use the same datetime and that the existing appointment has SCHEDULED status.

A traceback identifies where the test failed, but does not necessarily identify the underlying cause. The failure could result from incorrect conditions, arguments or stored data elsewhere in the application. Each hypothesis must therefore be checked against the source code and observed behaviour before deciding which repair is appropriate.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: 

Changing code immediately after seeing a failure is often a poor debugging strategy because the failure only shows that something went wrong, not necessarily what caused it. Without investigating first, a developer may misidentify the cause, change working code, or create new defects.

A failing test may also contain an incorrect expectation, meaning the issue could be with the test rather than the production code. The developer should first compare the expected and observed behaviour against the requirements, reproduce the failure, and investigate possible causes using evidence.

Once the cause is confirmed, use a focused regression test to demonstrate the defect before making the smallest necessary repair. Then run the relevant tests and the full test suite again to confirm the issue is resolved without affecting other existing code.


Classification responses (1–5, each with reason): Completed in A.1. All five statements have been classified as symptoms, evidence, hypotheses, or opinions, with explanations distinguishing observed behaviour from possible causes.
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: Completed in A.2 using the cancelled appointment history scenario. The record identifies the expected and observed behaviour, minimal reproduction steps, initial hypothesis and evidence to investigate, supported by FR-07 and AC-05.2.
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: Completed in A.5 using the practitioner booking conflict failure. The response identifies the failed assertion, expected and observed behaviour, application call path, supporting requirements, and three ranked hypotheses with investigation checks.

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: 6b2c70c4695a2b4c3e27a71b30d8998cc8b68f95 - SmartCare A3 Requirements Baseline 2026, revision 2.
- Baseline test command / working directory / observed result / evidence: The pre-injection Stage 7 code was verified at SHA 6b2c70c4695a2b4c3e27a71b30d8998cc8b68f95, immediately before the Stage 8 fault-injection commit. I created a separate Git worktree to preserve the existing debugging branch. Ran python -m pytest -q from smartcare-stage7-check/project/ using pytest 9.2.0. Result: 47 passed, 0 failed in 0.09 seconds. This confirms that all 47 existing tests passed before we introduced the controlled faults.
- Clean preparation SHA if a record-only commit followed Stage 7: N/A
- Branch and preparer / how teammates obtained this branch: During class, our tutor introduced the controlled Stage 8 faults on Kreesha's laptop using the debug/stage8 branch. The faulty-state changes were committed at SHA 27445c702a5c32c3922f94f4239768e481b60d5c and subsequently merged into main through GitHub pull request #4 (ad1a79e). The prepared code was then available to both group members through the shared GitHub repository. We are completing further debugging work on the debug/stage8-repairs branch.
- Downloaded tool version, source SHA256 and --check outcome: The controlled Stage 8 faults were introduced by our tutor during class on Kreesha's laptop. The original preparation utility and terminal output are no longer available to our group, so we could not independently verify the utility version, SHA256 hash, or --check result. However, the Git history confirms that the faults were introduced in commit 27445c702a5c32c3922f94f4239768e481b60d5c on 27 October 2026. The commit diff confirms that only project/smartcare/data_store.py was modified, introducing the practitioner conflict and cancelled appointment lookup defects.
- --apply and --verify output summaries / artefact references: The original --apply and --verify terminal outputs were not retained, as our tutor performed the controlled fault injection on Kreesha's laptop during class. However, we independently inspected the resulting changes through Git. Commit 27445c702a5c32c3922f94f4239768e481b60d5c confirms that only project/smartcare/data_store.py was modified. The changes introduced F8-01 by reversing the practitioner ID comparison from == to !=, and F8-02 by excluding cancelled appointments from find_appointment(). This confirms that both intended faults were present in the committed code, although we could not verify the original preparation utility's execution results.
- Bounded diff inspected and recovery location (not committed): The controlled Stage 8 changes were inspected using git show and git diff to compare the pre-injection commit 6b2c70c4695a2b4c3e27a71b30d8998cc8b68f95 with the prepared faulty-state commit 27445c702a5c32c3922f94f4239768e481b60d5c. The comparison confirmed that only project/smartcare/data_store.py was modified, introducing the two intended debugging faults without changing unrelated files. The local recovery folder project/.stage8_faults was not present on my computer, as the preparation was performed on Kreesha's laptop during class. However, the original pre-injection code remains available through Git commit 6b2c70c, providing a verified recovery reference without modifying the current debugging branch.
- Prepared faulty-state commit SHA: 27445c702a5c32c3922f94f4239768e481b60d5c
- Preparation or recovery issues and resolution, if any: The controlled Stage 8 fault injection was completed by our tutor on Kreesha's laptop during class. As the preparation was not performed on my computer, the original preparation utility, terminal output, and local recovery folder were unavailable for independent verification. To address this, I inspected the Git history to identify the original code and confirm the changes introduced during preparation. The pre-injection code was identified at SHA 6b2c70c4695a2b4c3e27a71b30d8998cc8b68f95, and the fault-injection commit was identified at SHA 27445c702a5c32c3922f94f4239768e481b60d5c. The Git diff confirmed that only project/smartcare/data_store.py was modified. I also created a separate Git worktree to test the pre-injection code, and all 47 tests passed. These checks confirmed the original working behaviour and the changes introduced during preparation without modifying the current debugging branch. The unavailable utility outputs remain an evidence limitation, but we can still recover the original code through Git. We will investigate and fix the two injected defects on debug/stage8-repairs.
- Initial prepared full-suite command / result / key failures: Ran python -m pytest -q from project/ on main at SHA d5bf17c1bf3b556c3339cbbf5e946ec13fcb32a5. Result: 42 passed, 5 failed in 0.32s. Two failures related to practitioner conflicts (F8-01), where a ValueError was expected but not raised. Three failures related to cancelled appointment history (F8-02), where cancelled records could not be retrieved and repeated cancellation raised LookupError instead of ValueError.

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: The system allowed a second appointment to be booked for the same practitioner at the same date and time. The existing tests expected a ValueError, but no exception was raised.
- Expected behaviour and requirement: According to FR-05 and AC-04.1, a practitioner cannot have two scheduled appointments at the same time. AC-04.2 allows different practitioners to have appointments at the same time. Rejected bookings must not change existing stored appointments.
- Minimal synthetic reproduction steps: Create a fresh SmartCareDataStore and register patients P001 and P002 and practitioners D001 and D002. Book appointment A001 for P001 with D001 at 2026-11-01 10:30. Attempt to book A002 for P002 with D001 at the same time. The expected result is ValueError, but the faulty implementation allows the booking. In a separate fresh test setup, book appointments with D001 and D002 at the same time to check that different practitioners are allowed. Check that rejected bookings do not change the stored appointment records.
- Meaningful failing test path/name and exact relevant failure: `tests/test_services.py::test_booking_rejects_practitioner_time_conflict` failed at line 102 because the expected ValueError was not raised. The supplied starter test `tests/test_starter.py::test_conflict_rule_and_different_practitioner` also failed at line 127 because the conflicting booking was accepted.
- Human hypothesis and intended checks: See E, F8-01.
- Supported root cause and inspected code/runtime evidence: The root cause was identified in SmartCareDataStore.has_practitioner_conflict() within project/smartcare/data_store.py. The condition appointment.practitioner.practitioner_id != practitioner_id incorrectly compares practitioner IDs using != instead of ==. This means the method checks for appointments belonging to different practitioners rather than identifying an existing appointment for the same practitioner at the same date and time. The call path was inspected in AppointmentService.book_appointment(), which correctly passes practitioner.practitioner_id and date_time to the conflict-checking method. This ruled out the alternative hypothesis that the service skipped the check or passed incorrect arguments. The failing tests test_booking_rejects_practitioner_time_conflict and test_conflict_rule_and_different_practitioner support this diagnosis, as both expected ValueError, but no exception was raised. The Git diff also confirmed that the comparison was changed from == to != during the controlled Stage 8 fault injection. Therefore, the incorrect comparison operator is the supported root cause of F8-01, contradicting FR-05 and AC-04.1.
- Smallest justified fix / diff / why other behaviour is preserved: The smallest repair was to change the practitioner ID comparison from != to == in SmartCareDataStore.has_practitioner_conflict() in project/smartcare/data_store.py. This allows the method to correctly identify an existing scheduled appointment for the same practitioner at the requested date and time. No other production code was changed. The appointment ID exclusion, exact date/time comparison, and scheduled-status condition were kept unchanged. The Git diff confirmed that only this comparison operator was changed. The repair was committed separately on debug/stage8-repairs as a79f2d712d33c5dbad9d895295f1c4dfd89522c5 (Stage 8 fix F8-01 practitioner booking conflict).
- Repair SHA / focused verification result: The F8-01 repair was committed on debug/stage8-repairs at SHA a79f2d712d33c5dbad9d895295f1c4dfd89522c5. After applying the one-operator fix, I ran python -m pytest -q tests/test_regressions.py::test_f8_01_practitioner_conflict_regression from project/, which passed with 1 passed in 0.01s. I then ran python -m pytest -q -k "booking_rejects_practitioner_time_conflict or conflict_rule_and_different_practitioner", which returned 2 passed, 47 deselected in 0.03s. This confirmed that all three F8-01 tests were passing. I also ran the full test suite using python -m pytest -q from project/, which returned 45 passed, 4 failed in 0.14s. All four remaining failures were related to F8-02, which had not yet been repaired. No F8-01 failures remained, and the previously passing tests continued to pass. These tests were run after the repair was applied and before the repair commit was created.

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: After cancelling an appointment, the data store returned None when searching for its ID. Attempting to cancel the same appointment again raised LookupError rather than ValueError.
- Expected behaviour and requirement: According to FR-06, FR-07, AC-05.2 and AC-05.3, cancellation must change the appointment status to CANCELLED without removing its stored history. The same object must remain retrievable, and a repeated cancellation must raise ValueError without changing the record.
- Minimal synthetic reproduction steps: Register P001 and D001, book A001 at 2026-11-01 10:30 and cancel it. Search for A001 using the same SmartCareDataStore instance, then attempt a second cancellation. The current tests show that lookup returns None and repeated cancellation raises LookupError.
- Meaningful failing test path/name and exact relevant failure: `tests/test_services.py::test_cancel_appointment_retains_record_and_changes_status` failed at line 134 because `store.find_appointment("A001")` returned None instead of the original appointment. `test_cancelling_again_raises_value_error_and_preserves_state` failed because LookupError was raised instead of ValueError. `test_cancelled_slot_can_be_booked_again` also failed because the cancelled original appointment could not be retrieved.
- Human hypothesis and intended checks: See E, F8-02.
- Supported root cause and inspected code/runtime evidence: The root cause of F8-02 is the cancelled-status condition in SmartCareDataStore.find_appointment() in project/smartcare/data_store.py. The method checks that the appointment ID matches but also requires appointment.status.value != "cancelled", which means it ignores appointments after they have been cancelled. The regression test confirmed that A001 remained in list_appointments() with CANCELLED status, but find_appointment("A001") returned None. This also explains why cancelling A001 a second time raises LookupError instead of ValueError: the service cannot retrieve the cancelled appointment to check its existing status. Inspecting the lookup condition and the failing regression test supports this diagnosis. The appointment has not been deleted, and the ID is correct. The problem is that find_appointment() filters out cancelled records when it should return stored appointments by ID, regardless of status.
- Smallest justified fix / diff / why other behaviour is preserved: The smallest repair was to remove the cancelled-status condition appointment.status.value != "cancelled" from SmartCareDataStore.find_appointment() in project/smartcare/data_store.py. The method now returns any stored appointment with a matching ID, regardless of whether its status is SCHEDULED or CANCELLED. I preserved the existing blank-ID validation and appointment ID comparison. No changes were made to the cancellation service or other production code. The Git diff confirmed that only the unnecessary status filter was removed. The repair was committed separately on debug/stage8-repairs at SHA c57312d93696542068b6d23a92617cfd68558364 (Stage 8 fix F8-02 cancelled appointment lookup).
- Repair SHA / focused verification result: The F8-02 repair was committed on debug/stage8-repairs at SHA c57312d93696542068b6d23a92617cfd68558364. After applying the repair, I ran python -m pytest -q tests/test_regressions.py::test_f8_02_cancelled_history_regression from project/, which returned 1 passed in 0.01s. I then ran python -m pytest -q -k "cancel_appointment_retains_record_and_changes_status or cancelling_again_raises_value_error_and_preserves_state or cancelled_slot_can_be_booked_again", which returned 3 passed, 46 deselected in 0.02s. I also ran the full test suite using python -m pytest -q from project/, which returned 49 passed in 0.05s, with no failures. This confirmed that cancelled appointments remain stored and retrievable by their original ID, cancelling the same appointment twice raises ValueError, and cancelled time slots can be booked again. I ran the tests after applying both repairs and before creating the F8-02 repair commit.

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: The datastore's practitioner conflict check may be using the wrong comparison operator. The failed tests show that a second booking for the same practitioner is not recognised as a conflict.
Evidence intended to inspect / competing explanation / discriminating check: Compare the practitioner IDs used in has_practitioner_conflict() and check the call from AppointmentService.book_appointment(). An alternative explanation is that the service isn't calling the conflict check. Inspecting the call path can distinguish these causes.
Member and saved sequence/time or commit showing this preceded consultation: Alex. 1/11/2026: 4:15 PM. `f552418d4aabab9f705bef9891b9650b20c150c9`

### F8-02 human entry
Likely cause and why plausible: Appointment lookup may be filtering out cancelled records rather than returning the stored appointment by ID. The failure occurs after cancellation even though the appointment object still exists in the workflow.
Evidence intended to inspect / competing explanation / discriminating check: Compare list_appointments() with find_appointment() after cancellation. Check whether the appointment remains stored but is filtered during lookup. Another possible cause is removal from the underlying appointment collection; the two observations distinguish them.
Member and saved sequence/time or commit showing this preceded consultation: Alex. 1/11/2026: 4:37 PM. `f552418d4aabab9f705bef9891b9650b20c150c9`

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: GitHub Copilot Chat was consulted by Alex through PyCharm on 3 November 2026, after the initial human hypothesis was recorded in Section E. The prompt outlined the requirements, expected and observed behaviour, failing tests, relevant code, and the original hypothesis. Copilot provided three ranked possible causes, evidence checks, and a suggested minimal repair without modifying any files. The revised prompt and its actual response are saved in stage08/copilot_f8_01_diagnosis.md.
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot's most likely diagnosis was that has_practitioner_conflict() uses the incorrect practitioner ID comparison operator (!= instead of ==). To check this, I inspected the condition in data_store.py and compared it against the expected behaviour in FR-05 and AC-04.1. The Git diff also confirmed that the operator was changed during the Stage 8 fault injection. The regression test failed because it accepted a second appointment for the same practitioner instead of raising ValueError. This suggestion was correct and accepted, as the evidence confirms that the incorrect comparison prevents the datastore from recognising conflicting appointments for the same practitioner.
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot's second suggestion was that AppointmentService.book_appointment() might be skipping the conflict check or passing incorrect arguments. To investigate, I inspected the method in services.py. The code confirmed that book_appointment() calls has_practitioner_conflict() using practitioner.practitioner_id and date_time, and raises ValueError when a conflict is detected. This suggestion was incorrect for the current defect and rejected, as the service call is implemented correctly. The failure is caused by the datastore returning the wrong conflict result, not by the service skipping the check.
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot's third suggestion was that the stored appointment's date, time, or status may not match the new booking. To investigate, I inspected the regression test and appointment conditions. Both bookings use the same datetime(2026, 11, 1, 10, 30), and newly created appointments have SCHEDULED status. The conflict-checking method compares the appointment's date and time directly and checks for the scheduled status. This suggestion was incorrect for the current defect and was rejected, as the test setup uses matching appointment times and the expected status. The evidence supports the practitioner ID comparison operator as the actual cause of the failure.
Final human conclusion and comparison with initial hypothesis: My original hypothesis was that the practitioner conflict check was using the wrong comparison operator. GitHub Copilot identified the same issue as its most likely diagnosis, supported by inspecting has_practitioner_conflict(), the call from book_appointment(), the failing tests, and the original fault-injection Git diff. The other two suggestions were investigated but did not explain the failure, as the service correctly passes the practitioner ID and appointment time, and the test uses matching times and a scheduled appointment. Therefore, the incorrect != operator is the confirmed root cause of F8-01. The smallest justified repair is to change != to == in the practitioner ID comparison, while preserving the existing appointment ID exclusion, date and time comparison, scheduled-status check, and exception behaviour. The regression tests will then be rerun to confirm that conflicting bookings are rejected, different practitioners can still be booked at the same time, and existing appointments remain unchanged.

### F8-02 Copilot review
Actual prompt / output reference and member: GitHub Copilot Chat was consulted by Alex Marek through PyCharm on 3 November 2026, after the initial human hypothesis was recorded in Section E. The prompt outlined the relevant requirements, expected and observed behaviour, failing tests, relevant code, and original hypothesis. Copilot provided three ranked possible causes, evidence checks, and a suggested minimal repair without modifying any files. The complete prompt and its actual response are saved in stage08/copilot_f8_02_diagnosis.md.
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot's most likely diagnosis was that find_appointment() incorrectly filters out cancelled appointments. To investigate, I inspected the lookup condition in data_store.py and compared it against FR-07 and AC-05.2. The condition appointment.status.value != "cancelled" prevents the method from returning an appointment once its status changes to CANCELLED. The regression test confirmed that the appointment was still present in list_appointments() with CANCELLED status, but find_appointment("A001") returned None instead of the original object. This suggestion was correct and accepted, as the evidence confirms that the cancelled-status condition caused the failed lookup.
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot's second suggestion was that cancelling an appointment might be removing or replacing the original object in the datastore. This could explain why the appointment could no longer be found by its ID. To investigate this, the F8-02 regression test checked whether the original appointment remained in store.list_appointments() after cancellation and whether the returned object was the same as the original. Both assertions passed before the test reached the failing lookup assertion, confirming that the appointment was still stored and had not been replaced. This suggestion was incorrect for the current defect and rejected, as the evidence shows that the appointment is retained but excluded by the lookup condition in find_appointment().
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot's third suggestion was that the appointment ID used during lookup might fail to match the ID stored in the datastore. An incorrect ID could cause find_appointment() to return None, even if the appointment still exists. To investigate, I reviewed the F8-02 regression test and the find_appointment() method. The test creates the appointment using ID "A001" and later searches for that same ID. The lookup method also removes surrounding whitespace before comparing the IDs. This suggestion was incorrect for the current defect and rejected, as the same appointment ID is used for booking, cancellation, and lookup. The evidence instead confirms that the cancelled-status condition prevents the matching appointment from being returned.
Final human conclusion and comparison with initial hypothesis: My original hypothesis was that find_appointment() filtered out cancelled appointments instead of returning all stored appointments by ID. I also considered whether cancellation was removing the appointment from the datastore. GitHub Copilot identified the cancelled-status filter as its most likely cause, which matched my original hypothesis. The regression test confirmed that A001 was still stored after cancellation and had CANCELLED status, but find_appointment("A001") returned None. The other two suggestions did not explain the failure because the original appointment remained in list_appointments(), and the same appointment ID was used throughout the test. I concluded that the condition appointment.status.value != "cancelled" in find_appointment() was the root cause of F8-02. The smallest justified repair is to remove this condition so appointments can be retrieved by ID regardless of their status, while keeping the blank-ID validation unchanged. After the repair, I will rerun the tests to confirm that cancelled appointments remain accessible, that cancelling the same appointment twice raises ValueError, and that cancelled time slots can still be booked again.

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | Faulty production code at SHA c45aa1c2e502b4027550411638bafb6a30832805. The regression test was uncommitted during the failing run and was saved in a separate test-only commit (5538842b53ca6b7fd12225f29a2d77570afd5d37) before any production code repairs. | python -m pytest tests/test_regressions.py::test_f8_01_practitioner_conflict_regression -v from project/. | 1 failed in 0.11s using Python 3.14.6 and pytest 9.2.0. The test failed at tests/test_regressions.py:37 with Failed: DID NOT RAISE ValueError. The system accepted a conflicting booking for the same practitioner instead of rejecting it, demonstrating F8-01 before repair. |
| F8-01 after repair | The one-operator repair was committed at SHA a79f2d712d33c5dbad9d895295f1c4dfd89522c5. I ran the tests after applying the same code change and before creating the commit. The Git diff confirmed that only != was changed to == in has_practitioner_conflict(). | Ran python -m pytest -q tests/test_regressions.py::test_f8_01_practitioner_conflict_regression and python -m pytest -q -k "booking_rejects_practitioner_time_conflict or conflict_rule_and_different_practitioner" from project/. | The new regression test passed (1 passed in 0.01s), and both original F8-01 tests passed (2 passed, 47 deselected in 0.03s). This confirms that conflicting bookings are rejected, existing appointments remain unchanged, and different practitioners can still be booked at the same time. The full suite returned 45 passed, 4 failed in 0.14s, with all remaining failures belonging to the unrepaired F8-02 defect. |
| F8-02 before repair | Faulty production code at SHA c45aa1c2e502b4027550411638bafb6a30832805. The regression test was uncommitted during the failing run and was saved in a separate test-only commit (5538842b53ca6b7fd12225f29a2d77570afd5d37) before any production code repairs. | python -m pytest tests/test_regressions.py::test_f8_02_cancelled_history_regression -v from project/. | 1 failed in 0.11s using Python 3.14.6 and pytest 9.2.0. The test failed at tests/test_regressions.py:64 because store.find_appointment("A001") returned None instead of the original appointment. The appointment remained in list_appointments() with CANCELLED status, confirming that the defect involves appointment lookup rather than deletion. |
| F8-02 after repair | The repair was committed at SHA c57312d93696542068b6d23a92617cfd68558364. I ran the tests after applying the same code change and before creating the commit. The Git diff confirmed that only the cancelled-status filter was removed from find_appointment(), while the blank-ID validation remained. | Ran python -m pytest -q tests/test_regressions.py::test_f8_02_cancelled_history_regression and python -m pytest -q -k "cancel_appointment_retains_record_and_changes_status or cancelling_again_raises_value_error_and_preserves_state or cancelled_slot_can_be_booked_again" from project/. | The new regression test passed (1 passed in 0.01s), and all three original F8-02 tests passed (3 passed, 46 deselected in 0.02s). This confirms that cancelled appointments remain retrievable, repeated cancellation raises ValueError, and cancelled time slots can be booked again. The full test suite also passed with 49 tests in 0.05s, with no failures. |
| Full suite after both repairs, before refactor | Both repairs were applied, with F8-01 committed at a79f2d712d33c5dbad9d895295f1c4dfd89522c5 and F8-02 subsequently committed at c57312d93696542068b6d23a92617cfd68558364. The test ran after both repairs were applied, before the F8-02 commit, and before any refactoring. | python -m pytest -q from project/. | 49 passed in 0.05s, with no failures. This confirms that both repairs work together and provides the passing baseline for the upcoming refactoring. |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: The F8-01 regression test checks that booking a second appointment for the same practitioner at the same time raises ValueError. This detects the original fault where the conflicting booking was incorrectly accepted. It also checks that the original appointment remains unchanged, the rejected appointment is not stored, and a different practitioner can still be booked at the same time. These assertions help ensure that fixing the conflict check does not affect valid bookings or existing records. 

The F8-02 regression test checks that cancelling an appointment changes its status to CANCELLED while keeping the original appointment in the datastore. It then checks that both the datastore and service can still retrieve the same appointment by its ID. This detects the original fault where cancelled appointments were excluded from lookup. The test also checks that cancelling the same appointment again raises ValueError without changing its status. Together, these assertions protect the required cancellation behaviour and help detect if either defect is reintroduced during future changes.

Unrelated failures investigated / resolution: Not applicable. No unrelated test failures were identified during Stage 8 debugging. Before either repair, the failing tests were associated with the two injected defects, F8-01 and F8-02. After repairing F8-01, the full test suite returned 45 passed, 4 failed, with all four remaining failures related to the unrepaired F8-02 defect. After repairing F8-02, the full suite returned 49 passed in 0.05s, with no failures. No unrelated production-code changes were needed.

## H. Refactoring decision and before/after verification

Smell and exact location: A magic string was identified in SmartCareDataStore.has_practitioner_conflict() in project/smartcare/data_store.py. The method uses appointment.status.value == "scheduled" to check whether an existing appointment is scheduled. This hardcoded string is a code smell because the project already has an AppointmentStatus enum to represent appointment statuses. Using a string instead of the existing enum makes the condition inconsistent with the rest of the application and could lead to mistakes if the status values change later.

Small proposed structural change / why justified: I plan to replace the hardcoded status comparison appointment.status.value == "scheduled" in SmartCareDataStore.has_practitioner_conflict() with appointment.status is AppointmentStatus.SCHEDULED, using the existing AppointmentStatus enum. This is a small refactoring that improves readability and consistency without changing how practitioner booking conflicts are detected. Using the enum also avoids relying on a manually typed status string when the project already defines appointment statuses in one place. The existing booking rules, appointment ID exclusion, date and time comparison, and cancellation behaviour will remain unchanged. No new features or modules are needed.

External behaviour to preserve / relevant tests: The refactoring must preserve the existing practitioner booking conflict rules in FR-05, AC-04.1, and AC-04.2. Two scheduled appointments for the same practitioner on the same date and time must still be rejected with ValueError, while different practitioners must still be allowed to have appointments at the same time. Rejected bookings must not change existing appointment records. The conflict check must also continue to ignore cancelled appointments so their time slots can be booked again. Cancelled appointments must remain stored and retrievable, and cancelling the same appointment twice must still raise ValueError. The F8-01 regression test, F8-02 regression test and existing service tests will check these behaviours. The full suite of 49 tests must also pass after refactoring, consistent with the passing result recorded before the change. No new functionality or changes to expected behaviour are intended.

Before result: see G, full passing suite.

Actual change / diff / separate refactor SHA: I replaced the hardcoded comparison appointment.status.value == "scheduled" with appointment.status is AppointmentStatus.SCHEDULED in SmartCareDataStore.has_practitioner_conflict() in project/smartcare/data_store.py. The AppointmentStatus enum was already imported, so no import changes were needed. The Git diff confirmed that only this one line was changed. The practitioner ID comparison, appointment ID exclusion, date and time comparison, and all other production code were left unchanged. The refactoring was committed separately on debug/stage8-repairs at SHA cf2f4fcf4f1cac9c5947abbc7a211336f58539c7 (Stage 8 refactor appointment status comparison to enum).

Focused and full after-refactor commands / working directory / results / evidence: Before refactoring, I ran python -m pytest -q from project/, which returned 49 passed in 0.05s. After replacing the hardcoded status comparison with AppointmentStatus.SCHEDULED, I ran python -m py_compile smartcare/data_store.py from project/, which completed without errors. I then reran the full test suite using python -m pytest -q from project/, which again returned 49 passed in 0.05s, with no failures. This included the F8-01 and F8-02 regression tests and the existing SmartCare tests. The Git diff also confirmed that the refactor changed only the status comparison. The tests were run before the separate refactoring commit cf2f4fcf4f1cac9c5947abbc7a211336f58539c7 was created. The full passing suite provides evidence that the refactor preserved the behaviour covered by the tests. No separate focused test command was run after refactoring.

Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: The refactoring was accepted because it removed the hardcoded "scheduled" string and used the existing AppointmentStatus.SCHEDULED enum instead, making the condition clearer and more consistent with the rest of the project. The Git diff confirmed that only the status comparison was changed, with no changes to the booking rules or other production code. The full test suite passed both before and after refactoring (49 passed in 0.05s each time). This included regression tests for F8-01 and F8-02, which confirmed the repaired booking conflict and cancellation behaviours were still working. Based on the passing tests and the limited code change, the refactoring preserved the existing behaviour covered by the test suite. No further changes were needed.

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: Three GitHub issues were created to document the two Stage 8 defects and the separate refactoring decision.
- F8-01 (Practitioner booking conflict): GitHub Issue #5. Covers the incorrect practitioner ID comparison, expected booking-conflict behaviour, minimal repair, and regression verification. Alex Marek completed the repair in commit a79f2d712d33c5dbad9d895295f1c4dfd89522c5.
- F8-02 (Cancelled appointment lookup): GitHub Issue #6. Covers the cancelled-status lookup filter, retained appointment history, minimal repair and regression verification. Repair completed by Alex in commit c57312d93696542068b6d23a92617cfd68558364.
- Refactoring (Appointment status comparison): GitHub Issue #7. Covers replacing the hardcoded "scheduled" string with AppointmentStatus.SCHEDULED whilst preserving existing behaviour. Refactoring completed by Alex Marek in commit cf2f4fcf4f1cac9c5947abbc7a211336f58539c7.

All three changes were completed on debug/stage8-repairs and included in Pull Request #8. Kreesha independently reviewed and approved the pull request without requesting changes. It was then merged into main at commit 7d8c533f4912ba1c0bd4775385f80805b9ab32e2.

Branch / prepared, repair and refactor checkpoints: The controlled Stage 8 faults were introduced on debug/stage8 in commit 27445c702a5c32c3922f94f4239768e481b60d5c, as documented in Section B. The debugging work was then completed on debug/stage8-repairs. The F8-01 and F8-02 regression tests were saved first in commit 5538842b53ca6b7fd12225f29a2d77570afd5d37. The F8-01 practitioner conflict repair was committed separately at a79f2d712d33c5dbad9d895295f1c4dfd89522c5 (Section C), followed by the F8-02 cancelled appointment lookup repair at c57312d93696542068b6d23a92617cfd68558364 (Section D). After both repairs passed the full test suite, I committed the behaviour-preserving status comparison refactor at cf2f4fcf4f1cac9c5947abbc7a211336f58539c7 (Section H). The assessment record and Copilot evidence were then committed separately as d338751. These changes were pushed to GitHub and submitted for independent review through Pull Request #8.

PR link and another member's reviewer identity: GitHub Pull Request #8 was created from debug/stage8-repairs into main to submit the two defect repairs, regression tests, and behaviour-preserving refactoring for independent review. I requested a review from Kreesha, who later approved it on GitHub.

Key human feedback, difference from Copilot findings and response/outcome: No feedback was given from Kreesha.

Actual review approval / merge evidence: Kreesha approved the changes on github through Pull Request #8. The merge commit is 7d8c533f4912ba1c0bd4775385f80805b9ab32e2.

Integrated code SHA and team pull/retest command / working directory / result: Pull Request #8 was merged into main at commit 7d8c533f4912ba1c0bd4775385f80805b9ab32e2. I verified the merge using git fetch origin main and git log -1 --format="%H%n%s%n%P" origin/main, which confirmed that the merge included the debug/stage8-repairs branch. To verify the integrated code without affecting my existing working branch, I created a separate Git worktree using git worktree add --detach ../smartcare-stage8-main-check origin/main. I then ran python -m pytest -q from smartcare-stage8-main-check/project/, which returned 49 passed in 0.09s, with no failures. This confirms that the full test suite still passes on the merged main code.

Evidence-only later SHA / explanation if different: 76ee2957e65af91c46ea10ad2defd12272802a6d. This commit was made after the pull request had already been merged, so it was not included in the original merge. It does not change the production code or tests. The final documentation will be integrated into main separately.

Each member's substantive contribution and artefact: Alex investigated both Stage 8 defects, recorded the human-first hypotheses, consulted and evaluated GitHub Copilot, wrote the F8-01 and F8-02 regression tests, completed both minimal repairs, and carried out the behaviour-preserving refactoring. These contributions are recorded in project/tests/test_regressions.py, project/smartcare/data_store.py, the separate Git commits, and Sections C-H of this assessment record. Kreesha Singh participated in the controlled fault-injection preparation during class, with the prepared code recorded in commit 27445c702a5c32c3922f94f4239768e481b60d5c. She also independently reviewed and approved Pull Request #8, which contains the completed debugging work. Her approval is recorded in the pull request's review history.

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? 

None of Copilot's incorrect diagnoses was particularly convincing once I compared them with the actual code and test results. However, one suggestion that originally seemed possible was that cancelling an appointment might be removing it from the datastore. This could have explained why the appointment could no longer be found using its ID.

After checking the F8-02 regression test, I found that the original appointment was still present in list_appointments() with CANCELLED status. This contradicted the suggestion that the record had been removed. Further inspection showed that find_appointment() was filtering out cancelled appointments instead.

This showed me why Copilot's suggestions should be treated as possible explanations rather than confirmed answers. Even when a suggestion sounds reasonable, it still needs to be checked against the requirements, source code and actual test results before deciding what to fix.

2. What evidence changed your group's view?

The most useful evidence came from comparing the failing tests with the actual code and the original Stage 8 fault-injection Git diff. For F8-01, I initially suspected that the practitioner ID comparison was incorrect, but also considered whether the booking service was passing the wrong arguments. Inspecting book_appointment() showed the service called the conflict check correctly, while the Git diff confirmed the practitioner comparison changed from == to !=.

For F8-02, I considered whether cancellation was removing the appointment from the datastore. However, the regression test showed that the cancelled appointment was still stored in list_appointments(). Inspecting find_appointment() then showed that the cancelled-status condition was preventing it from being retrieved.

The results helped narrow down the causes of both failures. After applying the two minimal repairs, all 49 tests passed, confirming that the changes resolved the observed problems without breaking the behaviour covered by the existing tests.

3. How did regression tests protect the refactoring? 

The regression tests helped ensure that the two defects we repaired were not accidentally reintroduced during refactoring. Before changing the code, I ran the full test suite and confirmed that all 49 tests passed.

The refactoring involved replacing the hardcoded "scheduled" string with the existing AppointmentStatus.SCHEDULED enum in has_practitioner_conflict(). Although this was only a small change, it was important to check that the booking and cancellation rules still worked correctly.

The F8-01 regression test checked that conflicting bookings for the same practitioner were rejected, while different practitioners could still be booked at the same time. The F8-02 regression test checked that cancelled appointments remained retrievable and that repeated cancellation raised ValueError.

After the refactoring, I ran the full test suite again, and all 49 tests passed in 0.05 seconds, consistent with the result before the change. This showed that the refactoring preserved the existing behaviour covered by the tests and did not reintroduce either defect.

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: 

Before changing any code, an engineer should first reproduce the failure and compare the expected and observed behaviour against the requirements. They should inspect the failing tests, traceback and relevant source code to identify possible causes, then check each hypothesis against the available evidence. Once the root cause has been identified, a regression test should demonstrate the failure before applying the smallest necessary repair. This reduces the risk of changing working code or introducing additional defects.

2. Where should expected behaviour come from during debugging?

Response:

Expected behaviour should come from the project's documented requirements and acceptance criteria, instead of assumptions about how the program should work. These provide a reliable reference for deciding whether the problem is in the production code or the test itself.

3. What is a debugging hypothesis?

Response: 

A debugging hypothesis is a possible explanation for why a program is behaving incorrectly. It is not a confirmed cause, so you must test it against evidence such as failing tests, source code, and runtime results.

4. What is a regression test and why is it retained?

Response: 

A regression test checks that a specific defect has been fixed and does not return after future code changes. It reproduces the original failure and checks that the program now behaves as required. Regression tests are retained in the test suite so they continue running alongside existing tests. This helps detect if a later repair, refactoring or new feature accidentally reintroduces the same problem. 

5. What is meant by root cause?

Response: 

The root cause is the underlying problem in the code or system that is responsible for an observed failure. It is different from a symptom, which only shows how the problem affects the program. Finding the root cause lets a developer fix the defect itself rather than just its effects.

6. What is refactoring?

Response: 

Refactoring is the process of improving the internal structure, readability or maintainability of existing code without changing its external behaviour. Unlike defect repair or adding a new feature, refactoring should not change what the program does.

7. What is a swallowed exception?

Response: 

A swallowed exception occurs when a program catches an exception but does not properly handle it, report it or allow it to propagate. This can hide errors and make debugging more difficult because the program may continue running without clearly indicating that something went wrong.

8. What is a code smell?

Response: 

A code smell is a sign that part of a program could be improved because its structure, readability or maintainability is not ideal. It doesn't necessarily mean the code is incorrect, but it may make the program harder to understand, modify, or maintain in the future.

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: 

GitHub Copilot-generated debugging diagnoses should be treated as suggestions or possible explanations rather than confirmed causes. Although Copilot can help detect potential problems, its suggestions may be incorrect or unsupported by the actual code and test results. An engineer should independently evaluate each suggestion by comparing it against the project requirements, inspecting the relevant source code and checking the available testing evidence. For example, during Stage 8, Copilot correctly identified the practitioner ID comparison and cancelled-status filter as the most likely causes of the two defects. However, I also investigated and rejected its alternative suggestions when the evidence did not support them. This showed me that Copilot can be useful during debugging. Still, the final diagnosis and repair decisions should be based on verified evidence and human judgement rather than simply accepting its responses.

10. What is the Stage 8 engineering rule?

Response: 

The Stage 8 engineering rule is to diagnose before fixing. Engineers should first reproduce the failure, understand the expected behaviour from the requirements, form hypotheses, and investigate the evidence before changing the code. Once the root cause is confirmed, make the smallest justified repair and verify it with regression tests. Refactor only when the tests are passing, and run the same tests afterwards to confirm existing behaviour has not changed. Any changes should also be independently reviewed before being merged and verified in the shared project. This ensures debugging decisions are based on evidence instead of assumptions or unverified AI suggestions.

## L. Completion and handover

- [x] Existing project, earlier tests and stage records preserved.
- [x] Passing Stage 7 SHA and safe preparation details recorded.
- [x] Both defects reproduced with meaningful failing tests.
- [x] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [x] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [x] One genuine refactor verified under passing before/after tests.
- [x] Human PR review, feedback resolution and integrated retest recorded.
- [x] Tutorial, three reflections and ten formative responses complete.
- [x] Local recovery metadata excluded from submitted source.
- [x] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: The verified integrated Stage 8 code is at commit 7d8c533f4912ba1c0bd4775385f80805b9ab32e2 on main, following the merge of Pull Request #8. I verified the merge using Git and created a separate worktree to test the integrated code without affecting the original debugging branch. I ran python -m pytest -q from smartcare-stage8-main-check/project/, which returned 49 passed in 0.09s, with no failures. This confirms that both Stage 8 repairs, the retained regression tests, and the refactoring are working in the merged project.

Submitted SHA and evidence-only difference if any: The Stage 8 code was integrated and verified on main at commit 7d8c533f4912ba1c0bd4775385f80805b9ab32e2, with all 49 tests passing. The final documentation updates were then merged through Pull Request #9 at commit 7cc820a54f64c7849a69a753d8fe8a3dc28a7918.

Unresolved issues or incomplete checks / owner / next action: No unresolved issues or incomplete checks. Kreesha approved the changes on github, and the pull request was merged. Alex is the owner. Next action is to finalise and commit the Stage 8 documentation, then push the changes to github.

Handover note: Everything is complete for Stage 8. The two defects were diagnosed, repaired, and verified with regression tests. A small refactoring was applied to improve code clarity without changing behaviour. The full test suite passed before and after the repairs and refactoring. All changes were independently reviewed and merged into main. The project is ready for Stage 9.