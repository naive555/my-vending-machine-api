import pytest

from app.models.cash_stock import CashStock


# Helpers
def create_sample_cash(db, denom=10, qty=5):
    item = CashStock(denomination=denom, quantity=qty)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# TEST: Create
def test_create_cash_stock(client):
    response = client.post(
        "/api/v1/cash-stock/", json={"denomination": 5, "quantity": 10}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["denomination"] == 5
    assert data["quantity"] == 10


def test_create_cash_stock_duplicate(client, db):
    create_sample_cash(db, denom=20)
    response = client.post(
        "/api/v1/cash-stock/", json={"denomination": 20, "quantity": 5}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Denomination already exists"


# TEST: Get one
def test_get_cash_stock(client, db):
    item = create_sample_cash(db, denom=50, qty=3)
    response = client.get(f"/api/v1/cash-stock/{item.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["denomination"] == 50
    assert data["quantity"] == 3


def test_get_cash_stock_not_found(client):
    response = client.get("/api/v1/cash-stock/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cash Stock not found"


# TEST: Get List
def test_list_cash_stock(client, db):
    create_sample_cash(db, 100, 1)
    create_sample_cash(db, 10, 2)
    create_sample_cash(db, 50, 3)

    response = client.get("/api/v1/cash-stock/")
    assert response.status_code == 200

    data = response.json()
    assert data[0]["denomination"] == 100
    assert data[1]["denomination"] == 50
    assert data[2]["denomination"] == 10


# TEST: Update
def test_update_cash_stock(client, db):
    item = create_sample_cash(db, denom=5, qty=10)
    response = client.put(
        f"/api/v1/cash-stock/{item.id}",
        json={"denomination": 5, "quantity": 99},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 99


def test_update_cash_stock_duplicate_denomination(client, db):
    a = create_sample_cash(db, denom=1, qty=3)
    b = create_sample_cash(db, denom=10, qty=3)

    response = client.put(
        f"/api/v1/cash-stock/{b.id}",
        json={"denomination": 1, "quantity": 2},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Denomination already exists"


def test_update_cash_stock_not_found(client):
    response = client.put(
        "/api/v1/cash-stock/9999",
        json={"denomination": 5, "quantity": 99},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Cash Stock not found"


# TEST: Delete
def test_delete_cash_stock(client, db):
    item = create_sample_cash(db, denom=2)
    response = client.delete(f"/api/v1/cash-stock/{item.id}")
    assert response.status_code == 200
    assert response.json() == {"success": True}


def test_delete_cash_stock_not_found(client):
    response = client.delete("/api/v1/cash-stock/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cash Stock not found"
