"""Stage 9 contracts for pure collection processing."""
from datetime import datetime

from smartcare.domain import Appointment, AppointmentStatus


def appointment_sort_key(appointment: Appointment) -> tuple[datetime, str]:
    """Return the date/time and appointment ID ordering key."""
    return appointment.date_time, appointment.appointment_id


def select_appointments(
    appointments: list[Appointment],
    practitioner_id: str,
    status: AppointmentStatus | None = None,
) -> list[Appointment]:
    """Return a new, sorted list of matching practitioner appointments.

    When status is None, appointments of every status are included.
    The original collection and Appointment objects are not modified.
    """
    selected = []

    for appointment in appointments:
        if appointment.practitioner.practitioner_id == practitioner_id:
            if status is None or appointment.status is status:
                selected.append(appointment)

    return sorted(selected, key=appointment_sort_key)

