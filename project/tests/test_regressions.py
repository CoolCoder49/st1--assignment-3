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
def regression_services():
    store = SmartCareDataStore()

    patients = PatientService(store)
    practitioners = PractitionerService(store)
    appointments = AppointmentService(store)

    patients.register_patient("P001", "Alice Smith")
    patients.register_patient("P002", "Bob Jones")

    practitioners.register_practitioner("D001", "Dr Lee", "Cardiology")
    practitioners.register_practitioner("D002", "Dr Brown", "General")

    return store, appointments


def test_f8_01_practitioner_conflict_regression(regression_services):
    store, appointments = regression_services
    when = datetime(2026, 11, 1, 10, 30)

    first = appointments.book_appointment("A001", "P001", "D001", when)

    with pytest.raises(ValueError):
        appointments.book_appointment("A002", "P002", "D001", when)

    assert store.find_appointment("A001") is first
    assert store.find_appointment("A002") is None
    assert first.status is AppointmentStatus.SCHEDULED
    assert len(store.list_appointments()) == 1

    second = appointments.book_appointment("A003", "P002", "D002", when)

    assert store.find_appointment("A003") is second
    assert second.practitioner.practitioner_id == "D002"
    assert len(store.list_appointments()) == 2


def test_f8_02_cancelled_history_regression(regression_services):
    store, appointments = regression_services
    when = datetime(2026, 11, 1, 10, 30)

    original = appointments.book_appointment("A001", "P001", "D001", when)

    cancelled = appointments.cancel_appointment("A001")

    assert cancelled is original
    assert original.status is AppointmentStatus.CANCELLED
    assert original in store.list_appointments()

    assert store.find_appointment("A001") is original
    assert appointments.find_appointment("A001") is original

    with pytest.raises(ValueError):
        appointments.cancel_appointment("A001")

    assert original.status is AppointmentStatus.CANCELLED
    assert store.find_appointment("A001") is original
