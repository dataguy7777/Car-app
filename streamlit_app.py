import streamlit as st
from pages import fetch_table_page  # Import the standalone page module

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Fetch Table from URL", "Other Page"])

    if page == "Fetch Table from URL":
        fetch_table_page.show_page()  # Display the fetch table page
    elif page == "Other Page":
        st.write("This could be another page.")

if __name__ == "__main__":
    main()