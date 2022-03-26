import streamlit as st
import pyvis  as pv

def app():
    st.title('The visualisation of intertextual connections')
    col1, col2 = st.columns([5, 5])
    with col1:
        options = []
        author = st.multiselect(
            label='Author',
            options=sorted(options)
        )
    with col2:
        connections = st.text_input(
            label='Number of connections:',
        )
    col1, col2 = st.columns([5, 5])
    with col1:
        options = []
        ref = st.multiselect(
            label='Reference',
            options=sorted(options)
        )
    with col2:
        ref_connections = st.text_input(
            label='Number of connections:'
        )
