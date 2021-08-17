import streamlit as st
import random
import time
import gc

gc.enable()


# [start] [HangMan]____________________________________________________
@st.cache
def loadWords():
    with open(f"data/englishWords.alpha.txt") as f:
        englishWords = sorted(set(f.read().split()))

    return englishWords


englishWords = loadWords()


def getWord():
    word = random.choice(englishWords)
    while "-" in word or " " in word:
        word = random.choice(englishWords)

    return word.upper()


def HangMan(hm):
    if not hm.hm_word:
        hm.hm_word = getWord()
    word_list = [letter if letter in hm.hm_used_letters else "-" for letter in hm.hm_word]

    st.sidebar.markdown("___")
    b_reset, b_show_answer = st.sidebar.columns([3, 2]), st.sidebar.columns([1, 1])
    show_answer = b_show_answer[0].button("🔍 Show Answer 🔭")

    st.markdown(
        f"""
        <br>

            You have used these letters: {" ".join(hm.hm_used_letters)}
            You have {hm.hm_n_lifes} lives left
            Current word: {"".join(word_list)}
        <br>
        """,
        unsafe_allow_html=True,
    )
    holder1, holder2, holder3 = st.empty(), st.empty(), st.empty()
    user_letter = holder1.text_input(
        "Guess a letter:", max_chars=1, key=str(hm.hm_idxml_key)
    ).upper()

    if len(set(hm.hm_word)) > 0 and hm.hm_n_lifes > 0 and user_letter != "":
        if user_letter in hm.hm_alphabet - hm.hm_used_letters:
            hm.hm_used_letters.add(user_letter)
            if user_letter in set(hm.hm_word):
                set(hm.hm_word).remove(user_letter)
                holder2.success("**Good guess. Keep going!**")
            else:
                holder2.error("**Character is not in word. Try again!**")
                hm.hm_n_lifes -= 1

        elif user_letter in hm.hm_used_letters:
            holder2.error("**You have already used that character. Try again!**")

        elif user_letter not in hm.hm_alphabet and user_letter != "":
            holder2.error("**Invalid character. Try again!**")

    elif len(set(hm.hm_word)) == 0 or hm.hm_n_lifes == 0 or show_answer:
        holder1.empty()

        if "".join(word_list) == hm.hm_word:
            holder1.success(
                f"*Congratulations! You guessed the word __{hm.hm_word}__ correctly!!*"
            )
            st.balloons()
        else:
            holder2.info(f"_The word is_ **{hm.hm_word}**")
            holder3.error("**Game over! Try again!**")
            time.sleep(1)

    time.sleep(1)

    if user_letter != "":
        hm.hm_idxml_key += 1
        st.experimental_rerun()

    if b_reset[1].button("🛑 Reset Game ⚙") or show_answer:
        hm.hm_word = ""
        hm.hm_used_letters = set()
        hm.hm_word_list = []
        hm.hm_n_lifes = 6
        hm.hm_idxml_key += 1
        st.experimental_rerun()

    st.sidebar.markdown("""___""")
    st.markdown("""___""")


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
gc.collect()
