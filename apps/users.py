import streamlit as st
import streamlit_authenticator as stauth

names = ['Катя Такташева','Катя Волошина']
usernames = ['tak_ty','vokat']
passwords = ['123','456']
hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
    'some_cookie_name','some_signature_key',cookie_expiry_days=30)

def app():
    name, authentication_status, username = authenticator.login('Login', 'main')
    if authentication_status:
        st.write('Добро пожаловать, *%s*' % (name))
        st.header('На этой стране можно редактировать базу данных')
        st.selectbox('Что вы хотите сделать?', ['удалить таблицу', 'добавить таблицу', 'редактировать'])
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
