import streamlit as st


def media_relations_sendgrid_analytics_dashboard():
    dashboard = st.Page(
        page="views/mr_dashboard.py",
        title="Media Relations Analytics",
    )
    return dashboard
