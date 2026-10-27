# Stage 7 Testing and Verification Record

Group/tutorial: [complete]  Members/cohorts: [complete]
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test                                                | Negative test | Key assertion |
|---|--------------------------------------------------------------|--|--|
| FR-01 Register patient | Register a patient with a new ID and a valid name.           | Attempt to register another patient using an existing ID | The new patient is stored and can be found. A duplicate ID raises ValueError and does not replace the original patient. |
| FR-05 Prevent practitioner conflict | Book an appointment when the practitioner has no booking at that time. | Attempt to book a second appointment with the same practitioner at the same date and time. | The first booking succeeds; the conflicting booking raises ValueError, and the original booking remains unchanged. |
| FR-06 Cancel appointment | Cancel an appointment whose status is SCHEDULED                                                             | Attempt to cancel an appointment that is already cancelled or has status COMPLETED. | A successful cancellation changes the status to CANCELLED. An invalid cancellation raises ValueError and leaves the status unchanged. |
| FR-07 Retain cancelled history | Cancel an appointment and look it up using its original ID.                                                             | Attempt to cancel the same appointment a second time. | The original appointment remains in the store with its ID, patient, practitioner and date/time unchanged. A repeated cancellation raises ValueError without deleting the record. |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: [Weak/unclear]  Why: Always passes and does not check any SmartCare behaviour.

`assert appointment is not None`
Judgement: [Weak/unclear]  Why: Checks that an object exists, but not whether it is the correct appointment or has the correct status.

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: [Strong for the cancellation-status behaviour]  Why: Confirms that the appointment has the required cancelled status. By itself, it does not prove that the record remains stored.

`assert len(results) > 0`
Judgement: [Weak/unclear]  Why: Confirms that at least one result exists, but not that the correct appointments were returned.

`assert data_store.find_appointment('A1') is appointment`
Judgement: [Strong for the stored-object identity behaviour]  Why: Confirms that looking up A1 returns the exact same object. By itself, it does not prove that its status and other fields are correct.

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract: Blank patient ID: '' - Expected Result: Raise ValueError; do not register or find a patient using a blank ID. Supporting contract: Required identifiers cannot be blank. Whitespace-only patient name: '   ' Expected Result- Raise ValueError; no patient should be registered. Supporting contract- Required text must contain non-whitespace characters. Same practitioner, same date and time, two scheduled bookings- Expected result: Reject the second booking with ValueError; preserve the original booking. Supporting contract: A practitioner cannot have two scheduled appointments at the same time. Existing appointment has been cancelled- Expected result: Allow a new appointment for the same practitioner at that time, provided there are no other conflicts. Retain the cancelled appointment. Supporting contract: Only SCHEDULED appointments cause practitioner conflicts. Attempt to cancel an already cancelled appointment- Expected result: Raise ValueError; leave it CANCELLED. Supporting contract: Only scheduled appointments may be cancelled. Attempt to cancel a completed appointment- Expected result: Raise ValueError; leave it COMPLETED. Supporting contract: Illegal appointment status transitions are rejected without changing state. Patient ID contains surrounding spaces, such as ' P1 '- Expected result: Look up the registered patient with ID P1. Supporting contract: Required text is trimmed before lookup. Patient ID is a valid but unknown ID, such as 'P999'- Expected result: A service lookup raises LookupError; it must not create a patient. Supporting contract: The patient service lookup contract.



### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|--|--|
| 1 | Checking only that an object is not None does not establish that the object is correct. | Register a patient and verify the patient's ID and name, then confirm that lookup returns the same stored object. |
| 2 | Checking only that an object exists does not prove that an appointment was cancelled correctly. | Cancel a scheduled appointment and assert that its status becomes CANCELLED. |
| 3 | assert True always passes and provides no evidence. | Attempt an illegal cancellation and verify that ValueError is raised and the original status is unchanged. |
| 4 | Assumes that SMS notifications exist, even though the supplied requirements do not establish that behaviour. | Test the documented appointment-booking result without assuming SMS notifications are implemented or required. |
| 5 | Again assumes an SMS notification requirement that is not established by the supplied contracts. | Test that a cancelled appointment remains retrievable with its original ID and unchanged appointment details. |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
100% code coverage means that the measured code was executed during testing. It does not prove that the code produced the correct results. Tests can execute every line while using weak assertions, missing important boundary cases, or failing to check the requirements. Effective verification requires meaningful tests that compare actual behaviour with expected behaviour.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| FR-01 | AC-01.1: A valid patient can be registered and stored. | B-T01 | Positive service test | `tests/test_services.py::test_register_patient_stores_patient` | The valid patient is registered and stored successfully. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-01 | AC-01.2: Duplicate patient IDs are rejected. | B-T02 | Negative service test | `tests/test_services.py::test_register_patient_rejects_duplicate_id` | Duplicate registration is rejected and the original patient is not replaced. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-01 | AC-01.2: The original patient is preserved after duplicate registration. | B-T03 | Regression test | `tests/test_starter.py::test_duplicate_patient_preserves_original` | The original patient remains unchanged after duplicate registration. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-01 | Supporting validation: Required text is trimmed and invalid text is rejected. | B-T04 | Unit test | `tests/test_domain.py::test_required_text_trims_whitespace`; `test_required_text_rejects_invalid_text` | Valid text is trimmed, and invalid text is rejected. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-01 | Supporting validation: Patient fields are trimmed and blank fields are rejected. | B-T05 | Domain test | `tests/test_domain.py::test_patient_stores_trimmed_fields`; `test_patient_rejects_blank_fields` | Patient fields are trimmed, and blank required fields are rejected. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-02 | AC-02.1: A registered patient can be found by ID. | B-T06 | Positive workflow test | `tests/test_starter.py::test_registration_and_booking` | A registered patient can be found and used in the workflow. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-02 | AC-02.2: An unknown patient ID is rejected. | B-T07 | Negative service test | `tests/test_services.py::test_find_patient_unknown_id_raises_lookup_error` | Looking up an unknown patient ID raises `LookupError`. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-02 | Supporting validation: A blank patient ID is rejected. | B-T08 | Boundary test | `tests/test_services.py::test_find_patient_blank_id_raises_value_error` | Looking up a blank patient ID raises `ValueError`. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-03 | Supporting criterion: A practitioner can be registered and found. | B-T09 | Positive service test | `tests/test_services.py::test_register_and_find_practitioner` | The registered practitioner can be retrieved using their ID. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-03 | Supporting criterion: An unknown practitioner ID is rejected. | B-T10 | Negative service test | `tests/test_services.py::test_find_practitioner_unknown_id_raises_lookup_error` | Looking up an unknown practitioner ID raises `LookupError`. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-03 | Supporting validation: A blank practitioner ID is rejected. | B-T11 | Boundary test | `tests/test_services.py::test_find_practitioner_blank_id_raises_value_error` | Looking up a blank practitioner ID raises `ValueError`. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-03 | Supporting validation: Practitioner fields are trimmed and blank fields are rejected. | B-T12 | Domain test | `tests/test_domain.py::test_practitioner_stores_trimmed_fields`; `test_practitioner_rejects_blank_fields` | Valid fields are trimmed, and blank required fields are rejected. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-03 | Supporting criterion: Duplicate practitioner registration preserves the original. | B-T13 | Regression test | `tests/test_starter.py::test_duplicate_practitioner_preserves_original` | The duplicate practitioner is rejected, and the original remains unchanged. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-04 | AC-03.1: A valid appointment can be booked with registered participants. | B-T14 | Positive service test | `tests/test_services.py::test_booking_stores_appointment_and_participant_objects` | The appointment is stored with the correct patient and practitioner objects. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-04 | AC-03.1: Registration and booking workflow succeeds. | B-T15 | Positive workflow test | `tests/test_starter.py::test_registration_and_booking` | The workflow successfully registers participants and creates an appointment. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-04 | AC-03.2: Booking with unregistered participants is rejected. | B-T16 | Negative workflow test | `tests/test_starter.py::test_unregistered_participants_rejected` | Booking is rejected if the required participants have not been registered. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-04 | Supporting validation: Appointment participants must be valid objects. | B-T17 | Negative domain test | `tests/test_domain.py::test_appointment_rejects_invalid_participant_objects` | Invalid participant objects cause `ValueError`. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-04 | Supporting criterion: Duplicate appointment registration preserves the original. | B-T18 | Regression test | `tests/test_starter.py::test_duplicate_appointment_preserves_original` | The duplicate appointment is rejected, and the original remains unchanged. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-05 | AC-04.1: The same practitioner cannot have two appointments at the same date and time. | B-T19 | Negative service test | `tests/test_services.py::test_booking_rejects_practitioner_time_conflict` | A conflicting booking is rejected, and the existing appointment is preserved. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-05 | AC-04.2: Different practitioners can have appointments at the same date and time. | B-T20 | Positive workflow test | `tests/test_starter.py::test_conflict_rule_and_different_practitioner` | Booking succeeds when the practitioner differs, even if the date and time match. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-05 | Supporting criterion: The same practitioner can be booked at a different time. | B-T21 | Positive service test | `tests/test_services.py::test_booking_allows_same_practitioner_at_different_time` | Booking succeeds when the same practitioner has a different appointment time. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-06 | AC-05.1: A scheduled appointment can be cancelled. | B-T22 | Positive domain test | `tests/test_domain.py::test_cancel_changes_scheduled_appointment_to_cancelled` | The appointment status changes from `SCHEDULED` to `CANCELLED`. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-06 | AC-05.1: Appointment cancellation works through the service. | B-T23 | Positive service test | `tests/test_services.py::test_cancel_appointment_retains_record_and_changes_status` | The service cancels the appointment and updates its status. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-06 | AC-05.3: Invalid cancellation transitions are rejected without changing status. | B-T24 | Negative domain test | `tests/test_domain.py::test_cancel_rejects_invalid_transition_without_changing_status` | An invalid transition raises `ValueError`, and the appointment status remains unchanged. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-06 | AC-05.3: Repeated cancellation is rejected without changing state. | B-T25 | Negative service test | `tests/test_services.py::test_cancelling_again_raises_value_error_and_preserves_state` | A second cancellation raises `ValueError`, and the appointment state is preserved. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-07 | AC-05.2: A cancelled appointment remains stored and retrievable. | B-T26 | Positive service test | `tests/test_services.py::test_cancel_appointment_retains_record_and_changes_status` | Cancellation changes the status but does not remove the appointment from storage. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-07 | Supporting criterion: A cancelled appointment's time slot can be booked again. | B-T27 | Positive service test | `tests/test_services.py::test_cancelled_slot_can_be_booked_again` | A new appointment can use the same practitioner's time slot after cancellation. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-08 | AC-06.1: A known appointment can be retrieved by ID. | B-T28 | Positive service test | `tests/test_services.py::test_booking_stores_appointment_and_participant_objects` | The stored appointment can be retrieved and its details checked. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-08 | Supporting validation: An unknown appointment ID is rejected. | B-T29 | Negative service test | `tests/test_services.py::test_find_appointment_unknown_id_raises_lookup_error` | Looking up an unknown appointment ID raises `LookupError`. | PASS — last recorded full-suite run: 47 passed. | Student-authored |
| FR-08 | Supporting validation: A blank appointment ID is rejected. | B-T30 | Boundary test | `tests/test_services.py::test_find_appointment_blank_id_raises_value_error` | Looking up a blank appointment ID raises `ValueError`. | PASS — last recorded full-suite run: 47 passed. | Student-authored |


## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| C-T01 | FR-01 – Register patient | AC-01.1 – A valid patient can be registered and stored. | Positive | `test_register_patient_stores_patient()` | The patient is stored successfully and can be retrieved using their patient ID. | Confirms successful registration and storage using a valid patient record. |
| C-T02 | FR-01 – Register patient | AC-01.2 – Duplicate patient IDs are rejected. | Negative | `test_register_patient_rejects_duplicate_id()` | A duplicate registration is rejected, and the original patient record remains unchanged. | Confirms duplicate IDs cannot overwrite an existing patient record. |
| C-T03 | FR-01 – Register patient | Required patient fields must contain valid text. | Boundary | `test_blank_patient_fields_are_rejected()` | Patient records with blank or whitespace-only required fields are rejected. | Checks invalid field values rather than only testing successful patient registration. |
| C-T04 | FR-02 – Find patient | AC-02.1 – A registered patient can be found using their ID. | Positive | `test_find_patient_by_id_returns_correct_patient()` | The correct patient record is returned for a registered patient ID. | Verifies that the returned record belongs to the requested patient, not just that a lookup succeeds. |
| C-T05 | FR-02 – Find patient | AC-02.2 – An unknown patient ID is rejected. | Negative | `test_unknown_patient_id_is_rejected()` | A `LookupError` is raised when the patient ID does not exist. | Confirms the system handles a lookup for a nonexistent patient correctly. |
| C-T06 | FR-02 – Find patient | A blank patient ID must not be accepted. | Boundary | `test_blank_patient_id_is_rejected()` | A `ValueError` is raised when the patient ID is blank or contains only whitespace. | Separates missing or blank input from a non-existent but otherwise valid ID. |
| C-T07 | FR-03 – Register and find practitioner | A valid practitioner can be registered and retrieved. | Positive | `test_register_and_find_practitioner()` | The registered practitioner can be found using their practitioner ID, and the returned details match the registered record. | Checks that practitioner registration and retrieval work together correctly. |
| C-T08 | FR-03 – Register and find practitioner | An unknown practitioner ID is rejected. | Negative | `test_unknown_practitioner_id_is_rejected()` | A `LookupError` is raised when the practitioner ID does not exist. | Provides evidence that unsuccessful practitioner lookups are handled appropriately. |
| C-T09 | FR-04 – Book appointment | AC-03.1 – An appointment can be booked with registered participants. | Positive | `test_booking_stores_appointment_and_participants()` | The appointment is stored with the correct patient and practitioner objects. | Confirms that the appointment connects to the correct registered participants. |
| C-T10 | FR-04 – Book appointment | AC-03.2 – An appointment cannot be booked with unregistered participants. | Negative | `test_unregistered_participants_are_rejected()` | The booking is rejected if the patient or practitioner has not been registered. | Checks that participant registration is enforced when creating a booking. |
| C-T11 | FR-04 – Book appointment | An appointment ID must not replace an existing appointment. | Negative | `test_duplicate_appointment_id_preserves_original()` | The duplicate appointment is rejected, and the original appointment remains unchanged. | Confirms that duplicate appointment IDs do not overwrite existing booking details. |
| C-T12 | FR-05 – Prevent appointment conflicts | AC-04.1 – The same practitioner cannot have conflicting appointments at the same date and time. | Negative | `test_same_practitioner_cannot_be_double_booked()` | The conflicting booking is rejected, and the existing appointment remains stored. | Checks the conflict rule for appointments involving the same practitioner. |
| C-T13 | FR-05 – Prevent appointment conflicts | AC-04.2 – Different practitioners may have appointments at the same time. | Positive | `test_different_practitioners_can_book_same_time()` | The booking succeeds when the appointments use different practitioners at the same date and time. | Confirms the conflict rule does not incorrectly prevent unrelated practitioners from being booked. |
| C-T14 | FR-05 – Prevent appointment conflicts | The same practitioner may have appointments at different times. | Positive | `test_same_practitioner_can_book_different_times()` | The booking succeeds when the existing appointment is at a different time. | Confirms that the conflict rule checks the date and time rather than blocking all additional appointments for a practitioner. |
| C-T15 | FR-06 – Cancel appointment | AC-05.1 – A scheduled appointment can be cancelled. | Positive | `test_cancel_changes_status_to_cancelled()` | The appointment status changes from `SCHEDULED` to `CANCELLED`. | Confirms the expected status transition when cancellation succeeds. |
| C-T16 | FR-06 – Cancel appointment | AC-05.3 – An invalid cancellation transition is rejected. | Negative | `test_invalid_cancellation_preserves_status()` | A `ValueError` is raised, and the appointment's original status remains unchanged. | Checks that an unsuccessful cancellation does not accidentally modify the appointment. |
| C-T17 | FR-06 – Cancel appointment | An appointment cannot be cancelled twice. | Negative | `test_repeated_cancellation_is_rejected()` | A second cancellation raises a `ValueError`, and the appointment remains in the `CANCELLED` state. | Confirms repeated cancellation is handled without changing the appointment's state incorrectly. |
| C-T18 | FR-07 – Retain cancelled appointments | AC-05.2 – A cancelled appointment remains stored and retrievable. | Positive | `test_cancelled_appointment_remains_stored()` | The cancelled appointment can still be retrieved, and its status is `CANCELLED`. | Verifies that cancellation changes the status without deleting the appointment record. |
| C-T19 | FR-07 – Retain cancelled appointments | A cancelled appointment's time slot can be reused. | Positive | `test_cancelled_slot_can_be_booked_again()` | A new appointment can be booked for the same practitioner and time after the previous appointment is cancelled. | Confirms that cancelled bookings no longer block the practitioner’s time slot. |
| C-T20 | FR-08 – Find appointment | AC-06.1 – An existing appointment can be retrieved using its ID. | Positive | `test_find_appointment_returns_correct_appointment()` | The correct appointment record is returned for a valid appointment ID. | Checks that appointment retrieval returns the requested booking's details. |
| C-T21 | FR-08 – Find appointment | An unknown appointment ID is rejected. | Negative | `test_unknown_appointment_id_is_rejected()` | A `LookupError` is raised when the appointment ID does not exist. | Confirms the system handles appointment lookups for nonexistent IDs correctly. |
| C-T22 | FR-08 – Find appointment | A blank appointment ID must not be accepted. | Boundary | `test_blank_appointment_id_is_rejected()` | A `ValueError` is raised when the appointment ID is blank or contains only whitespace. | Checks missing input separately from an unknown appointment ID. |

## D Arrange Act Assert Record

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| C-T01 | Create a valid patient with a unique patient ID and valid name and contact details. | Register the patient using the patient registration service. | Assert that the patient can be retrieved using their ID and that the stored details match the input. | Proves that valid patient information is stored correctly and can be retrieved. |
| C-T02 | Register a patient, then create another patient using the same ID but different details. | Attempt to register the second patient. | Use `pytest.raises(ValueError)` to assert that the duplicate is rejected, then check that the original patient details remain unchanged. | Proves duplicate IDs are rejected without overwriting the existing patient. |
| C-T03 | Prepare a patient record with a required field containing only spaces. | Attempt to create or register the patient. | Use `pytest.raises(ValueError)` to assert that invalid blank information is rejected. | Proves whitespace-only values are not accepted as valid required information. |
| C-T04 | Register a patient with a known ID and specific details. | Search for the patient using the registered ID. | Assert that the returned patient has the expected ID and details. | Proves the lookup returns the correct patient record rather than simply returning any patient. |
| C-T05 | Set up the patient service without registering a patient with the requested ID. | Search for the unknown patient ID. | Use `pytest.raises(LookupError)` to assert that the lookup fails as expected. | Proves the system handles requests for nonexistent patients correctly. |
| C-T06 | Prepare the patient service and provide a blank or whitespace-only patient ID. | Attempt to find the patient using the blank ID. | Use `pytest.raises(ValueError)` to assert that the invalid ID is rejected. | Proves blank input is handled as invalid rather than treated as a normal patient lookup. |
| C-T07 | Create a valid practitioner with a unique ID and register them. | Find the practitioner using their registered ID. | Assert that the returned practitioner has the expected ID and details. | Proves practitioner registration and retrieval work correctly together. |
| C-T08 | Set up the practitioner service without registering the requested practitioner ID. | Search for the unknown practitioner ID. | Use `pytest.raises(LookupError)` to assert that the lookup fails. | Proves the system does not return a practitioner record for an unknown ID. |
| C-T09 | Register a patient and practitioner, then prepare a valid appointment with a unique appointment ID, date and time. | Book the appointment. | Assert that the appointment is stored and references the correct patient and practitioner. | Proves a valid booking is created with the correct participants. |
| C-T10 | Prepare an appointment request using a patient or practitioner who has not been registered. | Attempt to book the appointment. | Use `pytest.raises(LookupError)` to assert that the booking is rejected. | Proves the system enforces participant registration before allowing a booking. |
| C-T11 | Create and store an appointment, then prepare another appointment with the same ID but different details. | Attempt to book the second appointment. | Assert that the duplicate is rejected and the original appointment's details remain unchanged. | Proves a duplicate appointment ID cannot overwrite an existing booking. |
| C-T12 | Register the required participants and book an appointment for a practitioner at a specific date and time. Prepare another booking for the same practitioner at the same date and time. | Attempt to book the conflicting appointment. | Use `pytest.raises(ValueError)` to assert that the booking is rejected, then check that the original appointment remains stored. | Proves the system prevents a practitioner from being double-booked at the same time. |
| C-T13 | Register two different practitioners and prepare appointments for both at the same date and time, using valid participants. | Book the second appointment. | Assert that the second appointment is successfully stored. | Proves the conflict rule allows simultaneous appointments when the practitioners are different. |
| C-T14 | Register a practitioner and book an appointment at one time. Prepare another appointment for the same practitioner at a different time. | Book the second appointment. | Assert that the second appointment is successfully stored. | Proves the system allows multiple appointments for one practitioner when their times do not conflict. |
| C-T15 | Create a valid appointment in the `SCHEDULED` state. | Cancel the appointment. | Assert that the appointment status is now `CANCELLED`. | Proves a valid cancellation produces the required status change. |
| C-T16 | Create or obtain an appointment in a state that does not allow cancellation under the system's rules. | Attempt to cancel the appointment. | Use `pytest.raises(ValueError)` to assert that cancellation is rejected, then check that the status remains unchanged. | Proves an invalid state transition is rejected without corrupting the appointment state. |
| C-T17 | Create an appointment and cancel it once so its status is `CANCELLED`. | Attempt to cancel the same appointment again. | Use `pytest.raises(ValueError)` to assert that the second cancellation is rejected and confirm the status remains `CANCELLED`. | Proves repeated cancellation is handled safely and does not cause an invalid state change. |
| C-T18 | Book an appointment and cancel it. | Retrieve the appointment using its ID. | Assert that the appointment still exists and its status is `CANCELLED`. | Proves cancellation changes the status instead of deleting the appointment record. |
| C-T19 | Book an appointment for a practitioner at a particular date and time, then cancel it. Prepare a new valid appointment for the same practitioner and time. | Book the new appointment. | Assert that the new appointment is stored successfully. | Proves a cancelled appointment no longer blocks the time slot. |
| C-T20 | Book an appointment with a unique appointment ID and known details. | Find the appointment using its ID. | Assert that the returned appointment has the expected ID, date, time and participants. | Proves appointment retrieval returns the correct booking details. |
| C-T21 | Set up the appointment service without an appointment matching the requested ID. | Search for the unknown appointment ID. | Use `pytest.raises(LookupError)` to assert that the lookup fails. | Proves the system correctly handles requests for nonexistent appointments. |
| C-T22 | Prepare the appointment service and provide a blank or whitespace-only appointment ID. | Attempt to find the appointment using the blank ID. | Use `pytest.raises(ValueError)` to assert that the invalid ID is rejected. | Proves blank appointment IDs are treated as invalid input. |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| E-T01 | Patient construction trims whitespace from valid fields. | `tests/test_domain.py::test_patient_stores_trimmed_fields()` | PASS |
| E-T02 | Patient construction rejects blank or invalid required fields. | `tests/test_domain.py::test_patient_rejects_blank_fields()` | PASS |
| E-T03 | Practitioner construction trims whitespace from valid fields. | `tests/test_domain.py::test_practitioner_stores_trimmed_fields()` | PASS |
| E-T04 | Practitioner construction rejects blank or invalid required fields. | `tests/test_domain.py::test_practitioner_rejects_blank_fields()` | PASS |
| E-T05 | Required text validation trims whitespace and rejects invalid text. | `tests/test_domain.py::test_required_text_trims_whitespace()`; `test_required_text_rejects_invalid_text()` | PASS |
| E-T06 | Appointment construction uses the expected initial status. | `tests/test_domain.py::test_appointment_has_expected_default_status()` | PASS |
| E-T07 | Appointment cancellation changes its status from scheduled to cancelled. | `tests/test_domain.py::test_cancel_changes_scheduled_appointment_to_cancelled()` | PASS |
| E-T08 | Appointment cancellation rejects an illegal state transition and preserves the original status. | `tests/test_domain.py::test_cancel_rejects_invalid_transition_without_changing_status()` | PASS |
| E-T09 | Appointment construction rejects invalid patient or practitioner objects. | `tests/test_domain.py::test_appointment_rejects_invalid_participant_objects()` | PASS |
| E-T10 | Appointment date and time validation accepts valid minute-precision values. | `tests/test_domain.py::test_validate_date_time_accepts_minute_precision()` | PASS |
| E-T11 | Appointment date and time validation rejects invalid values. | `tests/test_domain.py::test_validate_date_time_rejects_invalid_values()` | PASS |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| F-T01 | Registers a valid patient and stores the patient record. | FR-01 / AC-01.1 | `tests/test_services.py::test_register_patient_stores_patient()` | PASS |
| F-T02 | Rejects duplicate patient IDs. | FR-01 / AC-01.2 | `tests/test_services.py::test_register_patient_rejects_duplicate_id()` | PASS |
| F-T03 | Rejects lookup of an unknown patient ID. | FR-02 / AC-02.2 | `tests/test_services.py::test_find_patient_unknown_id_raises_lookup_error()` | PASS |
| F-T04 | Rejects a blank patient ID during lookup. | FR-02 / Supporting validation | `tests/test_services.py::test_find_patient_blank_id_raises_value_error()` | PASS |
| F-T05 | Registers and retrieves a practitioner. | FR-03 / Practitioner registration and lookup | `tests/test_services.py::test_register_and_find_practitioner()` | PASS |
| F-T06 | Rejects lookup of an unknown practitioner ID. | FR-03 / Supporting validation | `tests/test_services.py::test_find_practitioner_unknown_id_raises_lookup_error()` | PASS |
| F-T07 | Rejects a blank practitioner ID during lookup. | FR-03 / Supporting validation | `tests/test_services.py::test_find_practitioner_blank_id_raises_value_error()` | PASS |
| F-T08 | Creates and stores an appointment with the correct participant objects. | FR-04 / AC-03.1 | `tests/test_services.py::test_booking_stores_appointment_and_participant_objects()` | PASS |
| F-T09 | Rejects an appointment that conflicts with an existing booking for the same practitioner. | FR-05 / AC-04.1 | `tests/test_services.py::test_booking_rejects_practitioner_time_conflict()` | PASS |
| F-T10 | Allows the same practitioner to have appointments at different times. | FR-05 / Conflict validation | `tests/test_services.py::test_booking_allows_same_practitioner_at_different_time()` | PASS |
| F-T11 | Cancels an appointment while retaining its record. | FR-06 and FR-07 / AC-05.1 and AC-05.2 | `tests/test_services.py::test_cancel_appointment_retains_record_and_changes_status()` | PASS |
| F-T12 | Rejects a second cancellation and preserves the appointment state. | FR-06 / AC-05.3 | `tests/test_services.py::test_cancelling_again_raises_value_error_and_preserves_state()` | PASS |
| F-T13 | Allows a cancelled appointment's time slot to be booked again. | FR-07 / Cancelled slot reuse | `tests/test_services.py::test_cancelled_slot_can_be_booked_again()` | PASS |
| F-T14 | Rejects cancellation of an unknown appointment. | FR-06 / Supporting validation | `tests/test_services.py::test_cancel_unknown_appointment_raises_lookup_error()` | PASS |
| F-T15 | Rejects lookup of an unknown appointment ID. | FR-08 / Supporting validation | `tests/test_services.py::test_find_appointment_unknown_id_raises_lookup_error()` | PASS |
| F-T16 | Rejects a blank appointment ID during lookup. | FR-08 / Supporting validation | `tests/test_services.py::test_find_appointment_blank_id_raises_value_error()` | PASS |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| Register patient | Register a second patient using an existing patient ID but different details. | Registration is rejected, and the original patient's details remain unchanged. | B-T02 |
| Validate patient fields | Provide a patient with a blank or whitespace-only required field. | A `ValueError` is raised, and no invalid patient record is created. | B-T05 |
| Find patient | Search using a blank or whitespace-only patient ID. | A `ValueError` is raised, and the datastore remains unchanged. | B-T08 |
| Find patient | Search using a valid-format patient ID that does not exist. | A `LookupError` is raised, and no patient record is created or modified. | B-T07 |
| Register practitioner | Register a second practitioner using an existing practitioner ID but different details. | Registration is rejected, and the original practitioner's details remain unchanged. | B-T13 |
| Validate practitioner fields | Provide a practitioner with a blank or whitespace-only required field. | A `ValueError` is raised, and no invalid practitioner record is created. | B-T12 |
| Find practitioner | Search using a blank or whitespace-only practitioner ID. | A `ValueError` is raised, and the datastore remains unchanged. | B-T11 |
| Find practitioner | Search using a valid-format practitioner ID that does not exist. | A `LookupError` is raised, and no practitioner record is created or modified. | B-T10 |
| Book appointment | Attempt to book an appointment with an unregistered patient or practitioner. | The booking is rejected, and no appointment is stored. | B-T16 |
| Book appointment | Attempt to create an appointment using an existing appointment ID but different details. | The duplicate booking is rejected, and the original appointment remains unchanged. | B-T18 |
| Prevent booking conflicts | Book an appointment for a practitioner who already has an appointment at the same date and time. | The conflicting booking is rejected, and the original appointment remains unchanged. | B-T19 |
| Validate appointment participants | Supply an invalid patient or practitioner object when constructing an appointment. | A `ValueError` is raised, and an invalid appointment is not created. | B-T17 |
| Cancel appointment | Attempt to cancel an appointment in a state that does not permit cancellation. | A `ValueError` is raised, and the appointment's original status remains unchanged. | B-T24 |
| Cancel appointment | Attempt to cancel an already cancelled appointment. | A `ValueError` is raised, and the appointment remains in the `CANCELLED` state. | B-T25 |
| Cancel appointment | Attempt to cancel an appointment ID that does not exist. | A `LookupError` is raised, and the datastore remains unchanged. | B-T33 |
| Find appointment | Search using a blank or whitespace-only appointment ID. | A `ValueError` is raised, and the datastore remains unchanged. | B-T30 |
| Find appointment | Search using an appointment ID that does not exist. | A `LookupError` is raised, and no appointment record is created or modified. | B-T29 |
| Validate appointment date and time | Supply an invalid date or time value. | Validation rejects the value with the expected exception, and no invalid appointment is accepted. | B-T31 |

## H GitHub Copilot Test Design

**Requirement:** FR-06 – Cancel appointment.

**Acceptance criterion:** AC-05.1 – A scheduled appointment can be cancelled, changing its status from `SCHEDULED` to `CANCELLED`.

**Behaviour to test:** Cancelling a scheduled appointment changes its status to `CANCELLED`.

**Human-first test idea/categories:** Before using Copilot, I identified a positive test to check successful cancellation and negative tests to check invalid or repeated cancellation. The tests should arrange a valid appointment, perform one cancellation action, and assert the resulting status. Negative tests should verify that invalid cancellation attempts raise the expected exception and do not change the appointment's existing state.

**Prompt and purpose:** Prompt to use with GitHub Copilot:

"Using the existing SmartCare project and its current test framework, suggest a pytest test for FR-06, acceptance criterion AC-05.1. Arrange a valid scheduled appointment, cancel it using the existing Stage 6 service, and assert that its status becomes CANCELLED. Follow the existing fixtures and project conventions. Do not invent new business rules, change production code, or add unnecessary dependencies. Explain what behaviour the assertion verifies."

**Copilot test idea/candidate:** A test that creates a scheduled appointment, cancels it through the existing service, and checks its status.

**What it claims to verify:** A valid cancellation changes the appointment status from `SCHEDULED` to `CANCELLED`.

**Requirement trace:** FR-06, AC-05.1.

**Assertion quality:** A direct assertion that the appointment's status equals `CANCELLED` checks the required observable outcome. Merely asserting that the cancellation method completes without raising an exception would be weaker because it would not prove that the status changed.

**Human critique:** The candidate is relevant because it tests the stated acceptance criterion. It should use the existing SmartCare fixtures and services rather than introducing a separate implementation or excessive mocking. The test must also use the project's actual appointment status representation and current API.

**Decision:** Modify if necessary.

**Reason:** The test idea is appropriate, but the generated code must be checked against the existing project before it is accepted. Any incorrect method names, incorrect status values, or unnecessary assumptions must be corrected. The test should not introduce requirements beyond the stated cancellation behaviour.

**Final test reference if accepted/modified:** `tests/test_services.py::test_cancel_appointment_retains_record_and_changes_status` is an existing related test in the project. It should not be described as a newly generated or modified test unless Copilot was actually used to create or change it.

**Actual verification result:** The earlier full test run reported 47 passed. This is evidence that the existing test suite passed at that time, not evidence that a new Copilot-generated test was run.
| Field | Entry |
|---|---|
| Copilot test idea/candidate | Cancel a scheduled appointment and verify its status changes to `CANCELLED`. |
| What it claims to verify | Successful cancellation follows FR-06 / AC-05.1. |
| Requirement trace | FR-06 / AC-05.1. |
| Assertion quality | Strong if it directly checks the resulting appointment status. |
| Human critique | Check compatibility with the current project API, fixtures and status representation. |
| Decision | Modify if needed; accept only after reviewing the actual candidate. |
| Reason | The idea matches the criterion, but generated code must be checked for correctness and unsupported assumptions. |
| Final test reference if accepted/modified | Existing related test: `tests/test_services.py::test_cancel_appointment_retains_record_and_changes_status`. |
| Actual verification result | Existing suite previously passed 47 tests; no new Copilot candidate has been verified in this response. |

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak?

A test that only checked whether the cancellation method completed without raising an exception looked convincing, but it did not prove that the appointment was actually cancelled.

Why was it weak?

The test did not check the required observable outcome. The cancellation method could run without an error while the appointment status remained SCHEDULED. Therefore, the test did not provide enough evidence that acceptance criterion AC-05.1 was satisfied.

How did you strengthen it?

I strengthened the test by asserting that the appointment status changed from SCHEDULED to CANCELLED after the cancellation service was called. This directly checks the behaviour required by FR-06 and AC-05.1 instead of only checking that the method executed.

Accepted / modified / rejected test decisions and evidence:

The cancellation test idea was retained but required a stronger assertion. The proposed test was considered suitable after modification because it checked the required status change. The existing related test is tests/test_services.py::test_cancel_appointment_retains_record_and_changes_status. The earlier full test run reported 47 passing tests; however, this does not independently verify a newly generated Copilot test.

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---:|---:|---|---|---|
| `python -m pytest` | `project/` | Not recorded — retrieve the SHA for the tested commit | 47 | 0 | No failures reported. | No defects reported by this test run. | Previous full test run reported `47 passed in 0.03s`. This indicates that all tests passed at that time, but the run should be repeated against the current code before submission. |

Individual test runs and changed-order independence evidence: The full test suite previously reported 47 passed and 0 failed. Individual test files can be run using python -m pytest tests/test_domain.py, python -m pytest tests/test_services.py, and python -m pytest tests/test_starter.py. Changed-order independence can be checked by running python -m pytest tests/test_services.py tests/test_domain.py tests/test_starter.py and comparing the result with the normal full-suite run. Individual and changed-order results should be recorded after running these commands.
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: FR-06 / AC-05.1 → `tests/test_services.py::test_cancel_appointment_retains_record_and_changes_status` → The previous full test run reported 47 passed and 0 failed → No defect was identified in that run → No code change recorded → Verify by rerunning `python -m pytest` after any changes and confirming the test passes.

## K What the Suite Still Does Not Prove

What does your test suite still not prove? Although all 47 tests passed in the previous test run, the suite does not prove that SmartCare works correctly in every possible situation. It may not cover every invalid input, unusual combination of appointments, large amounts of data, or unexpected user behaviour. It also does not prove that the system meets every real-world user need or that it has no defects.
Coverage if used: Not used. No code coverage measurement was recorded.
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? Important areas include unusual appointment dates and times, interactions between multiple bookings, invalid input combinations, and whether records remain unchanged after rejected operations. These areas matter because errors could cause incorrect bookings or changes to patient and appointment records. Code coverage percentage alone does not establish correctness because executing a line of code does not prove that the code produces the correct result. Assertions must check the required behaviour, and tests must cover meaningful positive, negative and boundary cases.
Optional fixtures/parametrisation used and why, if any: The existing test suite uses the setup_services fixture in tests/test_services.py to provide test service and datastore setup. This helps tests use a consistent setup and reduces repeated code. Parameterised tests are also used in tests/test_domain.py to check multiple invalid values, allowing validation behaviour to be tested across different inputs without duplicating test functions.

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| SmartCare testing and verification | `main` *(confirm this is your branch)* | N/A — no PR recorded yet | N/A — no formal review recorded yet | No formal review feedback recorded. | The existing test suite previously reported 47 passed and 0 failed. |

## M Contribution Evidence

| Member  | Actual contribution | Evidence link |
|---------|---|---|
| Kreesha | Completed Stage 7 testing and verification, including test design, documenting test evidence, mapping tests to requirements, and recording regression testing results. | [SmartCare Assignment 3 GitHub repository](https://github.com/CoolCoder49/st1--assignment-3) — Stage 7 test documentation and test files. |
| Alex    | Completed Stage 6 implementation of the SmartCare system services, providing the functionality that was tested during Stage 7. | [SmartCare Assignment 3 GitHub repository](https://github.com/CoolCoder49/st1--assignment-3) — Stage 6 implementation and service files. |

## N Formative Questions

1. What question does verification answer?
Verification answers: “Are we building the system correctly?” It checks whether the software meets its specified requirements and has been implemented correctly.

2. What question does validation answer?
Validation answers: “Are we building the right system?” It checks whether the software meets the users' needs and solves the intended problem.

3. What is a unit test?
A unit test checks one small, individual part of a program, such as a function or method, to confirm that it behaves as expected.

4. What is a pytest fixture?
A pytest fixture provides setup or test data needed by a test. For example, a fixture can create a fresh SmartCare datastore and services before a test runs.

5. What is parametrisation in pytest?
Parametrisation allows the same test function to run multiple times with different input values. This helps test different valid and invalid cases without writing a separate function for every input.

6. What is regression testing?
Regression testing reruns existing tests after changes to check that previously working functionality still works and that new changes have not introduced defects.

7. What does code coverage tell us, and what does it not prove?
Code coverage indicates which parts of the code were executed during testing. However, it does not prove that the code is correct, because executing a line does not guarantee that it produces the right result.

8. What makes an assertion weak?
An assertion is weak when it does not directly check the required behaviour. For example, checking that a function runs without an exception does not prove that an appointment's status changed to CANCELLED.

9. What is the appropriate role of GitHub Copilot as a test assistant?
GitHub Copilot can suggest test cases and help generate test code, but the developer must review its suggestions. Tests should be checked against requirements, use appropriate assertions and exceptions, and avoid invented business rules. Generated tests must be run and verified before their results are reported.

10. What is the Stage 7 engineering rule?
Tests should be based on requirements, check meaningful observable behaviour, and provide evidence that the system works correctly. Test results must be reported honestly, and existing tests should be retained and rerun to check for regressions.

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]

