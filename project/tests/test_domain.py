from datetime import datetime, timezone

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
    required_text,
    validate_date_time,
)


def test_required_text_trims_whitespace():
    assert required_text("  Alice  ", "Name") == "Alice"


@pytest.mark.parametrize("value", ["", "   ", None, 123])
def test_required_text_rejects_invalid_text(value):
    with pytest.raises(ValueError):
        required_text(value, "Name")


def test_patient_stores_trimmed_fields():
    patient = Patient(" P001 ", " Alice Smith ")

    assert patient.patient_id == "P001"
    assert patient.name == "Alice Smith"


@pytest.mark.parametrize(
    "patient_id,name",
    [
        ("", "Alice"),
        ("P001", ""),
        ("P001", "   "),
    ],
)
def test_patient_rejects_blank_fields(patient_id, name):
    with pytest.raises(ValueError):
        Patient(patient_id, name)


def test_practitioner_stores_trimmed_fields():
    practitioner = Practitioner(" D001 ", " Dr Lee ", " Cardiology ")

    assert practitioner.practitioner_id == "D001"
    assert practitioner.name == "Dr Lee"
    assert practitioner.specialty == "Cardiology"


@pytest.mark.parametrize(
    "practitioner_id,name,specialty",
    [
        ("", "Dr Lee", "Cardiology"),
        ("D001", "", "Cardiology"),
        ("D001", "Dr Lee", ""),
    ],
)
def test_practitioner_rejects_blank_fields(
    practitioner_id, name, specialty
):
    with pytest.raises(ValueError):
        Practitioner(practitioner_id, name, specialty)


def test_validate_date_time_accepts_minute_precision():
    value = datetime(2026, 11, 1, 10, 30)

    assert validate_date_time(value) is value


@pytest.mark.parametrize(
    "value",
    [
        "2026-11-01 10:30",
        datetime(2026, 11, 1, 10, 30, 1),
        datetime(2026, 11, 1, 10, 30, 0, 1),
        datetime(2026, 11, 1, 10, 30, tzinfo=timezone.utc),
    ],
)
def test_validate_date_time_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        validate_date_time(value)


def make_appointment(status=AppointmentStatus.SCHEDULED):
    patient = Patient("P001", "Alice Smith")
    practitioner = Practitioner("D001", "Dr Lee", "Cardiology")

    return Appointment(
        "A001",
        patient,
        practitioner,
        datetime(2026, 11, 1, 10, 30),
        status,
    )


def test_appointment_has_expected_default_status():
    appointment = make_appointment()

    assert appointment.status is AppointmentStatus.SCHEDULED


def test_cancel_changes_scheduled_appointment_to_cancelled():
    appointment = make_appointment()

    appointment.cancel()

    assert appointment.status is AppointmentStatus.CANCELLED


@pytest.mark.parametrize(
    "status",
    [AppointmentStatus.CANCELLED, AppointmentStatus.COMPLETED],
)
def test_cancel_rejects_invalid_transition_without_changing_status(status):
    appointment = make_appointment(status)

    with pytest.raises(ValueError):
        appointment.cancel()

    assert appointment.status is status


def test_appointment_rejects_invalid_participant_objects():
    with pytest.raises(ValueError):
        Appointment(
            "A001",
            "not a patient",
            Practitioner("D001", "Dr Lee", "Cardiology"),
            datetime(2026, 11, 1, 10, 30),
        )