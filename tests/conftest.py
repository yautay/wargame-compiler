"""Temporary test repositories must never inherit the operator's host binding."""
import pytest


@pytest.fixture(autouse=True)
def isolate_host_binding(monkeypatch):
    monkeypatch.delenv('WGC_HOST_RUNTIME', raising=False)
    monkeypatch.delenv('WGC_HOST_RUNTIME_SHA256', raising=False)
