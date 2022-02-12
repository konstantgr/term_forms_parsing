import streamlit as st
import pandas as pd
import os
from parse_form import get_data

main_path = os.path.dirname(os.path.realpath(__file__))


def run():
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            zip_data = get_data(df)

            btn = st.download_button(
                label="Download ZIP",
                data=zip_data,
                file_name="data.zip",
                mime="application/zip"
            )


if __name__ == '__main__':
    run()
