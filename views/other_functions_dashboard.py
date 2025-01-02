import streamlit as st
import pandas as pd
import json

st.title("Filter your data and Export")

try:
    uploaded_file = st.file_uploader("Choose a Sendgrid CSV File", type="csv")
except Exception as e:
    uploaded_file = None
    st.write(f"Something went wrong while file upload. Exited with Exception {e}")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Filter Data")
    columns = df.columns.tolist()

    selected_column = st.selectbox("Select column to filter by", columns)
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("Select a value", unique_values)

    filtered_dataframe = df[df[selected_column] == selected_value]
    st.write(filtered_dataframe)

    grouped_df_by_args = df.groupby("unique_args")
    unique_args_as_list = df["unique_args"].unique()
    all_newsletter_ids = []

    for unique_arg in unique_args_as_list:
        arg = json.loads(unique_arg)
        newsletter_id = arg["newsletterId"]
        all_newsletter_ids.append(newsletter_id)

    all_newsletter_ids = list(set(all_newsletter_ids))
    print(all_newsletter_ids)

    # Assuming 'unique_args' column contains JSON strings, you need to apply json.loads first
    df['parsed_unique_args'] = df['unique_args'].apply(lambda x: json.loads(x))

    # Now filter based on the 'newsletterId'
    filtered_df_1 = df[df['parsed_unique_args'].apply(
        lambda x: str(all_newsletter_ids[0]) == str(x.get('newsletterId')
                                                    ))]
    st.write(filtered_df_1)

    filtered_df_1["distribution_id"] = filtered_df_1['parsed_unique_args'].apply(
        lambda x: x.get('distributionId')
    )

    # filtered_df_1['subject'] = filtered_df_1.groupby('distribution_id')['subject'].transform('first')
    # filtered_df_1['subject'] = filtered_df_1.groupby('unique_args')['subject'].transform(
    #     lambda x: x.ffill().bfill())

    st.write(filtered_df_1)
    filtered_df_1['from'] = "newsletters@meltwater.com"
    cols_to_keep = ["event", "subject", "from", "email", "parsed_unique_args", "distribution_id"]

    filtered_df_1 = filtered_df_1[cols_to_keep]

    st.write(filtered_df_1)
