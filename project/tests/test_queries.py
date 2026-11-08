
from datetime import datetime

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.queries import (
    appointment_sort_key,
    select_appointments,
)


def make_appointment(appointment_id, practitioner, date_time, status):
    patient = Patient("P1", "Alex Example")
    appointment = Appointment(
        appointment_id,
        patient,
        practitioner,
        date_time,
    )

    if status is AppointmentStatus.CANCELLED:
        appointment.cancel()

    return appointment


def test_appointment_sort_key_returns_datetime_and_id():
    practitioner = Practitioner("D1", "Taylor Example", "General Practice")
    appointment = make_appointment(
        "A1",
        practitioner,
        datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.SCHEDULED,
    )

    assert appointment_sort_key(appointment) == (
        datetime(2026, 10, 1, 9, 0),
        "A1",
    )


def test_select_appointments_filters_by_practitioner():
    d1 = Practitioner("D1", "Taylor Example", "General Practice")
    d2 = Practitioner("D2", "Jordan Smith", "Cardiology")

    a1 = make_appointment(
        "A1", d1, datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.SCHEDULED,
    )
    a2 = make_appointment(
        "A2", d2, datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.SCHEDULED,
    )

    results = select_appointments([a1, a2], "D1")

    assert results == [a1]


def test_select_appointments_includes_all_statuses_by_default():
    practitioner = Practitioner("D1", "Taylor Example", "General Practice")

    scheduled = make_appointment(
        "A1", practitioner, datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.SCHEDULED,
    )
    cancelled = make_appointment(
        "A2", practitioner, datetime(2026, 10, 1, 10, 0),
        AppointmentStatus.SCHEDULED,
    )
    cancelled.cancel()

    results = select_appointments([scheduled, cancelled], "D1")

    assert len(results) == 2
    assert scheduled in results
    assert cancelled in results


def test_select_appointments_filters_by_status():
    practitioner = Practitioner("D1", "Taylor Example", "General Practice")

    scheduled = make_appointment(
        "A1", practitioner, datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.SCHEDULED,
    )
    cancelled = make_appointment(
        "A2", practitioner, datetime(2026, 10, 1, 10, 0),
        AppointmentStatus.SCHEDULED,
    )
    cancelled.cancel()

    results = select_appointments(
        [scheduled, cancelled],
        "D1",
        AppointmentStatus.CANCELLED,
    )

    assert results == [cancelled]


def test_select_appointments_sorts_by_datetime_then_id():
    practitioner = Practitioner("D1", "Taylor Example", "General Practice")

    later = make_appointment(
        "A3", practitioner, datetime(2026, 10, 1, 10, 0),
        AppointmentStatus.SCHEDULED,
    )
    same_time_b = make_appointment(
        "A2", practitioner, datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.SCHEDULED,
    )
    same_time_a = make_appointment(
        "A1", practitioner, datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.SCHEDULED,
    )

    source = [later, same_time_b, same_time_a]
    original_order = source.copy()

    results = select_appointments(source, "D1")

    assert results == [same_time_a, same_time_b, later]
    assert source == original_order


def test_select_appointments_returns_a_new_list():
    practitioner = Practitioner("D1", "Taylor Example", "General Practice")

    appointment = make_appointment(
        "A1", practitioner, datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.SCHEDULED,
    )

    source = [appointment]
    results = select_appointments(source, "D1")

    assert results is not source
    assert results[0] is appointment


def test_select_appointments_returns_empty_list_when_no_match():
    practitioner = Practitioner("D1", "Taylor Example", "General Practice")

    appointment = make_appointment(
        "A1", practitioner, datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.SCHEDULED,
    )

    results = select_appointments([appointment], "D2")

    assert results == []