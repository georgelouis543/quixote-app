import streamlit as st


def newsletter_platform_overall_analytics_dashboard():
    dashboard = st.Page(
        page="views/platform_analytics.py",
        title="Platform Analytics"
    )
    return dashboard
