import pytest

from fastapi import status

from app.models.product import Product
from app.models.product_stock import ProductStock
from app.models.cash_stock import CashStock


@pytest.fixture(autouse=True)
def seed_data(db):

    p = Product(name="Soda", price=20)
    db.add(p)
    db.commit()
    db.refresh(p)

    db.add(ProductStock(product_id=p.id, quantity=5))

    for denom, qty in [(100, 1), (50, 1), (20, 2), (10, 5), (5, 10), (2, 25), (1, 50)]:
        db.add(CashStock(denomination=denom, quantity=qty))

    db.commit()


def test_purchase_exact_money(client):
    # buy soda price 20 with exact 20
    payload = {"product_id": 1, "payment": [{"denomination": 20, "count": 1}]}
    res = client.post("/api/v1/purchase", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] == True
    assert data["change"] == []


def test_purchase_with_change(client):
    payload = {"product_id": 1, "payment": [{"denomination": 50, "count": 1}]}
    res = client.post("/api/v1/purchase", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] == True
    # change must sum to 30
    total_change = sum(i["denomination"] * i["count"] for i in data["change"])
    assert total_change == 30


def test_purchase_insufficient_payment(client):
    payload = {"product_id": 1, "payment": [{"denomination": 10, "count": 1}]}
    res = client.post("/api/v1/purchase", json=payload)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    data = res.json()
    assert "detail" in data
    assert data["detail"] == "Insufficient payment"


def test_purchase_out_of_stock(client, db):
    db.query(ProductStock).update({"quantity": 0})
    db.commit()

    payload = {"product_id": 1, "payment": [{"denomination": 20, "count": 1}]}
    res = client.post("/api/v1/purchase", json=payload)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    data = res.json()
    assert "detail" in data
    assert data["detail"] == "Out of stock"


def test_purchase_product_not_found(client):
    payload = {"product_id": 999, "payment": [{"denomination": 20, "count": 1}]}
    res = client.post("/api/v1/purchase", json=payload)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    data = res.json()
    assert "detail" in data
    assert data["detail"] == "Product not found"


def test_purchase_cannot_provide_change(client, db):
    # empty all small denominations
    db.query(CashStock).update({"quantity": 0})
    db.commit()

    payload = {"product_id": 1, "payment": [{"denomination": 50, "count": 1}]}
    res = client.post("/api/v1/purchase", json=payload)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    data = res.json()
    assert "detail" in data
    assert data["detail"] == "Cannot provide change with current cash stock"
