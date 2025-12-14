# task03
#  string operators, indexing (positive and negative),
# slicing (start, end, step) with examples, f-string formatting,

# Step 1: Take user input (name,gender,age,salary,height,position)
name = str(input("enter your name"))
gender = str(input("enter your gender"))
age = int(input("enter your age"))
salary = int(input("enter your salary"))
height = float(input("enter your height"))
position = str(input("enter your position"))

# String indexing and slicing

print("original string:",name)
print("length of original string:",len(name))

# Indexing (positive and negative)

print(name[0]) # taking first character
print(name[-1]) # taking last character
print(name[3]) # taking character at index 3
print(name[0:4]) # taking character 0 to 4

# slicing (start,end,step)
print(position[0:10]) # first 9 character
print(len(position)) # length of the character
print(position[10:]) #  last word
print(position[::-1]) # reverse

# negative slicing
print(gender[-1])  # last character
print(gender[-1:-2]) #last two words

# String Formatting
name = input("Enter your name")
age1 = int(input("Enter your age"))
salary1 = int(input("Enter your salary"))
height1 = float(input("Enter your height"))

print("\n String Formatting")
print(f"My name is {name},i  am {age} years old ")
print(f"Next year i will be {age + 1} years old")
print(f"Height : {height:.4f} feet")
print(f"Name in uppercase : {name.upper()}")


## Multiline f strings
message = f"""
personal Details
----------
Name:{name:>10}
Age:{age:>10}
Height:{height:>8.1f}
"""
print(message)