import pytest

from app.models.product import Product


# Helpers
def create_product(db, name="Coke", price=20, image_url=None):
    product = Product(name=name, price=price, image_url=image_url)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


# TEST: Get List
def test_list_products(client, db):

    p1 = create_product(db, "A", 10)
    p2 = create_product(db, "B", 20)

    res = client.get("/api/v1/products/")
    assert res.status_code == 200

    data = res.json()
    assert len(data) == 2
    assert {item["name"] for item in data} == {"A", "B"}


# TEST: Get one
def test_get_product(client, db):

    p = create_product(db, "Tea", 15)

    res = client.get(f"/api/v1/products/{p.id}")
    assert res.status_code == 200

    data = res.json()
    assert data["id"] == p.id
    assert data["name"] == "Tea"


def test_get_product_not_found(client, db):
    res = client.get("/api/v1/products/9999")
    assert res.status_code == 404
    assert res.json()["detail"] == "Product not found"


# TEST: Create
def test_create_product(client, db):
    res = client.post(
        "/api/v1/products/",
        json={"name": "Water", "price": 12, "image_url": "http://x.jpg"},
    )

    assert res.status_code == 200

    data = res.json()
    assert data["name"] == "Water"
    assert data["price"] == 12
    assert data["image_url"] == "http://x.jpg"


# TEST: Update
def test_update_product(client, db):

    p = create_product(db, "Old", 10)

    res = client.put(
        f"/api/v1/products/{p.id}",
        json={"name": "New", "price": 99, "image_url": "image.png"},
    )

    assert res.status_code == 200
    data = res.json()

    assert data["name"] == "New"
    assert data["price"] == 99
    assert data["image_url"] == "image.png"


def test_update_product_not_found(client, db):
    res = client.put(
        "/api/v1/products/8888",
        json={"name": "X", "price": 1, "image_url": None},
    )

    assert res.status_code == 404
    assert res.json()["detail"] == "Product not found"


# TEST: Delete product
def test_delete_product(client, db):
    p = create_product(db, "DeleteMe", 25)

    res = client.delete(f"/api/v1/products/{p.id}")
    assert res.status_code == 200
    assert res.json() == {"success": True}


def test_delete_product_not_found(client, db):
    res = client.delete("/api/v1/products/7777")
    assert res.status_code == 404
    assert res.json()["detail"] == "Product not found"
