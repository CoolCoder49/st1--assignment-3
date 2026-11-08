
from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


@pytest.fixture
def smartcare_services():
    data_store = SmartCareDataStore()

    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    patients.register_patient("P1", "Alex Example")

    practitioners.register_practitioner(
        "D1", "Taylor Example", "General Practice"
    )
    practitioners.register_practitioner(
        "D2", "Jordan Smith", "Cardiology"
    )

    return data_store, appointments


def test_booking_and_conflict_rejection_preserve_records(smartcare_services):
    data_store, appointments = smartcare_services
    appointment_time = datetime(2026, 10, 1, 9, 0)

    first = appointments.book_appointment(
        "A1", "P1", "D1", appointment_time
    )

    before = data_store.list_appointments().copy()

    with pytest.raises(ValueError):
        appointments.book_appointment(
            "A2", "P1", "D1", appointment_time
        )

    assert data_store.list_appointments() == before
    assert appointments.find_appointment("A1") is first

    # A different practitioner can use the same time.
    second = appointments.book_appointment(
        "A2", "P1", "D2", appointment_time
    )

    assert appointments.find_appointment("A2") is second


def test_cancellation_retains_history_and_frees_time_slot(
    smartcare_services,
):
    data_store, appointments = smartcare_services
    appointment_time = datetime(2026, 10, 1, 9, 0)

    original = appointments.book_appointment(
        "A1", "P1", "D1", appointment_time
    )

    cancelled = appointments.cancel_appointment("A1")

    assert cancelled is original
    assert original.status is AppointmentStatus.CANCELLED
    assert appointments.find_appointment("A1") is original

    # The cancelled appointment remains in the all-status listing.
    all_appointments = appointments.list_practitioner_appointments("D1")
    assert all_appointments == [original]

    # It is not included in the scheduled-only listing.
    scheduled = appointments.list_practitioner_appointments(
        "D1", AppointmentStatus.SCHEDULED
    )
    assert scheduled == []

    # The cancelled time slot can now be booked again.
    replacement = appointments.book_appointment(
        "A2", "P1", "D1", appointment_time
    )

    assert replacement.status is AppointmentStatus.SCHEDULED
    assert appointments.find_appointment("A1") is original
    assert appointments.find_appointment("A2") is replacement


def test_unknown_patient_booking_does_not_change_records(
    smartcare_services,
):
    data_store, appointments = smartcare_services
    before = data_store.list_appointments().copy()

    with pytest.raises(LookupError):
        appointments.book_appointment(
            "A1",
            "UNKNOWN",
            "D1",
            datetime(2026, 10, 1, 9, 0),
        )

    assert data_store.list_appointments() == before


def test_unknown_practitioner_listing_raises_lookup_error(
    smartcare_services,
):
    _, appointments = smartcare_services

    with pytest.raises(LookupError):
        appointments.list_practitioner_appointments("UNKNOWN")


def test_invalid_status_listing_raises_value_error(smartcare_services):
    _, appointments = smartcare_services

    with pytest.raises(ValueError):
        appointments.list_practitioner_appointments(
            "D1", "scheduled"
        )
