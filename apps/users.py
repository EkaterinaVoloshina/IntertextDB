import streamlit as st
import streamlit_authenticator as stauth
import pymongo

names = ['Катя Такташева', 'Катя Волошина']
usernames = ['tak_ty', 'vokat']
passwords = ['123', '456']
hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)

def init_connection():
    return pymongo.MongoClient(st.secrets["mongo"]["key"])


def app():
    name, authentication_status, username = authenticator.login('Login', 'main')
    if authentication_status:
        st.write('Добро пожаловать, *%s*' % name)
        col1, col2 = st.columns([1, 8])
        with col2:
            st.header('Редактор базы данных')
        with col1:
            st.markdown(
                "<h1 style='text-align: center; font-size: 300%'>💻</h1>",
                unsafe_allow_html=True)

        client = init_connection()
        db = client.intertext

        todo = st.selectbox('Что вы хотите сделать?', ['удалить', 'добавить', 'редактировать'])

        if todo == 'удалить':
            st.subheader('Удалить')
            st.text('Здесь вы можете удалить нужные вам значени из базы')

            todelete = st.selectbox('Что вы хотите удалить?', ['поэта', 'сборник', 'поэму', 'отсылку'])

            if todelete == 'поэта':
                author = st.selectbox('Выберите поэта', db.authors.find().distinct("name"))
                button = st.button('Удалить', key='1')
                if button:
                    author_id = db.authors.find_one({'name': author})
                    if 'books' in author_id:
                        books = author_id['books']
                        db.books.delete_many({"_id": {"$in": books}})
                    if 'poems' in author_id:
                        poems = author_id['poems']
                        db.references.delete_many({'poem': {"$in": poems}})
                        db.poems.delete_many({"_id": {"$in": poems}})
                    db.authors.delete_one({"_id": author_id['_id']})
                    st.info(f'Автор {author} удален')
            elif todelete == 'сборник':
                book_name = st.selectbox(Выберите сборник', db.books.find().distinct("book_name"))
                button = st.button('Удалить', key='1')
                if button:
                    book_id = db.books.find_one({'book_name': book_name})
                    poems = list(map(
                        lambda x: x['_id'],
                        db.poems.find({"book": book_id['_id']}, {'_id': True}))
                    )
                    db.books.delete_one({"_id": book_id['_id']})
                    db.poems.delete_many({"_id": {"$in": poems}})
                    db.references.delete_many({'book': book_id['_id']})
                    st.info(f'Сборник {book_name} удален')
            elif todelete == 'поэму':
                poem_name = st.selectbox('Выберите поэму', db.poems.find().distinct("poem_name"))
                button = st.button('Удалить', key='1')
                if button:
                    poem_id = db.poems.find_one({'poem_name': poem_name})
                    db.poems.delete_one({"_id": poem_id['_id']})
                    db.references.delete_many({'poem': poem_id['_id']})
                    st.info(f'Поэма {poem_name} удалена')
            elif todelete == 'отсылку':
                reference = st.selectbox('Выберите отсылки на какого поэта вы хотите отредактировать',
                    db.references.find().distinct("person"))
                button = st.button('Удалить', key='1')
                if button:
                    db.references.delete_many({'person': reference})
                    st.info(f'Отсылки на автора {reference} удалены')

        elif todo == 'добавить':
            st.subheader('Добавить')
            st.text('Здесь вы можете добавить новые значения в базу')

            toadd = st.selectbox('Что вы хотите добавить?',
                                 ['поэта', 'cборник', 'поэму', 'отсылку'])
            if toadd == 'поэта':
                author = st.text_input(label='*Введите имя:')
                col1, col2 = st.columns([5, 5])
                with col1:
                    year_born = st.text_input('*Год рождения:')
                with col2:
                    year_dead = st.text_input('*Год смерти:')

                button = st.button('Добавить', key='1')
                if button:
                    if author == '' or year_born == '' or year_dead == '':
                        st.warning('Пожалуйста, заполните все необходимые поля')
                    else:
                        match = db.authors.find_one({
                            'name': author,
                            "year_born": int(year_born),
                            "year_deed": int(year_dead)
                        })
                        if match:
                            st.warning('Такой поэт уже существует')
                        else:
                            id = db.authors.insert_one({
                                "name": author,
                                "year_born": int(year_born),
                                "year_deed": int(year_dead)
                            }).inserted_id
                            st.info(f'Поэт добавлен в базу! Его сгенерированный id: {id}')
            elif toadd == 'сборник':
                book_name = st.text_input(label='*Введите название сборника:')
                col1, col2 = st.columns([5, 5])
                with col1:
                    year_published = st.text_input('*Год публикации:')
                with col2:
                    publishing_company = st.text_input('*Издательство:')
                button = st.button('Добавить', key='1')
                if button:
                    if book_name == '' or year_published == '' or publishing_company == '':
                        st.warning('Пожалуйста, заполните все необходимые поля')
                    else:
                        match = db.books.find_one({
                            'book_name': book_name,
                            "year_published": int(year_published),
                            "publishing_company": publishing_company
                        })
                        if match:
                            st.warning('Такой сборник уже существует')
                        else:
                            id = db.books.insert_one({
                                'book_name': book_name,
                                "year_published": int(year_published),
                                "publishing_company": publishing_company
                            }).inserted_id
                            st.info(f'Сборник добавлен в базу! Его сгенерированный id: {id}')
            elif toadd == 'поэму':
                author = st.selectbox('*Автор:', db.authors.find().distinct("name"))
                col1, col2 = st.columns([5, 5])
                with col1:
                    poem_name = st.text_input('*Название поэмы:')
                with col2:
                    poem_name_2 = st.text_input('Альтернативное название:')
                book_name = st.selectbox('*Название сборника:', db.books.find().distinct("book_name"))
                poem_text = st.text_input('*Текст поэмы:')
                st.text('Информация о комментарии')
                comment_author = st.text_input('*Автор комментария:')
                comment_text = st.text_input('*Текст комментария')
                button = st.button('Добавить', key='1')
                if button:
                    if author == '' or poem_name == ''\
                            or book_name == '' or poem_text == '' \
                            or comment_author == '' or comment_text == '':
                        st.warning('Пожалуйста, заполните все необходимые поля')
                    else:
                        author_id = db.authors.find_one({'name': author})['_id']
                        match = db.poems.find_one({
                            'poem_name': poem_name,
                            "author": author_id,
                        })
                        if match:
                            st.warning('Такая поэма уже существует')
                        else:
                            book_id = db.books.find_one({'book_name': book_name})['_id']
                            id = db.poems.insert_one({
                                "author": author_id,
                                "poem_name": poem_name,
                                "poem_name_2": poem_name_2 if poem_name_2 else poem_name,
                                "text": poem_text,
                                "book": book_id,
                                "comment": {"author": comment_author, 'text': comment_text}
                            }).inserted_id
                            st.info(f'Поэма добавлена в базу! Её сгенерированный id: {id}')
            elif toadd == 'отсылку':
                poem = st.selectbox('*Поэма:', db.poems.find().distinct("poem_name"))
                person = st.text_input('*На кого отсылка:')
                col1, col2 = st.columns([5, 5])
                with col1:
                    start = st.text_input('*Начало отсылки:')
                with col2:
                    finish = st.text_input('*Конец отсылки:')
                wiki_id = st.text_input('WikiDataID:')
                button = st.button('Добавить', key='1')
                if button:
                    if poem == '' or person == ''\
                            or start == '' or finish == '':
                        st.warning('Пожалуйста, заполните все необходимые поля')
                    else:
                        poem_id = db.poems.find_one({'poem_name': poem})['_id']
                        match = db.references.find_one({
                            'poem': poem_id,
                            "person": person,
                            "start": int(start),
                            "finish": int(finish)
                        })
                        if match:
                            st.warning('Такая поэма уже существует')
                        else:
                            id = db.references.insert_one({
                                'poem': poem_id,
                                "person": person,
                                "start": int(start),
                                "finish": int(finish),
                                "wiki_id": wiki_id
                            }).inserted_id
                            st.info(f'Отсылка добавлена в базу! Её сгенерированный id: {id}')

        elif todo == 'редактировать':
            st.subheader('Редактировать')
            st.text('Здесь вы можете редактировать записанные в базу документы.')
            st.text('Если вы не хотите менять атрибут, оставьте поле пустым.')

            tochange = st.selectbox('Что вы хотите изменить?',
                                 ['поэта', 'cборник', 'поэму'])

            if tochange == 'поэта':
                author = st.selectbox('Выберите поэта', db.authors.find().distinct("name"))
                st.markdown('---')
                new_name = st.text_input('Введите новое имя:')
                col1, col2 = st.columns([5, 5])
                with col1:
                    year_born = st.text_input('Год рождения:')
                with col2:
                    year_dead = st.text_input('Год смерти:')

                button = st.button('Изменить', key='1')
                if button:
                    query = {"$set": {}}
                    if new_name != '':
                        query['$set'].update({"name": new_name})
                    if year_born != '':
                        query['$set'].update({"year_born": int(year_born)})
                    if year_dead != '':
                        query['$set'].update({"year_dead": int(year_dead)})
                    if len(query["$set"]) != 0:
                        db.authors.update_one({"name": author}, query)
                        st.info(f"""Информация о поэте "{author}" изменена""")
                    else:
                        st.info("Нечего менять")

            elif tochange == 'сборник':
                book_name = st.selectbox('Выберите сборник', db.books.find().distinct("book_name"))
                st.markdown('---')
                new_name = st.text_input('Введите новое название:')
                col1, col2 = st.columns([5, 5])
                with col1:
                    year_published = st.text_input('Год публикации:')
                with col2:
                    publishing_company = st.text_input('Издательство:')
                button = st.button('Изменить', key='1')
                if button:
                    query = {"$set": {}}
                    if new_name != '':
                        query["$set"].update({"book_name": new_name})
                    if year_published != '':
                        query["$set"].update({"year_published": year_published})
                    if publishing_company != '':
                        query["$set"].update({"publishing_company": publishing_company})
                    if len(query["$set"]) != 0:
                        db.books.update_one({"book_name": book_name}, query)
                        st.info(f"""Информация о сборнике "{book_name}" изменена""")
                    else:
                        st.info("Нечего менять")

            elif tochange == 'поэму':
                poem_name = st.selectbox('Выберите поэму', db.poems.find().distinct("poem_name"))
                st.markdown('---')
                poem = db.poems.find_one({"poem_name": poem_name})
                author_id = poem['author']
                author_id = db.authors.find_one({"_id": author_id})
                authors = db.authors.find().distinct("name")
                author = st.selectbox('Имя автора:', authors, authors.index(author_id['name']))
                col1, col2 = st.columns([5, 5])
                with col1:
                    new_poem_name = st.text_input('Название поэмы:')
                with col2:
                    poem_name_2 = st.text_input('Альтернативное название:')
                books = db.books.find().distinct("book_name")
                book_id = poem['book']
                book_id = db.books.find_one({"_id": book_id})
                book_name = st.selectbox('Название сборника:', books,
                                         index=books.index(book_id['book_name']))
                poem_text = st.text_input('Текст поэмы:')
                st.text('Информация о комментарии')
                comment_author = st.text_input('Автор комментария:')
                comment_text = st.text_input('Текст комментария')
                button = st.button('Изменить', key='1')
                if button:
                    query = {"$set": {}}
                    if author != author_id['name']:
                        query["$set"].update({"author": db.authors.find_one({'name': author})['_id']})
                    if new_poem_name != '':
                        query["$set"].update({"poem_name": new_poem_name})
                    if poem_name_2 != '':
                        query["$set"].update({'poem_name_2': poem_name_2})
                    if book_name != book_id['book_name']:
                        query["$set"].update({'book': db.books.find_one({"book_name": book_name})['_id']})
                    if poem_text != '':
                        query["$set"].update({'text': poem_text})
                    comment = {'comment': {}}
                    if comment_author != '':
                        comment['comment'].update({'author': comment_author})
                    if comment_text != '':
                        comment['comment'].update({'text': comment_text})
                    if len(comment['comment']) != 0:
                        query["$set"].update(comment)
                    if len(query["$set"]) != 0:
                        db.poems.update_one({"poem_name": poem_name}, query)
                        st.info(f"""Информация о поэме "{poem_name}" изменена""")
                    else:
                        st.info("Нечего менять")
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
