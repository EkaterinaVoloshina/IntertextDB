import streamlit as st
import streamlit_authenticator as stauth

names = ['Katya Taktasheva','Katya Voloshina']
usernames = ['tak_ty','vokat']
passwords = ['123','456']
hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
    'some_cookie_name','some_signature_key',cookie_expiry_days=30)

def app():
    st.title('Users page')
    name, authentication_status, username = authenticator.login('Login', 'main')
    if authentication_status:
        st.write('Welcome, *%s*' % (name))
        st.title('Here you can delete, change data or add new poets.')
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')