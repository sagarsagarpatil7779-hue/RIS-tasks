library = {}   # dictionary only
running = True

while running:

    print("\n=== Library Menu ===")
    print("1. Add Book")
    print("2. Show All Books")
    print("3. Search Book")
    print("4. Update Book")
    print("5. Remove Book")
    print("6. Exit")
    print("========")

    choice = input("Enter your choice: ")

    # 1. ADD BOOK
    if choice == "1":
        book_id = input("Enter Book ID: ")
        title = input("Enter Book Title: ")
        library[book_id] = title
        print("Book Added Successfully!")

    # 2. SHOW ALL BOOKS

    elif choice == "2":
        print("\n---- Library Books ----")
        for key in library:
            print(key, ":", library[key])
        if len(library) == 0:
            print("(Library is empty)")

    # 3. SEARCH BOOK
    elif choice == "3":
        search_title = input("Enter title to search: ")
        found = False
        for key in library:
            if library[key].lower() == search_title.lower():
                print("Book Found ->", key, ":", library[key])
                found = True
                break
        if not found:
            print("Book Not Found")

    # 4. UPDATE BOOK
    elif choice == "4":
        update_id = input("Enter Book ID to update: ")
        if update_id in library:
            new_title = input("Enter new title: ")
            library[update_id] = new_title
            print("Book Updated!")
        else:
            print("Book ID Not Found")

    # 5. REMOVE BOOK
    elif choice == "5":
        remove_id = input("Enter Book ID to remove: ")
        if remove_id in library:
            del library[remove_id]
            print("Book Removed!")
        else:
            print("Book ID Not Found")

    # 6. EXIT PROGRAM
    elif choice == "6":
        print("Exiting... Goodbye!")
        running = False

    else:
        print("Invalid choice, try again.")