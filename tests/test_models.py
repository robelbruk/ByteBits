from gettext import Catalog
from models import FoodItem, Transaction, AllItems, Customer

# 1. Create some FoodItems
burger = FoodItem("Spicy Burger", 9.99, "Entrees", 4.5)
soda = FoodItem("Large Soda", 2.49, "Drinks", 4.0)
cake = FoodItem("Chocolate Cake", 4.99, "Desserts", 4.8)

print(burger.getName(), burger.getPrice()) # Spicy Burger 9.99

# 2. Build a Catalog
catalog = AllItems([burger, soda, cake])
drinks = catalog.filterByCategory("Drinks")
print(drinks[0].getName()) # Large Soda

# 3. Create a Transaction
tx = Transaction()
tx.addItem(burger)
tx.addItem(soda)
print(tx.getTotalCost()) # 12.48

# 4. Attach to a Customer
alice = Customer("Alice")
alice.addTransaction(tx)
print(alice.getName()) # Alice
print(len(alice.getOrderHistory())) # 1
print(alice.getOrderHistory()[0].getTotalCost()) # 12.48