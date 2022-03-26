import streamlit as st
import pandas as pd
from multiapp import MultiApp

from apps import home, search, poets, users, graphs # import your app modules here

app = MultiApp()

app.add_app("Home", home.app)
app.add_app("Log in", users.app)
app.add_app("Search", search.app)
app.add_app("Information", poets.app)
app.add_app("Visualisation", graphs.app)
# The main app
app.run()