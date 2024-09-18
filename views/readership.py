import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import httpx


# Function to check the final URL in a synchronous manner
def check_final_url(url):
    try:
        with httpx.Client(follow_redirects=True, timeout=10) as client:
            response = client.get(url)
            return str(response.url)
    except Exception as e:
        print(f"Exception {e} Occurred")
        return url


# Function to check a list of URLs using threading
def check_urls_concurrently(urls_list):
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust the number of threads as needed
        futures = [executor.submit(check_final_url, url) for url in urls_list]
        for future in futures:
            results.append(future.result())
    return results


@st.cache_data
def clicks_aggregator(input_df):
    input_df = input_df
    all_urls = input_df["url"].unique()
    filtered_clicked_urls_list = list(set(all_urls))
    print(filtered_clicked_urls_list)
    print(len(filtered_clicked_urls_list))
    out_url_arr = []
    for url in filtered_clicked_urls_list:
        out_url_dict = {}
        filtered_url_df = input_df[input_df["url"] == url]
        out_url_dict["transition_url"] = url
        out_url_dict["click_count"] = len(filtered_url_df)
        out_url_dict["email"] = list(set(email for email in filtered_url_df["email"]))
        out_url_arr.append(out_url_dict)
    print(out_url_arr)
    output_df = pd.DataFrame(out_url_arr)
    return output_df


st.set_page_config(layout="wide", page_title="Readership", page_icon="assets/QuixoteLogoVertical.ico")

st.title("Readership Analytics Dashboard")

try:
    uploaded_file = st.file_uploader("Choose a Sendgrid CSV File", type="csv")
except Exception as e:
    uploaded_file = None
    st.write(f"Something went wrong while file upload. Exited with Exception {e}")

try:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.header("Summary")
        st.markdown("""<hr
        style = "height: 2px;
        border: none;
        color: gray;
        background-color: gray;
        margin-top: 0;"
        /> """, unsafe_allow_html=True)

        readership_container = st.container(border=True)
        readership_container.subheader("Click Analytics")
        readership_container_columns = readership_container.columns([2, 1])
        url_df = clicks_aggregator(df)

        with readership_container_columns[0]:
            st.write(url_df.sort_values(by=["click_count"],
                                        ascending=False,
                                        ignore_index=True).dropna())
        with readership_container_columns[1]:
            st.write(url_df.sort_values(by=["click_count"],
                                        ascending=False,
                                        ignore_index=True).dropna().describe())

        top_articles_container = st.container(border=True)
        top_articles_container.subheader("Article Readership")

        urls_list = [str(url) for url in url_df["transition_url"]]
        print(urls_list)

        all_redirect_urls = check_urls_concurrently(urls_list)
        url_df.insert(1, "redirect_url", all_redirect_urls, True)
        top_articles_container.write(url_df.sort_values(by=["click_count"],
                                                        ascending=False,
                                                        ignore_index=True).dropna())

        sorted_url_df = url_df.sort_values(by=["click_count"],
                                           ascending=False,
                                           ignore_index=True).dropna()

        unique_redirect_urls = sorted_url_df["redirect_url"].unique().tolist()
        final_list = []
        grouped_by_redirect_urls = sorted_url_df.groupby("redirect_url").agg(
            {"click_count": "sum"}
        ).reset_index()
        top_articles_container.markdown("**Top Articles Read**")
        top_articles_container.write(grouped_by_redirect_urls.sort_values(by=["click_count"],
                                                                          ascending=False,
                                                                          ignore_index=True).dropna())
        top_articles_container.write(grouped_by_redirect_urls.sort_values(by=["click_count"],
                                                                          ascending=False,
                                                                          ignore_index=True).dropna().sum())
        top_articles_container.bar_chart(grouped_by_redirect_urls,
                                         x="redirect_url",
                                         y="click_count",
                                         x_label="Article",
                                         y_label="Clicks")

        all_clicks_df = df[df["event"] == "click"]
        all_emails = df["email"].tolist()
        all_emails = list(set(all_emails))
        out_arr = []
        total_clicks = 0
        for email in all_emails:
            out_dict = {}
            out_dict["email"] = email
            out_dict["total_clicks"] = int(len(all_clicks_df[all_clicks_df["email"] == email]))
            total_clicks += out_dict["total_clicks"]
            out_arr.append(out_dict)

        print(out_arr)
        print(total_clicks)
        st.write(pd.DataFrame(out_arr).sort_values(by=["total_clicks"],
                                                   ascending=False,
                                                   ignore_index=True))


except Exception as e:
    print(f"Exited with Exception {e}")
    st.write(f"Something wrong with the CSV file. "
             f"Are you sure you uploaded the right CSV file?")
