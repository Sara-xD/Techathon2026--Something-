"""Tests for the alert engine: office-hours boundary and room-all-on threshold."""
from datetime import timedelta

import pytest

from app.alerts import compute_alerts
from helpers import frozen_store, all_on


def _has(alerts, atype, room=None):
    return any(a["type"] == atype and (room is None or a["room"] == room) for a in alerts)


@pytest.mark.parametrize("hour,minute,expect_after_hours", [
    (9, 0, False),    # 9AM exactly = office open (inclusive)
    (8, 59, True),    # just before open
    (16, 59, False),  # just before 5PM = still office hours
    (17, 0, True),    # 5PM exactly = after hours (exclusive close)
    (22, 0, True),    # night
])
def test_after_hours_boundary(hour, minute, expect_after_hours):
    store, _ = frozen_store(hour=hour, minute=minute)
    all_on(store)
    assert _has(compute_alerts(store), "after_hours") is expect_after_hours


@pytest.mark.parametrize("hours_on,expect_alert", [
    (1.9, False),   # under threshold
    (2.0, True),    # exactly at threshold
    (3.5, True),    # well over
])
def test_room_all_on_threshold(hours_on, expect_alert):
    store, clock = frozen_store(hour=12)   # office hours -> isolate this alert
    all_on(store)
    store.room_all_on_since["work1"] = clock.now() - timedelta(hours=hours_on)
    assert _has(compute_alerts(store), "room_all_on", room="work1") is expect_alert


def test_turning_one_device_off_clears_room_alert():
    store, clock = frozen_store(hour=12)
    all_on(store)
    store.room_all_on_since["work1"] = clock.now() - timedelta(hours=3)
    assert _has(compute_alerts(store), "room_all_on", room="work1")

    store.set_status("work1-fan-1", False)
    store.update_room_continuity()
    assert store.room_all_on_since["work1"] is None
    assert not _has(compute_alerts(store), "room_all_on", room="work1")


def test_no_alerts_when_all_off_during_office_hours():
    store, _ = frozen_store(hour=12)
    assert compute_alerts(store) == []


def test_alerts_are_timestamped_and_identified():
    store, _ = frozen_store(hour=22)
    all_on(store)
    for a in compute_alerts(store):
        assert a["id"] and a["timestamp"] and a["room_name"] and a["message"]
