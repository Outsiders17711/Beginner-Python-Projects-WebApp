import random
import time

import pandas as pd
import streamlit as st

import gc

gc.enable()


# [start] [MineSweeper]______________________________________________
class MineSweeper:
    def __init__(self, ms, game_commentry):
        self.num_bombs = int(ms.percent_bombs * (ms.dim_size ** 2))
        self.commentry = game_commentry

        if not ms.ms_board_state:
            self.commentry.warning("**Game state reset. New board cooked up!**")
            ms.ms_board_state = [
                [" " for _ in range(ms.dim_size)] for _ in range(ms.dim_size)
            ]
            self.make_new_board(ms)
            self.assign_values_to_board(ms)

    def make_new_board(self, ms):
        bombs_planted = 0

        while bombs_planted < self.num_bombs:
            loc = random.randint(0, ms.dim_size ** 2 - 1)
            row = loc // ms.dim_size
            col = loc % ms.dim_size

            if ms.ms_board_state[row][col] == "*":
                continue

            ms.ms_board_state[row][col] = "*"
            bombs_planted += 1

    def assign_values_to_board(self, ms):
        for r in range(ms.dim_size):
            for c in range(ms.dim_size):
                if ms.ms_board_state[r][c] == "*":
                    continue

                ms.ms_board_state[r][c] = self.get_num_neighbouring_bombs(ms, r, c)

    def get_num_neighbouring_bombs(self, ms, row, col):
        num_neighbouring_bombs = 0

        for r in range(max(0, row - 1), min(ms.dim_size - 1, (row + 1)) + 1):
            for c in range(max(0, col - 1), min(ms.dim_size - 1, (col + 1)) + 1):
                if r == row and c == col:
                    continue

                if ms.ms_board_state[r][c] == "*":
                    num_neighbouring_bombs += 1

        return num_neighbouring_bombs

    def dig(self, ms, current_cell):
        row, col = current_cell
        ms.dug_cells.add((row, col))

        # scenerios:
        if ms.ms_board_state[row][col] == "*":
            return False

        elif ms.ms_board_state[row][col] > 0:
            return True

        elif ms.ms_board_state[row][col] == 0:
            for r in range(max(0, row - 1), min(ms.dim_size - 1, (row + 1)) + 1):
                for c in range(max(0, col - 1), min(ms.dim_size - 1, (col + 1)) + 1):
                    if (r, c) in ms.dug_cells:
                        continue

                    self.dig(ms, (r, c))

        return True

    def print_board_nums(self, ms):
        game_board = st.columns([1, 10, 1])

        df_board_nums = pd.DataFrame(
            [[f"{i}:{j}" for j in range(ms.dim_size)] for i in range(ms.dim_size)]
        )

        game_board[1].dataframe(df_board_nums)

    def print_board(self, ms, placeholder, actual=False):
        game_board = st.empty()
        if ms.dim_size == 10:
            game_board = placeholder.columns([2, 5, 2])  # 10
        elif ms.dim_size in [9, 8]:
            game_board = placeholder.columns([3, 6, 1])  # 9 & 8
        elif ms.dim_size in [7, 6]:
            game_board = placeholder.columns([4, 6, 2])  # 7 & 6

        visible_board = [[" " for i in range(ms.dim_size)] for j in range(ms.dim_size)]
        for row in range(ms.dim_size):
            for col in range(ms.dim_size):
                if (row, col) in ms.dug_cells:
                    visible_board[row][col] = str(ms.ms_board_state[row][col])
                else:
                    visible_board[row][col] = " "

        actual_board = [
            [str(ms.ms_board_state[i][j]) for j in range(ms.dim_size)]
            for i in range(ms.dim_size)
        ]

        count_bombs = sum(
            [
                actual_board[i][j] == "*"
                for j in range(ms.dim_size)
                for i in range(ms.dim_size)
            ]
        )

        if actual:
            game_board[1].dataframe(pd.DataFrame(actual_board))
        elif not actual:
            game_board[1].dataframe(pd.DataFrame(visible_board))

        # st.dataframe(pd.DataFrame(actual_board))

    def make_move(self, ms, boxes):
        list_boxes = [
            int(boxes[j][i]) for j in range(ms.dim_size) for i in range(ms.dim_size)
        ]

        if sum(list_boxes) == 0:
            self.commentry.error("**Make a move using the boxes in the sidebar!**")
            time.sleep(1)
            st.experimental_rerun()

        elif sum(list_boxes) > 1:
            self.commentry.error("**Invalid move! You can only tick one box!**")
            time.sleep(1)
            st.experimental_rerun()

        elif sum(list_boxes) == 1:
            square = list_boxes.index(1)
            row = square // ms.dim_size
            col = square % ms.dim_size
            ms.current_cell = (row, col)
            self.commentry.info(f"**Player makes a move to row {row} | column {col}.**")


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
# [start]____________________________________________________________
def playMineSweeper(ms):
    st.markdown("")
    st.sidebar.markdown("")

    options1, options2 = st.sidebar.columns([3, 2]), st.sidebar.columns([1, 7])
    size = options1[0].number_input(
        "Choose The Board Size [6-10]:",
        min_value=6,
        max_value=10,
        value=ms.dim_size,
    )
    percent = options2[1].slider(
        "Choose The Percentage Of Cells As Bombs [0.2-0.6]:",
        min_value=0.2,
        max_value=0.6,
        step=0.1,
        value=ms.percent_bombs,
    )

    if size != ms.dim_size or percent != ms.percent_bombs:
        ms.dim_size = size
        ms.percent_bombs = percent
        ms.ms_idx_widgets += 1
        ms.ms_board_state = []
        ms.dug_cells = set()
        ms.current_cell = (None, None)
        ms.safeDigging = True
        st.experimental_rerun()

    form = st.sidebar.form(f"form/{ms.ms_idx_widgets}", clear_on_submit=True)
    with form:
        form.write("Choose the next cell to uncover...")
        tick_boxes = [form.columns(ms.dim_size + 2)] * ms.dim_size
        col_labels = [col.write(idx) for idx, col in enumerate(tick_boxes[0][1:-1])]
        tick_boxes[0][0].write("")
        tick_boxes[0][0].write("")
        row_labels = [row[0].write(idx) for idx, row in enumerate(tick_boxes)]

        boxes = [
            [
                tick_boxes[i][(j % ms.dim_size) + 1].checkbox(
                    "", key=f"{i}/{j}/{ms.ms_idx_widgets}", value=False
                )
                for j in range(i * ms.dim_size, (i + 1) * ms.dim_size)
            ]
            for i in range(ms.dim_size)
        ]

    submit = form.form_submit_button("Play Move")

    game_commentry = st.empty()
    game_commentry.info("**Make a move using the boxes in the sidebar.**")
    ph_board, cheat_board = st.empty(), st.empty()
    board = MineSweeper(ms, game_commentry)
    board.print_board(ms, ph_board)
    # board.print_board(ms, cheat_board, actual=True)

    quitGame = False
    undug_cells = ms.dim_size ** 2 - board.num_bombs

    options1[1].write("")
    if options1[1].button("Quit Game Reset Game"):
        quitGame = True
        ms.safeDigging = False

    if submit and (len(ms.dug_cells) < undug_cells) and ms.safeDigging:
        board.make_move(ms, boxes)
        ms.safeDigging = board.dig(ms, ms.current_cell)
        board.print_board(ms, ph_board)

    if ms.safeDigging and (len(ms.dug_cells) == undug_cells):
        game_commentry.success("**Congratulations! You are victorious!!**")
        st.balloons()

        board.print_board(ms, ph_board, actual=True)
        time.sleep(3.5)

        ms.ms_idx_widgets += 1
        ms.ms_board_state = []
        ms.dug_cells = set()
        ms.current_cell = (None, None)
        ms.safeDigging = True
        st.experimental_rerun()

    elif not ms.safeDigging:
        if quitGame:
            game_commentry.info("**resetting...**")
        else:
            game_commentry.error("**You hit a bomb! Game over!!**")

        board.print_board(ms, ph_board, actual=True)
        time.sleep(3.5)

        ms.ms_idx_widgets += 1
        ms.ms_board_state = []
        ms.dug_cells = set()
        ms.current_cell = (None, None)
        ms.safeDigging = True
        st.experimental_rerun()

    st.markdown("___")


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
gc.collect()
