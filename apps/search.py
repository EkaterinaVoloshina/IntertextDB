import streamlit as st

def app():
    st.header('Intertextuality database')
    poem_text = st.text_input(
            label='Poem text:',
            # placeholder='Use the Latin script'
    )
    comment_text = st.text_input(
        label='Comment text:',
        # placeholder='Use the Latin script'
    )
    col1, col2 = st.columns([5, 5])
    with col1:
        options = []
        primary_sem = st.multiselect(
            label='Author',
            options=sorted(options)
        )
    with col2:
        options = ""
        add_sem = st.text_input(
            label='Year of birth:',
        )
    col1, col2 = st.columns([5, 5])
    with col1:
        lemmas = st.text_input(
            label='Lemmas'
        )
    with col2:
        lemmas_freq = st.text_input(
            label='Frequency of lemmas'
        )