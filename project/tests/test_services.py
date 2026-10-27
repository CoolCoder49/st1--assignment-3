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
def setup_services():
    store = SmartCareDataStore()

    patients = PatientService(store)
    practitioners = PractitionerService(store)
    appointments = AppointmentService(store)

    patient = patients.register_patient("P001", "Alice Smith")
    practitioner = practitioners.register_practitioner(
        "D001", "Dr Lee", "Cardiology"
    )

    return store, patients, practitioners, appointments, patient, practitioner


def test_register_patient_stores_patient(setup_services):
    store, patients, _, _, patient, _ = setup_services

    assert store.find_patient("P001") is patient
    assert patients.find_patient("P001") is patient


def test_register_patient_rejects_duplicate_id(setup_services):
    store, patients, _, _, original, _ = setup_services

    with pytest.raises(ValueError):
        patients.register_patient("P001", "Different Person")

    assert store.find_patient("P001") is original
    assert len(store.list_patients()) == 1


def test_find_patient_unknown_id_raises_lookup_error(setup_services):
    _, patients, _, _, _, _ = setup_services

    with pytest.raises(LookupError):
        patients.find_patient("UNKNOWN")


def test_find_patient_blank_id_raises_value_error(setup_services):
    _, patients, _, _, _, _ = setup_services

    with pytest.raises(ValueError):
        patients.find_patient("   ")


def test_register_and_find_practitioner(setup_services):
    store, _, practitioners, _, _, practitioner = setup_services

    assert store.find_practitioner("D001") is practitioner
    assert practitioners.find_practitioner("D001") is practitioner


def test_find_practitioner_unknown_id_raises_lookup_error(setup_services):
    _, _, practitioners, _, _, _ = setup_services

    with pytest.raises(LookupError):
        practitioners.find_practitioner("UNKNOWN")


def test_find_practitioner_blank_id_raises_value_error(setup_services):
    _, _, practitioners, _, _, _ = setup_services

    with pytest.raises(ValueError):
        practitioners.find_practitioner("   ")


def test_booking_stores_appointment_and_participant_objects(setup_services):
    store, _, _, appointments, patient, practitioner = setup_services
    when = datetime(2026, 11, 1, 10, 30)

    appointment = appointments.book_appointment(
        "A001", "P001", "D001", when
    )

    assert store.find_appointment("A001") is appointment
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.status is AppointmentStatus.SCHEDULED


def test_booking_rejects_practitioner_time_conflict(setup_services):
    store, _, _, appointments, _, _ = setup_services
    when = datetime(2026, 11, 1, 10, 30)

    first = appointments.book_appointment("A001", "P001", "D001", when)

    with pytest.raises(ValueError):
        appointments.book_appointment("A002", "P001", "D001", when)

    assert store.find_appointment("A001") is first
    assert store.find_appointment("A002") is None
    assert first.status is AppointmentStatus.SCHEDULED


def test_booking_allows_same_practitioner_at_different_time(setup_services):
    _, _, _, appointments, _, _ = setup_services

    first = appointments.book_appointment(
        "A001", "P001", "D001", datetime(2026, 11, 1, 10, 30)
    )
    second = appointments.book_appointment(
        "A002", "P001", "D001", datetime(2026, 11, 1, 11, 30)
    )

    assert first.appointment_id == "A001"
    assert second.appointment_id == "A002"


def test_cancel_appointment_retains_record_and_changes_status(setup_services):
    store, _, _, appointments, _, _ = setup_services
    when = datetime(2026, 11, 1, 10, 30)

    appointment = appointments.book_appointment(
        "A001", "P001", "D001", when
    )
    cancelled = appointments.cancel_appointment("A001")

    assert cancelled is appointment
    assert store.find_appointment("A001") is appointment
    assert appointment.status is AppointmentStatus.CANCELLED
    assert appointment.date_time == when
    assert appointment.patient.patient_id == "P001"
    assert appointment.practitioner.practitioner_id == "D001"


def test_cancelling_again_raises_value_error_and_preserves_state(setup_services):
    store, _, _, appointments, _, _ = setup_services
    appointment = appointments.book_appointment(
        "A001", "P001", "D001", datetime(2026, 11, 1, 10, 30)
    )
    appointments.cancel_appointment("A001")

    with pytest.raises(ValueError):
        appointments.cancel_appointment("A001")

    assert store.find_appointment("A001") is appointment
    assert appointment.status is AppointmentStatus.CANCELLED
    assert len(store.list_appointments()) == 1


def test_cancelled_slot_can_be_booked_again(setup_services):
    store, _, _, appointments, _, _ = setup_services
    when = datetime(2026, 11, 1, 10, 30)

    original = appointments.book_appointment("A001", "P001", "D001", when)
    appointments.cancel_appointment("A001")

    replacement = appointments.book_appointment("A002", "P001", "D001", when)

    assert original.status is AppointmentStatus.CANCELLED
    assert store.find_appointment("A001") is original
    assert store.find_appointment("A002") is replacement
    assert len(store.list_appointments()) == 2


def test_cancel_unknown_appointment_raises_lookup_error(setup_services):
    _, _, _, appointments, _, _ = setup_services

    with pytest.raises(LookupError):
        appointments.cancel_appointment("UNKNOWN")


def test_find_appointment_unknown_id_raises_lookup_error(setup_services):
    _, _, _, appointments, _, _ = setup_services

    with pytest.raises(LookupError):
        appointments.find_appointment("UNKNOWN")


def test_find_appointment_blank_id_raises_value_error(setup_services):
    _, _, _, appointments, _, _ = setup_services

    with pytest.raises(ValueError):
        appointments.find_appointment("   ")