import streamlit as st


def newsletter_sendgrid_analytics_dashboard():
    dashboard = nl_dashboard = st.Page(
        page="views/nl_dashboard.py",
        title="Newsletter Analytics",
        default=True
    )
    return dashboard
