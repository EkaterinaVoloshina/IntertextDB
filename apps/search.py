import streamlit as st
import pymongo
#from search_utils import main_search

# # authors=None,
# # year_min_a=None
# # year_max_a=None
# # poem_name=None,
# persons_ref=None,
# # book_name=None,
# # year_min_pub=None,
# # year_max_pub=None,
# # publishing_company=None,
# # lemmas=None,
# sort_year='year_born',
# sort_direction=1,
# skip=0

import pymongo
from bson import ObjectId


def search_author(authors=None, year_min=None, year_max=None):
    query = {}
    if authors is not None and len(authors) != 0:
        query.update({"name": {"$in": authors}})
    if year_min != '':
        year_min = int(year_min)
        query.update({"year_born": {"$gte": year_min}})
    if year_max != '':
        year_max = int(year_max)
        query.update({"year_dead": {"$lte": year_max}})

    query = query if len(query) != 0 else {"_id": {"$exists": "true"}}
    return {"$match": query}


def search_poem(poem_name=None):
    query = {}
    if poem_name is not None and poem_name != '':
        query.update({"poem_name": poem_name})
    query = query if len(query) != 0 else {"poem_name": {"$exists": "true"}}
    return {"$match": query}


def search_lemma(lemmas=None):
    query = {}
    if lemmas is not None and lemmas != '':
        lemmas = list(map(str.strip, lemmas.split(',')))
        query.update({"lemma": {"$in": lemmas}})
    query = query if len(query) != 0 else {"_id": {"$exists": "true"}}
    return {"$match": query}


def search_book(book_name=None, year_min=None, year_max=None, publishing_company=None):
    query = {}
    if book_name is not None and book_name != '':
        query.update({"book_name": book_name})
    year = {}
    if year_min is not None and year_min != '':
        year_min = int(year_min)
        year.update({"$gte": year_min})
    if year_max is not None and year_max != '':
        year_max = int(year_max)
        year.update({"$lte": year_max})
    if len(year) != 0:
        query.update({"year_published": year})
    if publishing_company is not None and len(publishing_company) != 0:
        query.update({"publishing_company": {"$in": publishing_company}})
    query = query if len(query) != 0 else {"book_name": {"$exists": "true"}}
    return {"$match": query}


def search_reference(persons=None):
    query = {}
    if persons is not None and len(persons) != 0:
        query.update({"person": {"$in": persons}})
    query = query if len(query) != 0 else {"_id": {"$exists": "true"}}
    return {"$match": query}


def sorting(year='year_born', direction=1):
    query = {"num_refs": -1, "name": 1, "poems.poem_name": 1}
    query.update({year: direction})
    return query


def main_search(db, authors=None, year_min_a=None, year_max_a=None,
                poem_name=None, persons_ref=None, book_name=None,
                year_min_pub=None, year_max_pub=None, publishing_company=None,
                lemmas=None, sort_year='year_born', sort_direction=1, skip=0):
    res = db.authors.aggregate([
            search_author(authors=authors, year_min=year_min_a, year_max=year_max_a),
            {
                "$lookup": {
                    "from": "poems",
                    "localField": "_id",
                    "foreignField": "author",
                    "pipeline": [search_poem(poem_name=poem_name)],
                    "as": "poems"
                }
            },
            {
                "$unwind": "$poems"
            },
            {
                "$lookup": {
                    "from": "references",
                    "localField": "poems._id",
                    "foreignField": "poem",
                    "pipeline": [search_reference(persons=persons_ref)],
                    "as": "references"
                }
            },
            {
                "$addFields": {
                    "book_id": "$poems.book",
                    "poem_id": "$poems._id",
                    "num_refs": {"$size":"$references"}
                }
            },
            {
                "$match": {"num_refs": {"$gt": 0}}
            },
            {
                "$lookup": {
                    "from": "books",
                    "localField": "book_id",
                    "foreignField": "_id",
                    "pipeline": [
                        search_book(
                            book_name=book_name,
                            year_min=year_min_pub,
                            year_max=year_max_pub,
                            publishing_company=publishing_company)
                    ],
                    "as": "books"
                }
            },
            {
                "$unwind": "$books"
            },
            (
                {
                    "$lookup": {
                        "from": "lemmas",
                        "let": {"poem_id": "$poem_id"},
                        "pipeline": [
                            {"$match": {"$expr": {"$in": ["$$poem_id", "$docs"]}}},
                            search_lemma(lemmas=lemmas),
                        ],
                        "as": "lemmas"
                    }
                }
                if lemmas is not None else {"$match": {"_id": {"$exists": "true"}}}
            ),
            (
                {
                "$match": {"$expr": {"$gt": [{"$size": "$lemmas"}, 0]}}
                }
                if lemmas is not None else {"$match": {"_id": {"$exists": "true"}}}
            ),
            {
                "$sort": sorting(year=sort_year, direction=sort_direction)
            },
            {
                "$limit": 5
            },
            {
                "$skip": skip
            },
            {
                "$project": {
                    "author": {
                        "name": "$name",
                        "year_born": "$year_born",
                        "year_dead": "$year_dead",
                    },
                    "author_born"
                    "num_refs": "$num_refs",
                    "poem": {
                        "poem_name": "$poems.poem_name",
                        "poem_name_2": "$poems.poem_name_2",
                        "text": "$poems.text"
                    },
                    "book": "$books",
                    "comment": "$poems.comment",
                    "references": "$references"
                }
            },
        ])
    return res

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
        
        st.code(results)
        for result in results:
            st.markdown('🖋 **' + str(result['poem']['poem_name']) + '** (' + result['book'] + ', ' + result['book']['publishing_company'] + ', ' + result['book']['year_published'] +')')
            st.markdown('👤' + result['author']['name'] + ', ' + str(int(result['author']['year_born'])) + '-' + str(int(result['author']['year_dead'])))
            
            with st.expander('Посмотреть текст'):
                st.text(result['poem']['text'])

