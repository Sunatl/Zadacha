import os

class FileManager:
    def __init__(self, filename):
        self.filename = filename
        self.data = self._load_file()

    def _load_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                data = {}
                for line in lines:
                    if line.strip():
                        name, price = line.strip().split(" — ")
                        data[name.lower()] = int(price)  
                return data
        return {}

    def _save_file(self):
        if os.path.dirname(self.filename):
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        with open(self.filename, 'w', encoding='utf-8') as file:
            for name, price in self.data.items():
                file.write(f"{name} — {price}\n")

    def handle_action(self, action, name=None, price=None, new_name=None):
        name = name.lower() if name else None
        new_name = new_name.lower() if new_name else None

        if action == "add":
            if name in self.data:
                print(f"'{name}' already exists.")
            else:
                self.data[name] = price
                self._save_file()
                print(f"Added: {name} — {price}")

        elif action == "update":
            if name in self.data:
                if new_name:
                    self.data[new_name] = self.data.pop(name)
                    print(f"Updated item name: {name} → {new_name}")
                if price is not None:
                    self.data[new_name if new_name else name] = price
                    print(f"Updated: {new_name if new_name else name} — {price}")
                self._save_file()
            else:
                print(f"'{name}' not found.")

        elif action == "delete":
            if name in self.data:
                del self.data[name]
                self._save_file()
                print(f"Deleted: {name}")
            else:
                print(f"'{name}' not found.")

        elif action == "display":
            if self.data:
                print("Items:")
                for item, price in self.data.items():
                    print(f"{item} — {price}")
            else:
                print("List is empty.")

        elif action == "total":
            total = sum(self.data.values())
            print(f"Total: {total}")
        else:
            print("Invalid action.")

def main():
    filename = "items.txt" 
    manager = FileManager(filename)

    while True:
        print("\nOptions: add, update, delete, display, total, exit")
        action = input("Enter action: ").strip().lower()

        if action == "exit":
            print("Goodbye!")
            break

        if action == "add":
            name = input("Enter item name: ").strip()
            while True:
                try:
                    price = int(input("Enter item price: ").strip())
                    if price < 0:
                        print("Price cannot be negative. Please enter a valid price.")
                        continue
                    manager.handle_action(action, name, price)
                    break
                except ValueError:
                    print("Price must be an integer. Please enter a valid price.")

        elif action == "update":
            name = input("Enter item name to update: ").strip().lower()  
            if name in manager.data:
                new_name = input("Enter new item name (press Enter to keep current name): ").strip().lower()  
                if new_name == "":
                    new_name = None  
                while True:
                    try:
                        price = int(input("Enter new item price: ").strip())
                        if price < 0:
                            print("Price cannot be negative. Please enter a valid price.")
                            continue
                        manager.handle_action(action, name, price, new_name)
                        break
                    except ValueError:
                        print("Price must be an integer. Please enter a valid price.")
            else:
                print(f"'{name}' not found.")

        elif action == "delete":
            name = input("Enter item name to delete: ").strip().lower()  
            manager.handle_action(action, name)

        elif action in ["display", "total"]:
            manager.handle_action(action)

        else:
            print("Invalid option.")

print(main())
