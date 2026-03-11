'''
The 4 classes designed include Customers, Food Items, AllItems, and Transactions
'''


class FoodItem:
    """A food item sold by ByteBites. Tracks name, price, category, and popularity rating."""

    def __init__(self, name: str, price: float, category: str, popularity: float):
        if price < 0:
            raise ValueError(f"Price cannot be negative: {price}")
        self._name = name
        self._price = price
        self._category = category
        self._popularity = popularity

    def getName(self) -> str:
        return self._name

    def getPrice(self) -> float:
        return self._price

    def getCategory(self) -> str:
        return self._category

    def getPopularity(self) -> float:
        return self._popularity


class Transaction:
    """Groups selected items into a single purchase. Stores items and computes total cost."""

    def __init__(self, items: list | None = None):
        self._items = list(items) if items else []
        self._totalCost = 0.0
        self.computeTotal()

    def getItems(self) -> list:
        return list(self._items)

    def getTotalCost(self) -> float:
        return self._totalCost

    def addItem(self, item: FoodItem) -> None:
        self._items.append(item)
        self.computeTotal()

    def removeItem(self, item_name: str) -> bool:
        for index, item in enumerate(self._items):
            if item.getName() == item_name:
                del self._items[index]
                self.computeTotal()
                return True
        return False

    def getItemCount(self) -> int:
        return len(self._items)

    def computeTotal(self) -> float:
        self._totalCost = sum(item.getPrice() for item in self._items)
        return self._totalCost


class AllItems:
    """Full collection of items. Holds all items and supports filtering by category."""

    def __init__(self, items: list | None = None):
        self._items = list(items) if items else []

    def getItems(self) -> list:
        return list(self._items)

    def filterByCategory(self, category: str) -> list:
        return [item for item in self._items if item.getCategory() == category]

    def filterByPrice(self, min_price: float | None = None, max_price: float | None = None) -> list:
        return [
            item for item in self._items
            if (min_price is None or item.getPrice() >= min_price)
            and (max_price is None or item.getPrice() <= max_price)
        ]

    def filterByPopularity(self, min_popularity: float) -> list:
        return [item for item in self._items if item.getPopularity() >= min_popularity]

    def filterItems(
        self,
        category: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        min_popularity: float | None = None,
    ) -> list:
        return [
            item for item in self._items
            if (category is None or item.getCategory() == category)
            and (min_price is None or item.getPrice() >= min_price)
            and (max_price is None or item.getPrice() <= max_price)
            and (min_popularity is None or item.getPopularity() >= min_popularity)
        ]

    def sortByPrice(self, desc: bool = False) -> list:
        return sorted(self._items, key=lambda item: item.getPrice(), reverse=desc)

    def sortByPopularity(self, desc: bool = True) -> list:
        return sorted(self._items, key=lambda item: item.getPopularity(), reverse=desc)

    def sortByName(self, desc: bool = False) -> list:
        return sorted(self._items, key=lambda item: item.getName(), reverse=desc)

    def sortItems(self, key: str = "name", desc: bool = False) -> list:
        valid_keys = {
            "name": lambda item: item.getName(),
            "price": lambda item: item.getPrice(),
            "popularity": lambda item: item.getPopularity(),
            "category": lambda item: item.getCategory(),
        }
        if key not in valid_keys:
            raise ValueError(f"Unsupported sort key: {key}")
        return sorted(self._items, key=valid_keys[key], reverse=desc)

    def addItem(self, item: FoodItem) -> None:
        self._items.append(item)


class Customer:
    """A ByteBites customer. Tracks name and past purchase history for verification."""

    def __init__(self, name: str, orderHistory: list | None = None):
        self._name = name
        self._orderHistory = list(orderHistory) if orderHistory else []

    def getName(self) -> str:
        return self._name

    def getOrderHistory(self) -> list:
        return list(self._orderHistory)

    def addTransaction(self, transaction: Transaction) -> None:
        self._orderHistory.append(transaction)

    def getLifetimeSpend(self) -> float:
        return sum(transaction.getTotalCost() for transaction in self._orderHistory)

    def getAverageOrderValue(self) -> float:
        if not self._orderHistory:
            return 0.0
        return self.getLifetimeSpend() / len(self._orderHistory)
