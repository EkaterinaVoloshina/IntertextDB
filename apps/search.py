import streamlit as st
import pymongo
from bson import ObjectId
from .search_utils import *


def init_connection():
    return pymongo.MongoClient(st.secrets["mongo"]["key"])

def app():
    
    client = init_connection()
    db = client.intertext
    
    # search buttons
    col1, col2 = st.columns([1, 8])
    with col2:
        st.header('Поиск')
    with col1:
        st.markdown("<h1 style='text-align: center; font-size: 300%'>🔍</h1>",
                    unsafe_allow_html=True)
    st.text('Здесь вы можете найти нужные вам отсылки')
    
    fulltext = st.text_input('
        label='Полнотекстовый поиск:',
         placeholder='стихотворение Пушкина'
    )

    if not fulltext:

        lemmas = st.text_input(
            label='Текст отсылки:',
            placeholder='Например: посвящать,отсылать'
        )

        poem_name = st.text_input(
            label='Название произведения:'
        )

        persons_ref = st.multiselect(
            label='Отсылка на:',
            options=db.references.find().distinct("person")
        )
        options = db.authors.find().distinct("name")
        authors = st.multiselect(
            label='Автор',
            options=sorted(options)
        )
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.text("Годы жизни:")
        with col2:
            year_min_a = st.text_input(
                label='с',
                key='born_from'
            )
        with col3:
            year_max_a = st.text_input(
                label='до',
                key='born_ttll'
            )
        col1, col2 = st.columns([6, 4])
        with col1:
            book_name = st.text_input(
                label='Название сборника:'
            )
        with col2:
            options = db.books.find().distinct("publishing_company")
            publishing_company = st.multiselect(
                label='Издательство:',
                options=sorted(options)
            )
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.text("Год публикации:")
        with col2:
            year_min_pub = st.text_input(
                label='с',
                key='pub_from'
            )
        with col3:
            year_max_pub = st.text_input(
                label='до',
                key='pub_till'

            )
    col1, col2 = st.columns([5, 5])
    with col1:
        sort_options = {
            'year_born': 'Году рождения',
            'year_dead': 'Году смерти',
            'books.year_published': 'Году публикации'
        }
        sort_year = st.radio(
            label='Сортировать по:',
            options=list(sort_options.keys()),
            format_func=lambda x: sort_options[x]
        )

    with col2:
        sort_dirs = {1: 'По возрастанию', -1: 'По убыванию'}
        sort_direction = st.radio(
            label='Направление:',
            options=list(sort_dirs.keys()),
            format_func=lambda x: sort_dirs[x]
        )
    with st.expander('Инструкция'):
        st.text('Инструкция')
    button = st.button('Search', key='1')

    # search results
    if button:
        st.markdown("---")
        st.subheader('Результаты поиска')
        results = main_search(
            db=db, authors=authors, year_min_a=year_min_a, year_max_a=year_max_a,
            poem_name=poem_name, persons_ref=persons_ref, book_name=book_name,
            year_min_pub=year_min_pub, year_max_pub=year_max_pub,
            publishing_company=publishing_company,
            lemmas=lemmas, sort_year=sort_year, sort_direction=sort_direction,
            skip=0
        )
        for result in results:
            if result is None:
                 st.info('Ничего не нашлось :(')
                 break
            st.markdown('🖋 **' + str(result['poem']['poem_name']) + '** (' + result['book']['book_name'] + ', ' + result['book']['publishing_company'] + ', ' + str(int(result['book']['year_published'])) +')')
            st.markdown('👤' + result['author']['name'] + ', ' + str(int(result['author']['year_born'])) + '-' + str(int(result['author']['year_dead'])))
            comment = result['comment']['text']
            for num, ref in enumerate(result['references']):
                start = ref['start'] + num * 6
                finish = ref['finish'] + num * 6
                comment = comment[:start] + '___' + comment[start:finish] + '___' + comment[finish:]
            st.markdown(comment + ' [' + result['comment']['author'] + ']')
            with st.expander('Посмотреть текст стихотворения'):
                st.text(result['poem']['text'])

