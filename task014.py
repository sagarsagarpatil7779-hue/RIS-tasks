import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
data=pd.read_csv(r"C:\Users\sagar\OneDrive\Desktop\RIS tasks\tasks\stock_prices.csv")

print(data)
print(data.info())
print(data.isnull().sum())

close=data["close"].to_numpy()
print(close)

daily_return=(close[1:]-close[:-1]) / close[:-1] # yesterday - today / today
print(daily_return) # like 259.59 - 270.49 /270.59

mean_r=np.mean(daily_return)
standard_r=np.std(daily_return) 

print(mean_r)
print(standard_r)

#top positive and negative 

top_five_p=np.argsort(daily_return)[-5:][::-1]
top_five_n=np.argsort(daily_return)[:5]

print("top five positive return ")

for i in top_five_p:
    print(f"day {i+1},{daily_return[i]*100 } % ")

print("top five negative return")
for i in top_five_n:
    print(f"day {i+1},{daily_return[i]*100} % ")

plt.hist(daily_return,bins=50)
plt.title("histogram of daily stock returns ")
plt.xlabel("daily returns")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()