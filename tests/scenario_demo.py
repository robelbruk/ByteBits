"""
Scenario: A customer browses the ByteBites menu, builds an order,
changes their mind, checks out, then comes back for a second order.
"""
from models import FoodItem, AllItems, Transaction, Customer

# --- Setup: stock the menu ---
menu = AllItems([
    FoodItem("Spicy Burger", 9.99, "Entrees", 4.5),
    FoodItem("Grilled Chicken", 11.49, "Entrees", 4.7),
    FoodItem("Large Soda", 2.49, "Drinks", 4.0),
    FoodItem("Chocolate Cake", 4.99, "Desserts", 4.8),
    FoodItem("Fries", 3.49, "Sides", 4.2),
    FoodItem("Iced Tea", 1.99, "Drinks", 3.9),
])

# --- Step 1: Add a new item to the menu ---
print("=== Step 1: Add a new item ===")
menu.addItem(FoodItem("Veggie Wrap", 8.49, "Entrees", 4.3))
entrees = menu.filterByCategory("Entrees")
print(f"Entrees on menu: {[i.getName() for i in entrees]}")

# --- Step 2: Sort the full menu by price (cheapest first) ---
print("\n=== Step 2: Sort menu by price ===")
by_price = menu.sortByPrice()
for item in by_price:
    print(f"  {item.getName():20s} ${item.getPrice():.2f}")

# --- Step 3: Filter — only highly popular items under $10 ---
print("\n=== Step 3: Filter popular items under $10 ===")
picks = menu.filterItems(min_popularity=4.2, max_price=10.00)
print(f"Matches: {[i.getName() for i in picks]}")

# --- Step 4: Customer builds an order, then removes an item ---
print("\n=== Step 4: Build an order ===")
order1 = Transaction()
order1.addItem(FoodItem("Spicy Burger", 9.99, "Entrees", 4.5))
order1.addItem(FoodItem("Fries", 3.49, "Sides", 4.2))
order1.addItem(FoodItem("Large Soda", 2.49, "Drinks", 4.0))
print(f"Items: {[i.getName() for i in order1.getItems()]}")
print(f"Total before removal: ${order1.getTotalCost():.2f}")

order1.removeItem("Large Soda")
print(f"Removed Large Soda → Total: ${order1.getTotalCost():.2f}")

# --- Step 5: Place a second order ---
print("\n=== Step 5: Second order ===")
order2 = Transaction([
    FoodItem("Chocolate Cake", 4.99, "Desserts", 4.8),
])
print(f"Order 2 total: ${order2.getTotalCost():.2f}")

# --- Step 6: Check customer history ---
print("\n=== Step 6: Customer lifetime stats ===")
customer = Customer("Alice")
customer.addTransaction(order1)
customer.addTransaction(order2)
print(f"Lifetime spend: ${customer.getLifetimeSpend():.2f}")
print(f"Average order:  ${customer.getAverageOrderValue():.2f}")
print(f"Order count:    {len(customer.getOrderHistory())}")