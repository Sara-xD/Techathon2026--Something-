"""A simulated clock.

Everything in the system (device timestamps, energy accounting, alerts) reads
the current time from this one clock so they stay consistent. It can run faster
than real time (SIM_SPEED) so a short demo can show a whole day, including
after-hours behaviour and continuous-on alerts.
"""
import time
from datetime import datetime, timedelta


class SimClock:
    def __init__(self, speed: float = 1.0, start: datetime | None = None):
        self.speed = speed
        self._real_anchor = time.monotonic()
        self._sim_anchor = start or datetime.now()

    def now(self) -> datetime:
        """Current simulated time."""
        real_elapsed = time.monotonic() - self._real_anchor
        return self._sim_anchor + timedelta(seconds=real_elapsed * self.speed)

    def is_office_hours(self, open_hour: int, close_hour: int) -> bool:
        h = self.now().hour
        return open_hour <= h < close_hour


def build_clock(speed: float, start_hhmm: str) -> SimClock:
    """Create the clock, optionally starting at a given HH:MM today."""
    start = None
    if start_hhmm:
        try:
            hh, mm = (int(x) for x in start_hhmm.split(":"))
            start = datetime.now().replace(hour=hh, minute=mm, second=0, microsecond=0)
        except ValueError:
            start = None
    return SimClock(speed=speed, start=start)
