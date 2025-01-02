import streamlit as st


def newsletter_article_readership_dashboard():
    dashboard = st.Page(
        page="views/readership.py",
        title="Readership",
    )
    return dashboard

