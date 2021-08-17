import streamlit as st
import random
import time

import gc

gc.enable()


# [start] [playRockPaperScissors]_____________________________________
def playRockPaperScissors(rps):
    st.sidebar.markdown("""___""")
    titles = st.sidebar.columns([2, 11, 1])
    titles[1].markdown(f"**> WINS <{'&nbsp'*5}> TIES <{'&nbsp'*5}> LOSSES <**")
    scores = st.sidebar.columns([4, 14, 1])
    scores[1].markdown(
        f"**`{rps.rps_wins}` {'&nbsp'*16} `{rps.rps_ties}` {'&nbsp'*17} `{rps.rps_losses}`**"
    )

    filled = st.columns([3, 10, 3])
    filled[1].markdown(
        f"""
        <br>

            {(">> CHOOSE <<").center(70)}
            {("[Rock]   ||   [Paper]   || [Scissors]").center(70)}
        <br>
        """,
        unsafe_allow_html=True,
    )

    _, col1, col2, col3, _ = st.columns([2, 2, 2, 2, 1])
    _r, _p, _s = (
        col1.button(("Rock").ljust(10)),
        col2.button(("Paper").center(10)),
        col3.button(("Scissors").rjust(10)),
    )

    user = ""
    if _r:
        user = "Rock"
    elif _p:
        user = "Paper"
    elif _s:
        user = "Scissors"
    computer = random.choice(["Rock", "Paper", "Scissors"])

    filled = st.columns([3, 10, 3])

    if _r or _s or _p:
        if user == computer:
            result = "It's a tie. ➰"
            filled[1].info(f"Computer chose `{computer}` ! {'&nbsp'*60} **{result}**")
            rps.rps_ties += 1
        else:
            if pRPS_isWin(user, computer):
                result = "You won! 💯"
                filled[1].success(
                    f"Computer chose `{computer}` ! {'&nbsp'*60} **{result}**"
                )
                st.balloons()
                rps.rps_wins += 1
            else:
                result = "You lost! 💔"
                filled[1].error(
                    f"Computer chose `{computer}` ! {'&nbsp'*60} **{result}**"
                )
                rps.rps_losses += 1

        time.sleep(1.5)
        st.experimental_rerun()

    b_reset = st.sidebar.columns([2, 3, 1])
    if b_reset[1].button("Reset Game"):
        rps.rps_wins, rps.rps_ties, rps.rps_losses = 0, 0, 0
        st.experimental_rerun()

    st.sidebar.markdown("""___""")
    st.markdown("""___""")


def pRPS_isWin(player, opponent):
    # r > s; s > p, p > r
    if (
        (player == "Rock" and opponent == "Scissors")
        or (player == "Scissors" and opponent == "Paper")
        or (player == "Paper" and opponent == "Rock")
    ):
        return True
    else:
        return False


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
gc.collect()
