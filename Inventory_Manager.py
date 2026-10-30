import json
import os

from inventory import Inventory
from product import Product

DATA_DIR = os.environ.get("DATA_DIR", ".")
FILENAME = os.path.join(DATA_DIR, "inventory.json")


# ---------- File handling ----------

def load_inventory():
    """Read inventory.json and turn each entry into a Product object."""
    inventory = Inventory()

    if not os.path.exists(FILENAME):
        print("inventory.json not found. Starting with an empty inventory.")
        return inventory

    print("\ninventory.json found.")
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
        for item in data:
            product = Product(item["id"], item["name"], item["price"], item["stock"])
            inventory.add_product(product)
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
        print("Could not read inventory.json. Starting with an empty inventory.")
        return Inventory()
    return inventory


def save_inventory(inventory):
    """Turn each Product back into a dictionary and write the list to JSON."""
    data = []
    for product in inventory.get_products():
        data.append({
            "id": product.product_id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
        })
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)


# ---------- Menu actions (user input lives here, not in the classes) ----------

def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if product_id == "":
        print("Product ID cannot be empty!")
        return
    if inventory.search_product(product_id) is not None:
        print("A product with that ID already exists!")
        return

    name = input("Name: ").strip()
    if name == "":
        print("Product Name cannot be empty!")
        return

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid input. Product not added.")
        return

    try:
        product = Product(product_id, name, price, stock)
    except ValueError:
        print("Price and stock cannot be negative. Product not added.")
        return

    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")

    try:
        new_stock = int(input("\nNew Stock Quantity: "))
    except ValueError:
        print("Invalid input. Stock not updated.")
        return

    try:
        product.update_stock(new_stock)
    except ValueError:
        print("Stock cannot be negative. Stock not updated.")
        return
    print("\nStock updated successfully!")


def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("-------------------------------------------------")
    product.display_information()
    print("-------------------------------------------------")


def print_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("========================================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================================")
    inventory = load_inventory()
    print_menu()

    while True:
        option = input("\nEnter option: ").strip()

        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
            print("Inventory saved successfully to inventory.json.")
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.\n")
            break
        else:
            print("\nInvalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
