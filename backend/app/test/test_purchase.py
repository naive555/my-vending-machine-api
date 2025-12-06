import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine, SessionLocal
from app.models.product import Product
from app.models.product_stock import ProductStock
from app.models.cash_stock import CashStock

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    # create all tables
    Base.metadata.create_all(bind=engine)

    # seed data
    db = SessionLocal()
    p = Product(name="Soda", price=20)
    db.add(p)
    db.commit()
    db.refresh(p)
    product_stock = ProductStock(product_id=p.id, quantity=5)
    db.add(product_stock)

    # seed some cash stock for change
    for denom, qty in [(100, 1), (50, 1), (20, 2), (10, 5), (5, 10), (2, 25), (1, 50)]:
        db.add(CashStock(denomination=denom, quantity=qty))
    db.commit()
    db.close()
    yield

    # teardown
    Base.metadata.drop_all(bind=engine)


def test_purchase_exact_money():
    # buy soda price 20 with exact 20
    payload = {"product_id": 1, "payment": [{"denomination": 20, "count": 1}]}
    res = client.post("/api/v1/purchase", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] == True
    assert data["change"] == []


def test_purchase_with_change():
    payload = {"product_id": 1, "payment": [{"denomination": 50, "count": 1}]}
    res = client.post("/api/v1/purchase", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] == True
    # change must sum to 30
    total_change = sum(i["denomination"] * i["count"] for i in data["change"])
    assert total_change == 30
