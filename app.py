import streamlit as st
import pandas as pd
from parse_form import get_data


def run():

    uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False)

    if uploaded_file is not None:
        extension = uploaded_file.name.split('.')[-1]

        if extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif extension == 'xlsx':
            df = pd.read_excel(uploaded_file)
        else:
            return

        # st.write(df)
        # st.dataframe(df)

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            with st.spinner('Анализ данных...'):
                zip_data = get_data(df)

            st.success('Анализ данных завершен')
            btn = st.download_button(
                label="Download ZIP",
                data=zip_data,
                file_name="data.zip",
                mime="application/zip"
            )


if __name__ == '__main__':
    run()
