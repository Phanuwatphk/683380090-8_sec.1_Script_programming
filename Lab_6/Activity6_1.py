"""Lab3_2_2.py"""

import random

number = random.randint(1, 100)
limit = 5

def guess(n):
    if n == number:
        print("Congratulations! You guessed it!")
        exit()
    elif n > number:
        print("Too high! Try again.")
    else:
        print("Too low! Try again.")

while True:
    n = int(input("Guess the number (1-100) : "))
    guess(n)
    limit -= 1
    if limit == 0:
        print("The guessing limit has been reached.")
        break