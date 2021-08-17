import dataclasses
import gc

import streamlit as st
from streamlit import caching
import streamlit.report_thread as ReportThread

st.set_page_config(page_title="Beginner Python Projects", layout="wide")
gc.enable()

from modules._strings import *
from modules._hangman import *
from modules._madlibs import *
from modules._rockpaperscissors import *
from modules._ticktacktoe import *
from modules._usercomputerguess import *
from modules._minesweeper import *
from modules._sudoku import *
from modules._markovchain import *
from modules._appSessionState import getSessionState


# [start] [page setup]__________________________________________________
appPages = ["Home Page", "Python Projects", "About Me"]

appProjects = [
    "Sudoku",
    "Markov Chain Text Composer",
    "Minesweeper",
    "Tic-Tac-Toe",
    "Hangman",
    "Rock Paper Scissors",
    "Guess The Number (Computer)",
    "Guess The Number (User)",
    "MadLibs",
]

aboutProjects = [
    aboutMadLibs(),
    aboutGuessTheNumberComputer(),
    aboutGuessTheNumberUser(),
    aboutRockPaperScissors(),
    aboutHangman(),
    aboutTicTacToe(),
    aboutMinesweeper(),
    aboutSudoku(),
    aboutMarkovChainTextComposer(),
]
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]

# [start] [persistent states]__________________________________________
webapp = getSessionState(
    # WebApp
    app_key=0,
    idx_current_page=0,
    page_selector_key=0,
    idx_current_project=0,
    project_selector_key=0,
    # HangMan,
    hm_word="",
    # hm_word_letters = set(hm_word),
    hm_alphabet=set(string.ascii_uppercase),
    hm_used_letters=set(),
    hm_word_list=[],
    hm_n_lifes=6,
    hm_idxml_key=0,
    # madlibs,
    ml_key=0,
    # MarkovChain,
    len_string=150,
    idx_source=0,
    idx_artist=0,
    idx_novel=0,
    mc_idx_widgets=0,
    pasted_text="",
    composition="",
    uploads=None,
    compose_again=False,
    # MineSweeper,
    dim_size=8,
    percent_bombs=0.25,
    ms_idx_widgets=0,
    ms_board_state=[],
    dug_cells=set(),
    current_cell=(None, None),
    safeDigging=True,
    # playRockPaperScissors,
    rps_wins=0,
    rps_losses=0,
    rps_ties=0,
    # Sudoku,
    size=9,
    percent_filled=0.8,
    sdk_idx_widgets=0,
    visible_board=[],
    c_visible_board=[],
    actual_board=[],
    game_over=False,
    # TicTacToe,
    x_player="Random Computer",
    o_player="Genius Computer",
    current_player="Random Computer",
    current_letter="X",
    ttt_board_state=[" " for _ in range(9)],
    start_game=False,
    any_winner=False,
    ttt_commentry="",
    ttt_idx_widgets=0,
    # userGuess,
    ug_min_val=0,
    ug_max_val=100000,
    ug_history={},
    ug_random_number=random.randint(1, 100000),
    # computerGuess,
    cg_min_val=0,
    cg_max_val=100000,
    cg_random_number=11111,
    cg_new_comp_min=0,
    cg_new_comp_max=100000,
    cg_history={},
    cg_game_on=False,
)


def reload():
    caching.clear_cache()
    gc.collect()
    # WebApp
    webapp.app_key = 0
    # webapp.idx_current_page = 0
    webapp.page_selector_key = 0
    # webapp.idx_current_project = 0
    webapp.project_selector_key = 0
    # HangMan
    webapp.hm_word = ""
    # webapp.hm_word_letters = set(hm_word)
    webapp.hm_alphabet = set(string.ascii_uppercase)
    webapp.hm_used_letters = set()
    webapp.hm_word_list = []
    webapp.hm_n_lifes = 6
    webapp.hm_idxml_key = 0
    # madlibs
    webapp.ml_key = 0
    # MarkovChain
    webapp.len_string = 150
    webapp.idx_source = 0
    webapp.idx_artist = 0
    webapp.idx_novel = 0
    webapp.mc_idx_widgets = 0
    webapp.pasted_text = ""
    webapp.composition = ""
    webapp.uploads = None
    webapp.compose_again = False
    # MineSweeper
    webapp.dim_size = 8
    webapp.percent_bombs = 0.25
    webapp.ms_idx_widgets = 0
    webapp.ms_board_state = []
    webapp.dug_cells = set()
    webapp.current_cell = (None, None)
    webapp.safeDigging = True
    # playRockPaperScissors
    webapp.rps_wins = 0
    webapp.rps_losses = 0
    webapp.rps_ties = 0
    # Sudoku
    webapp.size = 9
    webapp.percent_filled = 0.8
    webapp.sdk_idx_widgets = 0
    webapp.visible_board = []
    webapp.c_visible_board = []
    webapp.actual_board = []
    webapp.game_over = False
    # TicTacToe
    webapp.x_player = "Random Computer"
    webapp.o_player = "Genius Computer"
    webapp.current_player = "Random Computer"
    webapp.current_letter = "X"
    webapp.ttt_board_state = [" " for _ in range(9)]
    webapp.start_game = False
    webapp.any_winner = False
    webapp.ttt_idx_widgets = 0
    webapp.ttt_commentry = ""
    # userGuess
    webapp.ug_min_val = 0
    webapp.ug_max_val = 100000
    webapp.ug_history = {}
    webapp.ug_random_number = random.randint(1, 100000)
    # computerGuess
    webapp.cg_min_val = 0
    webapp.cg_max_val = 100000
    webapp.cg_random_number = 11111
    webapp.cg_new_comp_min = 0
    webapp.cg_new_comp_max = 100000
    webapp.cg_history = {}
    webapp.cg_game_on = False
    #
    st.experimental_rerun()


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]

# [start] [setup home page and side bar] ____________________________
st.markdown(
    f"""
    {pageConfig}
    <div style="text-align:center; margin-top:-75px; ">
    <h1 style="font-variant: small-caps; font-size: xx-large; margin-bottom:-45px;" >
    <font color=#008af3>w e b {nbsp*2} a p p</font>
    </h1>
    <h1> Beginner Python Projects </h1>
    <hr>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    f"""
    <div style="text-align:center; margin-top:-75px; margin-bottom:20px; ">
    <h3 style="font-variant: small-caps; font-size: xx-large; ">
    <font color=#008af3>s i d e {nbsp} b a r</font>
    </h3>
    <code style="font-size:smaller; ">{ReportThread.get_report_ctx().session_id}</code>
    </div>
    """,
    unsafe_allow_html=True,
)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]

# [start] [pages and projects]_______________________________________
redirects = st.sidebar.columns([1, 1, 1])
if redirects[1].button("About Me"):
    webapp.idx_current_page = appPages.index("About Me")
    st.experimental_rerun()
if redirects[2].button("Reload App"):
    reload()

if webapp.idx_current_page == appPages.index("About Me"):
    if redirects[0].button("Home Page"):
        webapp.idx_current_page = appPages.index("Home Page")
        st.experimental_rerun()

    st.markdown(aboutMe(), unsafe_allow_html=True)
    st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
    st.sidebar.image("data/images/highlord.jpg", use_column_width="auto")

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
elif webapp.idx_current_page == appPages.index("Home Page"):
    if redirects[0].button("📌 Projects"):
        webapp.idx_current_page = appPages.index("Python Projects")
        st.experimental_rerun()

    st.markdown(homePage()[0], unsafe_allow_html=True)
    kylie = st.columns([2, 1])
    kylie[0].video("https://www.youtube.com/watch?v=8ext9G7xspg")
    kylie[1].markdown(homePage()[1], unsafe_allow_html=True)

    st.markdown(homePage()[2], unsafe_allow_html=True)
    vid1, vid2 = st.columns([1, 1])
    vid1.video("https://www.youtube.com/watch?v=xl0N7tHiwlw")
    vid1.caption("Build A Machine Learning Web App From Scratch")
    vid2.video("https://www.youtube.com/watch?v=JwSS70SZdyM")
    vid2.caption("Build 12 Data Science Apps with Python and Streamlit - Full Course")

    st.markdown(homePage()[3], unsafe_allow_html=True)

    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    st.sidebar.image(
        "https://fiverr-res.cloudinary.com/images/q_auto,f_auto/gigs/129902646/original/9a48402b282b80e4c980f049f4c9572b7501cf90/python-project-and-assignment.jpg",
        caption="Source: https://www.fiverr.com/ajaydhangar/python-project-and-assignment",
    )

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
elif webapp.idx_current_page == appPages.index("Python Projects"):
    if redirects[0].button("Home Page"):
        webapp.idx_current_page = appPages.index("Home Page")
        st.experimental_rerun()

    ph_py_proj = st.sidebar.columns([4, 1, 3])

    # [start]____________________________________________________________

    project_selection = st.sidebar.selectbox(
        "Select Game:",
        appProjects,
        index=webapp.idx_current_project,
    )
    if project_selection != appProjects[webapp.idx_current_project]:
        webapp.idx_current_project = appProjects.index(project_selection)
        st.experimental_rerun()

    st.markdown(f"## Now Playing: {appProjects[webapp.idx_current_project]}")
    with st.expander(f"About {appProjects[webapp.idx_current_project]}..."):
        st.markdown(aboutProjects[webapp.idx_current_project], unsafe_allow_html=True)

    if webapp.idx_current_project == appProjects.index("MadLibs"):
        madlibs(webapp)
    elif webapp.idx_current_project == appProjects.index("Guess The Number (Computer)"):
        computerGuess(webapp)
    elif webapp.idx_current_project == appProjects.index("Guess The Number (User)"):
        userGuess(webapp)
    elif webapp.idx_current_project == appProjects.index("Rock Paper Scissors"):
        playRockPaperScissors(webapp)
    elif webapp.idx_current_project == appProjects.index("Hangman"):
        HangMan(webapp)
    elif webapp.idx_current_project == appProjects.index("Tic-Tac-Toe"):
        playTicTacToe(webapp)
    elif webapp.idx_current_project == appProjects.index("Minesweeper"):
        playMineSweeper(webapp)
    elif webapp.idx_current_project == appProjects.index("Sudoku"):
        playSudoku(webapp)
    elif webapp.idx_current_project == appProjects.index("Markov Chain Text Composer"):
        runMarkovChain(webapp)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
gc.collect()
