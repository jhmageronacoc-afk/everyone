"""
Angels Burger Ordering System
Group: DevOps Dynamics
Course: ITE 366 - Introduction to Computing
Period 2 Core Python Console System

This program is a local, console-based ordering and billing system.
Data is stored only during the current execution session.
"""

# -----------------------------
# VARIABLES AND DATA STRUCTURES
# -----------------------------

STAFF_USERNAME = "isaacgwapo"
STAFF_PASSWORD = "12345"

MENU = {
    1: {"name": "Classic Burger", "price": 100.00},
    2: {"name": "Chicken Burger", "price": 110.00},
    3: {"name": "Extra Large Burger", "price": 120.00},
    4: {"name": "Burger with egg", "price": 90.00},
    5: {"name": "Iced Tea", "price": 45.00},
}

orders = []
next_order_id = 1

# -----------------------------
# INPUT VALIDATION
# -----------------------------

def get_integer(prompt, minimum=None, maximum=None):
    """Return a valid integer within an optional range."""
    while True:
        value = input(prompt).strip()
        if not value.isdigit():
            print("Invalid input. Please enter a whole number.")
            continue

        number = int(value)

        if minimum is not None and number < minimum:
            print(f"Please enter a number from {minimum} to {maximum}.")
            continue

        if maximum is not None and number > maximum:
            print(f"Please enter a number from {minimum} to {maximum}.")
            continue

        return number


def get_customer_name():
    """Get and validate a customer's name."""
    while True:
        name = input("Enter customer name: ").strip()
        if name:
            return name
        print("Customer name cannot be empty.")

# -----------------------------
# LOGIN
# -----------------------------

def login():
    """Validate staff credentials and return True for successful login."""
    attempts = 3

    while attempts > 0:
        print("\n========== STAFF LOGIN ==========")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if username == STAFF_USERNAME and password == STAFF_PASSWORD:
            print("Login successful.")
            return True
        elif username != STAFF_USERNAME:
            print("Invalid username.")
        else:
            print("Invalid password.")

        attempts -= 1
        if attempts > 0:
            print(f"Attempts remaining: {attempts}")

    print("Too many failed attempts. System closed.")
    return False

# -----------------------------
# MENU DISPLAY
# -----------------------------

def display_menu():
    """Display all available food and drink items."""
    print("\n================ ANGELS BURGER MENU ================")
    print(f"{'No.':<5}{'Item':<25}{'Price':>10}")
    print("-" * 40)

    for number, item in MENU.items():
        print(f"{number:<5}{item['name']:<25}PHP {item['price']:>7.2f}")

    print("-" * 40)

# -----------------------------
# ORDER ENTRY
# -----------------------------

def create_order():
    """Capture a customer order and return the completed order dictionary."""
    global next_order_id

    customer = get_customer_name()
    items = []

    while True:
        display_menu()
        choice = get_integer("Enter item number (0 to finish): ", 0, len(MENU))

        if choice == 0:
            if not items:
                print("No items were added. Order cancelled.")
                return None
            break

        quantity = get_integer("Enter quantity: ", 1, 99)
        selected = MENU[choice]

        line_total = selected["price"] * quantity

        items.append({
            "item": selected["name"],
            "price": selected["price"],
            "quantity": quantity,
            "line_total": line_total
        })

        print(
            f"Added {quantity} x {selected['name']} "
            f"= PHP {line_total:.2f}"
        )

        more = input("Add another item? (Y/N): ").strip().lower()
        if more != "y":
            break

    subtotal = calculate_total(items)

    order = {
        "id": next_order_id,
        "customer": customer,
        "items": items,
        "total": subtotal,
        "status": "Pending"
    }

    next_order_id += 1
    return order

# -----------------------------
# CALCULATIONS
# -----------------------------

def calculate_total(items):
    """Calculate and return the total amount of all order lines."""
    total = 0.0

    for item in items:
        total += item["price"] * item["quantity"]

    return total

# -----------------------------
# RECEIPT / BILL
# -----------------------------

def print_bill(order):
    """Display the customer's bill."""
    print("\n================ BILL ================")
    print(f"Order ID : {order['id']}")
    print(f"Customer : {order['customer']}")
    print("-" * 40)

    for item in order["items"]:
        print(
            f"{item['quantity']} x {item['item']} "
            f"@ PHP {item['price']:.2f} = "
            f"PHP {item['line_total']:.2f}"
        )

    print("-" * 40)
    print(f"TOTAL PAYMENT: PHP {order['total']:.2f}")
    print(f"STATUS       : {order['status']}")
    print("=" * 40)

# -----------------------------
# ORDER QUEUE
# -----------------------------

def view_orders():
    """Display all orders in the current session."""
    print("\n=============== ACTIVE ORDER QUEUE ===============")

    if not orders:
        print("No orders recorded in the current session.")
        return

    for order in orders:
        print(
            f"Order #{order['id']} | Customer: {order['customer']} | "
            f"Total: PHP {order['total']:.2f} | Status: {order['status']}"
        )

    print("===================================================")

# -----------------------------
# STATUS UPDATE
# -----------------------------

def update_order_status():
    """Change the preparation status of an existing order."""
    if not orders:
        print("There are no orders to update.")
        return

    view_orders()
    order_id = get_integer("Enter order ID to update: ", 1)

    for order in orders:
        if order["id"] == order_id:
            print("\n1. Pending")
            print("2. Preparing")
            print("3. Ready")
            print("4. Completed")

            status_choice = get_integer("Choose new status: ", 1, 4)
            status_map = {
                1: "Pending",
                2: "Preparing",
                3: "Ready",
                4: "Completed"
            }

            order["status"] = status_map[status_choice]
            print(
                f"Order #{order['id']} status updated to "
                f"{order['status']}."
            )
            return

    print("Order ID not found.")

# -----------------------------
# FIND ORDER
# -----------------------------

def find_order():
    """Find and display one order by its ID."""
    if not orders:
        print("No orders recorded.")
        return

    order_id = get_integer("Enter order ID: ", 1)

    for order in orders:
        if order["id"] == order_id:
            print_bill(order)
            return

    print("Order ID not found.")

# -----------------------------
# MAIN MENU
# -----------------------------

def main_menu():
    """Run the main system flow until the employee chooses Exit."""
    while True:
        print("\n============== ANGELS BURGER ORDERING SYSTEM ==============")
        print("1. Display Menu")
        print("2. Enter Customer Order")
        print("3. View Active Order Queue")
        print("4. Update Order Preparation Status")
        print("5. View Order Bill")
        print("6. Exit")
        print("=====================================================")

        choice = get_integer("Select an option: ", 1, 6)

        if choice == 1:
            display_menu()
        elif choice == 2:
            order = create_order()
            if order is not None:
                orders.append(order)
                print(
                    f"Order #{order['id']} successfully recorded "
                    f"for {order['customer']}."
                )
                print_bill(order)
        elif choice == 3:
            view_orders()
        elif choice == 4:
            update_order_status()
        elif choice == 5:
            find_order()
        else:
            print("\nThank you for using the Angels Burger Ordering System.")
            break

# -----------------------------
# PROGRAM START
# -----------------------------

def main():
    """Start the program with login validation."""
    print("=====================================================")
    print("              ANGELS BURGER ORDERING SYSTEM")
    print("=====================================================")
    print("Local Python Console Application")

    if login():
        main_menu()


if __name__ == "__main__":
    main()
