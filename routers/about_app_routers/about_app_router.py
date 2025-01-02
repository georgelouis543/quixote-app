import streamlit as st


def about_app_dashboard():
    dashboard = st.Page(
        page="views/about_page.py",
        title="About",
    )
    return dashboard
