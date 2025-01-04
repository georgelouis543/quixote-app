import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from controllers.auth_controllers.google_login_controller import handle_login
from views.navbar import main_navigation_menu
from controllers.auth_controllers.logout_controller import handle_logout


def google_login_view(handle_login_result):
    result_after_login_check = handle_login_result

    if result_after_login_check["connected"] is True and result_after_login_check["is_meltwater_domain"] is True:

        main_navigation_menu()

        if st.button('Log out'):
            handle_logout(result_after_login_check["authenticator"])
            streamlit_js_eval(js_expressions="parent.window.location.reload()")

    elif result_after_login_check["connected"] is True and result_after_login_check["is_meltwater_domain"] is False:

        st.write("User Unauthorized! Please use a meltwater Account")
        if st.button('Log out'):
            handle_logout(result_after_login_check["authenticator"])

    else:
        st.link_button('Login with your Meltwater Account', result_after_login_check["authorization_url"])

