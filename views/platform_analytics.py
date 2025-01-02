# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import io
# import json
#
#
# def get_all_analytics(nl_id, auth_token):
#     nl_id = nl_id
#     auth_token = auth_token
#     url = f"https://nl-bff.newsletters.meltwater.io/newsletter/{nl_id}/distributions"
#
#     payload = ""
#     headers = {
#         "accept": "*/*",
#         "accept-language": "en-US,en;q=0.9",
#         "authorization": auth_token,
#         "content-type": "application/json",
#         "origin": "https://app.meltwater.com",
#         "priority": "u=1, i",
#         "referer": "https://app.meltwater.com/",
#         "sec-ch-ua": f'"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
#         "sec-ch-ua-mobile": "?0",
#         "sec-ch-ua-platform": "macOS",
#         "sec-fetch-dest": "empty",
#         "sec-fetch-mode": "cors",
#         "sec-fetch-site": "cross-site",
#         "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
#     }
#
#     response = requests.request("GET", url, data=payload, headers=headers)
#     print(response.text)
#     if response.status_code <= 400:
#
#         response_json = json.loads(response.text)
#         # print(response_json)
#         temp_arr = []
#
#         # print(response_json["distributions"])
#         dist_dict_array = []
#         for dist in response_json["distributions"]:
#             dist_dict = {"_id": dist["_id"], "scheduledDate": dist.get("scheduleDate")}
#             dist_dict_array.append(dist_dict)
#         # for dist in response_json["distributions"]:
#         #     print(dist["_id"])
#         print(dist_dict_array)
#         # nl_id = "660d52093948ca7fcd000006"
#
#         # analytics_url = "https://nl-api.newsletters.meltwater.io/analytics/get/recipients/672cdee89428ac76b2000001"
#         querystring = {"page": "0", "size": "25", "sortField": "emailAddress", "sortOrder": "desc"}
#         # temp_dict = {}
#         # total_opened = 0
#         # total_clicked = 0
#         # total_bounced = 0
#         # total_blocked = 0
#         # total_delivered = 0
#
#         final_array = []
#
#         for dist in dist_dict_array:
#             temp_dict = {}
#             total_opened = 0
#             total_clicked = 0
#             total_bounced = 0
#             total_blocked = 0
#             total_delivered = 0
#             analytics_url = f"https://nl-api.newsletters.meltwater.io/analytics/get/recipients/{dist['_id']}"
#             response_1 = requests.request(
#                 "GET",
#                 analytics_url,
#                 data=payload,
#                 headers=headers,
#                 params=querystring
#             )
#             temp_dict["distribution_id"] = dist["_id"]
#             temp_dict["scheduled_date"] = dist["scheduledDate"]
#             response_1_json = json.loads(response_1.text)
#             print(response_1_json["total"])
#             response_2 = requests.request(
#                 "GET",
#                 analytics_url,
#                 data=payload,
#                 headers=headers,
#                 params={"page": "0", "size": response_1_json["total"], "sortField": "emailAddress", "sortOrder": "desc"}
#             )
#             response_2_json = json.loads(response_2.text)
#             print(response_2_json["recipients"])
#             response_2_json_recipients = response_2_json["recipients"]
#             for recipient in response_2_json_recipients:
#                 total_opened += recipient["opened"]
#                 total_clicked += recipient["clicked"]
#                 total_bounced += recipient["bounced"]
#                 total_blocked += recipient["blocked"]
#                 total_delivered += recipient["delivered"]
#
#             temp_dict["total_opened"] = total_opened
#             temp_dict["total_clicked"] = total_clicked
#             temp_dict["total_bounced"] = total_bounced
#             temp_dict["total_blocked"] = total_blocked
#             temp_dict["total_delivered"] = total_delivered
#
#             final_array.append(temp_dict)
#
#         print(pd.DataFrame(final_array))
#
#         out_df = pd.DataFrame(final_array)
#         return out_df
#
#
# st.title("Export all distributions' Analytics from Platform")
#
# with st.form("Preview your Newsfeed"):
#     token = st.text_input("Enter Token")
#     newsletter_id = st.text_input("Enter Newsletter ID")
#     form_cols = st.columns(10)
#     with form_cols[0]:
#         submit = st.form_submit_button("Get Analytics")
#     with form_cols[1]:
#         clear = st.form_submit_button("Clear")
#
#     if submit and token and newsletter_id:
#         with st.spinner("Fetching analytics..."):
#             analytics_data = get_all_analytics(newsletter_id, token)
#             if not analytics_data.empty:
#                 st.success("Analytics fetched successfully!")
#                 st.write(analytics_data)
#                 # csv_buffer = io.StringIO()
#                 # analytics_data.to_csv(csv_buffer, index=False)
#                 # st.download_button(
#                 #     label="Download CSV",
#                 #     data=csv_buffer.getvalue(),
#                 #     file_name="analytics_data.csv",
#                 #     mime="text/csv",
#                 # )
#             else:
#                 st.warning("No data found for the given Newsletter ID.")


import streamlit as st
import requests
import pandas as pd
import json
from concurrent.futures import ThreadPoolExecutor
import io


# # Using concurrency for parallel execution of API requests (New Version)
# def fetch_distribution_data(dist, headers):
#     """
#     Fetch analytics for a single distribution.
#     """
#     dist_id = dist["_id"]
#     scheduled_date = dist.get("scheduleDate", None)
#     analytics_url = f"https://nl-api.newsletters.meltwater.io/analytics/get/recipients/{dist_id}"
#
#     try:
#         # Fetch total recipients
#         response_1 = requests.get(analytics_url, headers=headers, params={"page": "0", "size": "25"})
#         response_1.raise_for_status()
#         total_recipients = response_1.json()["total"]
#
#         # Fetch detailed data
#         response_2 = requests.get(
#             analytics_url,
#             headers=headers,
#             params={"page": "0", "size": total_recipients}
#         )
#         response_2.raise_for_status()
#         recipients = response_2.json()["recipients"]
#
#         # Aggregate metrics
#         metrics = {
#             "distribution_id": dist_id,
#             "scheduled_date": scheduled_date,
#             "total_opened": sum(r["opened"] for r in recipients),
#             "total_clicked": sum(r["clicked"] for r in recipients),
#             "total_bounced": sum(r["bounced"] for r in recipients),
#             "total_blocked": sum(r["blocked"] for r in recipients),
#             "total_delivered": sum(r["delivered"] for r in recipients),
#         }
#         return metrics
#
#     except requests.RequestException as e:
#         return {"distribution_id": dist_id, "scheduled_date": scheduled_date, "error": str(e)}
#
#
# def get_all_analytics(nl_id, auth_token):
#     """
#     Fetch analytics for all distributions in parallel.
#     """
#     headers = {
#         "accept": "*/*",
#         "authorization": auth_token,
#         "content-type": "application/json",
#         "user-agent": "Mozilla/5.0"
#     }
#
#     url = f"https://nl-bff.newsletters.meltwater.io/newsletter/{nl_id}/distributions"  #version
#     # url = f"https://app.meltwater.com/api/newsletters/newsletter/distribution/{nl_id}/distributions"  #legacy
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         distributions = response.json().get("distributions", [])
#
#         # Fetch data in parallel
#         final_data = []
#         with ThreadPoolExecutor(max_workers=40) as executor:
#             results = executor.map(lambda dist: fetch_distribution_data(dist, headers), distributions)
#             final_data.extend(results)
#
#         return pd.DataFrame(final_data)
#
#     except requests.RequestException as e:
#         st.error(f"Error fetching distributions: {e}")
#         return pd.DataFrame()
#
#
# st.title("Export Newsletter Analytics")
#
# with st.form("analytics_form"):
#     token = st.text_input("Enter Token")
#     newsletter_id = st.text_input("Enter Newsletter ID")
#     form_cols = st.columns([1, 1])
#     submit = form_cols[0].form_submit_button("Get Analytics")
#     clear = form_cols[1].form_submit_button("Clear")
#
#     if submit and token and newsletter_id:
#         with st.spinner("Fetching analytics..."):
#             analytics_data = get_all_analytics(newsletter_id, token)
#             if not analytics_data.empty:
#                 st.success("Analytics fetched successfully!")
#                 st.write(analytics_data)
#                 # csv_buffer = io.StringIO()
#                 # analytics_data.to_csv(csv_buffer, index=False)
#                 # st.download_button(
#                 #     label="Download CSV",
#                 #     data=csv_buffer.getvalue(),
#                 #     file_name="analytics_data.csv",
#                 #     mime="text/csv",
#                 # )
#             else:
#                 st.warning("No data found for the given Newsletter ID.")


# Using concurrency for parallel execution of API requests (Legacy Version)
def fetch_distribution_data(dist, headers):
    """
    Fetch analytics for a single distribution.
    """
    print(dist)
    dist_id = dist["_id"]
    scheduled_date = dist.get("scheduledDate", None)
    status = dist.get("status", None)
    subject = dist.get("newsletterSubject", None)
    analytics_url = f"https://nl-api.newsletters.meltwater.io/analytics/get/recipients/{dist_id}"

    try:
        # Fetch total recipients
        response_1 = requests.get(analytics_url, headers=headers, params={"page": "0", "size": "25"})
        response_1.raise_for_status()
        total_recipients = response_1.json()["total"]

        # Fetch detailed data
        response_2 = requests.get(
            analytics_url,
            headers=headers,
            params={"page": "0", "size": total_recipients}
        )
        response_2.raise_for_status()
        recipients = response_2.json()["recipients"]

        # Aggregate metrics
        metrics = {
            "distribution_id": dist_id,
            "subject": subject,
            "scheduled_date": scheduled_date,
            "status": status,
            "total_opened": sum(r["opened"] for r in recipients),
            "total_clicked": sum(r["clicked"] for r in recipients),
            "total_bounced": sum(r["bounced"] for r in recipients),
            "total_blocked": sum(r["blocked"] for r in recipients),
            "total_delivered": sum(r["delivered"] for r in recipients),
        }
        return metrics

    except requests.RequestException as e:
        return {"distribution_id": dist_id, "scheduled_date": scheduled_date, "error": str(e)}


def get_all_analytics(nl_id, auth_token):
    """
    Fetch analytics for all distributions in parallel.
    """
    headers = {
        "accept": "*/*",
        "authorization": auth_token,
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0"
    }

    # url = f"https://nl-bff.newsletters.meltwater.io/newsletter/{nl_id}/distributions"  #version
    url = f"https://app.meltwater.com/api/newsletters/newsletter/distribution/{nl_id}/distributions"  #legacy
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        # print(response.content)
        distributions = response.json()

        # Fetch data in parallel
        final_data = []
        with ThreadPoolExecutor(max_workers=40) as executor:
            results = executor.map(lambda dist: fetch_distribution_data(dist, headers), distributions)
            final_data.extend(results)

        return pd.DataFrame(final_data)

    except requests.RequestException as e:
        st.error(f"Error fetching distributions: {e}")
        return pd.DataFrame()


st.title("Export Newsletter Analytics")

with st.form("analytics_form"):
    token = st.text_input("Enter Token")
    newsletter_id = st.text_input("Enter Newsletter ID")
    form_cols = st.columns([1, 1])
    submit = form_cols[0].form_submit_button("Get Analytics")
    clear = form_cols[1].form_submit_button("Clear")

    if submit and token and newsletter_id:
        with st.spinner("Fetching analytics..."):
            analytics_data = get_all_analytics(newsletter_id, token)
            if not analytics_data.empty:
                st.success("Analytics fetched successfully!")
                st.write(analytics_data)
                # csv_buffer = io.StringIO()
                # analytics_data.to_csv(csv_buffer, index=False)
                # st.download_button(
                #     label="Download CSV",
                #     data=csv_buffer.getvalue(),
                #     file_name="analytics_data.csv",
                #     mime="text/csv",
                # )
                analytics_data_df = pd.DataFrame(analytics_data)
                st.write(analytics_data_df.describe())
            else:
                st.warning("No data found for the given Newsletter ID.")
