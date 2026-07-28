class Restaurant:
    our_menu = {
        "MAIN COURSE": {
            "Malakwang": 7000,
            "Pilau": 9000,
            "Dek Ngo": 8000,
            "Boo": 5000,
        },
        "SNACKS": {
            "Chapati": 3000,
            "Samosas": 2000,
            "Sausages": 5000,
        }
    }

    def __init__(self, restaurant_name):
        self.restaurant_name = restaurant_name

    def display_menu(self):
        print(f"\nWelcome to {self.restaurant_name}. ")
        print(f"Here's our Menu Layout:")
        print("=" * 35)
        for category, items in self.our_menu.items():
            print(f"\n[{category}]")
            for food_item, price in items.items():
                print(f"  * {food_item}: {price} UGX")
        print("=" * 35)


class Customer(Restaurant):
    def __init__(self, restaurant_name, name):
        super().__init__(restaurant_name)
        self.name = name
        # The cart dictionary now maps: item_name -> {"price": int, "qty": int}
        self.cart = {}

    def add_to_cart(self):
        print(f"\n--- {self.name} is adding items to their cart ---")

        # LOCAL VARIABLE: Build a lookup mapping lowercase names to (Original Name, Price)
        # No arguments needed, generated purely inside this method.
        menu_lookup = {}
        for category, items in self.our_menu.items():
            for food_item, price in items.items():
                menu_lookup[food_item.lower()] = (food_item, price)

        while True:
            # LOCAL VARIABLE: Capture user input
            choice = input("Enter item name to add (or type 'done' to stop): ").strip().lower()
            if choice == 'done':
                break

            if choice in menu_lookup:
                original_name, item_price = menu_lookup[choice]

                try:
                    qty = int(input(f"How many portions of {original_name}? "))
                    if qty <= 0:
                        print("Please enter a quantity greater than 0.")
                        continue

                    # Check if item already exists in cart to update quantity
                    if original_name in self.cart:
                        self.cart[original_name]["qty"] += qty
                    else:
                        # Storing a nested dictionary containing BOTH price and quantity
                        self.cart[original_name] = {
                            "price": item_price,
                            "qty": qty
                        }

                    print(f"Added: {qty}x {original_name} (@ {item_price} UGX each)")
                except ValueError:
                    print("Invalid amount. Please type a valid number.")
            else:
                print("Item not found. Please look at the menu spelling.")

    def show_cart(self):
        print(f"\n=== {self.name}'s Current Cart ===")
        if not self.cart:
            print("Your cart is empty.")
            return

        for item, details in self.cart.items():
            item_price = details["price"]
            quantity = details["qty"]
            item_subtotal = item_price * quantity
            print(f"  - {item} x{quantity} | Price: {item_price} UGX each | Subtotal: {item_subtotal} UGX")

    def checkout(self):
        print(f"\n====== FINAL RECEIPT FOR {self.name.upper()} ======")
        if not self.cart:
            print("Cart is empty. Nothing to bill.")
            return

        total_bill = 0
        for item, details in self.cart.items():
            item_price = details["price"]
            quantity = details["qty"]
            item_subtotal = item_price * quantity
            total_bill += item_subtotal
            print(f"  {item:<12} x{quantity:<2} @ {item_price:>5} UGX = {item_subtotal:>6} UGX")

        print("-" * 45)
        print(f"  TOTAL DUE: {total_bill} UGX")
        print("============================================")


# --- Running the Script ---

# Initialize your restaurant layout
my_restaurant = Restaurant("Jukon Diner")
my_restaurant.display_menu()

# Initialize your customer
client1 = Customer("Jukon Diner", "Byron")

# 1. Ask customer for input (stores price + qty internally)
client1.add_to_cart()

# 2. View the current items along with their saved prices
client1.show_cart()

# 3. Print the final bill summary
client1.checkout()
