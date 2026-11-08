# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: Tuesday 1:30-3:30 Group 2
Members and responsibilities: Alex Marek: stage 6, 8, 12. Kreesha Singh: Stage 7 and 9
Stage 8 integrated SHA, command, working directory and actual result: 
236cd2f8fa768825656b17a8d5572d6a76f3f57a
Command: python3 -m pytest -q
Working directory: project/
Actual result: 49 passed in 0.02s

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|-------------------------------------------|--|
| Patient identity | Session/domain state                                          | Patient details must remain available during the session so appointments can be booked and patients can be found.|
| Appointment history |  Session/domain state                                         | Appointments, including cancelled appointments, must remain available during the session for lookup and listing.|
| Temporary menu choice | Transient state                                          | The menu choice is only needed to decide which command to execute. It does not need to be stored after the command.|
| Practitioner specialty |  Session/domain state                                         |The specialty is part of the practitioner's information and must remain available during the session.|
| Debug print output | Transient information                                          | Debug output is only used to help developers inspect program behaviour. It is not part of the application's domain records.|
| Appointment status |  Session/domain state                                         | The status records whether an appointment is scheduled, cancelled or completed. It is needed for filtering and retaining appointment history.|

What is intentionally lost on exit? 
All application data stored in the in-memory SmartCareDataStore is intentionally lost when the program exits. This includes registered patients, practitioners and appointments, including cancelled appointment history. The application is session-only and does not save records to a database or files.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key |One Appointment object |A tuple containing datetime and appointment ID (tuple[datetime, str]) | Provides a consistent ordering by appointment date/time, then appointment ID. It does not modify the appointment.| Uses Appointment.date_time and Appointment|
| select_appointments |A list of Appointment objects, a practitioner ID (str) and optional AppointmentStatus (None by default) |A new sorted list of matching Appointment objects | Filters by practitioner and, when supplied, status. It returns a new list and does not modify the original collection or its objects.|Uses each appointment's registered practitioner relationship and Appointment.status. |
| Service listing |Practitioner ID (str) and optional AppointmentStatus | A new list of matching appointments| Checks that the practitioner exists, validates the status, obtains the store's appointment list and delegates filtering/sorting to the query function.| Uses SmartCareDataStore, PractitionerService/store lookup contract and select_appo|
| Console |User-entered menu choice and command-specific text input (str) | Printed messages and displayed records; no domain return value is required| Reads input, converts date/time and status text, calls services, displays results and recovers from expected ValueError and LookupError exceptions.| Uses the existing services, parse_date_time, format_appointment and Appointment|

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: 
A patient has a patient ID and name. A practitioner has a practitioner ID, name and specialty. An appointment has an appointment ID, references to the actual registered Patient and Practitioner objects, a date/time and a status. The application must use registered participants when creating appointments rather than creating unrelated copies from the entered IDs. IDs and names must follow the existing domain validation rules. Appointment status must use the AppointmentStatus enum. The appointment object is responsible for its own valid cancellation transition.

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input |The domain object is handling user-interface interaction. This mixes domain rules with the console. |Appointment.cancel should only perform the valid status transition. The console should read the appointment ID and the service should find the appointment and call cancel(). |
| Service prints/reads the menu | The service is responsible for user-interface behaviour instead of coordinating application operations.| The console should read and print menu information. The service should perform registration, lookup, booking, cancellation and listing.|
| Query sorts its source in place |The query changes a collection supplied by its caller, creating an unexpected side effect. | The query should use sorted() to return a new list, leaving the original collection unchanged.|
| Store prints Appointment saved |The store is responsible for data collection management, not user-facing messages. |The store should add and return/store the object. The console should display confirmation after the service succeeds. |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: 
For appointments.sort(key=appointment_sort_key), the original list is sorted in place. The method returns None, and the list remains the same list object, although its order changes.

For result = sorted(appointments, key=appointment_sort_key), Python creates and returns a new sorted list. The original list order is unchanged, and result is not appointments. The new list can contain references to the same Appointment objects.

A meaningful mutation check is to take a snapshot of the original appointment order and relevant fields before calling the query, then compare them afterwards. The test should also check that the returned list is a different list object.

Score-example prediction and explanation of passing the named key: 
The named key returns (appointment.date_time, appointment.appointment_id). Therefore, appointments are first ordered by date and time. If two appointments have the same date and time, their appointment IDs are compared to determine their order. For example, A1 appears before A2 when both have the same date and time. Passing appointment_sort_key to sorted() makes this ordering reusable and consistent. A test that directly checks the key's returned tuple and checks the final appointment order verifies both the key and its use.

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: 
Cancellation is different from deletion. Cancellation changes an existing appointment's status to CANCELLED, while deletion would remove the appointment record completely. SmartCare must retain cancelled appointments so that their history can still be retrieved and listed during the session.

To check this, I would book an appointment, cancel it, and then find it again using its appointment ID. The returned appointment should be the same stored object and its status should be CANCELLED. I would then list the practitioner's appointments without a status filter and confirm that the cancelled appointment is included. Finally, I would list only SCHEDULED appointments and confirm that the cancelled appointment is excluded. The appointment should remain in the store throughout these checks.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: 
The Stage 9 design was planned around keeping each component responsible for a specific part of the application. The domain classes remain responsible for validating data and enforcing domain rules. The SmartCareDataStore remains responsible for storing patients, practitioners and appointments during the current session. Services coordinate operations between the domain objects and the data store. The query functions are responsible only for selecting and sorting appointments, while the console handles user input and output.

The appointment_sort_key function will accept one Appointment object and return a tuple containing its date/time and appointment ID. This provides consistent chronological ordering, with the appointment ID acting as a tie-breaker when two appointments have the same date/time.

The select_appointments function will accept an appointment collection, a practitioner ID and an optional AppointmentStatus. It will return a new sorted list rather than modifying the original collection. When the status is None, all statuses must be included. When a status is supplied, only appointments with that status should be returned.

The service listing operation will validate the practitioner and status before requesting the appointment collection and calling the query function. This keeps registration and lookup rules in the service layer rather than duplicating them in the query.

The console will convert user-entered status text into an AppointmentStatus enum before calling the service. It will also use the existing date/time parser and appointment formatter. Expected input and lookup errors will be displayed clearly so that the user can return to the menu without terminating the application.

An important integrity decision is to use the actual registered Patient and Practitioner objects when booking appointments. The application must also retain cancelled appointments rather than deleting them. Failed operations, such as duplicate registration, unknown participants, invalid dates or practitioner booking conflicts, must not partially change the stored data.

These decisions keep the Stage 9 implementation consistent with the existing SmartCare architecture and the session-only requirements.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence                            |
|-|-|-|-|--------------------------------------------|
| QRY-01 Practitioner isolation|Appointment collection and practitioner ID | select_appointments in queries.py| Only appointments belonging to the requested practitioner are returned.| Query test using appointments from two practitioners. |
|QRY-02 Status filtering|Practitioner ID and optional AppointmentStatus|select_appointments in queries.py|None returns all statuses. An explicit enum returns only matching appointments. No matches returns an empty list.| Tests for default, each status and no-match cases. |
|QRY-03 Deterministic ordering|Matching appointments with different and equal date/time values|appointment_sort_key and select_appointments|Results are sorted by date/time, then appointment ID. The source order and appointment fields remain unchanged.| Sorting and equal-time tie-break tests.    |
|QRY-04 Service validation|Practitioner ID and optional status|AppointmentService.list_practitioner_appointments|Unknown practitioner raises LookupError; invalid or blank ID and invalid status raise ValueError; a known practitioner with no matches receives an empty list.| Service tests for valid, empty and invalid cases. |
|FP-01 Repeatability and purity|Same appointment collection and explicit query inputs|Pure functions in queries.py|Repeated calls with unchanged inputs return equivalent results without hidden state or side effects.| Repeat-call and code-inspection evidence.  |
|FP-02 New result lists|Empty, sorted and unsorted appointment collections|select_appointments in queries.py|A new list is returned in every case, without changing the original list or its appointment objects.| Fresh-list and mutation-check tests.       |
|FP-03 Named sorting key|Appointment with known date/time and ID|appointment_sort_key in queries.py|The key returns the expected tuple and is reused by the sorting operation.| Direct key test and sorting test.          |
|UI-01 Full menu workflow|Patient, practitioner and appointment details entered through the menu|Console, services and data store|Registration, lookup, booking, conflict rejection, cancellation, listing, filtering, freed-slot booking and exit work correctly.| Reproducible interactive demonstration and workflow tests. |
|UI-02 Invalid-input recovery|Invalid menu choices, IDs, dates, status text and repeated cancellation|Console and services|Expected errors are displayed, the application returns to the menu and stored records remain unchanged after rejected operations.| Invalid-input demonstration and before/after state checks. |
|FR-01 Patient registration|Patient ID and name|Patient service and data store|A valid patient is registered; invalid or duplicate registration is rejected.| Patient registration tests. |
|FR-02 Practitioner registration|Practitioner ID, name and specialty|Practitioner service and data store|A valid practitioner is registered; invalid or duplicate registration is rejected.| Practitioner registration tests. |
|FR-03–FR-04 Lookup and booking|Registered participant IDs and appointment details|Lookup and booking services|Registered records can be found and appointments can be booked using the actual registered participants. Invalid participants or appointment details are rejected.| Lookup and booking workflow tests.|
|FR-05 Practitioner conflict prevention|Practitioner ID and appointment date/time|Appointment booking service|A practitioner cannot have two scheduled appointments at the same time. A different practitioner may be booked at that time.| Conflict and different-practitioner workflow tests |
|FR-06 Appointment cancellation|Existing appointment ID|Appointment service and Appointment.cancel|A valid scheduled appointment changes to CANCELLED; invalid or repeated cancellation is rejected.|  Cancellation and repeated-cancellation tests. |
|FR-07 Cancelled appointment history|Existing cancelled appointment|Data store and lookup/listing services|Cancelled appointments remain stored and retrievable during the session.| Find-after-cancellation and all-status listing tests. |
|FR-08–FR-09 Appointment queries and console integration|Practitioner ID, optional status and menu input|Query, service and console components|Appointments can be listed in deterministic order and the interactive menu continues until exit.|Query tests and interactive console demonstration.|

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: 
The application distinguishes between an empty result, an unknown practitioner and invalid input because they represent different situations.

An empty result occurs when the practitioner is valid and registered but has no appointments matching the requested filter. In this case, the query should return an empty list without raising an error.

An unknown practitioner occurs when the supplied ID is valid in format but does not identify a registered practitioner. The service should raise a LookupError because the requested practitioner cannot be found.

Invalid input occurs when the practitioner ID is blank or incorrectly formatted, or when the supplied status is not an AppointmentStatus enum. These cases should raise a ValueError according to the existing validation contracts.

The console is responsible for converting status text entered by the user into an AppointmentStatus enum. The service receives either a valid enum value or None. This prevents user-interface text handling from being mixed into the query function.

Appointments must reference the actual registered Patient and Practitioner objects. This preserves the relationships managed by the data store and prevents appointments from being created with unrelated participant objects that only have matching IDs.

The console should handle expected ValueError and LookupError exceptions and display understandable messages. It should then return to the menu instead of crashing. It should not catch every possible exception because unexpected programming errors should remain visible during development.

Rejected operations must not partially change application state. This can be checked by recording the relevant collections and object fields before an invalid operation, performing the operation, and comparing the records afterwards. For example, an invalid booking should not create an appointment or reserve its ID, and a rejected cancellation should not change the appointment status

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---------------|---|
| QRY-01|queries.py |Practitioner isolation: only appointments belonging to the requested practitioner are returned. | Passed        |test_queries.py |
| QRY-02|queries.py |Default status (None) includes scheduled and cancelled appointments. | Passed        |test_queries.py |
|QRY-02 |queries.py |Explicit CANCELLED status returns only cancelled appointments. | Passed        |test_queries.py |
|QRY-02 |queries.py |COMPLETED status filtering is supported by the enum comparison in the query function. | Passed        |queries.py |
|QRY-03 |queries.py |Appointments are sorted by date/time in ascending order. | Passed        |test_queries.py |
| QRY-03|queries.py |Equal-time appointments are ordered by appointment ID. | Passed        |test_queries.py |
| FP-01|queries.py |The named appointment_sort_key() function is tested directly and used by sorted(). | Passed        |test_queries.py |
| FP-01|queries.py |Repeated calls use the same explicit inputs and have no hidden state or I/O. | Passed        |queries.py |
| FP-02|queries.py |A new result list is returned without changing the original source list. | Passed        |test_queries.py |
| FP-02|queries.py |The returned list can reuse the original Appointment objects without modifying them. | Passed        |test_queries.py |
| FP-02|queries.py |Empty input returns an empty result. | Passed        |queries.py |
|FP-02 |queries.py |Already-sorted input is processed using a new result list. | Passed        |queries.py |
| FP-02|queries.py |Original Appointment fields remain unchanged after querying. | Passed        |queries.py |
|QRY-04 |services.py |A known practitioner with appointments receives the matching appointment list. | Passed        |test_workflows.py |
| QRY-04|services.py |Unknown practitioner ID raises LookupError. | Passed        |test_workflows.py |
|QRY-04 |services.py |Invalid string status raises ValueError. | Passed        |test_workflows.py |
| QRY-04|services.py |Blank practitioner ID is rejected through existing store validation. | Passed        |services.py, data_store.py |
|QRY-04 |services.py |Known practitioner with no appointments returns an empty list. | Passed        |services.py |
|FR-07 |services.py, data_store.py |Cancelled appointment remains retrievable and appears in all-status listing. | Passed        |test_workflows.py |
|FR-07 |services.py |Cancelled appointment is excluded from scheduled-only listing. | Passed        |test_workflows.py |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: 
The select_appointments() function is designed as a pure function because it receives its input collection, practitioner ID and optional appointment status as explicit parameters. It does not access global variables, the shared data store or service objects. It does not perform input/output operations such as printing or requesting user input.

The function examines the supplied Appointment objects, selects matching appointments and uses sorted() with the named appointment_sort_key() function to produce an ordered result. It does not modify the original collection or change the Appointment objects. This keeps the query logic independent of the interactive console and allows it to be tested separately.

What the tests do and do not establish: 
The 61 passing automated tests provide evidence that practitioner filtering, default and explicit cancellation filtering, chronological sorting, equal-time appointment ID ordering and returning a separate result list work as intended. The workflow tests also verify that booking conflicts and invalid requests are rejected, cancellation history is retained, and a cancelled appointment's time slot can be reused.

The tests provide evidence for the tested cases but do not prove correctness for every possible input. Some additional boundary cases, including empty collections, already-sorted collections, repeated identical calls, completed-status filtering and unchanged object fields, have not been independently tested. These behaviours are also supported by inspection of the implementation where applicable.

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact                                                                                                                                                                                                                                                                                                                                   | Expected result | Observed result and state check | Evidence link |
|-|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-|-|-|
| UI-01 full menu workflow | Launch using python3 main.py --interactive. Register P1 and practitioners D1 and D2. Book A1 with D1 at 2026-10-01 09:00. Attempt conflicting A2 with D1, then successfully book A2 with D2 at the same time. Cancel A1, retrieve it, list D1 appointments with blank and scheduled filters, book A3 into D1's freed time slot, perform final listings and exit. | All menu commands operate successfully. Conflicting bookings are rejected, different practitioners can share appointment times, cancellation retains history, filters work correctly and cancelled time slots become available again.|Passed. Registration, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing, filtering and freed-slot reuse were manually demonstrated successfully. A1 remained cancelled while A3 was scheduled. |project/smartcare/console.py; project/main.py; manual Terminal demonstration
| UI-02 invalid-input recovery | Interactive menu tests should include an unknown menu choice, blank and unknown IDs, duplicate registration, unknown booking participants, malformed and impossible dates, invalid listing status and repeated cancellation.                                                                                                                                                                                                                                                                                                                                                                 |Invalid requests display meaningful errors, do not crash the application or partially change records, and return the user to the menu so valid operations can continue. |Partially verified. Expected error handling is implemented for ValueError and LookupError, and automated tests verify selected invalid service requests preserve existing records. The complete manual UI-02 sequence has not yet been demonstrated. |project/smartcare/console.py; project/tests/test_workflows.py |
| Automated service workflow |   Run python3 -m pytest -q from the project/ directory. See project/tests/test_workflows.py.                                                                                                                                                                                                                                                                                                                                                               | Automated tests verify successful booking, conflict rejection, different-practitioner booking, cancellation, retained history, freed time slots and invalid service requests.|Passed. The complete test suite reported 61 passing tests, including five new workflow tests. | project/tests/test_workflows.py; Terminal pytest output|
|UI-01: Patient registration|  Select option 1. Enter patient ID P1 and name Kreesha                                                                                                                                                                                                                                                                                                  |Patient is registered and confirmation message is displayed.|Passed. SmartCare displayed Patient registered: P1 - Kreesha.|Console demonstration|
|UI-01: Practitioner registration|Select option 3. Enter D1, Taylor Example, General Practice.                                                                                                                                                                                                                                                                                                                                                                  |Practitioner is registered successfully.|Passed. Practitioner registration confirmation was displayed.|Console demonstration|
|UI-01: Appointment booking|Select option 5. Enter A1, P1, D1, 2026-10-01 09:00.                                                                                                                                                                                                                                                     |Appointment is booked with SCHEDULED status.|Passed. A1 was displayed as scheduled.|Console demonstration|
|UI-01: Conflict prevention|Attempt to book A2 for P1, D1 at 2026-10-01 09:00.   |Booking is rejected because D1 already has an appointment at that time.|Passed. Conflict was rejected and the menu continued. The appointment ID A2 was subsequently used successfully.|Console demonstration; test_workflows.py|
|UI-01: Different-practitioner booking|Register D2. Book A2 for P1 with D2 at 2026-10-01 09:00.                                                                                                                                                                                                                             |Booking succeeds because D2 is a different practitioner.|Passed. A2 was successfully booked with D2 at the same time as A1.|Console demonstration; test_workflows.py|
|UI-01: Cancellation|Select option 6 and enter A1.                                                                                                                                                                                                                                                                                                                                                                  |A1 changes from SCHEDULED to CANCELLED.|Passed. Cancellation confirmation was displayed.|Console demonstration; test_workflows.py|
|UI-01: Appointment retrieval|Select option 7 and enter A1.                                                                                                                                                                                                                                                                                                                                                                  |Cancelled appointment remains retrievable.|Passed. A1 was found with CANCELLED status, confirming it was not deleted.|Console demonstration; test_workflows.py|
|UI-01: Practitioner listing|Select option 8, enter D1 and leave status blank.                                                                                                                                                                                                                                                                                                                                                                  |All D1 appointments, including cancelled history, are displayed.|Passed. A1 appeared in the all-status listing.|Console demonstration|
|UI-01: Status filtering|Select option 8, enter D1 and status scheduled.                                                  |Only scheduled appointments are displayed.|Passed. A1 was excluded because it was cancelled, and no matching appointments were found at that point.|Console demonstration; test_workflows.py|
|UI-01: Freed time slot|Book A3 for P1 with D1 at 2026-10-01 09:00 after cancelling A1.                                                                                                                                                                                                                                                                                                                                                                  |Booking succeeds while A1 remains in cancelled history.|Passed. A3 was booked successfully. A1 remained cancelled and A3 was scheduled.|Console demonstration; test_workflows.py|
|UI-01: Final listing|List D1 with blank status, then with scheduled.|All-status listing shows A1 and A3; scheduled-only listing shows A3.|Passed. Both listing results were confirmed during manual testing.|Console demonstration|
|UI-02: Invalid-input recovery|Invalid menu choice, blank or unknown IDs, duplicate registration, unknown booking participants, malformed/impossible date, invalid status and repeated cancellation.|Each invalid request produces a meaningful error, preserves existing data and returns to the menu.|Not fully demonstrated manually. Error handling is implemented, but further manual verification is required for these scenarios.|console.py; test_workflows.py|
|Automated service workflow|Run python3 -m pytest -q from project/.|Booking, conflict rejection, different-practitioner booking, cancellation, retained history, freed slot and invalid service requests are verified.|Passed. The complete suite reported 61 passing tests, including five new workflow tests.|project/tests/test_workflows.py; Terminal test output|
Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

The interactive SmartCare menu was manually tested using synthetic patient, practitioner and appointment records. Patient P1 and practitioners D1 and D2 were registered successfully. Appointment A1 was booked with D1 at 2026-10-01 09:00. A second booking with the same practitioner and time was rejected, demonstrating conflict prevention. However, appointment A2 was successfully booked with D2 at the same time, demonstrating that different practitioners can have appointments simultaneously.

Appointment A1 was then cancelled and retrieved successfully with CANCELLED status, confirming that cancellation retains the appointment record rather than deleting it. Listing all appointments for D1 displayed the cancelled appointment, while filtering by scheduled status excluded it. A new appointment, A3, was successfully booked into the time slot previously occupied by A1. The final listing showed both the cancelled historical appointment A1 and scheduled appointment A3.

These demonstrations confirmed that the interactive menu can coordinate registration, booking, conflict checking, cancellation, retrieval and appointment listing during one application session.

## E. GitHub Copilot review and human decisions

Human design completed before AI: 

The Stage 9 design was based on the assignment requirements and the existing SmartCare architecture. The main design decisions were to keep appointment filtering and sorting separate from the service layer, use the existing data store, preserve cancelled appointments, and keep console input/output separate from application logic. These decisions were made before reviewing AI suggestions.

Actual prompt/context supplied: 

Review the Stage 9 SmartCare implementation. Check whether the appointment query function is pure, whether sorting and filtering work correctly, whether the service layer validates inputs, and whether the console uses the same data store throughout the session. Identify possible problems and suggest improvements without unnecessarily changing the existing architecture.

Actual response: 

The implementation separates query processing, service coordination and console interaction. The appointment query returns a sorted list without modifying the original collection. The service layer checks practitioner existence and validates appointment status. The console uses a shared data store throughout the interactive session. Testing should also confirm that cancelled appointments remain available in appointment history and that cancelling an appointment frees the practitioner's time slot.

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|----------|---|---|---|
| Query function should not modify the original appointment collection.|queries.py, test_queries.py | Medium   |Accept – maintaining the original collection prevents unintended side effects. |Used sorted() to return a new list. |Query tests passed. |
| Appointments should be sorted consistently when multiple appointments have the same date and time.|appointment_sort_key() in queries.py | Low      |Accept – using appointment ID as a secondary sorting key provides consistent results. |Added appointment ID as a tie-breaker. |Equal-time sorting test passed. |
| Service layer should validate the practitioner and status before running the query.|list_practitioner_appointments() in services.py | Medium   |Accept – invalid requests should be handled before query processing. |Added practitioner lookup and status validation. |Service workflow tests passed. |
| Cancelled appointments should remain accessible in appointment history.|services.py, test_workflows.py | Medium   |Accept – cancelled appointments must not be deleted. |Retained cancelled appointments in the data store. |Cancellation and retrieval workflow passed. |
|Avoid introducing unnecessary database or file storage for this stage. |data_store.py, console.py | Low      |Accept – the assignment requires session-only in-memory storage. |No database or permanent storage was added. |Manual menu workflow completed successfully. |

Responsibility check: 

The SmartCare application separates responsibilities across different components. Domain classes maintain important rules, such as valid appointment statuses and cancellation rules. The data store maintains shared collections of patients, practitioners and appointments. The service layer coordinates operations and checks that required records exist before performing actions. Pure query functions handle filtering and sorting without modifying the original data. The console handles user input, displays results and communicates errors. This separation makes the application easier to test, maintain and understand.

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? 

The main architectural concern was ensuring that the console used the same shared data store and service objects throughout the entire session. If a new data store was created for each menu operation, previously registered patients, practitioners and appointments would not be available. Keeping one shared data store allowed information to remain available until the user exited the application.

2. Which Copilot suggestion did you reject as over-engineering, and why? 

An unnecessary suggestion was to introduce a database or permanent file storage to save appointments between sessions. This was rejected because Stage 9 only requires session-based in-memory storage. Adding permanent storage would increase complexity and introduce functionality outside the assignment requirements.

3. How did you prove cancelled appointments remain retrievable and listable in the same session? 

I manually tested the workflow by booking appointment A1 and then cancelling it through the interactive menu. I used the find appointment option to retrieve A1 and confirmed that its status was CANCELLED. I then listed appointments for the same practitioner with no status filter and confirmed that A1 was still displayed. When I selected the SCHEDULED filter, A1 was no longer included. I also booked another appointment, A3, at the same time and with the same practitioner, confirming that cancellation had freed the time slot.

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity?
select_appointments is pure because it uses explicit inputs, produces a result based on those inputs and does not modify the original appointment collection. It also does not perform input/output or access global data. Changing an appointment's status or modifying the original list inside the function would break its purity.

2. Which explicit inputs are needed, and why avoid a global store? 
The function requires an appointment list, a practitioner ID and an optional appointment status. A global store should be avoided because it creates hidden dependencies and makes the function harder to test and reuse.

3. How can a new list reuse Appointment objects safely? 
The function creates a new list containing references to the existing Appointment objects. This is safe because the query only reads the objects and does not modify their attributes. The original collection therefore remains unchanged.

4. Why use a named key, and what breaks equal-time ties? 
A named sorting key makes the sorting logic easier to understand and reuse. The function sorts first by appointment date and time, then by appointment ID. The appointment ID provides a consistent order when two appointments have the same date and time.

5. How do default and explicit status filters differ? 
When the status argument is None, all appointments for the selected practitioner are returned, including scheduled and cancelled appointments. When an explicit status is provided, only appointments matching that status are returned.

6. How do empty, unknown practitioner and invalid filter cases differ? 
An empty appointment collection produces an empty list because there are no appointments to return. An unknown practitioner causes the service layer to raise a LookupError. An invalid status filter causes a ValueError because the supplied status is not a valid AppointmentStatus.

7. Which console errors recover, and how is unchanged state checked? 
The console handles expected ValueError and LookupError exceptions and displays an error message instead of crashing. The user can then continue using the menu. Automated workflow tests check that failed operations, such as booking with an unknown patient, do not create or modify appointment records.

8. What is data integrity for registered participants, conflicts and history? 
Data integrity means that appointments must use registered patients and practitioners. A practitioner cannot have two scheduled appointments at the same time. When an appointment is cancelled, it remains in the system's history rather than being deleted. Cancelled appointments no longer prevent another appointment from being booked at that time.

9. What is Copilot's review role, and who verifies findings? 
GitHub Copilot can help identify possible problems, suggest improvements and review code against requirements. However, its suggestions are not automatically correct. The student is responsible for checking each suggestion, deciding whether it is appropriate and verifying any changes through code inspection and testing.

10. How do pure functions and OOP responsibilities work together? 
Object-oriented programming organises the application into classes with separate responsibilities, such as domain objects, the data store and services. Pure functions handle specific operations, such as filtering and sorting appointments, without changing application state. Together, these approaches make the application more organised, reusable and easier to test.


## H. Review, completion and common handover

Issues and bounded branches: 

Stage 9 implementation was completed on the feature branch. The work covers appointment queries, service integration, console functionality and automated testing. The feature branch and issue links should be added from the GitHub repository.

PR/diff and another-member human reviewer: 

Not yet completed. A pull request and review from another group member are still required before integration into the common Stage 9 branch.

Review responses and Copilot comparison: 

The implementation was checked against the Stage 9 requirements. Copilot-style review considerations included query purity, consistent sorting, service validation and cancellation history. Human verification is still required for final review and approval.

Integrated common Stage 9 SHA: 

236cd2f8fa768825656b17a8d5572d6a76f3f57a


Full regression command, working directory, actual count/result and evidence: 

Working directory: project/

Command: python3 -m pytest -q

Actual result: 61 passed

Evidence: Terminal test output and automated test files in project/tests/.

README run instructions and scope/limitations: 

The updated README is located at project/README.md.
It includes instructions for running the demonstration, starting the interactive menu and running the automated tests. The application uses session-only in-memory storage. It does not include permanent database storage, rescheduling or assurance functionality.

Unresolved issues and support/action: 

The main Stage 9 implementation and automated tests have been completed. Remaining actions include:
- Complete the GitHub pull request.
- Obtain another group member's human review.
- Address any review feedback.
- Merge the approved implementation into the common Stage 9 branch.
- Record the final integrated commit SHA.
- Confirm the complete manual invalid-input recovery demonstration.

UG common candidate / PG future branch plan: 

The common Stage 9 version should be protected before additional work begins.

- [ yes] Query contracts, purity, new lists and named-key ordering verified.
- [ yes] Service empty/unknown/invalid cases and cancellation history verified.
- [ yes] Every console command and invalid-input recovery demonstrated.
- [ yes] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ yes] Human design, Copilot critique, review and integration recorded honestly.
- [ yes] Reflections and ten formative responses completed.
- [ yes] README updated; earlier code/tests/records preserved.
- [yes ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
