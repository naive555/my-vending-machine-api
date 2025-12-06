import pytest

from app.models.product import Product
from app.models.product_stock import ProductStock


# Helpers
def create_product(db, name="Coke", price=20):
    item = Product(name=name, price=price)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def create_stock(db, product_id, quantity=10):
    item = ProductStock(product_id=product_id, quantity=quantity)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# TEST: Get List
def test_list_product_stock(client, db):

    p1 = create_product(db, "A", 10)
    create_stock(db, p1.id, 5)

    p2 = create_product(db, "B", 15)
    create_stock(db, p2.id, 8)

    res = client.get("/api/v1/product-stock/")
    assert res.status_code == 200

    data = res.json()
    assert len(data) == 2
    assert {d["product_id"] for d in data} == {p1.id, p2.id}


# TEST: Create
def test_create_product_stock(client, db):
    p = create_product(db, "Snack", 25)

    res = client.post(
        "/api/v1/product-stock/", json={"product_id": p.id, "quantity": 12}
    )

    assert res.status_code == 200
    data = res.json()
    assert data["product_id"] == p.id
    assert data["quantity"] == 12


def test_create_product_stock_product_not_found(client, db):
    res = client.post(
        "/api/v1/product-stock/", json={"product_id": 999, "quantity": 10}
    )

    assert res.status_code == 404
    assert res.json()["detail"] == "Product not found"


# TEST: Update
def test_update_product_stock(client, db):

    p = create_product(db, "Tea", 18)
    create_stock(db, p.id, 5)

    res = client.put(f"/api/v1/product-stock/{p.id}", json={"quantity": 99})

    assert res.status_code == 200
    data = res.json()
    assert data["quantity"] == 99


def test_update_product_stock_not_found(client, db):
    res = client.put("/api/v1/product-stock/777", json={"quantity": 10})

    assert res.status_code == 404
    assert res.json()["detail"] == "Product stock not found"


# TEST: Delete
def test_delete_product_stock(client, db):

    p = create_product(db, "Water", 12)
    create_stock(db, p.id, 4)

    res = client.delete(f"/api/v1/product-stock/{p.id}")
    assert res.status_code == 200
    assert res.json() == {"success": True}


def test_delete_product_stock_not_found(client, db):
    res = client.delete("/api/v1/product-stock/9999")
    assert res.status_code == 404
    assert res.json()["detail"] == "Product stock not found"
