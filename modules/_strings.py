import streamlit as st

import gc

gc.enable()

# [start]____________________________________________________________
pageConfig = """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
            width: 450px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
            width: 500px;
            margin-left: -450px;
        }
        </style>
        """
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]

nbsp = "&nbsp"
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]


@st.cache()
def aboutMe():
    return """
        ## **Hi 👋 I'm Umar...**

        <div style="text-align: justify;">

        I'm a highly resourceful mechanical engineer with over three years of industry experience in construction and telecommunications. I'm currently doing my masters in Robotics, Control and Smart Systems at the American University in Cairo.

        You can check out my personal [![](https://img.shields.io/static/v1?label=GitHub%20Pages&message=Blog&labelColor=2f363d&color=blue&style=flat&logo=github)](https://outsiders17711.github.io/Mein.Platz/) where I detail my experiences and development with `Machine Learning`, `Computer Vision` and `Gesture Recognition` as I work on my masters.

        </div>

        <hr>
        
        <div style="text-align: center;">

        ## 🔭 **Tools of Trade**

        🛠 **Programming**
        
        ![](https://img.shields.io/badge/python-%2314354C.svg?style=flat&logo=python&logoColor=white) | ![](https://img.shields.io/badge/markdown-%23000000.svg?style=flat&logo=markdown&logoColor=white) | ![](https://img.shields.io/badge/VisualStudioCode-0078d7.svg?style=flat&logo=visual-studio-code&logoColor=white) | ![](https://img.shields.io/badge/Jupyter-%23F37626.svg?style=flat&logo=Jupyter&logoColor=white) | ![](https://img.shields.io/badge/git-%23F05033.svg?style=flat&logo=git&logoColor=white) | ![](https://img.shields.io/badge/github-%23121011.svg?style=flat&logo=github&logoColor=white)
        
        <br>

        🛠 **Machine Learning & Computer Vision**
        
        ![](https://img.shields.io/badge/Keras-%23D00000.svg?style=flat&logo=Keras&logoColor=white) | ![](https://img.shields.io/badge/opencv-%23white.svg?style=flat&logo=opencv&logoColor=white) | ![](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=flat&logo=TensorFlow&logoColor=white) | ![](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=flat&logo=PyTorch&logoColor=white) | ![](https://img.shields.io/badge/pandas-%23150458.svg?style=flat&logo=pandas&logoColor=white) | ![](https://img.shields.io/badge/numpy-%23013243.svg?style=flat&logo=numpy&logoColor=white)

        </div>

        """


@st.cache()
def homePage():
    return (
        """
    This webapp is based on the <a href="https://www.youtube.com/watch?v=8ext9G7xspg" style="text-decoration: none;">**12 Beginner Python Projects - Coding Course**</a> developed by [Kylie Ying](https://www.youtube.com/ycubed) with the aim to help improve Python skills by following along with 12 different Python project tutorials.

    """,
        f"""
    <br><br> {nbsp*15}⭐️ Course Contents ⭐️<br>
    
        1. Madlibs 
        2. Guess the Number (Computer) 
        3. Guess the Number (User)
        4. Rock Paper Scissors
        5. Hangman
        6. Tic-Tac-Toe
        7. Minesweeper 
        8. Sudoku 
        9. Markov Chain Text Composer 

    {nbsp*15}⭐️ Course Contents ⭐️

    """,
        """
    <hr>

    <a href="https://streamlit.io/" style="text-decoration: none;">**StreamLit**</a> is used to create the Web Graphical User Interface (GUI). Streamlit is a cool way to turn data scripts into shareable web apps in minutes, all in Python. You can check out the launch <a href="https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace" style="text-decoration: none;">*blog post*</a> for more information.

    This web app was inspired by the awesome YouTube tutorials created by:
    
    - **Patrick Loeber**: <a href="https://www.youtube.com/watch?v=xl0N7tHiwlw" style="text-decoration: none;">Build A Machine Learning Web App From Scratch</a>
    - **Chanin Nantasenamat**: <a href="https://www.youtube.com/watch?v=JwSS70SZdyM" style="text-decoration: none;">Build 12 Data Science Apps with Python and Streamlit - Full Course</a>

    """,
        """

    Do check out their channels and websites for more informative and exciting Machine Learning & Data Science tutorials.

    <hr>
    """,
    )


@st.cache()
def aboutMadLibs():
    return """ 
    Mad Libs is a phrasal template word game created by Leonard Stern and Roger Price. It consists of one player prompting others for a list of words to substitute for blanks in a story before reading aloud. The game is frequently played as a party game or as a pastime.

    Mad Libs books contain short stories on each page with many key words replaced with blanks. Beneath each blank is specified a category, such as "noun", "verb", "place", "celebrity," "exclamation" or "part of the body". One player asks the other players, in turn, to contribute a word of the specified type for each blank, but without revealing the context for that word. Finally, the completed story is read aloud. The result is usually a sentence which is comical, surreal and/or takes on somewhat of a nonsensical tone.

    <code>_Check the Wikipedia **[page](https://en.wikipedia.org/wiki/Mad_Libs)** for more information._</code>
    """


@st.cache()
def aboutGuessTheNumberComputer():
    return """
    Enter your random number in the number box in the sidebar. Using the slider in the sidebar, you define a range of intergers (`min_number` to `max_number`) for the computer to guess from.  
    
    The computer will keep guessing numbers until it find's your random number using a too high/too low binary search pattern. The aim is to see how many iterations it takes the computer to find your number.
    """


@st.cache()
def aboutGuessTheNumberUser():
    return """
    The computer is going to randomly select an integer within a range: `min_number` to `max_number`. The `min_number` and `max_number` can both be increased or decreased using the slider in the sidebar.
    
    You'll keep guessing numbers until you find the computer's number, and the computer will tell you each time if your guess was too high or too low. 
    """


@st.cache()
def aboutRockPaperScissors():
    return """
    Rock paper scissors (also known by other orderings of the three items, with "rock" sometimes being called "stone", or as Rochambeau, roshambo, or ro-sham-bo) is a hand game usually played between two people, in which each player simultaneously forms one of three shapes with an outstretched hand. These shapes are "rock" (a closed fist), "paper" (a flat hand), and "scissors" (a fist with the index finger and middle finger extended, forming a V). "Scissors" is identical to the two-fingered V sign (also indicating "victory" or "peace") except that it is pointed horizontally instead of being held upright in the air.

    A simultaneous, zero-sum game, it has only two possible outcomes: a draw, or a win for one player and a loss for the other. A player who decides to play rock will beat another player who has chosen scissors ("rock crushes scissors" or sometimes "blunts scissors"), but will lose to one who has played paper ("paper covers rock"); a play of paper will lose to a play of scissors ("scissors cuts paper"). If both players choose the same shape, the game is tied and is usually immediately replayed to break the tie. The type of game originated in China and spread with increased contact with East Asia, while developing different variants in signs over time.

    <code>_Check the Wikipedia **[page](https://en.wikipedia.org/wiki/Rock_paper_scissors)** for more information._</code>
    """


@st.cache()
def aboutHangman():
    return """
    Hangman is a paper and pencil guessing game for two or more players. One player thinks of a word, phrase or sentence and the other(s) tries to guess it by suggesting letters within a certain number of guesses.

    The word to guess is represented by a row of dashes, representing each letter of the word. If the guessing player suggests a letter which occurs in the word, the other player writes it in all its correct positions. If the suggested letter does not occur in the word, the other player draws one element of a hanged man stick figure as a tally mark.

    The player guessing the word may, at any time, attempt to guess the whole word. If the word is correct, the game is over and the guesser wins. Otherwise, the other player may choose to penalize the guesser by adding an element to the diagram. On the other hand, if the other player makes enough incorrect guesses to allow his opponent to complete the diagram, the game is also over, this time with the guesser losing. However, the guesser can also win by guessing all the letters that appear in the word, thereby completing the word, before the diagram is completed.

    <code><i>Check the Wikipedia <a href="https://en.wikipedia.org/wiki/Hangman_(game)"><b>page</b></a> for more information.</i></code>
    """


@st.cache()
def aboutTicTacToe():
    return """
    Tic-tac-toe, noughts and crosses, or Xs and Os is a paper-and-pencil game for two players, X and O, who take turns marking the spaces in a 3×3 grid. The player who succeeds in placing three of their marks in a diagonal, horizontal, or vertical row is the winner. It is a solved game with a forced draw assuming best play from both players.
        
    To win the game, a player must place three of their marks in a horizontal, vertical, or diagonal row. There is no universally-agreed rule as to who plays first, but in this article the convention that X plays first is used. The following example games show wins in the horizontal, vertical and diagonal rows respectively:

    <div style="text-align: center;">

    ![](https://4.bp.blogspot.com/-xL7NMJ03Lwk/XDpTWIy4XUI/AAAAAAAAADU/n-ZE3Gsm0yIjc3E1iCoDZLOh1pXTaoyUwCLcBGAs/s1600/tic-tac-toe-fig-1-576x215.png "Credit: https://funpaperandpencilgames.blogspot.com/2019/02/")

    </div>

    <code>_Check the Wikipedia **[page](https://en.wikipedia.org/wiki/Tic-tac-toe)** for more information._</code>
    """


@st.cache()
def aboutMinesweeper():
    return """
    Minesweeper is a single-player puzzle video game. The objective of the game is to clear a rectangular board containing hidden "mines" or bombs without detonating any of them, with help from clues about the number of neighboring mines in each field.

    In Minesweeper, mines are scattered throughout a board, which is divided into cells. Cells have three states: uncovered, covered and flagged. A covered cell is blank and clickable, while an uncovered cell is exposed. Flagged cells are those marked by the player to indicate a potential mine location.

    A player left-clicks a cell to uncover it. If a player uncovers a mined cell, the game ends, as there is only 1 life per game. Otherwise, the uncovered cells displays either a number, indicating the quantity of mines diagonally and/or adjacent to it, or a blank tile (or "0"), and all adjacent non-mined cells will automatically be uncovered. To win the game, players must uncover all non-mine cells.

    <div style="text-align: center;">

    ![](https://thegeometryteacher.files.wordpress.com/2011/08/mine1.gif "Credit: https://thegeometryteacher.wordpress.com/2011/08/14/good-game-vol-4-minesweeper/")

    </div>

    <code><i>Check the Wikipedia <a href="https://en.wikipedia.org/wiki/Minesweeper_(video_game)"><b>page</b></a> for more information.</i></code>
    """


@st.cache()
def aboutSudoku():
    return """
    Sudoku (originally called Number Place) is a logic-based, combinatorial number-placement puzzle. In classic sudoku, the objective is to fill a 9×9 grid with digits so that each column, each row, and each of the nine 3×3 subgrids that compose the grid (also called "boxes", "blocks", or "regions") contains all of the digits from 1 to 9. The puzzle setter provides a partially completed grid, which for a well-posed puzzle has a single solution.

    The image below show a typical sudoku puzzle and its solution:

    <div style="text-align: center;">

    ![](https://miro.medium.com/max/1838/1*K7nuelC1TIFlwwGMThdBCA.png "Credit: https://medium.com/@littleowllabs/solving-sudoku-with-elixir-d36f40232499")

    </div>

    <code>_Check the Wikipedia **[page](https://en.wikipedia.org/wiki/Sudoku)** for more information._</code>
    """


@st.cache()
def aboutMarkovChainTextComposer():
    return """
    A Markov chain is a stochastic model describing a sequence of possible events in which the probability of each event depends only on the state attained in the previous event. The model requires a finite set of states with fixed conditional probabilities of moving from one state to another.

    A simple Markov chain text composer is implemented to represent relationships between words in a body of text (song lyrics, prose, poetry). The text composer will learn common patterns in word order and then apply these patterns to the input word (a randomly selected word) to get the output word with the highest probability of coming after the input word. 

    <div style="text-align: center;">

    ![](https://i2.wp.com/chalkdustmagazine.com/wp-content/uploads/2020/10/web_cover.png?resize=670%2C300&ssl=1 "Credit: https://chalkdustmagazine.com/features/fun-with-markov-chains/")

    </div>
    
    The output word becomes the new input word and the process is repeated until a specified number of words _"...ahem interpretive poetry..."_ have been composed.

    <code>_Check the Wikipedia **[page](https://en.wikipedia.org/wiki/Markov_chain)** for more information on Markov chains and Ryan Thelin's **[post](https://www.educative.io/blog/deep-learning-text-generation-markov-chains)** for more information on Markov chain text generation._</code>


    """


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
gc.collect()
