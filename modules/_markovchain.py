import dataclasses
import os
import random
import re
import string

import streamlit as st

import gc

gc.enable()

# [start] [defaults]__________________________________________
input_sources = [
    "Sample Music Lyrics",
    "Sample Literary Works",
    "Upload Text File(s)",
    "Paste Text Into Webapp",
]
input_artists = [
    "Alan Walker",
    "Armin Van Buuren",
    "Avicii",
    "Billie Eilish",
    "Celine Dion",
    "Drake",
    "Green Day",
    "Halsey",
    "Lady Gaga",
    "Linkin Park",
    "Queen",
    "Taylor Swift",
    "The Chainsmokers",
]
input_novels = [
    "10 Charles Dickens Works",
    "Harry Potter - Sorcerer's Stone",
    "Wuthering Heights",
    "Pride and Prejudice",
    "Alice’s Adventures in Wonderland",
    "The Adventures of Sherlock Holmes",
    "Moby-Dick or The Whale",
    "Dracula",
    "The Iliad",
    "A Tale of Two Cities",
]
error_text = """
                **Input text length is too short!**

                **Add more text or reduce the output composition length.**
                """
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]

# [start] [MarkovChain]______________________________________________
class Vertex(object):
    def __init__(self, value):
        self.value = value
        self.adjacent = {}
        self.neighbors = []
        self.neighbors_weights = []

    def __str__(self):
        return self.value + " ".join([node.value for node in self.adjacent.keys()])

    def add_edge_to(self, vertex, weight=0):
        self.adjacent[vertex] = weight

    def increment_edge(self, vertex):
        self.adjacent[vertex] = self.adjacent.get(vertex, 0) + 1

    def get_adjacent_nodes(self):
        return self.adjacent.keys()

    def get_probability_map(self):
        for (vertex, weight) in self.adjacent.items():
            self.neighbors.append(vertex)
            self.neighbors_weights.append(weight)

    def next_word(self):
        return random.choices(self.neighbors, weights=self.neighbors_weights)[0]


class Graph(object):
    def __init__(self):
        self.vertices = {}

    def get_vertex_values(self):
        return set(self.vertices.keys())

    def add_vertex(self, value):
        self.vertices[value] = Vertex(value)

    def get_vertex(self, value):
        if value not in self.vertices:
            self.add_vertex(value)
        return self.vertices[value]

    def get_next_word(self, current_vertex):
        return self.vertices[current_vertex.value].next_word()

    def generate_probability_mappings(self):
        for vertex in self.vertices.values():
            vertex.get_probability_map()


class MarkovChain:
    def __init__(self):
        self.punctuation = string.punctuation + "\u201c\u201d\u2018\u2019"
        self.words = []
        self.composition = ""

    def get_words_from_text(self, list_text_paths):
        for path in list_text_paths:
            with open(path, "r", encoding="utf-8") as file:
                text = file.read()
                text = re.sub(r"\[(.+)\]", " ", text)
                text = " ".join(text.split())
                text = text.lower()
                text = text.translate(str.maketrans("", "", self.punctuation))

            self.words.extend(text.split())

    def get_words_from_uploader(self, uploaded_files):
        for file in uploaded_files:
            text = file.read().decode("utf-8")
            text = re.sub(r"\[(.+)\]", " ", text)
            text = " ".join(text.split())
            text = text.lower()
            text = text.translate(str.maketrans("", "", self.punctuation))

            self.words.extend(text.split())

    def get_words_from_paste(self, mc):
        text = re.sub(r"\[(.+)\]", " ", mc.pasted_text)
        text = " ".join(text.split())
        text = text.lower()
        text = text.translate(str.maketrans("", "", self.punctuation))

        self.words.extend(text.split())

    def make_graph(self):
        self.graph = Graph()
        prev_word = None

        for word in self.words:
            word_vertex = self.graph.get_vertex(word)
            if prev_word:
                prev_word.increment_edge(word_vertex)

            prev_word = word_vertex

        self.graph.generate_probability_mappings()

    def compose_text(self, mc):
        composition = []
        word = self.graph.get_vertex(random.choice(self.words))

        for _ in range(mc.len_string):
            composition.append(word.value)
            word = self.graph.get_next_word(word)

        self.composition = " ".join(composition)


def runMarkovChain(mc):
    composer = MarkovChain()

    main_cols = st.columns([3, 7])
    main_cols[0].info("**Input Text**")
    main_cols[0].write("")
    main_cols[1].success("**Output Composition**")
    with main_cols[1]:
        output = st.empty()
    output.text_area(
        label="",
        value=mc.composition,
        height=350,
        key=f"outputtext_{mc.mc_idx_widgets}",
    )
    st.write("")
    if st.columns([3, 2, 3])[1].button("Compose (again) 🎼"):
        mc.compose_again = True
        st.experimental_rerun()
    error_display = st.empty()
    st.markdown("___")

    st.sidebar.markdown("")
    cols = st.sidebar.columns([1, 10, 1])
    length = cols[1].slider(
        "Choose The Length Of The Output Composition [50-250] :",
        min_value=50,
        max_value=250,
        step=25,
        value=mc.len_string,
        key=f"length_{mc.mc_idx_widgets}",
    )
    if length != mc.len_string:
        mc.len_string = length
        if mc.composition:
            mc.compose_again = True
        st.experimental_rerun()

    source = cols[1].radio(
        "Choose The Vocabulary Source :",
        input_sources,
        index=mc.idx_source,
        key=f"source_{mc.mc_idx_widgets}",
    )
    st.sidebar.markdown("___")

    if source != input_sources[mc.idx_source]:
        mc.idx_source = input_sources.index(source)
        mc.composition = ""
        st.experimental_rerun()

    if mc.idx_source == input_sources.index("Sample Music Lyrics"):
        artist = main_cols[0].radio(
            "Choose The Artist :",
            input_artists,
            index=mc.idx_artist,
            key=f"artist_{mc.mc_idx_widgets}",
        )
        if artist != input_artists[mc.idx_artist] or mc.compose_again:
            mc.idx_artist = input_artists.index(artist)

            artist = input_artists[mc.idx_artist]
            artist = artist.lower().replace(" ", "_")
            lyrics_files = [
                f"data\\songs\\{artist}\\{song}"
                for song in os.listdir(f"data\\songs\\{artist}")
            ]

            try:
                composer.get_words_from_text(lyrics_files)
                composer.make_graph()
                composer.compose_text(mc)

                mc.composition = composer.composition
                mc.compose_again = False
                st.experimental_rerun()
            except Exception:
                error_display.error(error_text)

    elif mc.idx_source == input_sources.index("Sample Literary Works"):
        novel = main_cols[0].radio(
            "Choose The Novel :",
            input_novels,
            index=mc.idx_novel,
            key=f"novel_{mc.mc_idx_widgets}",
        )
        if novel != input_novels[mc.idx_novel] or mc.compose_again:
            mc.idx_novel = input_novels.index(novel)

            novel = input_novels[mc.idx_novel]
            novel = novel.lower().replace(" ", "_")
            novel_file = [f"data\\texts\\{novel}.txt"]

            try:
                composer.get_words_from_text(novel_file)
                composer.make_graph()
                composer.compose_text(mc)

                mc.composition = composer.composition
                mc.compose_again = False
                st.experimental_rerun()
            except Exception:
                error_display.error(error_text)

    elif mc.idx_source == input_sources.index("Upload Text File(s)"):
        main_cols[0].markdown("<br><br>", unsafe_allow_html=True)
        main_cols[0].markdown(
            "<p style='font-size: small; '><b>Note</b>: All uploaded files will be joined into a single data source.</p>",
            unsafe_allow_html=True,
        )
        uploaded_files = main_cols[0].file_uploader(
            "Choose Your Text File(s) :",
            type=["txt"],
            accept_multiple_files=True,
            key=f"uploadedfiles_{mc.mc_idx_widgets}",
        )
        if uploaded_files and (uploaded_files != mc.uploads or mc.compose_again):
            mc.uploads = uploaded_files

            try:
                composer.get_words_from_uploader(mc.uploads)
                composer.make_graph()
                composer.compose_text(mc)

                mc.composition = composer.composition
                output.text_area(
                    label="",
                    value=composer.composition,
                    height=350,
                    key=f"uploaderoutput_{mc.mc_idx_widgets}",
                )
                mc.compose_again = False
            except Exception:
                error_display.error(error_text)

    elif mc.idx_source == input_sources.index("Paste Text Into Webapp"):
        paste = main_cols[0].text_area(
            "Paste Your Text Here",
            value="",
            height=335,
            key=f"pastedtext_{mc.mc_idx_widgets}",
        )
        if paste and (paste != mc.pasted_text or mc.compose_again):
            mc.pasted_text = paste

            try:
                composer.get_words_from_paste(mc)
                composer.make_graph()
                composer.compose_text(mc)

                mc.composition = composer.composition
                mc.compose_again = False
                st.experimental_rerun()
            except Exception:
                error_display.error(error_text)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-[end]
gc.collect()
