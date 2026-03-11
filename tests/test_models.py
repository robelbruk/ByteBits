import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from models import AllItems, Customer, FoodItem, Transaction


def build_catalog() -> AllItems:
    burger = FoodItem("Spicy Burger", 9.99, "Entrees", 4.5)
    soda = FoodItem("Large Soda", 2.49, "Drinks", 4.0)
    cake = FoodItem("Chocolate Cake", 4.99, "Desserts", 4.8)
    fries = FoodItem("Fries", 3.49, "Sides", 4.2)
    return AllItems([burger, soda, cake, fries])


def test_filter_by_category():
    catalog = build_catalog()
    drinks = catalog.filterByCategory("Drinks")
    assert [item.getName() for item in drinks] == ["Large Soda"]


def test_filter_by_price_bounds():
    catalog = build_catalog()
    filtered = catalog.filterByPrice(min_price=3.00, max_price=5.00)
    assert [item.getName() for item in filtered] == ["Chocolate Cake", "Fries"]


def test_filter_by_popularity():
    catalog = build_catalog()
    popular = catalog.filterByPopularity(4.5)
    assert [item.getName() for item in popular] == ["Spicy Burger", "Chocolate Cake"]


def test_filter_items_multi_criteria():
    catalog = build_catalog()
    filtered = catalog.filterItems(category="Desserts", min_price=4.00, min_popularity=4.5)
    assert [item.getName() for item in filtered] == ["Chocolate Cake"]


def test_sorting_methods():
    catalog = build_catalog()
    assert [i.getName() for i in catalog.sortByPrice()] == [
        "Large Soda",
        "Fries",
        "Chocolate Cake",
        "Spicy Burger",
    ]
    assert [i.getName() for i in catalog.sortByPopularity()] == [
        "Chocolate Cake",
        "Spicy Burger",
        "Fries",
        "Large Soda",
    ]
    assert [i.getName() for i in catalog.sortByName()] == [
        "Chocolate Cake",
        "Fries",
        "Large Soda",
        "Spicy Burger",
    ]


def test_sort_items_with_invalid_key_raises():
    catalog = build_catalog()
    with pytest.raises(ValueError):
        catalog.sortItems(key="calories")


def test_transaction_total_add_remove_and_count():
    burger = FoodItem("Spicy Burger", 9.99, "Entrees", 4.5)
    soda = FoodItem("Large Soda", 2.49, "Drinks", 4.0)
    tx = Transaction([burger, soda])

    assert tx.getItemCount() == 2
    assert tx.getTotalCost() == 12.48

    removed = tx.removeItem("Spicy Burger")
    assert removed is True
    assert tx.getItemCount() == 1
    assert tx.getTotalCost() == 2.49

    removed_missing = tx.removeItem("Not On Menu")
    assert removed_missing is False
    assert tx.getItemCount() == 1


def test_customer_aggregate_totals():
    burger = FoodItem("Spicy Burger", 9.99, "Entrees", 4.5)
    soda = FoodItem("Large Soda", 2.49, "Drinks", 4.0)
    cake = FoodItem("Chocolate Cake", 4.99, "Desserts", 4.8)

    tx1 = Transaction([burger, soda])  # 12.48
    tx2 = Transaction([cake])  # 4.99

    customer = Customer("Alice", [tx1, tx2])
    assert customer.getLifetimeSpend() == 17.47
    assert customer.getAverageOrderValue() == 8.735


def test_customer_aggregate_with_no_history():
    customer = Customer("Empty")
    assert customer.getLifetimeSpend() == 0.0
    assert customer.getAverageOrderValue() == 0.0