import streamlit as st
from streamlit_google_auth import Authenticate
from streamlit_js_eval import streamlit_js_eval

from views.navbar import main_navigation_menu


def handle_login():
    authenticator = Authenticate(
        secret_credentials_path='google_credentials.json',
        cookie_name='my_cookie_name',
        cookie_key='this_is_secret',
        redirect_uri='http://localhost:8501',
    )

    # Check if the user is already authenticated
    authenticator.check_authentification()
    authorization_url = None
    # Display the login button if the user is not authenticated
    if not st.session_state.get('connected', False):
        authorization_url = authenticator.get_authorization_url()
        return {
            "connected": False,
            "authorization_url": authorization_url,
            "is_meltwater_domain": False,
            "authenticator": authenticator
        }
    # Allow access
    else:
        if str(st.session_state["user_info"].get('email', "abc@email.com")).endswith("meltwater.com"):
            return {
                "connected": True,
                "authorization_url": authorization_url,
                "is_meltwater_domain": True,
                "authenticator": authenticator
            }
        else:
            return {
                "connected": True,
                "authorization_url": authorization_url,
                "is_meltwater_domain": False,
                "authenticator": authenticator
            }
