from typing import Dict, List, Tuple, Optional
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.product_stock import ProductStock
from app.models.cash_stock import CashStock
from sqlalchemy.exc import SQLAlchemyError


# transform payment list -> total and a dict of counts
def payment_to_counts(payment: List[dict]) -> Tuple[int, Dict[int, int]]:
    total = 0
    counts: Dict[int, int] = {}
    for pm in payment:
        denom = int(pm["denomination"])
        count = int(pm["count"])
        if count <= 0:
            continue

        counts[denom] = counts.get(denom, 0) + count
        total += denom * count

    return total, counts


# bounded DP to find one way to make `change` using available `stock` (denom -> count)
# returns dict denom -> count or None if impossible
def make_change_bounded(change: int, stock: Dict[int, int]) -> Optional[Dict[int, int]]:
    if change == 0:
        return {}

    denoms = sorted(stock.keys(), reverse=True)

    # dp[value] = dict of denom -> count to make value (first found)
    dp: List[Optional[Dict[int, int]]] = [None] * (change + 1)
    dp[0] = {}
    for denom in denoms:
        count = stock.get(denom, 0)
        if count <= 0:
            continue

        # apply bounded count using optimized loop: for k from 1..c
        for _ in range(count):
            for v in range(change, -1, -1):
                prev = dp[v]
                if prev is not None and v + denom <= change and dp[v + denom] is None:
                    new_map = prev.copy()
                    new_map[denom] = new_map.get(denom, 0) + 1
                    dp[v + denom] = new_map

                    if v + denom == change:
                        return dp[change]

    return dp[change]


# main service function
def purchase_product(db: Session, product_id: int, payment_list: List[dict]) -> dict:
    """
    Purchase product with product_id and payment_list(dicts with denomination,count).
    Returns dict with keys: success(bool), message, price, paid, change(dict), remaining_stock
    """
    try:
        total_paid, payment_counts = payment_to_counts(payment_list)

        # get product
        product = (
            db.query(Product)
            .filter(Product.id == product_id)
            .with_for_update()
            .one_or_none()
        )
        if not product:
            return {"success": False, "message": "Product not found"}

        # get product stock
        pstock = (
            db.query(ProductStock)
            .filter(ProductStock.product_id == product_id)
            .with_for_update()
            .one_or_none()
        )
        if pstock is None:
            return {"success": False, "message": "Out of stock"}
        stock_qty = pstock.quantity
        if stock_qty <= 0:
            return {"success": False, "message": "Out of stock"}

        price = int(product.price)

        if total_paid < price:
            return {
                "success": False,
                "message": "Insufficient payment",
                "paid": total_paid,
                "price": price,
            }

        change_needed = total_paid - price

        # build current cash stock map including the inserted payment (machine receives them first)
        cash_rows = db.query(CashStock).with_for_update().all()
        cash_map: Dict[int, int] = {
            cash.denomination: cash.quantity for cash in cash_rows
        }

        # add incoming payment to cash_map (machine accepts money before computing change)
        for denom, count in payment_counts.items():
            cash_map[denom] = cash_map.get(denom, 0) + count

        # attempt to make change using cash_map
        change_map = make_change_bounded(change_needed, cash_map)
        if change_map is None:
            return {
                "success": False,
                "message": "Cannot provide change with current cash stock",
            }

        # Use transaction
        # decrement product stock
        new_stock_qty = stock_qty - 1
        pstock.quantity = new_stock_qty
        db.add(pstock)

        # update cash stock: add payment, then subtract change
        # add payment_counts already reflected in cash_map, need to persist final cash_map - subtract change_map
        for denom, count in payment_counts.items():
            row = next((r for r in cash_rows if r.denomination == denom), None)
            if row:
                row.quantity += count
            else:
                # create new CashStock
                row = CashStock(denomination=denom, quantity=count)
                db.add(row)
                cash_rows.append(row)

        # subtract change
        for denom, count in change_map.items():
            row = next((r for r in cash_rows if r.denomination == denom), None)
            if not row or row.quantity < count:
                raise RuntimeError("Inconsistent cash stock while applying change")
            row.quantity -= count

        # commit done
        db.flush()

        change_list = [
            {"denomination": denom, "count": count}
            for denom, count in change_map.items()
        ]
        return {
            "success": True,
            "message": "Purchase successful",
            "product_id": product_id,
            "paid": total_paid,
            "price": price,
            "change": change_list,
            "remaining_stock": new_stock_qty,
        }

    except SQLAlchemyError as e:
        db.rollback()
        return {"success": False, "message": f"Database error: {e}"}
    except Exception as e:
        db.rollback()
        return {"success": False, "message": f"Error: {e}"}
