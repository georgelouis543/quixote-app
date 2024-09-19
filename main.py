import streamlit as st

nl_dashboard = st.Page(
    page="views/nl_dashboard.py",
    title="Newsletter Analytics",
    default=True
)

mr_dashboard = st.Page(
    page="views/mr_dashboard.py",
    title="Media Relations Analytics",
)

readership_dashboard = st.Page(
    page="views/readership.py",
    title="Readership",
)

newsfeed_page = st.Page(
    page="views/newsfeed_export.py",
    title="Newsfeed",
)

about_page = st.Page(
    page="views/about_page.py",
    title="About",
)

pg = st.navigation(pages=[nl_dashboard,
                          mr_dashboard,
                          readership_dashboard,
                          newsfeed_page,
                          about_page]
                   )

st.logo("assets/QuixoteLogoFinal2.png")

pg.run()
