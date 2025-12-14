#To-do list
tasks = [] # List to store tasks
choice = ()# entre your choice

while choice != "3":
    print("\n1️⃣. Add Task") #adding task
    print("2️⃣. View Tasks")#view task
    print("3️⃣. stop") #exit task
    choice = input("Enter choice: ")

    if choice == "1":
        task = input("Enter task: ")
        tasks.append(task)
        print("Task added!")
    elif choice == "2":
        print("Your Tasks:")
        for name in tasks:
            print("✅", name)
    elif choice == "3":
        print("Goodbye👋👋👋👋👋")
    else:
        print("Invalid choice❗❗❗❗")