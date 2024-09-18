import pandas as pd


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
