import streamlit as st

from controllers.auth_controllers.google_login_controller import handle_login
from views.auth.login_view import google_login_view

st.set_page_config(layout="wide")

# calling login controller for Google Login
handle_login_result = handle_login()
google_login_view(handle_login_result)
