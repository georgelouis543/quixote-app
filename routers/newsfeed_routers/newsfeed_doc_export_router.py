import streamlit as st


def newsfeed_article_export_dashboard():
    dashboard = st.Page(
        page="views/newsfeed_export.py",
        title="Newsfeed",
    )
    return dashboard
