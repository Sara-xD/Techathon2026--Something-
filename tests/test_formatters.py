"""Tests for the bot's factual formatters and room-name resolver.

These strings are the source of truth for the bot's replies (the LLM only
rewords them), so their correctness matters.
"""
import re

import pytest

import formatters as fmt
from helpers import frozen_store


@pytest.mark.parametrize("name,expected", [
    ("work1", "work1"),
    ("Work Room 1", "work1"),
    ("wr1", "work1"),
    ("1", "work1"),
    ("work2", "work2"),
    ("Work Room 2", "work2"),
    ("2", "work2"),
    ("drawing", "drawing"),
    ("Drawing Room", "drawing"),
    ("kitchen", None),
    ("", None),
])
def test_resolve_room_aliases(name, expected):
    assert fmt.resolve_room(name) == expected


def test_format_status_all_off():
    store, _ = frozen_store()
    rooms = [store.room_summary(r) for r in ("drawing", "work1", "work2")]
    text = fmt.format_status(rooms)
    assert text.count("all off") == 3
    assert "Drawing Room" in text and "Work Room 1" in text


def test_format_status_reports_counts():
    store, _ = frozen_store()
    store.set_status("drawing-fan-1", True)
    store.set_status("drawing-light-1", True)
    text = fmt.format_status([store.room_summary("drawing")])
    assert "1 fan(s) ON, 1 light(s) ON" in text


def test_format_room_includes_power():
    store, _ = frozen_store()
    store.set_status("work1-fan-1", True)   # 60 W
    text = fmt.format_room(store.room_summary("work1"))
    assert "Work Room 1" in text and "60" in text and "power" in text.lower()


def test_format_usage_contains_all_numbers():
    store, _ = frozen_store()
    store.set_status("work1-fan-1", True)   # 60 W
    usage = store.usage()
    text = fmt.format_usage(usage)
    # total, each per-room value, and kWh should all appear
    assert str(usage["total_watts"]) in text
    assert str(usage["today_kwh"]) in text
    for w in usage["per_room"].values():
        assert str(w) in text


def test_format_alerts_empty_and_nonempty():
    assert "No active alerts" in fmt.format_alerts([])
    sample = [{"room_name": "Work Room 2", "message": "left on"}]
    assert "Work Room 2" in fmt.format_alerts(sample)
