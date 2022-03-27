import streamlit as st
import pandas as pd
from multiapp import MultiApp
import pymongo 
from apps import home, search, poets, users, graphs # import your app modules here

def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

#client = init_connection()
app = MultiApp()
#db = client.intertext

app.add_app("Главная", home.app)
app.add_app("Вход", users.app)
app.add_app("Поиск", search.app)
app.add_app("Информация", poets.app)
app.add_app("Визуализация", graphs.app)
# The main app
app.run()
