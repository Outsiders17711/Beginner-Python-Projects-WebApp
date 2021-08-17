import streamlit as st
import random
import string
import time
import dataclasses
import math
import pandas as pd

import gc

gc.enable()

# [start] [TicTacToe]____________________________________________________________
class Player:
    def __init__(self, letter=None):
        self.letter = letter

    def get_move(self, game):
        pass


class NormalComputerPlayer(Player):
    def __init__(self, letter=None):
        super().__init__(letter)

    def get_move(self, ttt, game):
        square = random.choice(game.available_moves(ttt))
        return square

    def get_move_vs_human(self, ttt, game, game_commentry, boxes=None):
        square = random.choice(game.available_moves(ttt))

        ttt.ttt_board_state[square] = ttt.current_letter
        if game.winner(ttt, square, ttt.current_letter):
            ttt.any_winner = True
            game_commentry.success(
                f"**{ttt.current_player} <{ttt.current_letter}> wins!!**"
            )
            st.balloons()
        else:
            game_commentry.info(
                f"**{ttt.current_player} <{ttt.current_letter}> makes a move to square {square}. Player {'XO'.replace(ttt.current_letter, '')}'s turn.**"
            )
            ttt.current_letter = "X" if ttt.current_letter == "O" else "O"


class GeniusComputerPlayer(Player):
    def __init__(self, letter=None):
        super().__init__(letter)

    def get_move(self, ttt, game):
        if len(game.available_moves(ttt)) == 9:
            square = random.choice(game.available_moves(ttt))
        else:
            square = self.minimax(ttt, game, self.letter)["position"]

        return square

    def get_move_vs_human(self, ttt, game, game_commentry, boxes=None):
        if len(game.available_moves(ttt)) == 9:
            square = random.choice(game.available_moves(ttt))
        else:
            square = self.minimax(ttt, game, self.letter)["position"]

        ttt.ttt_board_state[square] = ttt.current_letter
        if game.winner(ttt, square, ttt.current_letter):
            ttt.any_winner = True
            game_commentry.success(
                f"**{ttt.current_player} <{ttt.current_letter}> wins!!**"
            )
            st.balloons()
        else:
            game_commentry.info(
                f"**{ttt.current_player} <{ttt.current_letter}> makes a move to square {square}. Player {'XO'.replace(ttt.current_letter, '')}'s turn.**"
            )
            ttt.current_letter = "X" if ttt.current_letter == "O" else "O"

    def minimax(self, ttt, gameState, player):
        max_player = self.letter  # yourself
        other_player = "O" if player == "X" else "X"

        if gameState.current_winner != None:
            return {
                "position": None,
                "score": 1 * (gameState.num_empty_squares(ttt) + 1)
                if gameState.current_winner == max_player
                else -1 * (gameState.num_empty_squares(ttt) + 1),
            }

        elif not gameState.empty_squares(ttt):
            return {"position": None, "score": 0}

        if player == max_player:
            best = {"position": None, "score": -math.inf}
        else:
            best = {"position": None, "score": math.inf}

        for possible_move in gameState.available_moves(ttt):
            gameState.make_move(ttt, possible_move, player)
            sim_score = self.minimax(ttt, gameState, other_player)
            ttt.ttt_board_state[possible_move] = " "
            gameState.current_winner = None
            sim_score["position"] = possible_move
            if player == max_player:
                if sim_score["score"] > best["score"]:
                    best = sim_score
            else:
                if sim_score["score"] < best["score"]:
                    best = sim_score
        return best


class HumanPlayer(Player):
    def __init__(self, letter=None):
        super().__init__(letter)

    def get_move_vs_human(self, ttt, game, game_commentry, boxes):
        list_boxes = [int(boxes[j][i]) for j in range(3) for i in range(3)]
        if sum(list_boxes) == 0:
            game_commentry.info("**Make a move using the boxes in the sidebar!**")

        elif sum(list_boxes) > 1:
            game_commentry.error("**Invalid move! You can only tick one box!**")

        elif sum(list_boxes) == 1:
            square = list_boxes.index(1)
            if ttt.ttt_board_state[square] != " ":
                game_commentry.error(
                    f"**Invalid square. Try again Player <{ttt.current_letter}>!**"
                )
            else:
                ttt.ttt_board_state[square] = ttt.current_letter
                if game.winner(ttt, square, ttt.current_letter):
                    ttt.any_winner = True
                    game_commentry.success(
                        f"**{ttt.current_player} <{ttt.current_letter}> wins!!**"
                    )
                    st.balloons()
                else:
                    ttt.ttt_commentry = f"**{ttt.current_player} <{ttt.current_letter}> makes a move to square {square}. Player {'XO'.replace(ttt.current_letter, '')}'s turn.**"
                    ttt.current_letter = "X" if ttt.current_letter == "O" else "O"
                    st.experimental_rerun()


class TicTacToe:
    def __init__(self):
        self.current_winner = None

    def print_board_nums(self, col_to_use):
        df_board_nums = pd.DataFrame(
            [[i for i in range(j * 3, (j + 1) * 3)] for j in range(3)],
            columns=["col0", "col1", "col2"],
            index=["row0", "row1", "row2"],
        )

        col_to_use[0].markdown(f"**{'-'*6}< BOARD LAYOUT >{'-'*5}**")
        col_to_use[1].dataframe(df_board_nums)
        col_to_use[2].markdown(f"**{'-'*6}< BOARD LAYOUT >{'-'*5}**")

    def print_board(self, ttt, col_to_use):
        df_board = pd.DataFrame(
            [row for row in [ttt.ttt_board_state[i * 3 : (i + 1) * 3] for i in range(3)]],
            columns=["col0", "col1", "col2"],
            index=["row0", "row1", "row2"],
        )

        col_to_use[0].markdown(f"**{'-'*7}< BOARD STATE >{'-'*7}**")
        col_to_use[1].dataframe(df_board)
        col_to_use[2].markdown(f"**{'-'*7}< BOARD STATE >{'-'*7}**")

    def available_moves(self, ttt):
        return [i for i, spot in enumerate(ttt.ttt_board_state) if spot == " "]

    def empty_squares(self, ttt):
        return " " in ttt.ttt_board_state

    def num_empty_squares(self, ttt):
        return ttt.ttt_board_state.count(" ")

    def make_move(self, ttt, square, letter):
        if ttt.ttt_board_state[square] == " ":
            ttt.ttt_board_state[square] = letter
            if self.winner(ttt, square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, ttt, square, letter):
        # checking rows:
        row_idx = square // 3
        row = ttt.ttt_board_state[row_idx * 3 : (row_idx + 1) * 3]
        if all([spot == letter for spot in row]):
            return True
        # checking columns:
        col_idx = square % 3
        column = [ttt.ttt_board_state[col_idx + (i * 3)] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        # checking disgonals:
        if square % 2 == 0:
            diagonal1 = [ttt.ttt_board_state[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [ttt.ttt_board_state[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
def computerTicTacToe(
    ttt, class_x_player, class_o_player, game, board_printout, game_commentry
):
    st.sidebar.markdown("")
    if st.sidebar.columns([2, 4])[1].button("Start Game"):
        ttt.start_game = True
    cols = st.sidebar.columns([1, 10, 1])
    game_speed = cols[1].slider(
        "Select Game Speed [ 1 (slow) - 5 (fast) ]:",
        min_value=1.0,
        max_value=5.0,
        step=0.5,
        value=3.0,
    )
    game_speed = 1.5 - (game_speed / 4)

    square = None
    while game.empty_squares(ttt) and ttt.start_game:
        if ttt.current_letter == "O":
            ttt.current_player = ttt.o_player
            square = class_o_player.get_move(ttt, game)

        elif ttt.current_letter == "X":
            ttt.current_player = ttt.x_player
            square = class_x_player.get_move(ttt, game)

        if game.make_move(ttt, square, ttt.current_letter):
            game_commentry.info(
                f"**{ttt.current_player} <{ttt.current_letter}> makes a move to square {square}. Player {'XO'.replace(ttt.current_letter, '')}'s turn.**"
            )
            game.print_board(ttt, board_printout)

            if game.current_winner:
                game_commentry.info(
                    f"**{ttt.current_player} <{ttt.current_letter}> wins!!**"
                )
                ttt.any_winner = True
                break

        ttt.current_letter = "O" if ttt.current_letter == "X" else "X"
        time.sleep(game_speed)

    if ttt.start_game and not ttt.any_winner:
        game_commentry.info("**Board filled. It's a tie!!**")
        ttt.any_winner = True

    if ttt.any_winner or not game.empty_squares(ttt):
        time.sleep(2)
        ttt.ttt_board_state = [" " for _ in range(9)]
        ttt.start_game = False
        ttt.current_letter = "X"
        ttt.any_winner = False
        st.experimental_rerun()


# [start]____________________________________________________________
def playTicTacToe(ttt):
    str_players = ["Human", "Genius Computer", "Normal Computer"]
    class_players_x = [
        HumanPlayer("X"),
        GeniusComputerPlayer("X"),
        NormalComputerPlayer("X"),
    ]
    class_players_o = [
        HumanPlayer("O"),
        GeniusComputerPlayer("O"),
        NormalComputerPlayer("O"),
    ]

    st.markdown("")
    st.sidebar.markdown("___")
    players = st.sidebar.columns([1, 1])
    x_player = players[0].radio(
        label="Choose the X Player",
        options=str_players,
        index=str_players.index(ttt.x_player),
    )
    o_player = players[1].radio(
        label="Choose the O Player",
        options=str_players,
        index=str_players.index(ttt.o_player),
    )

    if x_player != ttt.x_player or o_player != ttt.o_player:
        ttt.x_player = ttt.current_player = x_player
        ttt.o_player = o_player
        ttt.current_letter = "X"
        ttt.ttt_board_state = [" " for _ in range(9)]
        ttt.start_game = ttt.any_winner = False
        ttt.ttt_idx_widgets += 1
        ttt.ttt_commentry = ""
        st.experimental_rerun()

    class_x_player = class_players_x[str_players.index(ttt.x_player)]
    class_o_player = class_players_o[str_players.index(ttt.o_player)]

    game = TicTacToe()
    game_commentry = st.empty()
    if not ttt.ttt_commentry:
        ttt.ttt_commentry = (
            f"**{x_player} <X> | VS | {o_player} <O>. Player <X> starts.**"
        )
    game_commentry.info(ttt.ttt_commentry)

    game_board_cols = st.columns([3, 5, 1])
    with game_board_cols[1]:
        # board_layout = st.empty(), st.empty(), st.empty()
        # game.print_board_nums(board_layout)
        board_printout = st.empty(), st.empty(), st.empty()
        game.print_board(ttt, board_printout)

    # [start]____________________________________________________________
    if "Human" not in [x_player, o_player]:
        computerTicTacToe(
            ttt, class_x_player, class_o_player, game, board_printout, game_commentry
        )

    elif "Human" in [x_player, o_player]:
        st.sidebar.markdown("")
        start_reset = st.sidebar.columns([5, 4])
        if start_reset[0].button("Start Game") and not ttt.start_game:
            ttt.start_game = True
            st.experimental_rerun()
        quit_game = start_reset[1].button("Quit/Reset Game")
        form = st.sidebar.form(f"checkboxes/{ttt.ttt_idx_widgets}", clear_on_submit=True)

        with form:
            form.markdown("Click **Start Game** once to begin...")
            sizes = [2, 1, 1, 1, 1]
            cols_boxes = form.columns(sizes), form.columns(sizes), form.columns(sizes)
            col_labels = [col.write(idx) for idx, col in enumerate(cols_boxes[0][1:-1])]
            cols_boxes[0][0].write("🆔")
            row_labels = [row[0].write(idx) for idx, row in enumerate(cols_boxes)]

            boxes = [
                [
                    cols_boxes[i][(j % 3) + 1].checkbox(
                        f"", key=f"{i}/{j}/{ttt.ttt_idx_widgets}", value=False
                    )
                    for j in range(i * 3, (i + 1) * 3)
                ]
                for i in range(3)
            ]

        human_submit = form.form_submit_button("Play Move")

        if ttt.start_game:
            if ttt.current_letter == "O" and game.empty_squares(ttt):
                ttt.current_player = ttt.o_player
                if isinstance(class_o_player, HumanPlayer):
                    if human_submit and game.empty_squares(ttt):
                        class_o_player.get_move_vs_human(ttt, game, game_commentry, boxes)
                else:
                    time.sleep(1.5)
                    class_o_player.get_move_vs_human(ttt, game, game_commentry, boxes)

            elif ttt.current_letter == "X" and game.empty_squares(ttt):
                ttt.current_player = ttt.x_player
                if isinstance(class_x_player, HumanPlayer):
                    if human_submit and game.empty_squares(ttt):
                        class_x_player.get_move_vs_human(ttt, game, game_commentry, boxes)
                else:
                    time.sleep(1.5)
                    class_x_player.get_move_vs_human(ttt, game, game_commentry, boxes)

            game.print_board(ttt, board_printout)

            if (not game.empty_squares(ttt)) and (not ttt.any_winner):
                game_commentry.info("**Board filled. It's a tie!!**")
                ttt.any_winner = True

            if quit_game:
                game_commentry.error(
                    f"**{ttt.current_player} <{ttt.current_letter}> quits!**"
                )

            if ttt.any_winner or quit_game:
                time.sleep(2)
                ttt.current_letter = "X"
                ttt.ttt_board_state = [" " for _ in range(9)]
                ttt.start_game = ttt.any_winner = False
                ttt.ttt_idx_widgets += 1
                ttt.ttt_commentry = ""
                st.experimental_rerun()
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]

    st.markdown("___")


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
gc.collect()
