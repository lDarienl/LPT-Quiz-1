"""Tests para Problema 1: Sistema de navegación de páginas web."""

import pytest
from problema1_navegador import WebBrowser


def test_load_page():
    nav = WebBrowser()
    assert nav.loadPage("https://a.com") == "https://a.com"
    assert nav.current_page() == "https://a.com"
    assert nav.loadPage("https://b.com") == "https://b.com"
    assert nav.current_page() == "https://b.com"


def test_go_back_returns_previous():
    nav = WebBrowser()
    nav.loadPage("https://a.com")
    nav.loadPage("https://b.com")
    nav.loadPage("https://c.com")
    assert nav.goBack() == "https://b.com"
    assert nav.goBack() == "https://a.com"
    assert nav.current_page() == "https://a.com"


def test_go_back_when_empty_returns_none():
    nav = WebBrowser()
    assert nav.goBack() is None
    nav.loadPage("https://a.com")
    assert nav.goBack() is None  # una sola página, no hay "atrás"


def test_go_forward():
    nav = WebBrowser()
    nav.loadPage("https://a.com")
    nav.loadPage("https://b.com")
    nav.goBack()
    assert nav.current_page() == "https://a.com"
    assert nav.goForward() == "https://b.com"
    assert nav.current_page() == "https://b.com"


def test_go_forward_when_empty_returns_none():
    nav = WebBrowser()
    assert nav.goForward() is None
    nav.loadPage("https://a.com")
    assert nav.goForward() is None


def test_load_clears_forward():
    nav = WebBrowser()
    nav.loadPage("https://a.com")
    nav.loadPage("https://b.com")
    nav.goBack()
    nav.loadPage("https://c.com")  # nueva página: se pierde "forward" a b.com
    assert nav.goForward() is None
    assert nav.current_page() == "https://c.com"


def test_snake_case_methods():
    nav = WebBrowser()
    nav.load_page("https://x.com")
    assert nav.current_page() == "https://x.com"
    nav.load_page("https://y.com")
    assert nav.go_back() == "https://x.com"
    assert nav.go_forward() == "https://y.com"
