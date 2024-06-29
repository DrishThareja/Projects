import random
import math

# Taking input for limit
lower = int(input("Enter Lower Limit: "))
upper = int(input("Enter Upper Limit: "))

# Generating a random number according to limit
x = random.randint(lower, upper) 
range_of_numbers = upper - lower + 1

# Finding number of chances according to the range
total_chances = math.ceil(range_of_numbers / 10)
print(f"\nYou have {total_chances} chances to guess the integer!\n")

# Loop
for count in range(1, total_chances + 1):
    guess = int(input("Guess a number: "))

    if guess == x:
        print(f"Congratulations! You guessed the number in {count} tries.")
        break
    elif guess < x:
        print("You guessed too small number!")
    else:
        print("You guessed too high number!")
else:
    print(f"\nThe number was {x}. Better luck next time!")

