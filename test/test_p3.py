"""Tests para Problema 3: Sistema de recomendación de productos."""

import pytest
from problema3_recomendador import ProductRecommender


def test_get_recommendations_empty_user():
    rec = ProductRecommender()
    rec.addPurchase("Ana", "X")
    assert rec.getRecommendations("Bob") == []


def test_get_recommendations_basic():
    rec = ProductRecommender()
    rec.addPurchase("Ana", "Libro A")
    rec.addPurchase("Ana", "Libro B")
    rec.addPurchase("Bob", "Libro A")
    rec.addPurchase("Bob", "Libro C")
    recs = rec.getRecommendations("Ana")
    assert "Libro C" in recs
    assert "Libro A" not in recs
    assert "Libro B" not in recs


def test_multiple_user_product_relations():
    rec = ProductRecommender()
    rec.addPurchase("U1", "P1")
    rec.addPurchase("U1", "P2")
    rec.addPurchase("U2", "P1")
    rec.addPurchase("U2", "P3")
    rec.addPurchase("U3", "P1")
    rec.addPurchase("U3", "P3")
    recs = rec.getRecommendations("U1")
    assert "P3" in recs
    assert "P1" not in recs
    assert "P2" not in recs


def test_recommendations_ordered_by_frequency():
    rec = ProductRecommender()
    rec.addPurchase("Ana", "X")
    rec.addPurchase("Bob", "X")
    rec.addPurchase("Bob", "Y")
    rec.addPurchase("Carlos", "X")
    rec.addPurchase("Carlos", "Y")
    rec.addPurchase("Carlos", "Z")
    recs = rec.getRecommendations("Ana")
    # Y aparece 2 veces (Bob, Carlos), Z aparece 1 vez
    assert recs.index("Y") < recs.index("Z")


def test_snake_case_methods():
    rec = ProductRecommender()
    rec.add_purchase("User", "Prod")
    assert rec.get_recommendations("User") == []
