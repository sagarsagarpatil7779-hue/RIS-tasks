# --- Initial Student Data ---
students = {
    "101": {"name": "Sagar", "subjects": {"Python", "machine learner"}},
    "102": {"name": "aishwaray", "subjects": {"Science", "English"}},
    "103": {"name": "anile", "subjects": {"Biology", "Chemistry"}},
}

print("\n--- Initial Student Records ---")
for r, d in students.items():
    print(r, d)


# --- Add a New Student ---
students["104"] = {
    "name": "pooja",
    "subjects": {"docker", "Bash"}
}

print("\n--- After Adding New Student (104) ---")
for r, d in students.items():
    print(r, d)


# --- Update Existing Student ---
# Updating subjects for roll 102
students["102"]["subjects"].add("maths")
students["102"]["name"] = "saumay"

print("\n--- After Updating Student (102) ---")
for r, d in students.items():
    print(r, d)


# --- Remove a Student ---
students.pop("103")   # Remove roll 103

print("\n--- After Removing Student (103) ---")
for r, d in students.items():
    print(r, d)