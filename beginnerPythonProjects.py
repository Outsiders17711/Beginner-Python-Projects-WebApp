# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ### 12 Beginner Python Projects - Coding Course - Kylie Ying
#
# +  https://www.youtube.com/watch?v=8ext9G7xspg

# %% [markdown]
# #### 1. MADLIBS

# %%
def madlibs():
    try:
        adj = input("Adjective; type [x] to quit:  ")
        if adj == "x":
            raise ValueError
        verb1 = input("Verb; type [x] to quit:  ")
        if verb1 == "x":
            raise ValueError
        verb2 = input("Verb; type [x] to quit:  ")
        if verb2 == "x":
            raise ValueError
        famous_person = input("Famous Person; type [x] to quit:  ")
        if famous_person == "x":
            raise ValueError

        madlib = f"\nOUTPUT:\nComputer programming is so {adj}! It makes me so excited all the time because I love to {verb1}. Stay hydrated and {verb2} like you are {famous_person}!"

        print(madlib)
    except ValueError:
        print("quitting...")


if __name__ == "__main__":
    madlibs()

# %% [markdown]
# #### 2. GUESS THE NUMBER (COMPUTER)

# %%
import random


def userGuess(x):
    random_number = random.randint(1, x)
    guess = 0

    while guess != random_number:
        try:
            guess = int(
                input(f"Guess a random number between 1 and {x}; type [x] to quit:  ")
            )
            if guess < random_number:
                print("Sorry. Too low. Guess again!")
                continue
            elif guess > random_number:
                print("Sorry. Too high. Guess again!")
                continue

            print(f"Yay! You have guessed the number {random_number} correctly!")

        except ValueError:
            print("quitting...")
            break


if __name__ == "__main__":
    userGuess(10)

# %% [markdown]
# #### 2. GUESS THE NUMBER (USER)

# %%
import random


def computerGuess(x):
    low = 1
    high = x

    feedback = ""
    quitGame = False
    guess = None

    while feedback != "c":
        if low != high:
            guess = random.randint(low, high)
        else:
            guess = low  # could also be high since low=high

        feedback = input(
            f"Is {guess} too high [H], too low [L], or correct [C]. Type [X] to quit."
        ).lower()
        if feedback == "h":
            high = guess - 1
        elif feedback == "l":
            low = guess + 1
        elif feedback == "x":
            print("Quitting...")
            quitGame = True
            break

        else:
            print("Invalid input. Try again!")
            continue

    if not quitGame:
        print(f"Yay! The computer guessed your the number {guess} correctly!")


if __name__ == "__main__":
    computerGuess(1000)

# %% [markdown]
# #### 4. ROCK PAPER SCISSORS

# %%
import random


def playRockPaperScissors():
    user = None
    while user is None:
        temp = input(
            "CHOOSE: [r] for rock\n; [p] for paper; [s] for scissors; [x] to quit"
        ).lower()
        user = (
            temp if temp in ["r", "p", "s", "x"] else print("Invalid input. Try again!")
        )

    if user == "x":
        return "quitting..."

    computer = random.choice(["r", "p", "s"])
    print(f"Computer chose [{computer}]...")

    if user == computer:
        return "It's a tie!"

    # r > s; s > p, p > r
    if is_win(user, computer):
        return "You won!"

    return "You lost!"


def is_win(player, opponent):
    # r > s; s > p, p > r
    if (
        (player == "r" and opponent == "s")
        or (player == "s" and opponent == "p")
        or (player == "p" and opponent == "r")
    ):
        return True  # player won
    else:
        return False


if __name__ == "__main__":
    print(playRockPaperScissors())

# %% [markdown]
# ### 5. HANGMAN

# list of words gotten from [https://github.com/dwyl/english-words]

# %%
import random
import string

data_path = r"data\\"


def loadWords():
    with open(f"{data_path}englishWords.alpha.txt") as f:
        englishWords = sorted(set(f.read().split()))

    return englishWords


def get_validWord():
    englishWords = loadWords()
    word = random.choice(englishWords)
    while "-" in word or " " in word:
        word = random.choice(englishWords)

    return word.upper()


def hangman():
    word = get_validWord()
    word_letters = set(word)  # get all characters in the words
    alphabet = set(string.ascii_uppercase)
    used_letters = set()  # what the user has guessed
    n_lifes = 6
    word_list = []

    # getting user input
    while len(word_letters) > 0 and n_lifes > 0:
        # letters used
        print("You have used these letters: ", " ".join(used_letters))
        # number of lifes left
        print(f"You have {n_lifes} lives left")
        # current word with placeholders
        word_list = [letter if letter in used_letters else "-" for letter in word]
        print("Current word: ", "".join(word_list), "\n")

        user_letter = input("Guess a letter; enter [xx] to quit: ").upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                print("Character is not in word. Try again!")
                n_lifes -= 1

        elif user_letter in used_letters:
            print("You have already used that character. Try again!")

        elif user_letter.lower() == "xx":
            print(f"\nThe word is {word}")
            print("quitting...")
            break

        else:
            print("Invalid character. Try again!!")

    if "".join(word_list) == word:
        print(f"\nCongratulations! You guessed the word [{word}] correctly!!")
    else:
        print(f"\nThe word is {word}")
        print("Game over! Try again!")


if __name__ == "__main__":
    hangman()

# %% [markdown]
# ### 6. TIC-TAC-TOE

# %%
import time
import random
import math

# [start]____________________________________________________________
class Player:
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter

    # we want all players to get their next move
    def get_move(self, game):
        pass


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        # get a random valid spot for the next move
        square = random.choice(game.available_moves())
        return square


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None

        while not valid_square:
            square = input(self.letter + "'s turn. Input move (0-8); Enter [x] to quit: ")

            # quitting the game
            if square == "x":
                print("quitting...")
                return "quitGame"

            # checking if the input and the square are both valid
            try:
                val = int(square)

                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print("Invalid square. Try again!")

        return val


# [start]____________________________________________________________
# defining a minimax function so that the computer makes the best possible move
class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())  # choose random spot
        else:
            # get the square uisng the minimax algorithm
            square = self.minimax(game, self.letter)["position"]

        return square

    def minimax(self, gameState, player):
        max_player = self.letter  # yourself
        other_player = "O" if player == "X" else "X"

        # check if the previous move is a winner; base case
        if gameState.current_winner != None:
            # we need to track the position and score
            return {
                "position": None,
                "score": 1 * (gameState.num_empty_squares() + 1)
                if gameState.current_winner == max_player
                else -1 * (gameState.num_empty_squares() + 1),
            }

        elif not gameState.empty_squares():  # no winner and board is filled
            return {"position": None, "score": 0}

        if player == max_player:
            # each score should maximize (be larger); so we start at the lowest possible score ( negative infinity)
            best = {"position": None, "score": -math.inf}
        else:
            # each score should minimize (be smaller); so we start at the highest possible score (positive infinity)
            best = {"position": None, "score": math.inf}

        for possible_move in gameState.available_moves():
            # step 1: make a move; try that spot
            gameState.make_move(possible_move, player)
            # step 2: recurse after minimax to simulate a game after making that move
            sim_score = self.minimax(gameState, other_player)  # alternate players
            # step 3: undo the move; so we can try other moves
            gameState.board[possible_move] = " "
            gameState.current_winner = None
            sim_score["position"] = possible_move
            # step 4: update the dictionaries if necessary
            if player == max_player:
                if sim_score["score"] > best["score"]:
                    best = sim_score  # replace best; maximize max_player
            else:
                if sim_score["score"] < best["score"]:
                    best = sim_score  # replace best; minimize other_player
        return best


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
# [start]____________________________________________________________
# defining the game itself
class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]  # a single list representing 3x3
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i * 3 : (i + 1) * 3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 3 ... for each cell in the board
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]

        print("BOARD LAYOUT:")
        for row in number_board:
            print("\t\t| " + " | ".join(row) + " |")
        print("")

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def empty_squares(self):
        return " " in self.board

    def num_empty_squares(self):
        # return len(self.available_moves())
        return self.board.count(" ")

    def make_move(self, square, letter):
        if self.board[square] == " ":
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # winner if 3 in a row in [row, column, or diagonal]
        # checking rows:
        row_idx = square // 3
        row = self.board[row_idx * 3 : (row_idx + 1) * 3]
        if all([spot == letter for spot in row]):
            return True

        # checking columns:
        col_idx = square % 3
        column = [self.board[col_idx + (i * 3)] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # checking disgonals:
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]  # top-left-->bottom-right
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]  # top-right-->bottom-left
            if all([spot == letter for spot in diagonal2]):
                return True

        # if all checks fail
        return False


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
# [start]____________________________________________________________
def playTicTacToe(game, x_player, o_player, print_game=True):
    # retuns the winner of the game or None for a tie.
    if print_game:
        game.print_board_nums()

    letter = "X"  # starting square
    while game.empty_squares():
        # get move from the appropriate player
        if letter == "O":
            square = o_player.get_move(game)
            current_player = o_player
        else:
            square = x_player.get_move(game)
            current_player = x_player

        type_player = str(type(current_player)).split(".")[-1][:-2]
        if square == "quitGame":
            print(f"{type_player} <'{letter}'> quits!")
            return letter

        if game.make_move(square, letter):
            if print_game:
                print(letter + f" makes a move to square {square}...")
                game.print_board()
                print("")  # empty line

            if game.current_winner:
                if print_game:
                    print(f"{type_player} <'{letter}'> wins!!")
                return letter

        # after making a move, switch letters (players)
        letter = "O" if letter == "X" else "X"

        # add pause
        if (
            isinstance(x_player, RandomComputerPlayer)
            or isinstance(o_player, RandomComputerPlayer)
            or isinstance(x_player, GeniusComputerPlayer)
            or isinstance(o_player, GeniusComputerPlayer)
        ) and print_game:
            time.sleep(1)

    if print_game:
        print("It's a tie.")


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
if __name__ == "__main__":
    x_player = GeniusComputerPlayer("X")
    o_player = HumanPlayer("O")
    gameInstance = TicTacToe()
    playTicTacToe(gameInstance, x_player, o_player, print_game=True)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]

# %% [markdown]
# ### 7. BINARY SEARCH

# %%
import random
import time
from tqdm import tqdm
import sys

# [start]____________________________________________________________
def naive_search(l, target):
    for i in range(len(l)):
        if l[i] == target:
            return i
    return -1  # if the target is not found


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
# [start]____________________________________________________________
def binary_search(l, target, low=None, high=None):
    if low is None:
        low = 0
    if high is None:
        high = len(l) - 1

    if high < low:
        return -1  # if the target is not found

    # midpoint = len(l) // 2 # alternative
    midpoint = (low + high) // 2

    if l[midpoint] == target:
        return midpoint
    elif target < midpoint:
        # return binary_search(l[:midpoint-1], target) # alternative
        return binary_search(l, target, low, midpoint - 1)
    elif target > midpoint:
        # return binary_search(l[midpoint+1:], target) # alternative
        return binary_search(l, target, midpoint + 1, high)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
# [start]____________________________________________________________
def compareNativeBinary(length=10000):
    length = 10000
    # build a sorted list of length 10000
    sorted_list = set()
    while len(sorted_list) < length:
        sorted_list.add(random.randint(-3 * length, 3 * length))
    sorted_list = sorted(list(sorted_list))

    sttTime = time.time()
    with tqdm(total=length, desc="Naive Search", position=0, file=sys.stdout) as pbar1:
        for target in sorted_list:
            naive_search(sorted_list, target)
            pbar1.update(1)
    endTime = time.time()
    naiveTime = (endTime - sttTime) / length
    print(f"  {naiveTime:.7f} seconds per iteration...")

    sttTime = time.time()
    with tqdm(total=length, desc="Binary Search", position=1, file=sys.stdout) as pbar2:
        for target in sorted_list:
            binary_search(sorted_list, target)
            pbar2.update(1)
    endTime = time.time()
    binaryTime = (endTime - sttTime) / length
    print(f"  {binaryTime:.7f} seconds per iteration...")

    print(
        f"\nBinary search is {naiveTime/binaryTime:.2f} times faster then Naive search..."
    )


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
# [start]____________________________________________________________
if __name__ == "__main__":
    compareNativeBinary()

# %% [markdown]
# ### 9. MINESWEEPER

# %%
import random
import regex as re

# [start]____________________________________________________________
class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # creating the board
        self.board = self.make_new_board()  # plant bombs too
        self.assign_values_to_board()

        # init a set to keep track of uncovered locations; save (row, column) tuples
        self.dug = set()

    def make_new_board(self):
        # create board based on dim_size and num_bombs; using list of lists
        board = [[" " for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size ** 2 - 1)  # 0 <= N <= 99 in this case
            row = loc // self.dim_size  # number of times dim_size goes into loc
            col = loc % self.dim_size  # remainder from the above division

            if board[row][col] == "*":
                # this means a bomb has been planted at this loc; restart the loop
                continue

            board[row][col] = "*"
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        # assign number from 0-8 to a cell represeting the number of bombs in adjacent cells
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    continue
                self.board[r][c] = self.get_num_neighbouring_bombs(r, c)

    def get_num_neighbouring_bombs(self, row, col):
        # itertaing through all adjacent cells:
        # top left: [row-1, col-1]
        # top middle: [row-1, col]
        # top right: [row-1, col+1]
        # left: [row, col-1]
        # right: [row, col+1]
        # bottom left: [row+1, col-1]
        # bottom middle: [row+1, col]
        # bottom right: [row+1, col+1]

        num_neighbouring_bombs = 0
        # the max and min is to make sure we dont go out of bounds at the board edges
        for r in range(max(0, row - 1), min(self.dim_size - 1, (row + 1)) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, (col + 1)) + 1):
                if r == row and c == col:
                    # original location, dont check
                    continue
                if self.board[r][c] == "*":
                    num_neighbouring_bombs += 1

        return num_neighbouring_bombs

    def dig(self, row, col):
        # dig at that location
        # return True [successful dig]; False [bomb located]

        self.dug.add((row, col))  # keep track of dug locations

        # scenerios:
        if self.board[row][col] == "*":
            # dig location has a bomb -> game over
            return False
        elif self.board[row][col] > 0:
            # dig location has neighbouring bombs -> finish dig
            return True
        elif self.board[row][col] == 0:
            # dig location has no neighbouring bombs -> recursively dig neighbours
            for r in range(max(0, row - 1), min(self.dim_size - 1, (row + 1)) + 1):
                for c in range(max(0, col - 1), min(self.dim_size - 1, (col + 1)) + 1):
                    if (r, c) in self.dug:
                        continue  # dug location, dont check
                    self.dig(r, c)

        # since there wasnt a bomb in the first scenerio; we shouldnt hit a bomb here
        return True

    def __str__(self):
        # this is a magic function; if print is called on this object (class Board); it will print out whatever this function returns
        # we ll return a string that shows the board to the player

        # array that represents what the user should see
        visible_board = [
            [" " for _ in range(self.dim_size)] for _ in range(self.dim_size)
        ]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = self.board[row][col]
                else:
                    visible_board[row][col] = " "

        # convert the visible_board array into a formatted string
        padding = self.dim_size * 5
        visible_board_string = ""
        visible_board_string += (
            "\n"
            + ("< BOARD LAYOUT >").center(padding, "=")
            + "\n"
            + (
                "      " + "   ".join([str(i) for i in range(self.dim_size)]) + "   "
            ).center(padding, " ")
            + "\n"
            + ("").center(padding, "-")
            + "\n"
        )

        for row in range(self.dim_size):
            visible_board_string += (
                (
                    f"{row}  | " + " | ".join([str(i) for i in visible_board[row]]) + " |"
                ).center(padding, " ")
                + "\n"
                + ("").center(padding, "-")
                + "\n"
            )

        return visible_board_string


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
# [start]____________________________________________________________
def playMineSweeper(dim_size=10, num_bombs=10):
    # Step 1: create the board and plant the bombs
    # Step 2: show the user the board and ask where they want to dig
    # Step 3a: if the location is a bomb, show game over message
    # Step 3b: dig recursively until each square is at least next to a bomb
    # Step 4: repeat steps 2 and 3a/b until there are no more places to dig -> VICTORY!

    board = Board(dim_size, num_bombs)

    safeDigging = True
    quitGame = False
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = input(
            "Where would you like to dig [row,column]?; types [x] to quit : "
        )
        if user_input.lower() == "x":
            safeDigging = False
            quitGame = True
            break

        # checking that the inputs are in the required format
        try:
            if "." in user_input:
                regex_exp = "\\.(\\s)*"
            elif "," in user_input:
                regex_exp = ",(\\s)*"
            else:
                raise ValueError

            user_input = re.split(regex_exp, user_input)  # to handle [0.0; 0. 0; 0.   0]
            row, col = int(user_input[0]), int(user_input[-1])

        except:
            print("Invalid input! Try again!")
            continue

        # checking that inputs are within bounds
        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print("Invalid location! Out of bounds! Try again!")
            continue

        # for valid locations
        safeDigging = board.dig(row, col)
        if not safeDigging:
            # game over; break the loop
            break

    if safeDigging:
        # if we went through the board without hitting any bombs
        print("Congratulations! You are victorious!!")
    elif not safeDigging:
        if quitGame:
            # user quit the game
            print("quitting...")
        else:
            # if we hit a bomb at any point
            print("You hit a bomb! Game over!!")

    # reveal the entire board
    # set all cells as dug; making them visible
    board.dug = set(
        [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
    )
    print(board)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
if __name__ == "__main__":
    playMineSweeper(dim_size=10, num_bombs=10)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]

# %% [markdown]
# ### 10. SUDOKU SOLVER

# %%
import random
import time
from collections import Counter
import regex as re
import copy

# convert the visible_board array into a formatted string
# [start]____________________________________________________________
def printBoard(puzzle):
    dim_size = len(puzzle[0])
    padding = dim_size * 5

    board_string = ("< BOARD LAYOUT >").center(padding, "-") + "\n" + " " * 7
    for i in range(dim_size):
        board_string += (f"-{i+1}-").center(4, " ")
    board_string += "\n"
    board_string += ("").center(padding, "-") + "\n"

    for row in range(dim_size):
        row_string = (f"-{row+1}- ").center(3, " ")
        row_string += "|"
        for col in range(dim_size):
            row_string += (f"{puzzle[row][col]}").center(3, " ") + "|"

        board_string += (row_string).center(padding, " ") + "\n"
        board_string += ("").center(padding, "-") + "\n"

    print(board_string)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
# filling the puzzle
# [start]____________________________________________________________
def fillSudokuBoard(percent_filled_cells=0.75, addBlanks=True, verbose=False):
    dim_size = 9
    puzzle = [[None for _ in range(1, dim_size + 1)] for _ in range(1, dim_size + 1)]
    possible_values = set([i for i in range(1, dim_size + 1)])
    num_blank_cells = int((dim_size ** 2) - percent_filled_cells * (dim_size ** 2))

    numTries = 0
    sttTime = time.time()
    try:
        numTries += 1
        for row in range(dim_size):
            for col in range(dim_size):
                current_row = puzzle[row]
                current_col = [row[col] for row in puzzle]
                # or
                # current_col = [
                #     _col
                #     for _row in puzzle
                #     for _idx, _col in enumerate(_row)
                #     if _idx == col
                # ]

                grid1, grid2 = row // 3, col // 3
                grid = [
                    [puzzle[idxr][idxc] for idxc in range(grid2 * 3, (grid2 + 1) * 3)]
                    for idxr in range(grid1 * 3, (grid1 + 1) * 3)
                ]
                current_grid = [
                    puzzle[idxr][idxc]
                    for idxc in range(grid2 * 3, (grid2 + 1) * 3)
                    for idxr in range(grid1 * 3, (grid1 + 1) * 3)
                ]
                available_values = (
                    possible_values
                    - set(current_row)
                    - set(current_col)
                    - set(current_grid)
                )

                if verbose:
                    print("current_row", current_row, "current_col", current_col)
                    print("available_values", available_values)
                    printBoard(puzzle)

                while (
                    # current_row.count(puzzle[row][col]) > 1
                    Counter(current_row)[puzzle[row][col]] > 1
                    # or current_col.count(puzzle[row][col]) > 1
                    or Counter(current_col)[puzzle[row][col]] > 1
                    or puzzle[row][col] is None
                ):
                    random_int = random.choice(list(available_values))
                    if random_int not in current_row and random_int not in current_col:
                        puzzle[row][col] = random_int

        endTime = time.time()
        if verbose:
            print(f"after {numTries} tries and {endTime-sttTime:.3f} seconds....")
            printBoard(puzzle)

        if addBlanks:
            for _ in range(num_blank_cells):
                puzzle[random.randint(0, dim_size - 1)][
                    random.randint(0, dim_size - 1)
                ] = "*"

    except IndexError:
        if verbose:
            print("IndexError: trying again....")
        puzzle = fillSudokuBoard(
            percent_filled_cells=percent_filled_cells, addBlanks=addBlanks
        )

    return puzzle


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
def find_next_empty(puzzle):
    # finds the next empty row, col thats not filled yet (represented by *)
    # return (row, col) tuple or (None, None) if all cells are filled

    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == "*":
                return r, c

    return None, None  # no empty spaces; all cells are filled


def is_valid(puzzle, guess, row, col):
    # figures out if the guess at the row, column, and grid are valid
    # row
    row_vals = puzzle[row]
    if guess in row_vals:
        return False
    # col
    col_vals = [row[col] for row in puzzle]
    if guess in col_vals:
        return False
    # grid
    gridr, gridc = (row // 3) * 3, (col // 3) * 3
    for r in range(gridr, gridr + 3):
        for c in range(gridc, gridc + 3):
            if puzzle[r][c] == guess:
                return False

    # else, the guess is valid
    return True


def solveSudoku(puzzle, verbose=False):
    # solve using a backtracking technique
    # the puzzle is a list of lists; each inner list is a row in the puzzle
    # return whether a solution exists
    # mutates the puzzle to be the solution; if solution exists

    # step 1: choose somewhere to make a guess
    row, col = find_next_empty(puzzle)
    if verbose:
        print(f"empty @ row={row+1}, col={col+1}") if row is not None else print(
            f"empty @ row={row}, col={col}"
        )

    # step 1: if all cells are filled, then we are done
    if row is None:  # or col is None
        return True

    # step 2: if there is an empty space, make a guess between 1 and 9
    for guess in range(1, 10):
        # step 3: check if this is a valid guess
        if is_valid(puzzle, guess, row, col):
            # step 3.1: if this is a valid guess, place in the puzzle
            puzzle[row][col] = guess
            # step 4: now recurse the function
            if solveSudoku(puzzle):
                return True

        # step 5: if not valid OR or the guess did not solve the puzzle;
        # we need to back track
        puzzle[row][col] = "*"  # resetting the value at that cell

    # step 6: if still no solution
    return False


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
# [start]____________________________________________________________
def _checkEmptyCells(puzzle):
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == "*":
                return False

    return True  # no empty spaces; all cells are filled


def _getUserInput(type, puzzle=None):
    output = None
    try:
        if type == "difficulty":
            difficulty = input("Enter the difficulty level [1/2/3]; type [x] to quit: ")
            if difficulty.lower() == "x":
                print("quitting...")
                return "quitGame"

            if int(difficulty) not in [1, 2, 3]:
                raise ValueError

            difficulty = 10 - int(difficulty)
            output = difficulty

        elif type == "coordinates":
            coordinates = input(
                "Where would you like to play [row(,/.)column]?; type [x] to quit : "
            )
            if coordinates.lower() == "x":
                print("quitting...")
                return "quitGame", "quitGame"

            if "." in coordinates:
                regex_exp = "\\.(\\s)*"
            elif "," in coordinates:
                regex_exp = ",(\\s)*"
            else:
                raise ValueError

            coordinates = re.split(regex_exp, coordinates)
            row, col = int(coordinates[0]) - 1, int(coordinates[-1]) - 1

            # checking that inputs are within bounds
            if row < 0 or row >= 9 or col < 0 or col >= 9 or puzzle[row][col] != "*":
                print("Invalid location! Out of bounds!")
                raise ValueError

            output = row, col

        elif type == "cellvalue":
            cellvalue = input("Enter the cell value [1-9]; type [x] to quit : ")
            if cellvalue.lower() == "x":
                print("quitting...")
                return "quitGame"

            if int(cellvalue) < 1 or int(cellvalue) > 9:
                raise ValueError

            output = int(cellvalue)

    except ValueError:
        print("Invalid input. Try again!")
        output = _getUserInput(type, puzzle)

    return output


def _checkWinStatus(puzzle):
    winStatus = True
    chars = set("[]")

    for row in range(9):
        for col in range(9):
            if isinstance(puzzle[row][col], str):
                cellvalue = int("".join(i for i in puzzle[row][col] if i not in chars))

                cellStatus = "CORRECT!"
                row_vals = puzzle[row]
                if cellvalue in row_vals:
                    cellStatus = "WRONG!"
                    winStatus = False
                col_vals = [row[col] for row in puzzle]
                if cellvalue in col_vals:
                    cellStatus = "WRONG!"
                    winStatus = False
                gridr, gridc = (row // 3) * 3, (col // 3) * 3
                for r in range(gridr, gridr + 3):
                    for c in range(gridc, gridc + 3):
                        if puzzle[r][c] == cellvalue:
                            cellStatus = "WRONG!"
                            winStatus = False

                print(f"checking cell @ row={row+1}.column={col+1}....{cellStatus}")

    return winStatus


def playSudoku():
    playGame = True
    quitGame = False
    gameBoard, b_gameBoard = [], []

    difficulty = _getUserInput("difficulty")
    if difficulty == "quitGame":
        playGame = False
        quitGame = True

    if playGame:
        gameBoard = fillSudokuBoard(percent_filled_cells=(0.1055 * difficulty))
        b_gameBoard = copy.deepcopy(gameBoard)

    while playGame:
        printBoard(gameBoard)
        row, col = _getUserInput("coordinates", gameBoard)
        if row == "quitGame":
            playGame = False
            break

        cellvalue = _getUserInput("cellvalue")
        if cellvalue == "quitGame":
            playGame = False
            break

        gameBoard[row][col] = f"[{cellvalue}]"
        if _checkEmptyCells(gameBoard):
            break

    if playGame and not quitGame:
        print("all cells have been filled; checking if cell values are correct...")

        if _checkWinStatus(gameBoard):
            print("Congratulations! You won!!")
        else:
            print("Sorry. You lost.")

    if not quitGame:
        print("The answer is:")
        solveSudoku(b_gameBoard)
        printBoard(b_gameBoard)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
if __name__ == "__main__":
    # exampleBoard = fillSudokuBoard(addBlanks=True, percent_filled_cells=0.95)
    # print(solveSudoku(exampleBoard))
    # printBoard(exampleBoard)
    playSudoku()


# %% [markdown]
# ### PHOTO PROCESSING

# https://github.com/kying18/pyphotoshop
# python files are in the _beginnerPythonProjects folder

# %% [markdown]
# ### MARKOV CHAIN TEXT COMPOSER

# https://github.com/kying18/graph-composer
# python files are in the _beginnerPythonProjects folder

# %%
# my markov chain implementation using dictionaries
import string
import random

# [start]____________________________________________________________
def createMarkovChain(raw_string):
    words = " ".join(raw_string.lower().split())

    punctuation = "".join(
        [c for c in string.punctuation] + ["\u201c", "\u201d", "\u2018", "\u2019"]
    )
    words = words.translate(str.maketrans("", "", punctuation))
    words = words.split()

    markovChain = {}
    for idx, word in enumerate(words):
        if idx + 1 < len(words):
            if word not in markovChain.keys():
                markovChain[word] = {words[idx + 1]: 1}
            elif word in markovChain.keys():
                markovChain[word][words[idx + 1]] = (
                    1
                    if words[idx + 1] not in markovChain[word].keys()
                    else markovChain[word][words[idx + 1]] + 1
                )

    return markovChain


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
def chooseNextWord(current_word, chain, type):
    if type == "best":
        n_occurs_best_next = max(list(chain[current_word].values()))
        idx_best_next = list(chain[current_word].values()).index(n_occurs_best_next)
        best_next = list(chain[current_word].keys())[idx_best_next]

        return best_next

    elif type == "weighted":
        word_weights = list(chain[current_word].values())
        word_choices = list(chain[current_word].keys())
        weighted_next = random.choices(word_choices, word_weights, k=1)[0]

        # n_occurs_weighted_next = chain[current_word][weighted_next]
        # print('n_occurs_best_next', n_occurs_best_next, 'n_occurs_weighted_next', n_occurs_weighted_next)

        return weighted_next


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
def getPredictedString(
    raw_string, length_string, starting_word=None, prediction_type="weighted"
):

    markov_chain = createMarkovChain(raw_string)

    if starting_word is None:
        starting_word = random.choice(list(markov_chain.keys()))

    output_string = []
    while length_string > len(output_string):
        next_word = chooseNextWord(starting_word, markov_chain, prediction_type)
        output_string.append(next_word)
        starting_word = next_word

    output_string = " ".join(output_string)
    print("output_string:\n", output_string)
    return output_string


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
if __name__ == "__main__":
    with open(r"data\texts\wuthering_heights.txt", "r", encoding="utf-8") as f:
        raw_string = f.read()
    getPredictedString(raw_string, 50)
# %% [markdown]
# ## _end
