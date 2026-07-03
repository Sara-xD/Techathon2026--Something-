"""Tests for the simulated clock."""
from app import config
from app.clock import SimClock, build_clock


def test_is_office_hours_boundaries():
    def office(hour):
        c = SimClock(speed=0.0, start=_at(hour))
        return c.is_office_hours(config.OFFICE_OPEN_HOUR, config.OFFICE_CLOSE_HOUR)
    assert office(9) is True     # inclusive open
    assert office(16) is True
    assert office(17) is False   # exclusive close
    assert office(8) is False
    assert office(23) is False


def test_build_clock_with_start_time():
    clock = build_clock(speed=1.0, start_hhmm="16:45")
    now = clock.now()
    assert now.hour == 16 and now.minute == 45


def test_build_clock_blank_start_defaults_to_now():
    clock = build_clock(speed=1.0, start_hhmm="")
    assert clock.now() is not None


def _at(hour):
    from datetime import datetime
    return datetime(2026, 7, 3, hour, 0, 0)
