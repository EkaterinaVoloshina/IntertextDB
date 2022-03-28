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
    
    st.header('НАША КОМАНДА')
    col1, col2, col3, col4, col5 = st.columns([5, 5, 5, 5, 5])
    with col1:
        st.markdown('<p style="text-align: center;">Анна Аксенова</p>', unsafe_allow_html=True)
    with col3:
        st.image('img/me.png')
        st.markdown('<p style="text-align: center;">Екатерина Волошина</p>', unsafe_allow_html=True)
    with col5:
        st.image('img/polina.png')
        st.markdown('<p style="text-align: center;">Полина Кудрявцева</p>', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns([5, 5, 5, 5, 5])
    with col2:
        st.image('img/katya.png')
        st.markdown('<p style="text-align: center;">Екатерина Такташева</p>', unsafe_allow_html=True)
    with col4:
        st.markdown('<p style="text-align: center;">Екатерина Тарасова</p>', unsafe_allow_html=True)
