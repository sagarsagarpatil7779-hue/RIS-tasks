# find number it's positive or negative
a= int(input("entre any number "))
if a>0:
     print("positive number")
elif a<0 :
    print("negative number")
else :
    print("zero number")

# simple calculator
a = int(input("entre first number "))
b = int(input("entre second number "))
c = input("Enter operator (+, -, *, /, //, %): ")
if c == "+":
    print(a + b)
elif c == "-":
    print(a - b)
elif c == "*":
    print(a * b)
elif c == "/":
    print(a / b)
elif c == "%":
    print(a % b)
else :
    print("invalid input")

#user eligible for vote!
a = float(input("entre your age"))
if a >= 18:
    print("You are eligible for vote ")
elif a <18:
    print("You are not eligible for vote")
elif a<0:
    print("please entre positive numbers ")
else :

    print("invalid")