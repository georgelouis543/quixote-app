import streamlit as st
from streamlit_google_auth import Authenticate


def handle_logout(authenticator):
    authenticator.logout()
