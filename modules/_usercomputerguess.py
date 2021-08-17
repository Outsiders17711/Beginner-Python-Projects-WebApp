import streamlit as st
import random
import time

import gc

gc.enable()

# [start] [userGuess]_________________________________________________
def userGuess(ucg):
    st.sidebar.markdown("""___""")
    cols = st.sidebar.columns([1, 20, 1])
    min_max = cols[1].slider(
        "Choose The Range Of The Computer's Guess:",
        min_value=1,
        max_value=100000,
        value=(ucg.ug_min_val, ucg.ug_max_val),
    )
    if min_max != (ucg.ug_min_val, ucg.ug_max_val):
        ucg.ug_min_val, ucg.ug_max_val = min_max
        ucg.ug_history = {}
        ucg.ug_random_number = random.randint(ucg.ug_min_val, ucg.ug_max_val)
        st.experimental_rerun()
    # st.write(ucg.ug_random_number)

    guess = st.number_input(
        f"Guess A Random Number Between {ucg.ug_min_val} and {ucg.ug_max_val}:",
        value=0,
    )

    output = "Take a guess!"
    if guess != 0:
        if guess < ucg.ug_min_val or guess > ucg.ug_max_val:
            output = "Sorry. Outside bounds. Guess again!"
            st.error(output)
        elif guess < ucg.ug_random_number:
            output = "Sorry. Too low. Guess again!"
            st.info(output)
        elif guess > ucg.ug_random_number:
            output = "Sorry. Too high. Guess again!"
            st.info(output)
        elif guess == ucg.ug_random_number:
            output = f"Yay! You have guessed the number {ucg.ug_random_number} correctly!"
            st.success(output)
            st.balloons()

        ucg.ug_history[len(ucg.ug_history)] = f"{guess}: {output}"
        st.write(ucg.ug_history)

    b_reset = st.sidebar.columns([2, 3, 1])
    if b_reset[1].button("Reset Game"):
        ucg.ug_min_val = 0
        ucg.ug_max_val = 100000
        ucg.ug_history = {}
        ucg.ug_random_number = random.randint(1, 100000)
        st.experimental_rerun()

    st.sidebar.markdown("""___""")
    st.markdown("""___""")


# [start] [computerGuess]_____________________________________________
def computerGuess(ucg):
    st.sidebar.markdown("""___""")
    cols = st.sidebar.columns([1, 20, 1])
    min_max = cols[1].slider(
        "Choose The Range For Your Random Guess:",
        min_value=1,
        max_value=100000,
        value=(ucg.cg_min_val, ucg.cg_max_val),
    )
    user_guess = cols[1].number_input(
        f"Choose Your Random Number [{ucg.cg_min_val} - {ucg.cg_max_val}]:",
        min_value=ucg.cg_min_val,
        max_value=ucg.cg_max_val,
    )
    if min_max != (ucg.cg_min_val, ucg.cg_max_val) or user_guess != ucg.cg_random_number:
        ucg.cg_new_comp_min, ucg.cg_new_comp_max = (
            ucg.cg_min_val,
            ucg.cg_max_val,
        ) = min_max
        ucg.cg_history = {}
        ucg.cg_random_number = int(user_guess)
        st.experimental_rerun()

    cg_options = st.sidebar.columns([1, 5, 4, 1])
    if cg_options[1].button("Start Game"):
        ucg.cg_game_on = True if ucg.cg_game_on is False else False
        st.experimental_rerun()

    if cg_options[2].button("Reset Game"):
        ucg.cg_new_comp_min, ucg.cg_new_comp_max = ucg.cg_min_val, ucg.cg_max_val = (
            0,
            100000,
        )
        ucg.cg_history, ucg.cg_game_on = {}, False
        ucg.cg_random_number = random.randint(1, 100000)
        st.experimental_rerun()

    cg_outputs = st.empty(), st.empty()
    cg_outputs[0].markdown(
        """
        <br>

            Choose your random number and select the range of guesses...
        """,
        unsafe_allow_html=True,
    )

    while ucg.cg_game_on:
        cg_outputs[0].markdown(
            """
            <br>

                Guessing...
            """,
            unsafe_allow_html=True,
        )

        if ucg.cg_new_comp_min != ucg.cg_new_comp_max:
            guess = random.randint(ucg.cg_new_comp_min, ucg.cg_new_comp_max)
        else:
            guess = ucg.cg_new_comp_min

        output = ""
        if guess < ucg.cg_random_number:
            output = "Too low. Guessing again!"
            ucg.cg_new_comp_min = guess + 1
        elif guess > ucg.cg_random_number:
            output = "Too high. Guessing again!"
            ucg.cg_new_comp_max = guess - 1
        elif guess == ucg.cg_random_number:
            break

        ucg.cg_history[len(ucg.cg_history) + 1] = f"{guess}: {output}"
        cg_outputs[1].write(ucg.cg_history)
        time.sleep(1)

    if ucg.cg_game_on:
        cg_outputs[0].success(
            f"**Yay! Number {ucg.cg_random_number} guessed correctly after {len(ucg.cg_history) + 1} iterations!!!**"
        )
        st.balloons()

    st.sidebar.markdown("""___""")
    st.markdown("""___""")


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
gc.collect()
