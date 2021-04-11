import curses, os, sys
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint, choice, randrange
from time import sleep

curses.initscr()  # initialize screen
window = curses.newwin(30, 60, 0, 0)  # Create a new window
window.keypad(True)  # Turn on keypad
curses.noecho()  # Turn off echo
curses.curs_set(0)
randomColor = 1
window.nodelay(True)  # Don't wait for any input

# Init colors
curses.start_color()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)


# initiate values
key = KEY_RIGHT
score = 0
# initialize first fruit and snake coordinates
snake = [[5, 8], [5, 7], [5, 6]]
fruit = [10, 25]
fruitIcon = ["○", "Ω", "♥", "♦", "♣", "♠"]
# Display the first fruit
window.addch(fruit[0], fruit[1], choice(fruitIcon), curses.color_pair(1))

while key != 27:  # While they Esc key is not being pressed
    window.border(0)
    # Display the score and the title
    window.addstr(0, 2, "Score: " + str(score) + " ")
    window.addstr(0, 27, " Snake ")
    window.addstr(29, 2, " By: Alex Yoesting ")
    window.addstr(29, 44, " Next Point: " + str(randomColor) + " ")
    # Makes the snake speed up as it eats more
    window.timeout(140 - (int(len(snake) / 5) + int(len(snake) / 10) % 120))
    # refreshes the screen and then waits for the user to hit a key
    event = window.getch()
    key = key if event == -1 else event

    # Calculates the new coordinates of the head of the snake.
    snake.insert(
        0,
        [
            snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1),
            snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1),
        ],
    )
    # Exit if snake crosses the boundaries (Uncomment to enable)
    if snake[0][0] == 0 or snake[0][0] == 29 or snake[0][1] == 0 or snake[0][1] == 59:
        break
    # Exit if snake runs over itself
    if snake[0] in snake[1:]:
        break

    # When the snake eats the fruit
    if snake[0] == fruit:
        fruit = []
        if randomColor == 1:
            score += 1
        else:
            score += randomColor

        while fruit == []:
            # Generate coordinates for next piece of fruit
            fruit = [randint(1, 28), randint(1, 58)]
            if fruit in snake:
                fruit = []
        randomColor = randrange(1, 5)
        window.addch(
            fruit[0], fruit[1], choice(fruitIcon), curses.color_pair(randomColor)
        )  # Render the fruit
    else:
        last = snake.pop()
        window.addch(last[0], last[1], " ")
    window.addch(
        snake[0][0], snake[0][1], "■", curses.color_pair(5)
    )  # Add a block to snakes tail


def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question + " (y/n): ")).lower().strip()
        if reply[0] == "y":
            return True
        if reply[0] == "n":
            return False


curses.endwin()  # Close the window and ends the game
print("\nScore: " + str(score))  # Prints the score on game end
continueGame = yes_or_no("Woule you like to play again?")

if continueGame == True:
    sleep(1)
    os.execv(sys.executable, sys.argv)

# curses.endwin()  # Close the window and ends the game
# print("\nScore: " + str(score))  # Prints the score on game end
