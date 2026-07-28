#!/usr/bin/env python3

#=====================================
#This Simulation was created by Claude
#=====================================
"""
🍽️  TableTurn — Casual Dining Restaurant Simulator
Simulates a full day of restaurant operations:
  • Staff shifts & roles
  • Table management & reservations
  • Kitchen queue & order flow
  • Inventory & ingredient tracking
  • Daily financial report (P&L)
"""

import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

# ═══════════════════════════════════════════════════════════
#  CONSTANTS & CONFIG
# ═══════════════════════════════════════════════════════════

RESTAURANT_NAME = "The Olive Fork"
CURRENCY = "UGX"
SEATING_CAPACITY = 40   # 10 tables × 4 seats

SHIFTS = {
    "Morning Prep":  ("06:00", "10:00"),
    "Lunch Service": ("10:00", "15:00"),
    "Dinner Service":("15:00", "22:00"),
    "Close & Clean": ("22:00", "23:30"),
}

ROLES = {
    "Head Chef":        {"wage_per_hour": 8000,  "dept": "Kitchen"},
    "Sous Chef":        {"wage_per_hour": 5500,  "dept": "Kitchen"},
    "Line Cook":        {"wage_per_hour": 4000,  "dept": "Kitchen"},
    "Dishwasher":       {"wage_per_hour": 2500,  "dept": "Kitchen"},
    "Restaurant Manager":{"wage_per_hour": 9000, "dept": "FOH"},
    "Waiter/Waitress":  {"wage_per_hour": 3500,  "dept": "FOH"},
    "Cashier":          {"wage_per_hour": 3000,  "dept": "FOH"},
    "Bartender":        {"wage_per_hour": 4500,  "dept": "FOH"},
    "Host/Hostess":     {"wage_per_hour": 3000,  "dept": "FOH"},
    "Security":         {"wage_per_hour": 2800,  "dept": "FOH"},
}

# Menu: item -> {price, ingredients: {ingredient: grams}, prep_minutes}
MENU = {
    "Grilled Tilapia":       {"price": 28000, "prep": 18, "ingredients": {"tilapia_fillet":300,"tomatoes":80,"onion":60,"cooking_oil":30,"spices":10}},
    "Beef Stew & Rice":      {"price": 22000, "prep": 15, "ingredients": {"beef":250,"rice":200,"carrots":80,"onion":60,"spices":15}},
    "Rolex (Egg Roll)":      {"price": 8000,  "prep": 8,  "ingredients": {"eggs":100,"chapati_flour":120,"cabbage":60,"tomatoes":50,"cooking_oil":20}},
    "Chicken Burger":        {"price": 18000, "prep": 12, "ingredients": {"chicken_breast":180,"burger_bun":80,"lettuce":40,"tomatoes":60,"cooking_oil":25}},
    "Veggie Pasta":          {"price": 16000, "prep": 14, "ingredients": {"pasta":200,"tomatoes":150,"onion":60,"garlic":20,"cooking_oil":25,"spices":10}},
    "Goat Meat Stew":        {"price": 30000, "prep": 25, "ingredients": {"goat_meat":280,"potatoes":200,"onion":80,"tomatoes":100,"spices":20}},
    "Pilao Rice & Chicken":  {"price": 25000, "prep": 20, "ingredients": {"chicken_breast":200,"rice":250,"spices":30,"onion":80,"tomatoes":80}},
    "Fresh Juice (Passion)": {"price": 6000,  "prep": 4,  "ingredients": {"passion_fruit":200,"sugar":30}},
    "Sodas":                 {"price": 3500,  "prep": 1,  "ingredients": {}},
    "Mineral Water":         {"price": 2000,  "prep": 1,  "ingredients": {}},
}

# Inventory: ingredient -> {stock_grams, reorder_at, cost_per_gram}
INVENTORY = {
    "tilapia_fillet":  {"stock": 4000,  "reorder_at": 600,  "cost_per_g": 12},
    "beef":            {"stock": 5000,  "reorder_at": 500,  "cost_per_g": 14},
    "goat_meat":       {"stock": 3500,  "reorder_at": 500,  "cost_per_g": 13},
    "chicken_breast":  {"stock": 6000,  "reorder_at": 800,  "cost_per_g": 10},
    "rice":            {"stock": 10000, "reorder_at": 2000, "cost_per_g": 2},
    "pasta":           {"stock": 5000,  "reorder_at": 1000, "cost_per_g": 3},
    "tomatoes":        {"stock": 8000,  "reorder_at": 1500, "cost_per_g": 1},
    "onion":           {"stock": 6000,  "reorder_at": 1000, "cost_per_g": 1},
    "potatoes":        {"stock": 5000,  "reorder_at": 800,  "cost_per_g": 1},
    "carrots":         {"stock": 3000,  "reorder_at": 500,  "cost_per_g": 1},
    "eggs":            {"stock": 3000,  "reorder_at": 600,  "cost_per_g": 4},
    "chapati_flour":   {"stock": 5000,  "reorder_at": 800,  "cost_per_g": 2},
    "burger_bun":      {"stock": 2000,  "reorder_at": 400,  "cost_per_g": 5},
    "lettuce":         {"stock": 2000,  "reorder_at": 300,  "cost_per_g": 2},
    "cabbage":         {"stock": 3000,  "reorder_at": 500,  "cost_per_g": 1},
    "garlic":          {"stock": 1000,  "reorder_at": 200,  "cost_per_g": 4},
    "cooking_oil":     {"stock": 4000,  "reorder_at": 500,  "cost_per_g": 3},
    "spices":          {"stock": 2000,  "reorder_at": 300,  "cost_per_g": 8},
    "passion_fruit":   {"stock": 4000,  "reorder_at": 500,  "cost_per_g": 2},
    "sugar":           {"stock": 3000,  "reorder_at": 400,  "cost_per_g": 2},
}

FIXED_COSTS = {
    "Rent":            850000,
    "Electricity":     180000,
    "Water":           45000,
    "Gas / LPG":       90000,
    "Internet & POS":  35000,
    "Licenses & Fees": 20000,
}

# ═══════════════════════════════════════════════════════════
#  DATA CLASSES
# ═══════════════════════════════════════════════════════════

@dataclass
class Staff:
    name: str
    role: str
    shift: str
    hours_worked: float = 0.0

    @property
    def wage_per_hour(self):
        return ROLES[self.role]["wage_per_hour"]

    @property
    def dept(self):
        return ROLES[self.role]["dept"]

    @property
    def daily_wage(self):
        shift_hours = {
            "Morning Prep": 4, "Lunch Service": 5,
            "Dinner Service": 7, "Close & Clean": 1.5
        }
        return self.wage_per_hour * shift_hours.get(self.shift, 4)


@dataclass
class Table:
    number: int
    seats: int = 4
    status: str = "empty"   # empty | occupied | reserved | needs_cleaning
    party_size: int = 0
    order_ids: List[int] = field(default_factory=list)


@dataclass
class Order:
    order_id: int
    table_number: int
    items: Dict[str, int]   # item_name -> qty
    status: str = "received"  # received | in_kitchen | ready | served | paid
    time_placed: str = ""
    waiter: str = ""

    @property
    def subtotal(self):
        return sum(MENU[item]["price"] * qty for item, qty in self.items.items())

    @property
    def total_with_tax(self):
        return int(self.subtotal * 1.18)   # 18% VAT


# ═══════════════════════════════════════════════════════════
#  RESTAURANT STATE
# ═══════════════════════════════════════════════════════════

class Restaurant:
    def __init__(self):
        self.tables: Dict[int, Table] = {i: Table(i) for i in range(1, 11)}
        self.staff: List[Staff] = []
        self.orders: List[Order] = []
        self.kitchen_queue: List[int] = []   # order_ids
        self.inventory = {k: dict(v) for k, v in INVENTORY.items()}
        self.order_counter = 1
        self.revenue = 0
        self.ingredient_cost = 0
        self.waste_cost = 0
        self.low_stock_alerts: List[str] = []
        self.events_log: List[str] = []
        self.current_time = "10:00"
        self.sim_day = datetime.now().strftime("%A, %d %B %Y")

    def log(self, msg):
        self.events_log.append(f"  [{self.current_time}] {msg}")

    def get_order(self, oid) -> Optional[Order]:
        return next((o for o in self.orders if o.order_id == oid), None)


# ═══════════════════════════════════════════════════════════
#  DISPLAY HELPERS
# ═══════════════════════════════════════════════════════════

def sep(char="═", width=60):
    print(char * width)

def header(title):
    sep()
    print(f"  {title}")
    sep()

def fmt(amount):
    return f"{CURRENCY} {amount:,}"

def pause():
    input("\n  ► Press Enter to continue...")

def get_int(prompt, lo, hi):
    while True:
        try:
            v = int(input(prompt))
            if lo <= v <= hi:
                return v
            print(f"  ⚠  Enter a number between {lo} and {hi}.")
        except ValueError:
            print("  ⚠  Numbers only please.")

def get_str(prompt, options=None):
    while True:
        v = input(prompt).strip()
        if not options or v in options:
            return v
        print(f"  ⚠  Choose from: {', '.join(options)}")

# ═══════════════════════════════════════════════════════════
#  SECTION 1 — STAFF MANAGEMENT
# ═══════════════════════════════════════════════════════════

FIRST_NAMES = ["Aisha","Brian","Christine","Daniel","Esther","Francis",
               "Grace","Henry","Irene","Julius","Kylie","Liam","Mary",
               "Nathan","Olivia","Patrick","Quickie","Ronald","Sarah","Tom"]

def staff_menu(rest: Restaurant):
    while True:
        header("👥  STAFF MANAGEMENT")
        print(f"  Current staff on roster: {len(rest.staff)}\n")
        print("  [1] Hire staff (auto-generate)")
        print("  [2] View all staff & wages")
        print("  [3] View staff by department")
        print("  [4] View shift schedule")
        print("  [0] Back to main menu\n")
        ch = get_int("  Choice: ", 0, 4)

        if ch == 0:
            break
        elif ch == 1:
            hire_staff(rest)
        elif ch == 2:
            view_all_staff(rest)
        elif ch == 3:
            view_by_dept(rest)
        elif ch == 4:
            view_schedule(rest)


def hire_staff(rest: Restaurant):
    header("  ➕ Hire Staff")
    print("  Roles available:\n")
    roles = list(ROLES.keys())
    for i, r in enumerate(roles, 1):
        info = ROLES[r]
        print(f"  [{i:>2}] {r:<25}  {fmt(info['wage_per_hour'])}/hr   ({info['dept']})")

    print(f"\n  [ 0] Cancel\n")
    choice = get_int("  Select role: ", 0, len(roles))
    if choice == 0:
        return

    role = roles[choice - 1]
    name = random.choice(FIRST_NAMES) + " " + random.choice(["Okello","Nakato","Ssemwogerere","Atuhe","Mugisha","Namubiru","Kibuuka"])
    shifts = list(SHIFTS.keys())
    print(f"\n  Shifts:\n")
    for i, s in enumerate(shifts, 1):
        t = SHIFTS[s]
        print(f"  [{i}] {s:<20} ({t[0]} – {t[1]})")
    sc = get_int("\n  Assign shift: ", 1, len(shifts))
    shift = shifts[sc - 1]
    emp = Staff(name=name, role=role, shift=shift)
    rest.staff.append(emp)
    rest.log(f"Hired {name} as {role} on {shift}")
    print(f"\n  ✅  {name} hired as {role} on {shift}.")
    time.sleep(0.6)


def view_all_staff(rest: Restaurant):
    header("  📋 All Staff — Daily Wages")
    if not rest.staff:
        print("  No staff hired yet.")
        pause()
        return
    total_wages = 0
    print(f"  {'Name':<28} {'Role':<22} {'Shift':<18} {'Daily Wage'}")
    print("  " + "─" * 82)
    for s in rest.staff:
        dw = s.daily_wage
        total_wages += dw
        print(f"  {s.name:<28} {s.role:<22} {s.shift:<18} {fmt(dw)}")
    print("\n  " + "─" * 82)
    print(f"  {'TOTAL DAILY WAGE BILL':<68} {fmt(total_wages)}")
    pause()


def view_by_dept(rest: Restaurant):
    header("  🏢 Staff by Department")
    depts = defaultdict(list)
    for s in rest.staff:
        depts[s.dept].append(s)
    for dept, members in depts.items():
        print(f"\n  ── {dept} ──")
        for s in members:
            print(f"     • {s.name:<25} {s.role}")
    if not rest.staff:
        print("  No staff hired yet.")
    pause()


def view_schedule(rest: Restaurant):
    header("  🗓  Shift Schedule")
    for shift, (start, end) in SHIFTS.items():
        assigned = [s for s in rest.staff if s.shift == shift]
        print(f"\n  {shift}  ({start} – {end})")
        if assigned:
            for s in assigned:
                print(f"     {'✓'} {s.name:<25} — {s.role}")
        else:
            print(f"     ⚠  No staff assigned to this shift!")
    pause()


# ═══════════════════════════════════════════════════════════
#  SECTION 2 — TABLE & RESERVATION MANAGEMENT
# ═══════════════════════════════════════════════════════════

def tables_menu(rest: Restaurant):
    while True:
        header("🪑  TABLE MANAGEMENT")
        _print_floor_plan(rest)
        print("\n  [1] Seat a walk-in party")
        print("  [2] Mark table as needs cleaning")
        print("  [3] Clear / reset a table")
        print("  [4] View all table statuses")
        print("  [0] Back\n")
        ch = get_int("  Choice: ", 0, 4)

        if ch == 0:
            break
        elif ch == 1:
            seat_party(rest)
        elif ch == 2:
            flag_table(rest, "needs_cleaning")
        elif ch == 3:
            flag_table(rest, "empty")
        elif ch == 4:
            view_tables(rest)


def _print_floor_plan(rest: Restaurant):
    icons = {"empty": "⬜", "occupied": "🟥", "reserved": "🟨", "needs_cleaning": "🟫"}
    labels = {"empty": "Empty", "occupied": "Occupied",
              "reserved": "Reserved", "needs_cleaning": "Needs Clean"}
    print("\n  ── Floor Plan ──")
    row = "  "
    for i, t in rest.tables.items():
        row += f"{icons[t.status]} T{t.number:<2}  "
        if i % 5 == 0:
            print(row)
            row = "  "
    print(f"\n  Legend: " + "  ".join(f"{v} {labels[v]}" for v in icons.values()))


def seat_party(rest: Restaurant):
    empty = [t for t in rest.tables.values() if t.status == "empty"]
    if not empty:
        print("\n  ⚠  No empty tables available right now!")
        pause()
        return
    header("  🪑 Seat a Party")
    size = get_int("  Party size (1–4): ", 1, 4)
    available = [t for t in empty if t.seats >= size]
    if not available:
        print("\n  ⚠  No table fits that party size.")
        pause()
        return
    table = available[0]
    table.status = "occupied"
    table.party_size = size
    rest.log(f"Party of {size} seated at Table {table.number}")
    print(f"\n  ✅  Party of {size} seated at Table {table.number}.")
    time.sleep(0.5)


def flag_table(rest: Restaurant, new_status: str):
    tnum = get_int("  Table number (1–10): ", 1, 10)
    rest.tables[tnum].status = new_status
    if new_status == "empty":
        rest.tables[tnum].party_size = 0
        rest.tables[tnum].order_ids = []
    rest.log(f"Table {tnum} set to '{new_status}'")
    print(f"  ✔  Table {tnum} → {new_status}")
    time.sleep(0.4)


def view_tables(rest: Restaurant):
    header("  🪑 All Tables")
    print(f"  {'Table':<8} {'Status':<16} {'Party Size':<12} {'Open Orders'}")
    print("  " + "─" * 50)
    for t in rest.tables.values():
        orders = len(t.order_ids)
        print(f"  {t.number:<8} {t.status:<16} {t.party_size if t.party_size else '—':<12} {orders}")
    pause()


# ═══════════════════════════════════════════════════════════
#  SECTION 3 — ORDERING & KITCHEN
# ═══════════════════════════════════════════════════════════

def orders_menu(rest: Restaurant):
    while True:
        header("📋  ORDERS & KITCHEN")
        pending = [o for o in rest.orders if o.status not in ("served", "paid")]
        print(f"  Active orders: {len(pending)}   |   Kitchen queue: {len(rest.kitchen_queue)}\n")
        print("  [1] Take a new order")
        print("  [2] View kitchen queue")
        print("  [3] Mark order as ready (kitchen done)")
        print("  [4] Mark order as served")
        print("  [5] Process bill / payment")
        print("  [6] View all orders today")
        print("  [0] Back\n")
        ch = get_int("  Choice: ", 0, 6)

        if ch == 0:
            break
        elif ch == 1:
            take_order(rest)
        elif ch == 2:
            view_kitchen(rest)
        elif ch == 3:
            advance_order(rest, "in_kitchen", "ready")
        elif ch == 4:
            advance_order(rest, "ready", "served")
        elif ch == 5:
            process_bill(rest)
        elif ch == 6:
            view_all_orders(rest)


def take_order(rest: Restaurant):
    occupied = [t for t in rest.tables.values() if t.status == "occupied"]
    if not occupied:
        print("\n  ⚠  No occupied tables. Seat a party first!")
        pause()
        return

    header("  📝 New Order")
    print("  Occupied tables: " + ", ".join(str(t.number) for t in occupied))
    tnum = get_int("  Table number: ", 1, 10)
    table = rest.tables[tnum]
    if table.status != "occupied":
        print("  ⚠  That table is not occupied.")
        pause()
        return

    # Pick waiter
    waiters = [s for s in rest.staff if s.role == "Waiter/Waitress"]
    waiter_name = waiters[0].name if waiters else "Self-service"

    # Build order
    items = {}
    menu_items = list(MENU.keys())
    print(f"\n  ── Menu ──\n")
    for i, (item, info) in enumerate(MENU.items(), 1):
        avail = _can_make(rest, item, 1)
        status = "✓" if avail else "✗ OUT"
        print(f"  [{i:>2}] {item:<28} {fmt(info['price'])}   {status}")

    print(f"\n  Enter item numbers and quantities. Type 0 when done.\n")
    while True:
        ic = get_int("  Item # (0 to finish): ", 0, len(menu_items))
        if ic == 0:
            break
        item_name = menu_items[ic - 1]
        if not _can_make(rest, item_name, 1):
            print(f"  ⚠  {item_name} cannot be made — insufficient ingredients.")
            continue
        qty = get_int(f"  Qty for '{item_name}': ", 1, 10)
        if not _can_make(rest, item_name, qty):
            print(f"  ⚠  Not enough ingredients for {qty}×.")
            continue
        items[item_name] = items.get(item_name, 0) + qty

    if not items:
        print("  ℹ  No items added.")
        return

    # Deduct inventory
    for item, qty in items.items():
        _deduct_ingredients(rest, item, qty)

    order = Order(
        order_id=rest.order_counter,
        table_number=tnum,
        items=items,
        status="received",
        time_placed=rest.current_time,
        waiter=waiter_name,
    )
    rest.order_counter += 1
    rest.orders.append(order)
    rest.kitchen_queue.append(order.order_id)
    table.order_ids.append(order.order_id)
    order.status = "in_kitchen"

    rest.log(f"Order #{order.order_id} placed — Table {tnum} — {waiter_name}")
    print(f"\n  ✅  Order #{order.order_id} sent to kitchen.")
    print(f"  Items: {', '.join(f'{q}× {n}' for n,q in items.items())}")
    print(f"  Est. total: {fmt(order.total_with_tax)} (incl. 18% VAT)")
    time.sleep(0.5)


def _can_make(rest: Restaurant, item: str, qty: int) -> bool:
    for ing, grams in MENU[item]["ingredients"].items():
        if rest.inventory.get(ing, {}).get("stock", 0) < grams * qty:
            return False
    return True


def _deduct_ingredients(rest: Restaurant, item: str, qty: int):
    for ing, grams in MENU[item]["ingredients"].items():
        if ing in rest.inventory:
            used = grams * qty
            rest.inventory[ing]["stock"] -= used
            cost = used * rest.inventory[ing]["cost_per_g"]
            rest.ingredient_cost += cost
            if rest.inventory[ing]["stock"] <= rest.inventory[ing]["reorder_at"]:
                alert = f"LOW STOCK: {ing} ({rest.inventory[ing]['stock']}g remaining)"
                if alert not in rest.low_stock_alerts:
                    rest.low_stock_alerts.append(alert)


def view_kitchen(rest: Restaurant):
    header("  👨‍🍳 Kitchen Queue")
    in_kitchen = [o for o in rest.orders if o.status == "in_kitchen"]
    if not in_kitchen:
        print("  ✅  Kitchen is clear — no active orders.")
    else:
        print(f"  {'Order #':<10} {'Table':<8} {'Items':<35} {'Est. Prep'}")
        print("  " + "─" * 65)
        for o in in_kitchen:
            items_str = ", ".join(f"{q}×{n[:12]}" for n, q in o.items.items())
            max_prep = max(MENU[n]["prep"] for n in o.items)
            print(f"  #{o.order_id:<9} T{o.table_number:<7} {items_str[:35]:<35} ~{max_prep} min")
    pause()


def advance_order(rest: Restaurant, from_status: str, to_status: str):
    eligible = [o for o in rest.orders if o.status == from_status]
    if not eligible:
        print(f"\n  ℹ  No orders with status '{from_status}'.")
        pause()
        return
    header(f"  🔄 Mark '{from_status}' → '{to_status}'")
    for o in eligible:
        print(f"  #{o.order_id}  Table {o.table_number}  —  {', '.join(o.items)}")
    oid = get_int("\n  Order # to advance: ", 1, rest.order_counter - 1)
    order = rest.get_order(oid)
    if not order or order.status != from_status:
        print("  ⚠  Order not found or wrong status.")
    else:
        order.status = to_status
        if oid in rest.kitchen_queue:
            rest.kitchen_queue.remove(oid)
        rest.log(f"Order #{oid} → {to_status}")
        print(f"  ✅  Order #{oid} marked as '{to_status}'.")
    time.sleep(0.4)


def process_bill(rest: Restaurant):
    served = [o for o in rest.orders if o.status == "served"]
    if not served:
        print("\n  ℹ  No served orders awaiting payment.")
        pause()
        return
    header("  💳 Process Bill")
    for o in served:
        print(f"  #{o.order_id}  Table {o.table_number}  —  {fmt(o.total_with_tax)}")
    oid = get_int("\n  Order # to settle: ", 1, rest.order_counter - 1)
    order = rest.get_order(oid)
    if not order or order.status != "served":
        print("  ⚠  Not found or not ready for payment.")
    else:
        order.status = "paid"
        rest.revenue += order.total_with_tax
        table = rest.tables[order.table_number]
        table.status = "needs_cleaning"
        table.party_size = 0
        rest.log(f"Order #{oid} PAID — {fmt(order.total_with_tax)}")
        print(f"\n  💰  Payment received: {fmt(order.total_with_tax)}")
        print(f"  Table {order.table_number} flagged for cleaning.")
    time.sleep(0.5)


def view_all_orders(rest: Restaurant):
    header("  📋 All Orders Today")
    if not rest.orders:
        print("  No orders placed yet.")
        pause()
        return
    print(f"  {'#':<6} {'Table':<7} {'Status':<14} {'Items':<30} {'Total'}")
    print("  " + "─" * 72)
    for o in rest.orders:
        items_str = ", ".join(f"{q}×{n[:10]}" for n, q in o.items.items())
        print(f"  #{o.order_id:<5} T{o.table_number:<6} {o.status:<14} {items_str[:30]:<30} {fmt(o.total_with_tax)}")
    pause()


# ═══════════════════════════════════════════════════════════
#  SECTION 4 — INVENTORY
# ═══════════════════════════════════════════════════════════

def inventory_menu(rest: Restaurant):
    while True:
        header("🥩  INVENTORY & STOCK")
        print("  [1] View all inventory levels")
        print("  [2] Restock an ingredient")
        print("  [3] View low-stock alerts")
        print("  [4] Simulate food waste")
        print("  [0] Back\n")
        ch = get_int("  Choice: ", 0, 4)
        if ch == 0:
            break
        elif ch == 1:
            view_inventory(rest)
        elif ch == 2:
            restock(rest)
        elif ch == 3:
            view_alerts(rest)
        elif ch == 4:
            simulate_waste(rest)


def view_inventory(rest: Restaurant):
    header("  📦 Inventory Levels")
    print(f"  {'Ingredient':<22} {'Stock (g)':<12} {'Reorder At':<14} {'Status'}")
    print("  " + "─" * 60)
    for ing, data in rest.inventory.items():
        stock = data["stock"]
        reorder = data["reorder_at"]
        status = "🔴 LOW" if stock <= reorder else "🟢 OK"
        print(f"  {ing:<22} {stock:<12,} {reorder:<14,} {status}")
    pause()


def restock(rest: Restaurant):
    header("  🔄 Restock Ingredient")
    ings = list(rest.inventory.keys())
    for i, ing in enumerate(ings, 1):
        print(f"  [{i:>2}] {ing}")
    idx = get_int("\n  Select ingredient: ", 1, len(ings))
    ing = ings[idx - 1]
    qty = get_int(f"  How many grams to add? ", 100, 50000)
    cost = qty * rest.inventory[ing]["cost_per_g"]
    rest.inventory[ing]["stock"] += qty
    rest.ingredient_cost += cost
    rest.log(f"Restocked {qty}g of {ing} — cost {fmt(cost)}")
    print(f"  ✅  Added {qty:,}g of {ing}. Cost: {fmt(cost)}")
    time.sleep(0.4)


def view_alerts(rest: Restaurant):
    header("  🚨 Low Stock Alerts")
    _check_all_stock(rest)
    if not rest.low_stock_alerts:
        print("  ✅  All ingredients are sufficiently stocked.")
    else:
        for a in rest.low_stock_alerts:
            print(f"  ⚠  {a}")
    pause()


def _check_all_stock(rest: Restaurant):
    for ing, data in rest.inventory.items():
        if data["stock"] <= data["reorder_at"]:
            alert = f"LOW STOCK: {ing} ({data['stock']}g remaining)"
            if alert not in rest.low_stock_alerts:
                rest.low_stock_alerts.append(alert)


def simulate_waste(rest: Restaurant):
    header("  🗑  Simulate Food Waste")
    waste_items = random.sample(list(rest.inventory.keys()), k=3)
    total_waste_cost = 0
    print("  Simulating end-of-day spoilage...\n")
    for ing in waste_items:
        waste_g = random.randint(100, 500)
        waste_g = min(waste_g, rest.inventory[ing]["stock"])
        cost = waste_g * rest.inventory[ing]["cost_per_g"]
        rest.inventory[ing]["stock"] -= waste_g
        rest.waste_cost += cost
        total_waste_cost += cost
        print(f"  🗑  {ing}: {waste_g}g wasted — {fmt(cost)}")
    rest.log(f"Food waste event — total cost {fmt(total_waste_cost)}")
    print(f"\n  Total waste cost today: {fmt(rest.waste_cost)}")
    pause()


# ═══════════════════════════════════════════════════════════
#  SECTION 5 — SIMULATE A SERVICE PERIOD (AUTO)
# ═══════════════════════════════════════════════════════════

def auto_simulate(rest: Restaurant):
    header("⚡  AUTO-SIMULATE A SERVICE PERIOD")
    print("  This runs a lunch or dinner service automatically.\n")
    print("  [1] Lunch Service (10:00 – 15:00)")
    print("  [2] Dinner Service (17:00 – 22:00)")
    print("  [0] Cancel\n")
    ch = get_int("  Choice: ", 0, 2)
    if ch == 0:
        return

    service = "Lunch" if ch == 1 else "Dinner"
    hours = ["11:00","12:00","13:00","14:00"] if ch == 1 else ["18:00","19:00","20:00","21:00"]

    print(f"\n  🚀 Starting {service} Service...\n")
    time.sleep(0.5)

    # Ensure some waiters exist
    waiters = [s for s in rest.staff if s.role == "Waiter/Waitress"]
    if not waiters:
        rest.staff.append(Staff("Auto Waiter", "Waiter/Waitress", "Lunch Service"))
        waiters = [rest.staff[-1]]

    menu_items = [m for m in MENU.keys()]
    tables_used = list(rest.tables.values())

    for hour in hours:
        rest.current_time = hour
        # Seat some tables
        for table in random.sample(tables_used, k=random.randint(2, 5)):
            if table.status == "empty":
                table.status = "occupied"
                table.party_size = random.randint(1, 4)

        # Place orders for occupied tables without orders
        for table in rest.tables.values():
            if table.status == "occupied" and not table.order_ids:
                items = {}
                for _ in range(random.randint(1, 3)):
                    item = random.choice(menu_items)
                    qty = random.randint(1, table.party_size)
                    if _can_make(rest, item, qty):
                        items[item] = items.get(item, 0) + qty
                        _deduct_ingredients(rest, item, qty)
                if items:
                    order = Order(
                        order_id=rest.order_counter,
                        table_number=table.number,
                        items=items,
                        status="in_kitchen",
                        time_placed=hour,
                        waiter=random.choice(waiters).name,
                    )
                    rest.order_counter += 1
                    rest.orders.append(order)
                    table.order_ids.append(order.order_id)
                    rest.log(f"[AUTO] Order #{order.order_id} — Table {table.number}")

        # Advance kitchen orders to served
        for order in rest.orders:
            if order.status == "in_kitchen" and random.random() > 0.3:
                order.status = "served"
                rest.log(f"[AUTO] Order #{order.order_id} served")

        # Collect payment for served orders
        for order in rest.orders:
            if order.status == "served" and random.random() > 0.4:
                order.status = "paid"
                rest.revenue += order.total_with_tax
                rest.tables[order.table_number].status = "needs_cleaning"
                rest.log(f"[AUTO] Order #{order.order_id} paid — {fmt(order.total_with_tax)}")

        # Clean some tables
        for table in rest.tables.values():
            if table.status == "needs_cleaning" and random.random() > 0.5:
                table.status = "empty"
                table.order_ids = []
                table.party_size = 0

        paid_count = sum(1 for o in rest.orders if o.status == "paid")
        print(f"  {hour}  →  Revenue so far: {fmt(rest.revenue)}   |   Orders paid: {paid_count}")
        time.sleep(0.3)

    _check_all_stock(rest)
    print(f"\n  ✅  {service} service complete!")
    pause()


# ═══════════════════════════════════════════════════════════
#  SECTION 6 — FINANCIAL REPORT
# ═══════════════════════════════════════════════════════════

def financial_report(rest: Restaurant):
    header("💰  DAILY FINANCIAL REPORT")
    print(f"  {RESTAURANT_NAME}  —  {rest.sim_day}\n")

    # Revenue breakdown
    paid_orders = [o for o in rest.orders if o.status == "paid"]
    gross = rest.revenue
    vat_collected = int(gross * (18/118))
    net_revenue = gross - vat_collected

    print("  ── REVENUE ──────────────────────────────")
    print(f"  Gross revenue (incl. VAT):    {fmt(gross):>14}")
    print(f"  VAT collected (18%):          {fmt(vat_collected):>14}")
    print(f"  Net revenue:                  {fmt(net_revenue):>14}")
    print(f"  Orders completed:             {len(paid_orders):>14}")
    avg = int(gross / len(paid_orders)) if paid_orders else 0
    print(f"  Avg. order value:             {fmt(avg):>14}")

    # Costs
    wage_bill = sum(s.daily_wage for s in rest.staff)
    fixed_total = sum(FIXED_COSTS.values())
    total_costs = wage_bill + rest.ingredient_cost + rest.waste_cost + fixed_total
    net_profit = net_revenue - total_costs

    print("\n  ── COSTS ────────────────────────────────")
    print(f"  Ingredient / food cost:       {fmt(rest.ingredient_cost):>14}")
    print(f"  Food waste:                   {fmt(rest.waste_cost):>14}")
    print(f"  Staff wages:                  {fmt(wage_bill):>14}")
    for k, v in FIXED_COSTS.items():
        print(f"  {k:<30}  {fmt(v):>14}")
    print(f"  ─────────────────────────────────────────")
    print(f"  Total costs:                  {fmt(total_costs):>14}")

    # P&L
    margin = (net_profit / net_revenue * 100) if net_revenue else 0
    verdict = "✅ PROFITABLE" if net_profit > 0 else "🔴 LOSS"
    print(f"\n  ── PROFIT & LOSS ────────────────────────")
    print(f"  Net revenue:                  {fmt(net_revenue):>14}")
    print(f"  Total costs:                  {fmt(total_costs):>14}")
    print(f"  ─────────────────────────────────────────")
    print(f"  Net profit / (loss):          {fmt(net_profit):>14}   {verdict}")
    print(f"  Profit margin:                {margin:>13.1f}%")

    # Coverage ratios
    food_cost_pct = (rest.ingredient_cost / net_revenue * 100) if net_revenue else 0
    labour_pct = (wage_bill / net_revenue * 100) if net_revenue else 0
    print(f"\n  ── KEY RATIOS ───────────────────────────")
    print(f"  Food cost %:                  {food_cost_pct:>13.1f}%  (ideal < 35%)")
    print(f"  Labour cost %:                {labour_pct:>13.1f}%  (ideal < 30%)")

    # Inventory value
    inv_value = sum(d["stock"] * d["cost_per_g"] for d in rest.inventory.values())
    print(f"  Remaining inventory value:    {fmt(int(inv_value)):>14}")

    pause()


# ═══════════════════════════════════════════════════════════
#  SECTION 7 — EVENT LOG
# ═══════════════════════════════════════════════════════════

def view_event_log(rest: Restaurant):
    header("📜  EVENT LOG")
    if not rest.events_log:
        print("  No events recorded yet.")
    else:
        for entry in rest.events_log[-40:]:
            print(entry)
    pause()


# ═══════════════════════════════════════════════════════════
#  MAIN MENU
# ═══════════════════════════════════════════════════════════

def main_menu(rest: Restaurant):
    alerts = len(rest.low_stock_alerts)
    revenue_str = fmt(rest.revenue)
    orders_paid = sum(1 for o in rest.orders if o.status == "paid")

    print(f"""
╔══════════════════════════════════════════════════════════╗
║  🍽   {RESTAURANT_NAME:<30}         ║
║  📅  {rest.sim_day:<50} ║
╠══════════════════════════════════════════════════════════╣
║  💰 Revenue: {revenue_str:<15}  📋 Orders paid: {orders_paid:<6}   ║
║  👥 Staff: {len(rest.staff):<5}  🚨 Low-stock alerts: {alerts:<3}              ║
╚══════════════════════════════════════════════════════════╝

  [1] 👥  Staff Management
  [2] 🪑  Table Management
  [3] 📋  Orders & Kitchen
  [4] 🥩  Inventory & Stock
  [5] ⚡  Auto-Simulate a Service Period
  [6] 💰  Daily Financial Report
  [7] 📜  Event Log
  [0] 🚪  Close Restaurant for the Day
""")


def main():
    rest = Restaurant()
    print(f"""
╔══════════════════════════════════════════════════════════╗
║    🍽️   Welcome to TableTurn Restaurant Simulator        ║
║         Running: {RESTAURANT_NAME:<38}║
╚══════════════════════════════════════════════════════════╝
  A full casual-dining operations simulator.
  Manage staff, tables, kitchen, inventory & finances.
""")
    time.sleep(1)

    while True:
        main_menu(rest)
        ch = get_int("  Your choice: ", 0, 7)
        if ch == 0:
            print("\n  🔒 Closing up. Generating end-of-day summary...\n")
            time.sleep(0.5)
            financial_report(rest)
            print("  👋 Good night! See you tomorrow.\n")
            break
        elif ch == 1: staff_menu(rest)
        elif ch == 2: tables_menu(rest)
        elif ch == 3: orders_menu(rest)
        elif ch == 4: inventory_menu(rest)
        elif ch == 5: auto_simulate(rest)
        elif ch == 6: financial_report(rest)
        elif ch == 7: view_event_log(rest)


if __name__ == "__main__":
    main()