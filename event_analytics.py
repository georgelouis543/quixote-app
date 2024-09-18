import pandas as pd
from pandas.core.groupby import DataFrameGroupBy
import json


def event_analytics_aggregator(input_df):
    try:
        df = input_df
        grouped = df.groupby('unique_args')
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
