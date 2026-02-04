"""Tests para Problema 2: Función de autocompletar."""

import pytest
from problema2_autocomplete import Autocomplete


def test_insert_and_autocomplete():
    ac = Autocomplete()
    ac.insert("casa")
    ac.insert("casamiento")
    ac.insert("casero")
    assert set(ac.autocomplete("cas")) == {"casa", "casamiento", "casero"}
    # Con prefijo "casa" solo coinciden "casa" y "casamiento" (no "casero")
    assert ac.autocomplete("casa") == ["casa", "casamiento"]


def test_autocomplete_no_match():
    ac = Autocomplete()
    ac.insert("python")
    assert ac.autocomplete("pyx") == []
    assert ac.autocomplete("java") == []


def test_autocomplete_empty_prefix_returns_all():
    ac = Autocomplete()
    ac.insert("a")
    ac.insert("ab")
    ac.insert("abc")
    result = ac.autocomplete("")
    assert set(result) == {"a", "ab", "abc"}
    assert len(result) == 3


def test_multiple_prefixes():
    ac = Autocomplete()
    ac.insert("casa")
    ac.insert("casamiento")
    ac.insert("python")
    ac.insert("pyramid")
    assert set(ac.autocomplete("cas")) == {"casa", "casamiento"}
    assert set(ac.autocomplete("py")) == {"python", "pyramid"}
    assert ac.autocomplete("p") == ["pyramid", "python"]


def test_insert_empty_ignored():
    ac = Autocomplete()
    ac.insert("")
    ac.insert("  ")
    assert ac.autocomplete("") == []


def test_case_insensitive():
    ac = Autocomplete()
    ac.insert("Casa")
    ac.insert("CASERO")
    assert "casa" in ac.autocomplete("cas")
    assert "casero" in ac.autocomplete("cas")
