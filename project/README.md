# SmartCare Stage 12

**Requirements baseline:** SmartCare A3 2026, revision 2
**Release scope:** Common undergraduate functionality from Stages 6-9
**Starting SHA:** `89d106fecbd1671a184728f233c3e669ea0a7957`
**Final release SHA:** Pending Stage 12 verification and integration

## Overview

SmartCare is a Python appointment management application that allows users to register and find patients and practitioners, book and cancel appointments, retrieve appointment history, and list appointments using an interactive console.

## Setup and Running

The teaching baseline uses Python 3.13 and pytest 8.3.5. The project uses the Python standard library, with pytest required for testing.

From the repository root:

```powershell
cd project
python -m pip install -r requirements-dev.txt
```

Run the demonstration:

```powershell
python main.py
```

Launch the interactive menu:

```powershell
python main.py --interactive
```

Run the automated tests:

```powershell
python -m pytest -q
```

Verified Stage 12 results: All 61 tests passed using Python 3.13.17 and pytest 8.3.5 in 0.11 seconds. The demonstration (python main.py) and interactive menu (python main.py --interactive) also ran successfully. The tests previously passed using Python 3.14.6 and pytest 9.2.0. Final independent review and fresh-copy reproducibility verification remain pending.

## Features

- Patient and practitioner registration and lookup.
- Appointment booking using registered participants.
- Prevention of conflicting scheduled appointments for the same practitioner and time.
- Appointment cancellation with retained history.
- Appointment lookup by ID.
- Practitioner appointment listing with optional status filtering.
- Deterministic sorting by appointment date/time and ID.
- Interactive menu with input validation and error recovery.

## Project Structure

- `main.py` - Starts the demonstration or interactive menu.
- `smartcare/domain.py` - Domain classes, validation and appointment status.
- `smartcare/data_store.py` - In-memory patient, practitioner and appointment records.
- `smartcare/services.py` - Registration, lookup, booking, cancellation and listing operations.
- `smartcare/queries.py` - Pure filtering and sorting functions.
- `smartcare/console.py` - Console input, output and menu handling.
- `tests/` - Automated tests covering the application.

## Known Limitations

SmartCare stores data only during the current session. All records are lost when the application exits. Permanent storage is not required because FR-10 restart persistence has been retired.

The application uses local date/time values at minute precision. It does not implement patient scheduling conflicts, appointment durations, age restrictions or restrictions on past appointment dates.

The application is a teaching project, not a production medical system. Use synthetic data only. Authentication, billing, notifications and clinical record management are outside its scope.

Stages 10 and 11 are PG-only and are not applicable to this undergraduate release.

## Testing and Responsible AI

The accumulated test suite contains 61 tests covering domain validation, services, appointment conflicts, cancellation, queries and workflows.

GitHub Copilot was used during earlier development stages, with prompts, findings and human decisions recorded in the relevant stage evidence files. We evaluated suggestions against the requirements and tests.

Stage 12 includes a final documentation, code-quality and release review. Independent approval and the final submitted SHA will be recorded after verification.