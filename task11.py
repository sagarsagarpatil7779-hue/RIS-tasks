# taking user input
Speed=float(input("enter your vehicle Speed "))
Time=float(input("enter time"))

def calculate_distance(Speed,Time):
    distance=Speed*Time  #formula for distance
    return distance
#result...
result=calculate_distance(Speed,Time)

print(f"Distance Covered by a Vehicle ={result}")