#!/usr/bin/env python3

#=================================
#Claude built this simulation
#=================================
"""
🍔 QuickBite - Food Delivery App Simulator (CLI MVP)
Features: Browse restaurants, view menus, add to cart, place orders
"""

import time
import random
from datetime import datetime

# ──────────────────────────────────────────────
# DATA
# ──────────────────────────────────────────────

RESTAURANTS = {
    1: {
        "name": "The Burger Joint",
        "cuisine": "American",
        "rating": 4.5,
        "delivery_time": "20-30 min",
        "delivery_fee": 2000,
        "min_order": 10000,
        "menu": {
            1: {"name": "Classic Burger",       "price": 15000, "description": "Beef patty, lettuce, tomato, cheese"},
            2: {"name": "BBQ Bacon Burger",     "price": 18000, "description": "Smoky BBQ sauce, crispy bacon, onion rings"},
            3: {"name": "Veggie Burger",        "price": 13000, "description": "Plant-based patty, avocado, sprouts"},
            4: {"name": "Loaded Fries",         "price": 8000,  "description": "Fries topped with cheese & jalapeños"},
            5: {"name": "Chocolate Milkshake",  "price": 7000,  "description": "Thick and creamy, made fresh"},
        },
    },
    2: {
        "name": "Spice Garden",
        "cuisine": "Indian",
        "rating": 4.7,
        "delivery_time": "30-45 min",
        "delivery_fee": 1500,
        "min_order": 15000,
        "menu": {
            1: {"name": "Butter Chicken",       "price": 18000, "description": "Creamy tomato curry with tender chicken"},
            2: {"name": "Paneer Tikka Masala",  "price": 16000, "description": "Cottage cheese in spiced gravy"},
            3: {"name": "Garlic Naan (x2)",     "price": 5000,  "description": "Soft, buttery flatbread"},
            4: {"name": "Biryani",              "price": 20000, "description": "Fragrant basmati rice with chicken & spices"},
            5: {"name": "Mango Lassi",          "price": 6000,  "description": "Chilled yogurt & mango drink"},
        },
    },
    3: {
        "name": "Kampala Pizza Co.",
        "cuisine": "Italian",
        "rating": 4.3,
        "delivery_time": "25-40 min",
        "delivery_fee": 2500,
        "min_order": 20000,
        "menu": {
            1: {"name": "Margherita Pizza",     "price": 22000, "description": "Classic tomato, mozzarella, basil"},
            2: {"name": "Pepperoni Pizza",      "price": 25000, "description": "Loaded with spicy pepperoni"},
            3: {"name": "BBQ Chicken Pizza",    "price": 27000, "description": "Tangy BBQ base with grilled chicken"},
            4: {"name": "Caesar Salad",         "price": 12000, "description": "Romaine, parmesan, croutons, dressing"},
            5: {"name": "Tiramisu",             "price": 10000, "description": "Classic Italian dessert"},
        },
    },
    4: {
        "name": "Wok & Roll",
        "cuisine": "Chinese",
        "rating": 4.1,
        "delivery_time": "20-35 min",
        "delivery_fee": 1000,
        "min_order": 12000,
        "menu": {
            1: {"name": "Kung Pao Chicken",     "price": 16000, "description": "Spicy stir-fry with peanuts & peppers"},
            2: {"name": "Fried Rice",           "price": 10000, "description": "Egg fried rice with vegetables"},
            3: {"name": "Spring Rolls (x4)",    "price": 8000,  "description": "Crispy rolls with veggie filling"},
            4: {"name": "Sweet & Sour Pork",    "price": 17000, "description": "Tender pork in tangy sauce"},
            5: {"name": "Dim Sum Basket",       "price": 14000, "description": "Assorted steamed dumplings"},
        },
    },
}

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────

def clear():
    print("\n" + "═" * 55)

def fmt_ugx(amount):
    return f"UGX {amount:,}"

def pause():
    input("\n  Press Enter to continue...")

def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"  ⚠  Please enter a number between {lo} and {hi}.")
        except ValueError:
            print("  ⚠  Invalid input. Please enter a number.")

# ──────────────────────────────────────────────
# SCREENS
# ──────────────────────────────────────────────

def show_banner():
    print("""
╔═══════════════════════════════════════════════════╗
║        🛵  QuickBite Food Delivery  🍔            ║
║         Fast. Fresh. Delivered to you.            ║
╚═══════════════════════════════════════════════════╝""")

def show_restaurants():
    clear()
    print("\n  📍 Restaurants Near You\n")
    print(f"  {'#':<4} {'Restaurant':<22} {'Cuisine':<12} {'Rating':<8} {'ETA':<15} {'Min Order'}")
    print("  " + "─" * 72)
    for rid, r in RESTAURANTS.items():
        stars = "★" * int(r["rating"]) + "☆" * (5 - int(r["rating"]))
        print(f"  {rid:<4} {r['name']:<22} {r['cuisine']:<12} {r['rating']:<4} {stars:<4}  {r['delivery_time']:<15} {fmt_ugx(r['min_order'])}")

def show_menu(restaurant):
    clear()
    r = restaurant
    print(f"\n  🍽  {r['name']}  —  {r['cuisine']}")
    print(f"  ⏱  {r['delivery_time']}   |   🚴 Delivery: {fmt_ugx(r['delivery_fee'])}   |   ⭐ {r['rating']}\n")
    print(f"  {'#':<4} {'Item':<26} {'Price':<12} Description")
    print("  " + "─" * 68)
    for mid, item in r["menu"].items():
        print(f"  {mid:<4} {item['name']:<26} {fmt_ugx(item['price']):<12} {item['description']}")

def show_cart(cart, restaurant):
    if not cart:
        print("\n  🛒 Your cart is empty.")
        return
    clear()
    print(f"\n  🛒 Your Cart  —  {restaurant['name']}\n")
    subtotal = 0
    for item_id, qty in cart.items():
        item = restaurant["menu"][item_id]
        line = item["price"] * qty
        subtotal += line
        print(f"  • {item['name']:<26} x{qty}  =  {fmt_ugx(line)}")
    delivery = restaurant["delivery_fee"]
    total = subtotal + delivery
    print("\n  " + "─" * 42)
    print(f"  Subtotal:      {fmt_ugx(subtotal):>12}")
    print(f"  Delivery fee:  {fmt_ugx(delivery):>12}")
    print(f"  TOTAL:         {fmt_ugx(total):>12}")
    return subtotal, total

def simulate_order(restaurant, total):
    clear()
    print("\n  ✅ Order placed successfully!\n")
    order_id = f"QB-{random.randint(10000,99999)}"
    now = datetime.now().strftime("%H:%M")
    print(f"  Order ID   : {order_id}")
    print(f"  Restaurant : {restaurant['name']}")
    print(f"  Total paid : {fmt_ugx(total)}")
    print(f"  Placed at  : {now}")
    print(f"  ETA        : {restaurant['delivery_time']}\n")

    stages = [
        ("📋", "Order confirmed by restaurant"),
        ("👨‍🍳", "Your food is being prepared"),
        ("📦", "Order packed and ready"),
        ("🛵", "Rider picked up your order"),
        ("🏠", "Delivered! Enjoy your meal 🎉"),
    ]
    for icon, msg in stages:
        time.sleep(0.6)
        print(f"  {icon}  {msg}")

# ──────────────────────────────────────────────
# MAIN FLOW
# ──────────────────────────────────────────────

def restaurant_flow(rid):
    restaurant = RESTAURANTS[rid]
    cart = {}

    while True:
        show_menu(restaurant)
        print("\n  Options:")
        print("  [1-5] Add item to cart   [6] View cart   [0] Back to restaurants\n")
        choice = get_int("  Your choice: ", 0, 6)

        if choice == 0:
            break

        elif 1 <= choice <= 5:
            item = restaurant["menu"][choice]
            qty = get_int(f"  How many '{item['name']}'? (1-10): ", 1, 10)
            cart[choice] = cart.get(choice, 0) + qty
            print(f"\n  ✔  Added {qty}× {item['name']} to cart.")
            time.sleep(0.8)

        elif choice == 6:
            if not cart:
                print("\n  🛒 Your cart is empty. Add some items first!")
                pause()
                continue

            result = show_cart(cart, restaurant)
            if result is None:
                pause()
                continue
            subtotal, total = result

            if subtotal < restaurant["min_order"]:
                print(f"\n  ⚠  Minimum order is {fmt_ugx(restaurant['min_order'])}. Add more items.")
                pause()
                continue

            print("\n  [1] Place Order   [2] Clear Cart   [0] Keep Shopping")
            action = get_int("  Your choice: ", 0, 2)

            if action == 1:
                simulate_order(restaurant, total)
                pause()
                return  # back to main menu after order
            elif action == 2:
                cart.clear()
                print("\n  🗑  Cart cleared.")
                time.sleep(0.8)

def main():
    show_banner()
    print("\n  Welcome! Browse restaurants and order your favourite meal.\n")
    time.sleep(1)

    while True:
        show_restaurants()
        print("\n  [1-4] Select a restaurant   [0] Quit\n")
        choice = get_int("  Your choice: ", 0, 4)

        if choice == 0:
            clear()
            print("\n  👋 Thanks for using QuickBite. See you next time!\n")
            break

        restaurant_flow(choice)

if __name__ == "__main__":
    main()