import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class Settings:
    #OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    #OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
    #OPENAI_MODEL = os.getenv("OPENAI_MODEL")

    #AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    #AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    #AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
    #AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")

    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    OPENAI_BASE_URL = st.secrets["OPENAI_BASE_URL"]
    OPENAI_MODEL = st.secrets["OPENAI_MODEL"]

    AUTH0_DOMAIN = st.secrets["AUTH0_DOMAIN"]
    AUTH0_CLIENT_ID = st.secrets["AUTH0_CLIENT_ID"]
    AUTH0_CLIENT_SECRET = st.secrets["AUTH0_CLIENT_SECRET"]
    AUTH0_CALLBACK_URL = st.secrets["AUTH0_CALLBACK_URL"]

settings = Settings()