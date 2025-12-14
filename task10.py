import json
import os

FILE = "contacts.json"


# LOAD CONTACTS
def load_contacts():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}  # empty dictionary if file doesn't exist


# SAVE CONTACTS
def save_contacts(contacts):
    with open(FILE, "w") as f:
        json.dump(contacts, f, indent=4)


# ADD CONTACT
def add_contact(contacts):
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    email = input("Enter email: ")

    contacts[name] = {"phone": phone, "email": email}
    save_contacts(contacts)
    print("Contact added successfully!\n")


#UPDATE CONTACT
def update_contact(contacts):
    name = input("Enter name to update: ")

    if name in contacts:
        phone = input("Enter new phone: ")
        email = input("Enter new email: ")

        contacts[name] = {"phone": phone, "email": email}
        save_contacts(contacts)
        print("Contact updated!\n")
    else:
        print("Contact not found.\n")


# DELETE CONTACT
def delete_contact(contacts):
    name = input("Enter name to delete: ")

    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
        print("Contact deleted!\n")
    else:
        print("Contact not found.\n")


# SEARCH CONTACT
def search_contact(contacts):
    name = input("Enter name to search: ")

    if name in contacts:
        print("\n--- Contact Found ---")
        print(f"Name : {name}")
        print(f"Phone: {contacts[name]['phone']}")
        print(f"Email: {contacts[name]['email']}\n")
    else:
        print("Contact not found.\n")


#  MAIN MENU 
def main():
    contacts = load_contacts()

    while True:
        print("\n===== CONTACT BOOK =====")
        print("1. Add Contact")
        print("2. Update Contact")
        print("3. Delete Contact")
        print("4. Search Contact")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            update_contact(contacts)
        elif choice == "3":
            delete_contact(contacts)
        elif choice == "4":
            search_contact(contacts)
        elif choice == "5":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice, try again.\n")


# Run the program
main()