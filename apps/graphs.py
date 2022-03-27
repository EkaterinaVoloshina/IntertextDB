import streamlit as st
import pyvis  as pv

def app():
    st.header('The visualisation of intertextual connections')
    options = []
    author = st.multiselect(
            label='Author',
            options=sorted(options)
    )
    col1, col2 = st.columns([5, 5])
    with col1:
        options = ['greater', 'equal', 'less']
        ref = st.selectbox(
            label='Mode',
            options=sorted(options)
        )
    with col2:
        ref_connections = st.text_input(
            label='Number of references:',
        )
    button = st.button('Show graph')
