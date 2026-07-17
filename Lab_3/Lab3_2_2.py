import random

number = random.randint(1, 100)
limit = 5
while True:
    n = int(input("Guess the number (1-100) : "))
    if n == number:
        print("Congratulations! You guessed it!")
    elif n > number:
        print("Too high! Try again.")
    else:
        print("Too low! Try again.")

    limit -= 1
    if limit == 0:
        print("The guessing limit has been reached.")
        break