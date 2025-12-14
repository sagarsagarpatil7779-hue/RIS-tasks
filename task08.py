# DATA OF MULTIPLE STUDENTS 
students = [
    {"name": "pooja",  "roll": "101", "marks": [85, 90, 88, 92, 80,90]},
    {"name": "Aisha",  "roll": "102", "marks": [70, 65, 72, 68, 75,50]},
    {"name": "anil",  "roll": "103", "marks": [55, 60, 58, 62, 50,35]},
    {"name": "sagar",   "roll": "104", "marks": [45, 40, 38, 50, 42,98]},
]


def calculate_total(marks):
    return sum(marks)

def calculate_percentage(total):
    return total / len(marks)

def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "Fail"


def show_report(student):
    print("\n  Student Report Card ")
    print("Name:", student["name"])
    print("Roll No:", student["roll"])
    print("Marks:", student["marks"])
    print("Total out of 600:", student["total"])
    print("Percentage:", round(student["percentage"], 2))
    print("Grade:", student["grade"])



# PROCESS EACH STUDENT 
for student in students:
    marks = student["marks"]
    total = calculate_total(marks)
    percentage = total / len(marks)
    grade = calculate_grade(percentage)

    student["total"] = total
    student["percentage"] = percentage
    student["grade"] = grade

    show_report(student)