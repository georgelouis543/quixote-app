import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.units import inch

from concurrent.futures import ThreadPoolExecutor
import httpx
import io
from io import BytesIO


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


# Function to create the PDF report using ReportLab
def create_pdf_report(top_articles_df, top_email_df):
    buffer = BytesIO()

    # Define margins
    margin_left = 50
    margin_right = 50
    margin_top = 50
    margin_bottom = 50

    # Create PDF document with custom margins
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=margin_right,
                            leftMargin=margin_left,
                            topMargin=margin_top,
                            bottomMargin=margin_bottom)

    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    header_style = styles['Heading2']
    normal_style = styles['BodyText']
    wrap_style = ParagraphStyle(
        name='WrapStyle',
        fontSize=10,
        leading=12,
        alignment=1,  # Align center
        wordWrap='CJK'  # Wrap text for CJK languages; useful for general text wrapping as well
    )

    # Content
    content = []

    # Title
    content.append(Paragraph("Analytics Report", title_style))
    content.append(Paragraph("<br/><br/>", normal_style))  # Add space

    # Top 10 Articles
    content.append(Paragraph("Top 10 Articles", header_style))
    content.append(Paragraph("<br/>", normal_style))  # Add space

    # Prepare data for Top 10 Articles
    article_data = [["Redirect URL", "Click Count"]] + [
        [Paragraph(f"<para>{url}</para>", wrap_style), count]
        for url, count in top_articles_df[["redirect_url", "click_count"]].values.tolist()
    ]
    article_table = Table(article_data, colWidths=[4 * inch, 1 * inch], hAlign='LEFT')  # Adjust column widths as necessary

    article_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#d0d0d0'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),  # Align header text left
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),  # Align data text left
        ('VALIGN', (0, 1), (-1, -1), 'TOP'),  # Align data text to top
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
        ('BACKGROUND', (0, 1), (-1, -1), '#f5f5f5'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONT', (0, 1), (-1, -1), 'Helvetica'),
        ('TEXTCOLOR', (0, 1), (-1, -1), '#000000'),
    ]))

    content.append(article_table)
    content.append(Paragraph("<br/>", normal_style))  # Add space

    # Top Email Contributors
    content.append(Paragraph("Top Email Contributors", header_style))
    content.append(Paragraph("<br/>", normal_style))  # Add space

    # Table for Top Email Contributors
    email_data = [["Email", "Total Clicks"]] + top_email_df[["email", "total_clicks"]].values.tolist()
    email_table = Table(email_data, colWidths=[4 * inch, 1 * inch], hAlign='LEFT')  # Adjust column widths as necessary
    email_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#d0d0d0'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),  # Align header text left
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),  # Align data text left
        ('VALIGN', (0, 1), (-1, -1), 'TOP'),  # Align data text to top
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
        ('BACKGROUND', (0, 1), (-1, -1), '#f5f5f5'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONT', (0, 1), (-1, -1), 'Helvetica'),
        ('TEXTCOLOR', (0, 1), (-1, -1), '#000000'),
    ]))

    content.append(email_table)

    # Build PDF
    doc.build(content)
    buffer.seek(0)
    return buffer.getvalue()


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

        email_clicks_df = pd.DataFrame(out_arr).sort_values(by=["total_clicks"],
                                                            ascending=False,
                                                            ignore_index=True)

        # Creating an Excel file with multiple sheets
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            url_df.to_excel(writer, sheet_name='Click Analytics', index=False)
            grouped_by_redirect_urls.to_excel(writer, sheet_name='Article Readership', index=False)
            email_clicks_df.to_excel(writer, sheet_name='Total Clicks by Email', index=False)

        # Seek to the beginning of the stream
        excel_buffer.seek(0)

        # Download button
        st.download_button(
            label="Download EXCEL Report",
            data=excel_buffer,
            file_name="analytics_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Create a PDF report
        pdf_bytes = create_pdf_report(grouped_by_redirect_urls.head(10), email_clicks_df)

        # Download button
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name="analytics_report.pdf",
            mime="application/pdf"
        )


except Exception as e:
    print(f"Exited with Exception {e}")
    st.write(f"Something wrong with the CSV file. "
             f"Are you sure you uploaded the right CSV file?")
