import random

name = input("What is your name? ")
print("Best of Luck!", name)

words = ['Java', 'Python', 'Kotlin', 'Javascript', 'HTML', 'CSS', 'Swift', 'Ruby']

word = random.choice(words).lower() # selecting a random word and making them lower case

print("Please guess the character: ")
chances = len(word) # giving limited chances to the player

guesses = ''    # what the user will guess will store in guesses
attempts = 0    # track the number of attempts

while attempts < chances:
    for char in word:
        if char in guesses:
            print(char, end=' ')    # end prevent the print to goes to next line
        else:
            print("_", end=" ")
    print() # move to next line

    guess = input("Guess the character: ").lower()  # making it lower too so that it doesn't create problem while checking the character

    if guess in guesses:
        print("You have already guessed this character")
        continue
    guesses += guess
    attempts += 1

    if guess in word:
        print("Correct Guess")
    else:
        print("Wrong Guess")

    remaining_chances = chances - attempts
    if remaining_chances > 0:
        print(f"You have {remaining_chances} chances left.")
    else:
        print("No more chances left.")

    if guesses == word:
        print(f"Congrats! You guessed the word correctly. The word was {word}")
        break

if guesses != word:
    print(f"Sorry, you did not guess the word correctly. The word was {word}")
    print("Play again, Thanku for Playing")
