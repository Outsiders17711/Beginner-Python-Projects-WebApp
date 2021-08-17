import copy
import dataclasses
import random
import sys
import time
from collections import Counter

import pandas as pd
import streamlit as st

import gc

gc.enable()
sys.setrecursionlimit(3500)


# [start] [Sudoku]____________________________________________________
class Sudoku:
    def __init__(self, sdk, game_commentry):
        self.commentry = game_commentry

        if not sdk.visible_board:
            self.commentry.warning("**Game state reset. New board cooked up!**")
            self.createSudokuBoard(sdk)

    def printBoard(self, sdk, placeholder, actual=False):
        game_board = placeholder.columns([2, 6, 2])

        visible_board = [
            [str(sdk.visible_board[i][j]) for j in range(sdk.size)]
            for i in range(sdk.size)
        ]
        for row in range(sdk.size):
            for col in range(sdk.size):
                if sdk.c_visible_board[row][col] == "*":
                    visible_board[row][col] = (f"[{visible_board[row][col]}]").center(2)
                else:
                    visible_board[row][col] = (f"{visible_board[row][col]}").center(2)

        actual_board = [
            [str(sdk.actual_board[i][j]) for j in range(sdk.size)]
            for i in range(sdk.size)
        ]
        for row in range(sdk.size):
            for col in range(sdk.size):
                if sdk.c_visible_board[row][col] == "*":
                    actual_board[row][col] = (f"[{actual_board[row][col]}]").center(2)
                else:
                    actual_board[row][col] = (f"{actual_board[row][col]}").center(2)

        if actual:
            game_board[1].markdown("**`Solved Puzzle State`**")
            game_board[1].dataframe(pd.DataFrame(actual_board))
        elif not actual:
            game_board[1].markdown("**`Current Puzzle State`**")
            game_board[1].dataframe(pd.DataFrame(visible_board))

    def createSudokuBoard(self, sdk):
        puzzle = [[None for _ in range(1, sdk.size + 1)] for _ in range(1, sdk.size + 1)]
        possible_values = set([i for i in range(1, sdk.size + 1)])
        num_blank_cells = int((sdk.size ** 2) - sdk.percent_filled * (sdk.size ** 2))
        # st.write("num_blank_cells", num_blank_cells)

        try:
            for row in range(sdk.size):
                for col in range(sdk.size):
                    current_row = puzzle[row]
                    current_col = [row[col] for row in puzzle]

                    grid1, grid2 = row // 3, col // 3
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

                    while (
                        Counter(current_row)[puzzle[row][col]] > 1
                        or Counter(current_col)[puzzle[row][col]] > 1
                        or puzzle[row][col] is None
                    ):
                        random_int = random.choice(list(available_values))
                        if (
                            random_int not in current_row
                            and random_int not in current_col
                        ):
                            puzzle[row][col] = random_int

            sdk.actual_board = copy.deepcopy(puzzle)

            for _ in range(num_blank_cells):
                puzzle[random.randint(0, sdk.size - 1)][
                    random.randint(0, sdk.size - 1)
                ] = "*"

            sdk.visible_board = copy.deepcopy(puzzle)
            sdk.c_visible_board = copy.deepcopy(puzzle)
            del puzzle

        except IndexError:
            self.createSudokuBoard(sdk)

    def checkEmptyCells(self, sdk):
        for r in range(9):
            for c in range(9):
                if sdk.visible_board[r][c] == "*":
                    return False

        return True

    def getUserInput(self, sdk, coords, values):
        list_coords = [
            int(coords[j][i]) for j in range(sdk.size) for i in range(sdk.size)
        ]
        if sum(list_coords) == 0:
            self.commentry.error("**Choose a cell location!**")
            time.sleep(1)
            st.experimental_rerun()

        elif sum(list_coords) > 1:
            self.commentry.error("**Invalid cell location! You can only tick one box!**")
            time.sleep(1)
            st.experimental_rerun()

        elif sum(list_coords) == 1:
            square = list_coords.index(1)
            row, col = square // sdk.size, square % sdk.size

            if sdk.c_visible_board[row][col] != "*":
                self.commentry.error("**Invalid cell location! Cell is pre-filled!**")
                time.sleep(1)
                st.experimental_rerun()

            list_values = [int(i) for i in values]
            if sum(list_values) == 0:
                self.commentry.error("**Choose a cell value!**")
                time.sleep(1)
                st.experimental_rerun()

            elif sum(list_values) > 1:
                self.commentry.error("**Invalid cell value! You can only tick one box!**")
                time.sleep(1)
                st.experimental_rerun()

            elif sum(list_values) == 1:
                value = list_values.index(1) + 1
                sdk.visible_board[row][col] = value
                self.commentry.info(
                    f"**Player inputs <<{value}>> @ row-{row} | column-{col}.**"
                )

    def checkWinStatus(self, sdk):
        winStatus = True
        chars = set("[]")

        for row in range(9):
            for col in range(9):
                if isinstance(sdk.visible_board[row][col], str):
                    cellvalue = int(
                        "".join(i for i in sdk.visible_board[row][col] if i not in chars)
                    )

                    row_vals = sdk.visible_board[row]
                    if cellvalue in row_vals:
                        winStatus = False

                    col_vals = [row[col] for row in sdk.visible_board]
                    if cellvalue in col_vals:
                        winStatus = False

                    gridr, gridc = (row // 3) * 3, (col // 3) * 3
                    for r in range(gridr, gridr + 3):
                        for c in range(gridc, gridc + 3):
                            if sdk.visible_board[r][c] == cellvalue:
                                winStatus = False

        return winStatus


def playSudoku(sdk):
    st.markdown("")
    st.sidebar.markdown("")

    options = st.sidebar.columns([1, 20, 1])
    percent = options[1].slider(
        "Choose The Percentage Of Filled Cells [0.5 - 0.9] :",
        min_value=0.5,
        max_value=0.9,
        step=0.1,
        value=sdk.percent_filled,
    )

    if percent != sdk.percent_filled:
        sdk.percent_filled = percent
        sdk.sdk_idx_widgets += 1
        sdk.visible_board = sdk.actual_board = sdk.c_visible_board = []
        sdk.game_over = False
        st.experimental_rerun()

    form = st.sidebar.form(f"form/{sdk.sdk_idx_widgets}", clear_on_submit=True)
    with form:
        form.markdown("**`Choose the cell location :`**")
        tick_boxes = [form.columns(sdk.size + 2)] * sdk.size
        col_labels = [col.write(idx) for idx, col in enumerate(tick_boxes[0][1:-1])]
        tick_boxes[0][0].write("")
        tick_boxes[0][0].write("")
        row_labels = [row[0].write(idx) for idx, row in enumerate(tick_boxes)]

        coords = [
            [
                tick_boxes[i][(j % sdk.size) + 1].checkbox(
                    "", key=f"{i}/{j}/{sdk.sdk_idx_widgets}", value=False
                )
                for j in range(i * sdk.size, (i + 1) * sdk.size)
            ]
            for i in range(sdk.size)
        ]

        form.write("**`Choose the cell value :`**")
        tick_boxes = form.columns(sdk.size + 2)
        col_labels = [col.write(idx + 1) for idx, col in enumerate(tick_boxes[1:-1])]
        values = [
            col.checkbox("", key=f"{idx}/{sdk.sdk_idx_widgets}", value=False)
            for idx, col in enumerate(tick_boxes[1:-1])
        ]

    submit = form.form_submit_button("Play Move")

    game_commentry = st.empty()
    game_commentry.info("**Make a move using the boxes in the sidebar.**")
    ph_board, cheat_board = st.empty(), st.empty()
    game = Sudoku(sdk, game_commentry)
    game.printBoard(sdk, ph_board)
    # game.printBoard(sdk, cheat_board, actual=True)

    resetGame, quitGame = False, False
    reset_quit = st.sidebar.columns([1, 6, 5, 1])
    if reset_quit[1].button("Quit Game"):
        quitGame = True
    if reset_quit[2].button("Reset Game"):
        resetGame = True

    if submit and (not game.checkEmptyCells(sdk)) and (not sdk.game_over):
        game.getUserInput(sdk, coords, values)
        game.printBoard(sdk, ph_board)

    if game.checkEmptyCells(sdk):
        sdk.game_over = True
        game_commentry.info(
            "**All cells have been filled; checking if cell values are correct...**"
        )
        time.sleep(1)

        if sdk.visible_board == sdk.actual_board:
            game_commentry.success("**Congratulations! You won!!**")
            st.balloons()
        else:
            game_commentry.error("**Sorry. You lost.**")

        game.printBoard(sdk, ph_board, actual=True)

    if quitGame:
        sdk.game_over = True
        game_commentry.info("Quitting... Click **Reset Game** to play again.")
        game.printBoard(sdk, ph_board, actual=True)

    if resetGame:
        sdk.percent_filled = 0.8
        sdk.sdk_idx_widgets += 1
        sdk.visible_board = sdk.actual_board = sdk.c_visible_board = []
        sdk.game_over = False
        st.experimental_rerun()

    st.write("___")


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
gc.collect()
