import streamlit as st
import pymongo
from bson import ObjectId
from .search_utils import *


def init_connection():
    return pymongo.MongoClient(st.secrets["mongo"]["key"])

def app():
    
    client = init_connection()
    db = client.intertext
    
   
    col1, col2 = st.columns([1, 8])
    with col2:
        st.header('Поиск')
    with col1:
        st.markdown("<h1 style='text-align: center; font-size: 300%'>🔍</h1>",
                    unsafe_allow_html=True)
    st.markdown('На этой странице вы можете найти все необходимые вам отсылки.')
    
    with st.expander('Инструкция'):
        st.markdown('### Полнотекстовый поиск')
        st.markdown('Полнотекстовый поиск позволяет искать точные формы по тексту отсылки. Просто напишите нужное вам слово/сочетание. Например: "стихотворение Пушкина". **Важно**: полнотекстовый поиск не подразумевает выбора подкорпуса.')
        st.markdown('### Основной поиск')
        st.markdown('В основном поиске можно задавать лексемы, встречающиеся в комментарии. Для этого укажите все необходимые леммы через запятую в поле **Текст отсылки**. Например: "стихотворение,Пушкин". ')
        st.markdown('Основной поиск позволяет органичить подкорпус, по которому будет осуществляться поиск.')
        st.markdown('**Параметры поиска:**')
        st.markdown('**Название произведения**: выберите названия произведений из списка, чтобы осуществлять поиск только по определенным произведениям.')
        st.markdown('**Автор:** вы ограничить поиск по автору произведения')
        st.markdown('**Отсылка на**: здесь вы можете выберать автора, отсылки на которого вы хотите найти.')
        st.markdown('**Годы жизни:** вы можете указать годы жизни автора, например, чтобы найти все отсылки авторов, живших до 1900 года.')
        st.markdown('**Название сборника:** выберите все сборники, по которым хотите осуществить поиск.')
        st.markdown('**Год публикации:** вы можете ограничить подкорпус по году публикации сборника.')
        st.markdown('### Параметры выдачи')
        st.markdown('Вы можете сортировать выдачу по нескольким параметрам: **году рождения** автора, **году смерти автора** и **году публикации** сборника. Выдача может быть выведена в порядке **по возрастанию** или **по убыванию**.')
    
    st.subheader('Полнотекстовый поиск')
    fulltext = st.text_input(
        label='',
        placeholder='стихотворение Пушкина',
        key='полнотекстовый поиск'
    )

    if not fulltext:
        st.subheader('Основной поиск')
        lemmas = st.text_input(
            label='Текст отсылки:',
            placeholder='Например: посвящать,отсылать'
        )

        poem_name = st.multiselect(
            label='Название произведения:',
            options=sorted(db.poems.find().distinct("poem_name"))
        )
        
        authors = st.multiselect(
            label='Автор:',
            options=sorted(db.authors.find().distinct("name"))
        )
        persons_ref = st.multiselect(
            label='Отсылка на:',
            options=db.references.find().distinct("person")
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
    button = st.button('Search', key='1')

    # search results
    if button:
        st.markdown("---")
        if fulltext:
            with st.spinner('⏳ Ищем документы...')
                results = fulltext_search(db=db, text=fulltext, 
                                          sort_year=sort_year, sort_direction=sort_direction,
                                          skip=0)
        else:
            with st.spinner('⏳ Ищем документы...')
                results = main_search(
                    db=db, authors=authors, year_min_a=year_min_a, year_max_a=year_max_a,
                    poem_name=poem_name, persons_ref=persons_ref, book_name=book_name,
                    year_min_pub=year_min_pub, year_max_pub=year_max_pub,
                    publishing_company=publishing_company,
                    lemmas=lemmas, sort_year=sort_year, sort_direction=sort_direction,
                    skip=0
                )
        st.subheader('Результаты поиска')
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

