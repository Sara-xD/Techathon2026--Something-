"""Make the backend and bot packages importable from the test suite.

The tests exercise pure logic (device store, alerts, clock, bot formatters) with
no network, no Discord, and no Gemini calls.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "backend"))
sys.path.insert(0, os.path.join(ROOT, "bot"))
