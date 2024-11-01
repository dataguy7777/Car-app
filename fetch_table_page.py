import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_html_content(url):
    """
    Fetches the HTML content from the specified URL.

    Args:
        url (str): The URL of the web page to fetch the HTML content from.

    Returns:
        str: The HTML content of the page if successful, None otherwise.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        st.info("HTML content fetched successfully.")
        return response.text
    except requests.RequestException as e:
        st.error(f"Error fetching HTML content: {e}")
        return None

def parse_table_from_html(html_content):
    """
    Parses the first HTML table from the page content and converts it into a DataFrame.

    Args:
        html_content (str): The HTML content of the page.

    Returns:
        pd.DataFrame: A DataFrame containing the table data if available, None otherwise.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')  # Finds the first table on the page
    if not table:
        st.warning("No table found on the page.")
        return None
    
    # Extract table headers
    headers = [header.text.strip() for header in table.find_all('th')]
    
    # Extract table rows
    rows = []
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if columns:
            row_data = [column.text.strip() for column in columns]
            rows.append(row_data)
    
    # Create DataFrame from table data
    if rows:
        df = pd.DataFrame(rows, columns=headers)
        st.success("Table parsed successfully.")
        return df
    else:
        st.warning("Table has no data.")
        return None

def show_page():
    st.title("Fetch Table from URL")
    
    url = st.text_input("Enter the URL to scrape:", "https://www.alvolante.it/listino_auto/nissan-x-trail")
    if st.button("Fetch and Parse Table"):
        html_content = fetch_html_content(url)
        if html_content:
            table_df = parse_table_from_html(html_content)
            if table_df is not None:
                st.write("Extracted Table Data:")
                st.dataframe(table_df)