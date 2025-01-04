import streamlit as st

from routers.other_routers.other_functions_router import other_test_functions_dashboard
from routers.about_app_routers.about_app_router import about_app_dashboard
from routers.newsfeed_routers.newsfeed_doc_export_router import newsfeed_article_export_dashboard
from routers.newsletter_routers.newsletter_article_readership_router import newsletter_article_readership_dashboard
from routers.newsletter_routers.newsletter_platform_analytics_router import \
    newsletter_platform_overall_analytics_dashboard
from routers.media_relations_routers.media_relations_sendgrid_analytics_router import \
    media_relations_sendgrid_analytics_dashboard
from routers.newsletter_routers.newsletter_sendgrid_analytics_router import newsletter_sendgrid_analytics_dashboard


def main_navigation_menu():

    # All newsletter-related routers below
    newsletter_sendgrid_analytics_route = newsletter_sendgrid_analytics_dashboard()
    newsletter_platform_analytics_route = newsletter_platform_overall_analytics_dashboard()
    newsletter_article_readership_route = newsletter_article_readership_dashboard()

    # All media-relations-related routers below
    media_relations_sendgrid_analytics_route = media_relations_sendgrid_analytics_dashboard()

    # All newsfeed-related routers below
    newsfeed_article_export_route = newsfeed_article_export_dashboard()

    # All test/misc. function routers below
    other_functions_route = other_test_functions_dashboard()

    # The app info router goes below
    about_app_route = about_app_dashboard()

    nav_list = st.navigation(pages=[
        newsletter_sendgrid_analytics_route,
        newsletter_platform_analytics_route,
        newsletter_article_readership_route,
        media_relations_sendgrid_analytics_route,
        newsfeed_article_export_route,
        other_functions_route,
        about_app_route
    ])

    st.logo("assets/QuixoteLogoFinal2.png")

    nav_list.run()
