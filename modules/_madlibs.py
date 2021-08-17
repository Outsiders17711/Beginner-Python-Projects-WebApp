import streamlit as st
import time
import gc

gc.enable()


# [start] [madlibs]___________________________________________________
def madlibs(ml):
    st.markdown(
        """
        <br>

            Fill in all cells.
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3, col4 = st.columns(4)

    adj = (col1.text_input("Adjective:", key=f"adj{ml.ml_key}")).lower()
    verb1 = (col2.text_input("Verb:", key=f"verb1{ml.ml_key}")).lower()
    verb2 = (col3.text_input("Verb:", key=f"verb2{ml.ml_key}")).lower()
    celeb = (col4.text_input("Famous Person:", key=f"celeb{ml.ml_key}")).lower()

    madlib = f"Computer programming is so {adj.strip()}! It makes me so excited all the time because I love to {verb1.strip()}. Stay hydrated and {verb2.strip()} like you are {celeb.strip()}!"

    if "" not in [adj, verb1, verb2, celeb]:
        st.success(f"""**{madlib}**""")
        ml.ml_key += 1
        time.sleep(3)
        st.experimental_rerun()

    st.markdown("""___""")


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
gc.collect()
