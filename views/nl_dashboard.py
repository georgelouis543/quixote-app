import streamlit as st
import pandas as pd
import plotly.express as px
from pandas.core.groupby import DataFrameGroupBy
import json
import httpx
import io
from io import BytesIO

st.set_page_config(layout="wide", page_title="Export NL analytics", page_icon="assets/QuixoteLogoVertical.ico")

st.title('Newsletter Analytics Dashboard')


def check_final_url(url):
    try:
        with httpx.Client(follow_redirects=True) as client:
            response = client.get(url)
            return response.url
    except Exception as e:
        print(f"Exited with Exception {e}")
        return None


@st.cache_data
def email_analytics_aggregator(input_df):
    try:
        df = input_df
        grouped_by_email = df.groupby('email')
        out_arr = []
        for email, group in grouped_by_email:
            out_dict1 = {}
            # print(email)
            out_dict1["Email"] = str(email)
            group_by_event = group.groupby('event')

            for event, sub_group_by_event in group_by_event:
                # print(event)
                # print(len(sub_group_by_event))
                out_dict1[str(event)] = int(len(sub_group_by_event))

            out_arr.append(out_dict1)

        # Convert the list of dictionaries to a DataFrame
        df_out = pd.DataFrame(out_arr)

        # Replace NaN values with 0
        df_out = df_out.fillna(0)
        return df_out

    except Exception as e:
        print(f"Exited with Exception {e}")
        return None


@st.cache_data
def event_analytics_aggregator(input_df):
    try:
        input_df = input_df
        grouped = input_df.groupby('unique_args')
        print(grouped)
        out_arr = []

        for unique_arg, group in grouped:
            total_processed_counter = int(0)
            total_delivered_counter = int(0)
            total_deferred_counter = int(0)
            total_bounced_counter = int(0)
            total_blocked_counter = int(0)
            total_open_counter = int(0)
            total_click_counter = int(0)
            out_dict1 = {}
            subject_value = group['subject'].iloc[0]
            print(subject_value)
            print(unique_arg)
            dict_unique_arg = json.loads(unique_arg)
            out_dict1["Subject"] = subject_value
            out_dict1["Newsletter_ID"] = dict_unique_arg["newsletterId"]
            out_dict1["Distribution_ID"] = dict_unique_arg["distributionId"]
            out_dict1["Date"] = group.iloc[0]["processed"]
            print(dict_unique_arg)
            # print(group)
            groupby_event: DataFrameGroupBy = group.groupby('event')

            for event, subgroup in groupby_event:
                print(event)
                print(subgroup)
                subgroup_count = len(subgroup)
                print(subgroup_count)

                if str(event) == 'processed':
                    total_processed_counter = len(subgroup)
                    print(event)

                elif str(event) == 'delivered':
                    total_delivered_counter = len(subgroup)
                    print("yes")

                elif str(event) == 'open':
                    total_open_counter = len(subgroup)

                elif str(event) == 'click':
                    total_click_counter = len(subgroup)

                elif str(event) == 'deferred':
                    total_deferred_counter = len(subgroup)
                    print(event)

                elif str(event) == 'bounce':
                    total_bounced_counter = len(subgroup)

            out_dict1["Total_Processed"] = total_processed_counter
            out_dict1["Total_Delivered"] = total_delivered_counter
            out_dict1["Total_Opened"] = total_open_counter
            out_dict1["Total_Clicked"] = total_click_counter
            out_dict1["Total_Deferred"] = total_deferred_counter
            out_dict1["Total_Bounced"] = total_bounced_counter
            out_arr.append(out_dict1)

        out_df = pd.DataFrame(out_arr)
        return out_df

    except Exception as e:
        print(f"Exited with Exception {e}")
        return None


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

        nl_count_columns = st.columns(2)
        all_distributions_sent = df["unique_args"].unique()
        count_all_distributions_sent = len(all_distributions_sent)
        all_nls = []
        for dist in all_distributions_sent:
            unique_info = json.loads(dist)
            all_nls.append(unique_info["newsletterId"])
        print(len(all_nls))
        all_nls = list(set(all_nls))
        print(len(all_nls))
        count_all_nls_sent = len(all_nls)

        with nl_count_columns[0]:
            container1 = st.container(border=True)
            container1.subheader("**All Newsletters Present**")
            container1.header(count_all_nls_sent)

        with nl_count_columns[1]:
            container2 = st.container(border=True)
            container2.subheader("**All Distributions Sent**")
            container2.header(count_all_distributions_sent)

        overall_analytics_container = st.container(border=True)
        overall_analytics_container.subheader("Overall Analytics by Events")

        col = overall_analytics_container.columns(6)
        overall_numbers_dict = {}
        average_numbers_dict = {}
        overall_numbers_dict["Figures"] = "Sum"
        average_numbers_dict["Figures"] = "Average"

        total_clicks = len(df[df["event"] == "click"])
        avg_clicks = round(total_clicks / 30, 2)
        overall_numbers_dict["clicks"] = total_clicks
        average_numbers_dict["clicks"] = avg_clicks

        total_opens = len(df[df["event"] == "open"])
        avg_opens = round(total_opens / 30, 2)
        overall_numbers_dict["opens"] = total_opens
        average_numbers_dict["opens"] = avg_opens

        total_delivered = len(df[df["event"] == "delivered"])
        avg_delivered = round(total_delivered / 30, 2)
        overall_numbers_dict["delivered"] = total_delivered
        average_numbers_dict["delivered"] = avg_delivered

        total_deferred = len(df[df["event"] == "deferred"])
        avg_deferred = round(total_deferred / 30, 2)
        overall_numbers_dict["deferred"] = total_deferred
        average_numbers_dict["deferred"] = avg_deferred

        total_bounced = len(df[df["event"] == "bounce"])
        avg_bounced = round(total_bounced / 30, 2)
        overall_numbers_dict["bounced"] = total_bounced
        average_numbers_dict["bounced"] = avg_bounced

        total_processed = len(df[df["event"] == "processed"])
        avg_processed = round(total_processed / 30, 2)
        overall_numbers_dict["processed"] = total_processed
        average_numbers_dict["processed"] = avg_processed

        overall_num_arr = []
        overall_num_arr.append(overall_numbers_dict)
        overall_num_arr.append(average_numbers_dict)
        overall_num_df = pd.DataFrame(overall_num_arr)

        click_percentage = round(total_clicks * 100 / total_opens, 2)
        open_percentage = round(total_opens * 100 / total_processed, 2)
        defer_percentage = round(total_deferred * 100 / total_processed, 2)
        bounce_percentage = round(total_bounced * 100 / total_processed, 2)
        delivery_percentage = round(total_delivered * 100 / total_processed, 2)

        with col[0]:
            st.metric(label="Clicks (vs Opens)", value=f"{total_clicks} ({click_percentage}%)")
        with col[1]:
            st.metric(label="Opens", value=f"{total_opens}")
        with col[2]:
            st.metric(label="Deliveries", value=f"{total_delivered} ({delivery_percentage}%)")
        with col[3]:
            st.metric(label="Defers", value=f"{total_deferred} ({defer_percentage}%)")
        with col[4]:
            st.metric(label="Bounces", value=f"{total_bounced} ({bounce_percentage}%)")
        with col[5]:
            st.metric(label="Total Processed", value=total_processed)

        avg_analytics_container = st.container(border=True)
        avg_analytics_container.subheader("Average Figures by Day")
        col1 = avg_analytics_container.columns(6)
        with col1[0]:
            st.metric(label="Clicks", value=avg_clicks)
        with col1[1]:
            st.metric(label="Opens", value=avg_opens)
        with col1[2]:
            st.metric(label="Deliveries", value=avg_delivered)
        with col1[3]:
            st.metric(label="Defers", value=avg_deferred)
        with col1[4]:
            st.metric(label="Bounces", value=avg_bounced)
        with col1[5]:
            st.metric(label="Processed", value=avg_processed)

        email_analytics_container = st.container(border=True)
        email_analytics_container.subheader("Analytics by Email")
        col2 = email_analytics_container.columns(2)
        select_box_column = email_analytics_container.columns(1)
        col3 = email_analytics_container.columns(2)
        email_analytics_df = email_analytics_aggregator(df)

        with col2[0]:
            st.write(email_analytics_df)
        with col2[1]:
            st.write(email_analytics_df.describe())

        with select_box_column[0]:
            event_list_for_email_analytics = [
                "delivered",
                "open",
                "processed",
                "click",
            ]
            event_select_y = st.selectbox("Select Event", event_list_for_email_analytics)

        email_bar_fig = px.bar(
            email_analytics_df,
            x="Email",
            y=event_select_y,
            labels={"Email": "Email", event_select_y: "Event Count"},
            title="Email Analytics Bar Chart",
            color_discrete_sequence=["#27BABB"]
        )

        col3[0].plotly_chart(email_bar_fig, use_container_width=True)

        email_area_fig = px.line(
            email_analytics_df.describe(),  # Using the described DataFrame
            y=event_select_y,  # y-axis will be event_select_y
            labels={event_select_y: "Event Count"},  # Update labels
            title="Email Analytics Area Chart",
            line_shape='linear'  # Keep the lines linear for area chart
        )

        # Fill the area under the line
        email_area_fig.update_traces(fill='tozeroy', line_color='#38795B')

        col3[1].plotly_chart(email_area_fig, use_container_width=True)

        event_analytics_container = st.container(border=True)
        col4 = event_analytics_container.columns(2)
        event_analytics_container.subheader("Event analytics by Distribution")
        event_analytics_df = event_analytics_aggregator(df)

        if event_analytics_df is not None:
            event_analytics_container.write(event_analytics_df)
            event_analytics_container.write(event_analytics_df.describe())
            # event_analytics_container.write(event_analytics_df["Total_Opened"].sum())
            event_analytics_container.markdown("**Analyze Events Trend**")
            event_list = [
                "Total_Clicked",
                "Total_Delivered",
                "Total_Opened",
                "Total_Deferred",
                "Total_Bounced",
                "Total_Processed"
            ]
            event_axis_y = event_analytics_container.selectbox("Select Event to plot", event_list)

            line_fig = px.line(
                event_analytics_df,
                x="Date",
                y=event_axis_y,
                labels={"Date": "Sent Date", event_axis_y: "Event Count"},
                title="Event Analytics Over Time",
                color_discrete_sequence=["#27BABB"]
            )
            event_analytics_container.plotly_chart(line_fig, use_container_width=True)

            bar_fig = px.bar(
                event_analytics_df,
                x="Date",
                y=event_axis_y,
                labels={"Date": "Sent Date", event_axis_y: "Event Count"},  # Update labels
                title="Event Analytics Bar Chart",
                color_discrete_sequence=["#00429d"]
            )
            bar_fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')),
                                  opacity=0.9)
            bar_fig.update_layout(bargap=0.05)
            event_analytics_container.plotly_chart(bar_fig, use_container_width=True)

        readership_container = st.container(border=True)
        readership_container.subheader("Readership Analytics")
        readership_container_columns = readership_container.columns([2, 1])
        url_df = clicks_aggregator(df)
        url_df_sorted = url_df.sort_values(by=["click_count"],
                                           ascending=False,
                                           ignore_index=True).dropna()
        with readership_container_columns[0]:
            st.write(url_df.sort_values(by=["click_count"],
                                        ascending=False,
                                        ignore_index=True).dropna())
        with readership_container_columns[1]:
            st.write(url_df.sort_values(by=["click_count"],
                                        ascending=False,
                                        ignore_index=True).dropna().describe())

        # Creating an Excel file with multiple sheets
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer,
                            engine='openpyxl') as writer:
            email_analytics_df.to_excel(writer,
                                        sheet_name='Email Analytics',
                                        index=False)
            email_analytics_df.describe().to_excel(writer,
                                                   sheet_name='Email Analytics Description',
                                                   index=True)
            event_analytics_df.to_excel(writer,
                                        sheet_name='Event Analytics',
                                        index=False)
            overall_num_df.to_excel(writer,
                                    sheet_name='Overall and Avg',
                                    index=False)
            event_analytics_df.describe().to_excel(writer,
                                                   sheet_name='Event Analytics Description',
                                                   index=True)
            url_df_sorted.to_excel(writer,
                                   sheet_name='Readership',
                                   index=False)

        # Seek to the beginning of the stream
        excel_buffer.seek(0)

        # Download button
        st.download_button(
            label="Download EXCEL Report",
            data=excel_buffer,
            file_name="Overall_analytics_NL_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )



except Exception as e:
    print(f"Exited with Exception {e}")
    st.write(f"Something wrong with the CSV file. "
             f"Are you sure you uploaded the right CSV file?")
