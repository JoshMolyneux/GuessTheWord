# A game involving TWO players. One chooses a word, another gets to guess the word one letter at a time until they run out of attempts...
#=============================#
# Author Student ID: 18043053
# Date: 05/05/2020
#=============================#

#----------SCRIPT STRUCTURE----------#
# Import Modules
# Constants & List Initialisations
# Counters
# Main Function
# Functions
# Turtle Initialisations
# Turtle Functions
# Exterior Function Calls
#------------------------------------#

#----------IMPORT MODULES----------#
from os import system as sys, name as operating_system #Import system modules from the 'os' library
import turtle # Import the graphics library we'll be using for our game
sys('mode con: cols=100 lines=40') # Set a preliminary size on the command window

#----------CONSTANTS & LIST INITIALISATIONS----------#
ALLOWED_CHARACTERS = "abcdefghijklmnopqrstuvwxyz-" # Characters allowed to be used in the game
WRONG_GUESSES_LIST = [] # Initialise our list of letters guessed incorrectly
CORRECT_GUESSES_LIST = [] # Initialise our list of letters guessed correctly

#----------COUNTERS----------#
attempts_counter = 8 # A counter to track how many attempts have been made

#----------MAIN FUNCTION----------#
def main():

    global attempts_counter
    # Create some placeholder variables for our scores
    playerOneScore = 0
    playerTwoScore = 0
    print("=========== GUESS THE WORD ===========\n")
    # Define our two player names for a personalised game experience. But also for ease when keeping score
    playerOneName, playerTwoName = get_player_names()
    # Create some empty string variables. These are placeholders for the time-being
    wordCreator = ""
    wordGuesser = ""
    # Default bool variable. We'll use this to check which player is which
    isPlayerOneGuessing = False
    
    clear_terminal()

    # Let's check our 'isPlayerOneGuessing' bool value and assign some variables dependant on the result.
    # This is always the same on the first instance, but is subject to change further in the program
    while(True):
        if (isPlayerOneGuessing):
            wordGuesser = playerOneName
            wordCreator = playerTwoName
        else:
            wordGuesser = playerTwoName
            wordCreator = playerOneName
    
        # Display some welcome information and display our static text on the Turtle Screen, ready for use!
        turtle_gfx_text_static()

        # Re-draw our scores for each player, per game
        draw_score(playerOneName, playerTwoName, playerOneScore, playerTwoScore)

        # Introduce both players to the game
        introduction(wordCreator, wordGuesser)

        # Assign the function return value to a vriable. The function will do some validation checks on the given word 
        word = get_valid_word()

        # This function will populate our Correct Guesses list with '*'
        initialise_hidden_word(word)
        
        # Draw the populated Correct Guesses list on the Turtle Screen
        turtleHiddenText_dynamic.write(' '.join(CORRECT_GUESSES_LIST), font=turtleHiddenTextStyle, align="left")

        # Show the users how many attempts are remaining on the Turtle Screen
        draw_attempts_remaining()
        
        # This function DOES NOT WORK when using the 'F5' | 'Run Module' in IDLE.
        # But, only when you run the actual Python file straight from the directory
        clear_terminal()

        # Let's loop while the attempts_counter remains ABOVE zero
        while(attempts_counter > 0):
            # Some visual feedback to show the guessing player that it's their turn
            print("===========", wordGuesser, "- Guess the Word! ===========\n")
            print("Attempts Remaining:", attempts_counter)
            print("Wrong Guesses:", WRONG_GUESSES_LIST)
            print("Word:", CORRECT_GUESSES_LIST)
            
            # Assign the function return value to a vriable. The function will do some validation checks on the given guess 
            guess = get_valid_guess()

            # Let's do some checks to see if the given guess matches a character in the word
            match_guess_to_word(guess, word)

            # Cleaner console allows for better visuals
            clear_terminal()

            # This 'if' block will allow us to draw different parts of the ambulance dependant on the value of attempts_counter
            if (attempts_counter == 7):
                turtle_gfx_attempt_ONE()
            elif (attempts_counter == 6):
                turtle_gfx_attempt_TWO()
            elif (attempts_counter == 5): 
                turtle_gfx_attempt_THREE()
            elif (attempts_counter == 4): 
                turtle_gfx_attempt_FOUR()
            elif (attempts_counter == 3): 
                turtle_gfx_attempt_FIVE()
            elif (attempts_counter == 2): 
                turtle_gfx_attempt_SIX()
            elif (attempts_counter == 1): 
                turtle_gfx_attempt_SEVEN()
            elif (attempts_counter <= 0):
                # The player guessing the word has lost. The attempts_counter has fallen below or equal to zero
                turtle_gfx_attempt_EIGHT()    
                print(wordGuesser + " LOSES")
                turtleEndGameOutcome.color("red")
                turtleEndGameOutcome.write(wordGuesser + " LOSES!", font=turtleWinStyle, align="right")
                # The game has finished, let's swap the players around by re-assigning our boolean variable
                isPlayerOneGuessing = not isPlayerOneGuessing
                # Run our restart function to clear all lists and all neccessary turtle instances
                restart()
                # Break out of our nested loop and re-run the game
                break

            # If this is TRUE, the user has won. There are no more '*' in the CORRECT_GUESSES_LIST
            if (is_winner(wordGuesser)):
                # Check which player has won the game and give them a point, adding on to their score
                if (isPlayerOneGuessing):
                    playerOneScore += 1
                else:
                    playerTwoScore += 1
                # The game has finished, let's swap the players around by re-assigning our boolean variable
                isPlayerOneGuessing = not isPlayerOneGuessing
                # Run our restart function to clear all lists and all neccessary turtle instances
                restart()
                # Break out of our nested loop and re-run the game
                break

#----------FUNCTIONS----------#
def clear_terminal(): 
    # for Windows OS
    if (operating_system == 'nt'): 
        sys('cls') 
    # for Mac OS and Linux 
    else:
        sys('clear')
        
def get_player_names():
    # User input, find their names and strip any spaces
    playerOne = input("Player 1 Name: ").strip()
    playerTwo = input("Player 2 Name: ").strip()

    # Check if the input is the same, if it is, ask Player Two to try again
    while(playerOne == playerTwo):
        print("[!]You cannot have the same name as Player 1[!]")
        playerTwo = input("Player 2 Name: ").strip()

    return playerOne, playerTwo

def introduction(playerOne, playerTwo):
    print("=========== Welcome", playerOne,"===========")
    print("[!]Please ensure that", playerTwo,"doesn't look at your word[!]\n")
    
def get_valid_word():
    
    # Define our word string with some validation of what characters it can use
    # Store it in a list for iterative-use later on
    while True:
        word = list(input("Enter your word (if it has a space, use '-', e.g. ice-cream): ").lower())

        # Check if our character is NOT in the ALLOWED_CHARACTERS string and if it's NOT greater than zero
        if not (all(char in ALLOWED_CHARACTERS for char in word) and len(word) > 0):
            print("[!]Invalid character. Please try again[!]")
            print("[!]Allowed Characters:", ALLOWED_CHARACTERS, "[!]\n")
            continue

        return word
    
def get_valid_guess():

    # Define our guess input character with some validation of what characters it can use
    while True:
        guess = input("Please GUESS a character:")

        # If the guess is more than one character, re-run the loop and ask for input again
        # Else, assign a variable to hold the input in lowercase
        if (len(guess) != 1):
            print("[!]Please enter ONE character[!]\n")
            continue
        else:
            guess = str(guess.lower())

        # Check all characters in our allowed characters string and compare it against the input
        # If it does, break out of the loop
        if not all(char in ALLOWED_CHARACTERS for char in guess):
            print("[!]Invalid character. Please try again[!]")
            print("[!]Allowed Characters:", ALLOWED_CHARACTERS, "[!]\n")
            continue

        # Check if the guess has already been made
        if (guess in WRONG_GUESSES_LIST or guess in CORRECT_GUESSES_LIST):
            print("[!]You've guessed this already[!]\n")
            continue
        
        return guess

def initialise_hidden_word(word):
    # Find the length of 
    wordLength = len(word)
    # In this For Loop, we're going to populate a list with '*'. This will be displayed on the turtle screen
    for i in range(wordLength):
        CORRECT_GUESSES_LIST.append("*")

def match_guess_to_word(guess, word):
    
    global attempts_counter

    # Iterate through the length of our populated correct guesses list
    # Check if the guess is in the word and insert the character
    for i in range(len(CORRECT_GUESSES_LIST)):
        if(guess == word[i]):
            CORRECT_GUESSES_LIST.pop(i)
            CORRECT_GUESSES_LIST.insert(i, guess)
            
            turtleHiddenText_dynamic.clear()
            turtleHiddenText_dynamic.write(' '.join(CORRECT_GUESSES_LIST).upper(), font=turtleHiddenTextStyle, align="left")
    # If the letter is not in the word, subtract 1 from our attempts_counter and add it to the WRONG_GUESSES_LIST some Turtle GUI
    if (guess not in word):
        attempts_counter -= 1
        WRONG_GUESSES_LIST.append(guess)

        turtleWrongGuesses_dynamic.clear()
        turtleWrongGuesses_dynamic.write(', '.join(WRONG_GUESSES_LIST).upper(), font=turtleWrongGuessesStyle, align="left")
                        
        draw_attempts_remaining()
        
def is_winner(wordGuesser):
    # We can determine if the wordGuesser has to make any more correct guesses by checking for '*' in the list
    if ("*" not in CORRECT_GUESSES_LIST):
        clear_terminal() # Clear the terminal screen
        print("The Word was:", ''.join(CORRECT_GUESSES_LIST).upper()) # Display the word to the user in the terminal
        print(wordGuesser + " WINS!")
        turtleEndGameOutcome.color("#32CD32")
        turtleEndGameOutcome.write(wordGuesser + " WINS!", font=turtleWinStyle, align="right")      
        return True
    else:
        return False

def restart():
    global attempts_counter
    
    # At the end of the game, we want to restart. Give them a chance to see who won, etc and move on when they're ready
    input("Press ENTER to restart the game!")

    # Set back some default values and clear all lists and turtle drawings necessary, etc
    attempts_counter = 8
    WRONG_GUESSES_LIST.clear()
    CORRECT_GUESSES_LIST.clear()
    turtleDrawShapes.clear()
    turtleEndGameOutcome.clear()
    turtleHiddenText_dynamic.clear()
    turtleWrongGuesses_dynamic.clear()
    turtleAttemptsRemaining_dynamic.clear()
    turtleScore.clear()
    clear_terminal()
    
# Turtle Docs: https://docs.python.org/3.3/library/turtle.html
#----------TURTLE DEFAULTS----------#
turtle.title("GUESS THE WORD") # Set a title
turtle.bgcolor("yellow") # Set our background colour
turtle.setup(width=700, height=650, startx=1150, starty=200) # Set a turtle window size on open

# Below we are going to set up some turtle instances with some default styles and positions 
turtleDrawShapes = turtle.Turtle()
turtleDrawShapes.hideturtle()
turtleDrawShapes.speed(9)

turtleHiddenText_dynamic = turtle.Turtle()
turtleHiddenText_dynamic.hideturtle()
turtleHiddenTextStyle = ("calibri", 30, "italic")
turtleHiddenText_dynamic.color("blue")
turtleHiddenText_dynamic.penup()
turtleHiddenText_dynamic.goto(-300, 200)
turtleHiddenText_dynamic.pendown()

turtleAttemptsRemaining_dynamic = turtle.Turtle()
turtleAttemptsRemaining_dynamic.hideturtle()
turtleAttemptsRemainingStyle = ("calibri", 15, "italic")
turtleAttemptsRemaining_dynamic.color("black")

turtleWrongGuesses_dynamic = turtle.Turtle()
turtleWrongGuesses_dynamic.hideturtle()
turtleWrongGuessesStyle = ("calibri", 30, "italic")
turtleWrongGuesses_dynamic.color("green")
turtleWrongGuesses_dynamic.penup()
turtleWrongGuesses_dynamic.goto(-300, -250)
turtleWrongGuesses_dynamic.pendown()

turtleEndGameOutcome = turtle.Turtle()
turtleEndGameOutcome.speed(0)
turtleEndGameOutcome.hideturtle()
turtleWinStyle = ("calibri", 50, "bold")
turtleLoseStyle = ("calibri", 50, "bold")
turtleEndGameOutcome.penup()
turtleEndGameOutcome.goto(280, 135)
turtleEndGameOutcome.pendown()

turtleScore = turtle.Turtle()
turtleScore.hideturtle()
turtleScoreStyle = ("calibri", 20)
turtleScoreTitleStyle = ("calibri", 20, "bold")
turtleScore.color("black")

#----------TURTLE DRAW FUNCTIONS----------#
# Score text
def draw_score(playerOneName, playerTwoName, playerOneScore, playerTwoScore):
    turtleScore.penup()
    turtleScore.goto(330, -260)
    turtleScore.pendown()
    turtleScore.write("SCORE", font=turtleScoreStyle, align="right")
    turtleScore.penup()
    turtleScore.goto(330, -290)
    turtleScore.pendown()
    turtleScore.write(playerOneName + ": " + str(playerOneScore), font=turtleScoreStyle, align="right")
    turtleScore.penup()
    turtleScore.goto(330, -310)
    turtleScore.pendown()
    turtleScore.write(playerTwoName + ": " + str(playerTwoScore), font=turtleScoreStyle, align="right")

# Attempts remaining text
def draw_attempts_remaining():
    turtleAttemptsRemaining_dynamic.clear()

    turtleAttemptsRemaining_dynamic.penup()
    turtleAttemptsRemaining_dynamic.goto(-130, -300)
    turtleAttemptsRemaining_dynamic.pendown()
    turtleAttemptsRemaining_dynamic.write(attempts_counter, font=turtleAttemptsRemainingStyle, align="left")

    turtleAttemptsRemaining_dynamic.penup()
    turtleAttemptsRemaining_dynamic.goto(-110, -300)
    turtleAttemptsRemaining_dynamic.pendown()
    turtleAttemptsRemaining_dynamic.write("attempt(s) remaining", font=turtleAttemptsRemainingStyle, align="left")

# Static text displayed in the Turtle window
def turtle_gfx_text_static():
    turtleText_static = turtle.Turtle()
    turtleText_static.hideturtle()
    turtleText_static.color("blue")
    guessWordStyle=("calibri", 30, "italic")
    turtleWrongGuessesStyle = ("calibri", 30, "italic")
    turtleText_static.penup()
    turtleText_static.goto(-300, 250)
    turtleText_static.pendown()
    turtleText_static.write("GUESS THE WORD:", font=guessWordStyle, align="left")

    turtleText_static.color("green")
    turtleText_static.penup()
    turtleText_static.goto(-300, -200)
    turtleText_static.pendown()
    turtleText_static.write("WRONG GUESSES:", font=turtleWrongGuessesStyle, align="left")

#Turtle Ambulance Main Body
def turtle_gfx_attempt_ONE():
    turtleDrawShapes.penup()
    turtleDrawShapes.goto(-200, -100)
    turtleDrawShapes.color("blue", "white")
    turtleDrawShapes.pendown()
    turtleDrawShapes.begin_fill()
    for i in range(2):
        turtleDrawShapes.forward(240)
        turtleDrawShapes.left(90)
        turtleDrawShapes.forward(200)
        turtleDrawShapes.left(90)
    turtleDrawShapes.end_fill()
    turtleDrawShapes.penup()
    
#Turtle Ambulance Front
def turtle_gfx_attempt_TWO():
    turtleDrawShapes.goto(40, -100)
    turtleDrawShapes.color("blue", "white")
    turtleDrawShapes.pendown()
    turtleDrawShapes.begin_fill()
    for i in range(4):
        turtleDrawShapes.forward(150)
        turtleDrawShapes.left(90)
    turtleDrawShapes.end_fill()
    turtleDrawShapes.penup()
    
#Turtle Ambulance Back Wheel
def turtle_gfx_attempt_THREE():
    turtleDrawShapes.setpos(-140, -150)
    turtleDrawShapes.fillcolor("blue")
    turtleDrawShapes.pendown()
    turtleDrawShapes.begin_fill()
    turtleDrawShapes.circle(50)
    turtleDrawShapes.end_fill()
    turtleDrawShapes.penup()

#Turtle Ambulance Front Wheel
def turtle_gfx_attempt_FOUR():
    turtleDrawShapes.setpos(110, -150)
    turtleDrawShapes.fillcolor("blue")
    turtleDrawShapes.pendown()
    turtleDrawShapes.begin_fill()
    turtleDrawShapes.circle(50)
    turtleDrawShapes.end_fill()
    turtleDrawShapes.penup()

#Turtle Ambulance Windscreen
def turtle_gfx_attempt_FIVE():
    turtleDrawShapes.setpos(70, 0)
    turtleDrawShapes.color("blue", "white")
    turtleDrawShapes.pendown()
    turtleDrawShapes.begin_fill
    for i in range(2):
        turtleDrawShapes.forward(70)
        turtleDrawShapes.left(90)
        turtleDrawShapes.forward(30)
        turtleDrawShapes.left(90)
    turtleDrawShapes.end_fill()
    turtleDrawShapes.penup()

#Turtle Ambulance ELS (Light)
def turtle_gfx_attempt_SIX():
    turtleDrawShapes.setpos(-100, 100)
    turtleDrawShapes.color("blue", "red")
    turtleDrawShapes.pendown()
    turtleDrawShapes.begin_fill()
    for i in range(2):
        turtleDrawShapes.forward(40)
        turtleDrawShapes.left(90)
        turtleDrawShapes.forward(15)
        turtleDrawShapes.left(90)
    turtleDrawShapes.end_fill()
    turtleDrawShapes.penup()

#Turtle Ambulance Red-Cross Part 1 (Vertical)
def turtle_gfx_attempt_SEVEN():
    turtleDrawShapes.setpos(-100, -30)
    turtleDrawShapes.color("red")
    turtleDrawShapes.pendown()
    turtleDrawShapes.begin_fill()
    for i in range(2):
        turtleDrawShapes.forward(40)
        turtleDrawShapes.left(90)
        turtleDrawShapes.forward(100)
        turtleDrawShapes.left(90)
    turtleDrawShapes.end_fill()
    turtleDrawShapes.penup()

# Turtle Ambulance Red-Cross Part 2 (Horizontal)    
def turtle_gfx_attempt_EIGHT():
    turtleDrawShapes.setpos(-130, 0)
    turtleDrawShapes.color("red")
    turtleDrawShapes.pendown()
    turtleDrawShapes.begin_fill()
    for i in range(2):
        turtleDrawShapes.forward(100)
        turtleDrawShapes.left(90)
        turtleDrawShapes.forward(40)
        turtleDrawShapes.left(90)
    turtleDrawShapes.end_fill()
    turtleDrawShapes.penup()

#----------EXTERIOR FUNCTION CALLS----------# 
main()
