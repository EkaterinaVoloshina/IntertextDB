import streamlit as st

def app():
    st.title('ЦИФРОВЫЕ ИССЛЕДОВАНИЯ ИНТЕРТЕКСТУАЛЬНОСТИ НА МАТЕРИАЛЕ РУССКОЙ ПОЭЗИИ')
    st.header('О ПРОЕКТЕ')
    st.text("""Проект посвящен исследованию интертекстуальности на материале русской поэзии.""")
    st.text("""Этот ресурс может быть полезен как исследователям, так и непродвинутым""")
    st.text('пользователям, так как помимо узкоспециализированной информации на нем') 
    st.text('представлены научно-популярные статьи и подробная инструкция для пользователей.')
    st.text('Школьная программа не предполагает интертекстуального анализ апоэзии, поэтому')
    st.text('увлеченным литературой учащимся наш ресурс поможет открыть много нового.')
    
    st.header('Наша команда')
    
    col1, col2, col3 = st.columns([5, 5, 5])
    with col1:
        st.text('Анна Аксенова')
    with col2:
        st.text('Екатерина Волошина')
    with col3:
        st.text('Полина Кудрявцева')
    col1, col2 = st.columns([5, 5])
    with col1:
        st.text('Екатерина Такташева')
    with col2:
        st.text('Екатерина Тарасова')
    
