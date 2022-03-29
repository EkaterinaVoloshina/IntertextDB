import streamlit as st
from .search_utils import *


def init_connection():
    return pymongo.MongoClient(st.secrets["mongo"]["key"])


def full_text_reset():
    if 'button' in st.session_state:
        del st.session_state.button
    if 'fulltext' not in st.session_state:
        st.session_state['fulltext'] = False
    st.session_state['fulltext'] = not st.session_state['fulltext']

    
def lemmas_reset():
    if 'button' in st.session_state:
        del st.session_state.button
    if 'lemmas' not in st.session_state:
        st.session_state['lemmas'] = False
    st.session_state['lemmas'] = not st.session_state['lemmas']


def button_reset():
    if 'button' in st.session_state:
        del st.session_state.button


def change_state():
    st.session_state.button = True
    st.session_state.page = 0


def next_page():
    st.session_state['page'] += 1


def prev_page():
    st.session_state['page'] -= 1


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
        st.markdown('### Поиск по точным формам')
        st.markdown(
            'Полнотекстовый поиск позволяет искать точные формы по тексту отсылки. Просто напишите нужное вам слово/сочетание. Например: "стихотворение Пушкина".')
        st.markdown('### Поиск по леммам')
        st.markdown(
            'Здесь можно задавать лексемы, встречающиеся в комментарии. Для этого укажите все необходимые леммы через запятую в поле **Текст отсылки**. Например: "стихотворение,Пушкин". ')
        st.markdown('### Выбор подкорруса')
        st.markdown('Здесь вы можете выбрать подкорпус, по которому хотите осуществлять поиск')
        st.markdown(
            '**Название произведения**: выберите названия произведений из списка, чтобы осуществлять поиск только по определенным произведениям.')
        st.markdown('**Автор:** вы ограничить поиск по автору произведения')
        st.markdown(
            '**Отсылка на**: здесь вы можете выберать автора, отсылки на которого вы хотите найти.')
        st.markdown(
            '**Годы жизни:** вы можете указать годы жизни автора, например, чтобы найти все отсылки авторов, живших до 1900 года.')
        st.markdown(
            '**Название сборника:** выберите все сборники, по которым хотите осуществить поиск.')
        st.markdown(
            '**Год публикации:** вы можете ограничить подкорпус по году публикации сборника.')
        st.markdown('### Параметры выдачи')
        st.markdown(
            'Вы можете сортировать выдачу по нескольким параметрам: **году рождения** автора, **году смерти автора** и **году публикации** сборника. Выдача может быть выведена в порядке **по возрастанию** или **по убыванию**.')

    st.subheader('Поиск по точным формам')
    fulltext = st.text_input(
        label='',
        placeholder='стихотворение Пушкина',
        key='полнотекстовый поиск',
        on_change=full_text_reset
    )
    st.subheader('Поиск по леммам')
    lemmas = st.text_input(
        label='Текст отсылки:',
        placeholder='Например: посвящать,отсылать',
        on_change=lemmas_reset
    )

    st.subheader('Выбор подкорпуса')

    poem_name = st.multiselect(
        label='Название произведения:',
        options=sorted(db.poems.find().distinct("poem_name")),
        on_change=button_reset
    )

    authors = st.multiselect(
        label='Автор:',
        options=sorted(db.authors.find().distinct("name"),
                       key=lambda x: x.split()[-1]),
        on_change=button_reset
    )
    persons_ref = st.multiselect(
        label='Отсылка на:',
        options=sorted(db.references.find().distinct("person"),
                       key=lambda x: x.split()[-1]),
        on_change=button_reset
    )

    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        st.text("Годы жизни:")
    with col2:
        year_min_a = st.text_input(
            label='с',
            key='born_from',
            on_change=button_reset
        )
    with col3:
        year_max_a = st.text_input(
            label='до',
            key='born_till',
            on_change=button_reset
        )
    col1, col2 = st.columns([6, 4])
    with col1:
        book_name = st.multiselect(
            label='Название сборника:',
            options=sorted(db.books.find().distinct("book_name")),
            on_change=button_reset
        )
    with col2:
        publishing_company = st.multiselect(
            label='Издательство:',
            options=sorted(db.books.find().distinct("publishing_company")),
            on_change=button_reset
        )
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        st.text("Год публикации:")
    with col2:
        year_min_pub = st.text_input(
            label='с',
            key='pub_from',
            on_change=button_reset
        )
    with col3:
        year_max_pub = st.text_input(
            label='до',
            key='pub_till',
            on_change=button_reset
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
            format_func=lambda x: sort_options[x],
            on_change=button_reset
        )

    with col2:
        sort_dirs = {1: 'По возрастанию', -1: 'По убыванию'}
        sort_direction = st.radio(
            label='Направление:',
            options=list(sort_dirs.keys()),
            format_func=lambda x: sort_dirs[x],
            on_change=button_reset
        )
    if 'lemmas' not in st.session_state:
        st.session_state['lemmas'] = False
    if 'fulltext' not in st.session_state:
        st.session_state['fulltext'] = False

    if st.session_state['fulltext'] and st.session_state['lemmas']:
        st.warning('Нельзя осуществлять поиск одновременно по леммам и точным формам')
    else:
        st.button('Поиск', key='1', on_click=change_state)

    if 'button' in st.session_state and st.session_state.button:

        st.markdown("---")

        def results_page(page):
            if st.session_state.fulltext:
                with st.spinner('⏳ Ищем документы...'):
                    results = fulltext_search(
                        db=db, text=fulltext, authors=authors, year_min_a=year_min_a,
                        year_max_a=year_max_a,
                        poem_name=poem_name, persons_ref=persons_ref,
                        book_name=book_name,
                        year_min_pub=year_min_pub, year_max_pub=year_max_pub,
                        publishing_company=publishing_company, sort_year=sort_year,
                        sort_direction=sort_direction,
                        skip=page * 3
                    )
            else:
                with st.spinner('⏳ Ищем документы...'):
                    results = main_search(
                        db=db, authors=authors, year_min_a=year_min_a,
                        year_max_a=year_max_a,
                        poem_name=poem_name, persons_ref=persons_ref,
                        book_name=book_name,
                        year_min_pub=year_min_pub, year_max_pub=year_max_pub,
                        publishing_company=publishing_company,
                        lemmas=lemmas, sort_year=sort_year,
                        sort_direction=sort_direction,
                        skip=page * 3
                    )
            results = list(results)
            return results

        results = results_page(st.session_state.page)
        
        st.subheader('Результаты поиска')
        if len(results) == 0:
            st.text('Ничего не нашлось :(')
        else:
            for result in results:
                st.markdown(
                    '🖋 **' + str(result['poem']['poem_name']) + '** (' +
                    result['book']['book_name'] + ', ' + result['book'][
                        'publishing_company'] + ', ' + str(
                        int(result['book']['year_published'])) + ')')
                st.markdown('👤' + result['author']['name'] + ', ' + str(
                    int(result['author']['year_born'])) + '-' + str(
                    int(result['author']['year_dead'])))
                comment = result['comment']['text']
                for num, ref in enumerate(result['references']):
                    start = ref['start'] + num * 6
                    finish = ref['finish'] + num * 6
                    comment = comment[:start] + '___' + comment[
                                                        start:finish] + '___' + comment[
                                                                                finish:]
                st.markdown(comment + ' [' + result['comment']['author'] + ']')
                with st.expander('Посмотреть текст стихотворения'):
                    st.text(result['poem']['text'])

        col1, col2, col3 = st.columns([2, 4, 0.5])
        with col1:
            if st.session_state['page'] > 0:
                st.button('<<', on_click=prev_page, key='next')
            else:
                st.text('')
        with col2:
            st.text('')
        with col3:
            if len(results) == 5:
                st.button('>>', on_click=next_page, key='prev')
