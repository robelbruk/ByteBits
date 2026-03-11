import pytest
from models import FoodItem, Transaction, AllItems, Customer


# ── Helpers ──────────────────────────────────────────────────────────


def build_catalog() -> AllItems:
    """Reusable catalog with a mix of categories."""
    return AllItems([
        FoodItem("Burger", 10.00, "Entrees", 4.5),
        FoodItem("Pizza", 12.00, "Entrees", 4.7),
        FoodItem("Soda", 5.00, "Drinks", 3.8),
        FoodItem("Chocolate Cake", 6.50, "Desserts", 4.9),
        FoodItem("Fries", 3.50, "Sides", 4.2),
    ])


# ── User-requested tests ────────────────────────────────────────────


def test_transaction_total_two_items():
    burger = FoodItem("Burger", 10.00, "Entrees", 4.5)
    soda = FoodItem("Soda", 5.00, "Drinks", 3.8)
    tx = Transaction([burger, soda])
    assert tx.getTotalCost() == 15.00


def test_negative_price_raises():
    with pytest.raises(ValueError):
        FoodItem("Donut", -1.00, "Desserts", 3.0)


def test_filter_entrees_returns_only_main_items():
    catalog = build_catalog()
    entrees = catalog.filterByCategory("Entrees")
    names = [item.getName() for item in entrees]
    assert names == ["Burger", "Pizza"]


def test_sort_by_price_ascending():
    catalog = build_catalog()
    names = [item.getName() for item in catalog.sortByPrice()]
    assert names == ["Fries", "Soda", "Chocolate Cake", "Burger", "Pizza"]


def test_sort_by_price_descending():
    catalog = build_catalog()
    names = [item.getName() for item in catalog.sortByPrice(desc=True)]
    assert names == ["Pizza", "Burger", "Chocolate Cake", "Soda", "Fries"]


def test_sort_by_name():
    catalog = build_catalog()
    names = [item.getName() for item in catalog.sortByName()]
    assert names == ["Burger", "Chocolate Cake", "Fries", "Pizza", "Soda"]


def test_sort_by_popularity():
    catalog = build_catalog()
    names = [item.getName() for item in catalog.sortByPopularity()]
    assert names == ["Chocolate Cake", "Pizza", "Burger", "Fries", "Soda"]


# ── Additional tests ────────────────────────────────────────────────


def test_food_item_getters():
    item = FoodItem("Taco", 7.99, "Entrees", 4.3)
    assert item.getName() == "Taco"
    assert item.getPrice() == 7.99
    assert item.getCategory() == "Entrees"
    assert item.getPopularity() == 4.3


def test_zero_price_allowed():
    item = FoodItem("Free Sample", 0, "Sides", 5.0)
    assert item.getPrice() == 0


def test_empty_transaction_total():
    tx = Transaction()
    assert tx.getTotalCost() == 0.0
    assert tx.getItemCount() == 0


def test_transaction_add_and_remove():
    burger = FoodItem("Burger", 10.00, "Entrees", 4.5)
    soda = FoodItem("Soda", 5.00, "Drinks", 3.8)

    tx = Transaction()
    tx.addItem(burger)
    tx.addItem(soda)
    assert tx.getItemCount() == 2
    assert tx.getTotalCost() == 15.00

    assert tx.removeItem("Soda") is True
    assert tx.getItemCount() == 1
    assert tx.getTotalCost() == 10.00

    assert tx.removeItem("Nonexistent") is False
    assert tx.getItemCount() == 1


def test_sort_items_invalid_key_raises():
    catalog = build_catalog()
    with pytest.raises(ValueError):
        catalog.sortItems(key="calories")


def test_filter_items_multi_criteria():
    catalog = build_catalog()
    results = catalog.filterItems(category="Entrees", min_price=11.00, min_popularity=4.5)
    names = [item.getName() for item in results]
    assert names == ["Pizza"]


def test_customer_lifetime_spend_and_average():
    tx1 = Transaction([FoodItem("Burger", 10.00, "Entrees", 4.5)])
    tx2 = Transaction([FoodItem("Soda", 5.00, "Drinks", 3.8)])
    customer = Customer("Alice", [tx1, tx2])
    assert customer.getLifetimeSpend() == 15.00
    assert customer.getAverageOrderValue() == 7.50


def test_customer_no_orders():
    customer = Customer("Bob")
    assert customer.getLifetimeSpend() == 0.0
    assert customer.getAverageOrderValue() == 0.0
