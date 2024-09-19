import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io


@st.cache_data
def parse_newsfeed_rss(newsfeed_url: str):
    try:
        response = requests.get(newsfeed_url, timeout=10)
        xml_response = response.content.decode('utf-8')  # Ensure UTF-8 encoding
        soup = BeautifulSoup(xml_response, 'xml')
        items = soup.find_all('item')
        parsed_data = []

        for item in items:
            image = []
            urls = []
            temp_dict = {}
            try:
                temp_dict["title"] = item.title.get_text()
            except:
                temp_dict["title"] = None
            try:
                temp_dict["description"] = item.description.get_text()
            except:
                temp_dict["description"] = None
            try:
                temp_dict["pubDate"] = item.pubDate.get_text()
            except:
                temp_dict["pubDate"] = None
            try:
                temp_dict["source"] = item.source.get_text()
            except:
                temp_dict["source"] = None
            try:
                source = item.find('source')["url"]
                temp_dict["sourceUrl"] = source
            except:
                temp_dict["sourceUrl"] = None
            try:
                temp_dict["link"] = item.link.get_text()
            except:
                temp_dict["link"] = None
            try:
                sourceId = item.find('tint:sourceId')
                temp_dict["post_id"] = sourceId.get_text()
            except:
                temp_dict["post_id"] = None
            try:
                creator = item.find('dc:creator')
                temp_dict["author"] = creator.get_text()
            except:
                temp_dict["author"] = None
            try:
                author_image = item.find('tint:author-image')
                temp_dict["authorImage"] = author_image.get_text()
            except:
                temp_dict["authorImage"] = None
            try:
                image = item.find_all('media:thumbnail')
                urls = [thumbnail['url'] for thumbnail in image]
                if (image is not None) and (len(image) > 0):
                    temp_dict["image"] = urls[len(urls) - 1]
                else:
                    temp_dict["image"] = "https://www.meltwaternews.com/ext/blr/george/MeltwaterLogoMWFeeds.png"
            except:
                temp_dict["image"] = "https://www.meltwaternews.com/ext/blr/george/MeltwaterLogoMWFeeds.png"

            parsed_data.append(temp_dict)

        return parsed_data

    except Exception as e:
        print(f"Exception {e} occurred")
        return []


st.title("Preview and Export your Newsfeed")

try:
    with st.form("Preview your Newsfeed"):
        rss_url = st.text_input("RSS URL")
        form_cols = st.columns(10)
        with form_cols[0]:
            submit = st.form_submit_button("Preview")
        with form_cols[1]:
            clear = st.form_submit_button("Clear")

    if clear:
        rss_url = ""
        newsfeed_items = []

    if submit:
        # st.write(rss_url)
        newsfeed_items = parse_newsfeed_rss(rss_url)

        if len(newsfeed_items) > 0:
            newsfeed_df = pd.DataFrame(newsfeed_items)

            with st.container(height=500):
                st.subheader(f"Total Articles: {len(newsfeed_items)}")
                st.markdown(f"<hr style='margin: 0; color: black; background-color: black;'/>",
                            unsafe_allow_html=True)
                for item in newsfeed_items:
                    st.markdown(
                        f"""
                        <div style="border: 1px solid #ddd; 
                        padding: 10px; 
                        margin: 10px 0; 
                        border-radius: 5px; 
                        background-color: #fff; display: flex;">
                        <div>
                        <img src={item['image']} style="width: 150px; padding-right: 15px; 
                        margin-top: 12px;"/>
                        </div>
                        <div>
                            <h4>{item['title'] if item['title'] else 'No title available'}</h4>
                            <p><strong>Description:</strong> {item['description'] if item['description']
                        else 'No description available'}</p>
                            <p><strong>Published on:</strong> {item['pubDate'] if item['pubDate'] else
                        'No publication date'}</p>
                            <p><strong>Source:</strong> {item['source'] if item['source'] else
                        'No source available'}</p>
                            <a href="{item['link']}" target="_blank" style="color: blue; 
                            text-decoration: underline;">Read more</a>
                        </div>
                        </div>
                        """, unsafe_allow_html=True
                    )

            excel_buffer = io.BytesIO()

            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                newsfeed_df.to_excel(writer,
                                     sheet_name='Email Analytics',
                                     index=False)

            excel_buffer.seek(0)

            cols = st.columns(8)
            with cols[0]:
                st.download_button(
                    label="Export as Excel",
                    data=excel_buffer,
                    file_name="Newsfeed_Export.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            csv_data = newsfeed_df.to_csv(index=False)
            with cols[1]:
                st.download_button(
                    label="Export as CSV",
                    data=csv_data,
                    file_name="Newsfeed_Export.csv",
                    mime="text/csv"
                )



        else:
            st.write("No items present")

except Exception as e:
    print(f"Exception {e} occurred")
    st.error("Something went wrong. Please try later.")
