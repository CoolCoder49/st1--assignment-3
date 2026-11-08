# SmartCare Stage 6 starter

Requirements baseline: SmartCare A3 2026 revision 2. Python 3.13 and pytest 8.3.5 verified. Runtime uses only the standard library.

From this directory, using a Python environment with the development dependency installed:

```sh
python main.py
python -m pytest
```

If needed in your approved environment: `python -m pip install -r requirements-dev.txt`.

The demo registers synthetic records and books/finds an appointment. All supplied tests pass. Data exists only in this session and is lost on exit; FR-10 restart persistence is retired. Use synthetic information only.

`domain.py` contains the entities, status and guarded cancellation. `data_store.py` holds three dictionaries through add/find/list methods. The three services share that object. Supplied registration, booking, appointment lookup and conflict checking work. IDs are trimmed, non-blank and case-sensitive. Properties provide read-only identity/appointment state; changes go through domain methods. No special architecture terminology is required.

Stage 6 TODOs: service patient/practitioner lookup and cancellation. Stage 9 TODOs: pure query, named sort key, service listing and interactive menu. The starter TODO contracts are in docstrings. All three Stage 6 TODO calls deliberately raise NotImplementedError; future TODOs remain stubs. No PG rescheduling or assurance solution is supplied.

Service booking accepts IDs and a `datetime` (local, minute precision). Console parser accepts exactly `YYYY-MM-DD HH:MM`. Store lookups return None when absent; service lookups raise LookupError. Invalid values, duplicates, conflicts and illegal transitions raise ValueError. Lists are new containers holding the stored objects. No age, duration, patient-conflict or past-date rules apply.

SmartCare Application — Stage 9

Environment: Python 3.13 and pytest 8.3.5. The application uses only the Python standard library.

Running the Application

Run these commands from the project/ directory.

To run the supplied demonstration:

python3 main.py

To launch the interactive menu:

python3 main.py --interactive

To run the automated test suite:

python3 -m pytest -q

Stage 9 Features

The application supports:

Registering and finding patients.

Registering and finding practitioners.

Booking appointments.

Preventing appointments from being booked with the same practitioner at the same time.

Cancelling existing appointments while retaining their history.

Finding appointments by appointment ID.

Listing appointments for a practitioner.

Filtering appointments by scheduled, cancelled or completed status.

Sorting appointments by date/time and appointment ID.

The interactive menu provides options for these operations and continues until the user selects Exit.

Queries and Services

The queries.py module contains two pure functions:

appointment_sort_key() provides a reusable appointment sorting key.

select_appointments() filters appointments by practitioner and optional status, returning a new sorted list without modifying the original collection.

The AppointmentService coordinates appointment listing and validates practitioner IDs and status values before using the query function.

The application separates responsibilities between domain entities, the in-memory data store, services, pure query functions and console interaction.

Testing and Verification

The project includes the original tests and additional Stage 9 tests:

test_queries.py tests appointment filtering, sorting and non-mutation.

test_workflows.py tests booking, conflict prevention, cancellation, retained history and practitioner listing.

Latest recorded test result: 61 passed.

Run the complete test suite using:

python3 -m pytest -q

Data Storage and Limitations

SmartCare uses an in-memory data store containing patients, practitioners and appointments.

Records are available only during the current application session and are discarded when the application exits. The application does not implement database storage or restart persistence. FR-10 restart persistence is retired.

Only synthetic information should be used when testing the application.

The application does not implement additional rules for patient scheduling conflicts, appointment duration, age restrictions or past appointment dates.