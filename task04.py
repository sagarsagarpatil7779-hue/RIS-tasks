# List to store student records
students = []

# Add students
s1 = ("Sagar", 85)
s2 = ("Anil", 92)
s3 = ("pooja", 88)
s4 = ("aishwary",92)

# Add tuples to list
students.append(s1)
students.append(s2)
students.append(s3)
students.append(s4)

# Display students and grades
print("Student Grades:")
for student in students:
    print(student[0], "-", student[1])
