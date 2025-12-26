# Simulate rolling two dice 1000 times using np.random.randint()

import numpy as np
dice1=np.random.randint(1,7,1000)
dice2=np.random.randint(1,7,1000)
print("The Dice 1  first 20 elements are : ",dice1[:20])
print("The Dice 2 first 20 elements are : ",dice2[:20])
sum_dice = dice1+dice2
print(f"The sum of 2 dice is: {sum_dice[:20]}" )