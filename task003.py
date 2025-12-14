# Username Generator using String Operations

print("== USERNAME GENERATOR ==")

# Step 1: Take user inputs
first_name = input("Enter your first name: ").strip()
last_name = input("Enter your last name: ").strip()
fav_word = input("Enter your favourite word: ").strip()

# Step 2: Create different username styles using string operations

# Using slicing and concatenation
username1 = first_name[:4].lower() + last_name[:2].lower()

# Using title case and joining
username2 = "-".join([first_name.title(), last_name.title()])

# Using reverse and concatenation
username3 = first_name[::-2] + last_name[0].upper()

# Using f-string formatting
username4 = f"{first_name.lower()}_{fav_word.upper()}_{len(first_name) + len(last_name)}"

# Step 3: Display the generated usernames
print("\nHere are some username suggestions:")
print(f"1️. {username1}")
print(f"2️. {username2}")
print(f"3️. {username3}")
print(f"4. {username4}")

# Step 4: Let user choose one
choice = input("\nEnter the number of your favourite username (1-4): ").strip()

# Step 5: Display the final username using f-string formatting
if choice == "1":
    final = username1
elif choice == "2":
    final = username2
elif choice == "3":
    final = username3
elif choice == "4":
    final = username4
else:
    final = "Invalid choice"

print(f"\n✅ Your final username is: {final}")

