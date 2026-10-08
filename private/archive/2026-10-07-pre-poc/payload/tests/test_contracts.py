"""Contracts: every schema is a valid 2020-12 schema, valid fixtures pass, invalid fixtures fail."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from wgc import contracts

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "contracts" / "fixtures"


@pytest.mark.parametrize("schema_file", sorted(contracts.SCHEMA_DIR.glob("*.schema.json")), ids=lambda p: p.name)
def test_schema_is_valid_2020_12(schema_file):
    Draft202012Validator.check_schema(json.loads(schema_file.read_text(encoding="utf-8")))


def test_every_schema_file_is_registered():
    registered = set(contracts.CONTRACTS.values()) | {"common.schema.json"}
    assert {f.name for f in contracts.SCHEMA_DIR.glob("*.schema.json")} == registered


@pytest.mark.parametrize("fixture", sorted((FIXTURES / "valid").glob("*.yaml")), ids=lambda p: p.name)
def test_valid_fixture(fixture):
    assert contracts.errors(contracts.load(fixture)) == []


@pytest.mark.parametrize("fixture", sorted((FIXTURES / "invalid").glob("*.yaml")), ids=lambda p: p.name)
def test_invalid_fixture(fixture):
    assert contracts.errors(contracts.load(fixture)), f"{fixture.name} should be rejected"


def test_every_contract_has_a_valid_fixture():
    used = {contracts.load(f)["schema"] for f in (FIXTURES / "valid").glob("*.yaml")}
    assert used == set(contracts.CONTRACTS)
