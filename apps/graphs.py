import streamlit as st
from pyvis import network as net
import pymongo
import streamlit.components.v1 as components


def init_connection():
    return pymongo.MongoClient("mongodb+srv://myuser:WJaeLEbqzFLKrONL@cluster0.4ikl0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


def app():
    client = init_connection()
    db = client.intertext
    col1, col2 = st.columns([1, 8])
    with col2:
        st.header('Визуализация интертекстуальных связей')
    with col1:
        st.markdown("<h1 style='text-align: center; font-size: 300%'>📊</h1>",
                    unsafe_allow_html=True)
        
    with st.expander('Инструкция'):
        st.markdown('**Автор**: выберите автора, чтобы посмотреть, к каким людям он отсылал в своем творчестве или какие люди ссылались на него.')
        st.markdown('Ограничить число отсылок можно с помощью **фильтра**. Выберите "больше" и число *n* в поле **Количество отсылок**, если хотите получить больше отсылок, чем *n*. Также можете выбрать "равно"  (=*n*) или "меньше" (<*n*).')
         
    options = db.authors.find().distinct("name")
    name = st.selectbox(
        label='Автор',
        options=sorted(options)
    )
    col1, col2 = st.columns([5, 5])
    with col1:
        options = {'$gt': 'больше',
                   '$eq': 'равно',
                   '$lt': 'меньше'}
        sort = st.selectbox(
            label='Фильтр',
            options=list(options.keys()),
            format_func = lambda x: options[x]
        )
    with col2:
        freq = st.number_input(
            label='Количество отсылок:', step=1,
        )
    
    button = st.button('Show graph')
    if button:
        res = db.authors.aggregate([
            {'$match': {'name': name}},
            {'$lookup': {
                'from': 'poems',
                'localField': '_id',
                'foreignField': 'author',
                'as': 'poems'
            }},
            {'$lookup': {
                'from': 'references',
                'localField': 'poems._id',
                'foreignField': 'poem',
                'as': 'references'
            }},
            {'$unwind': '$references'},
            {'$project': {
                '_id': 1,
                'author': '$name',
                'ref.id': '$references.person',
            }},
            {'$group':
                {
                    '_id': '$ref.id',
                    'count': {'$sum': 1}
                }},
            {'$match': {'count': {sort: freq}}
             },
            {'$project': {
                '_id': '$_id'
            }}
        ])
        g = net.Network(height='400px', width='50%', heading='')
        g.add_node(name)
        for num, ref in enumerate(res):
            ref_name = ref['_id']
            g.add_node(ref_name)
            g.add_edge(name, ref_name)


        g.show('example.html')
        components.html(open('example.html', 'r', encoding='utf-8').read(), height=1500, width=1500)
