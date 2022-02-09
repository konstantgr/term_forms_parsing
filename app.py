import streamlit as st
import pandas as pd
import shutil
import os
from parse_form import get_people_data, get_subjects_data

main_path = os.path.dirname(os.path.realpath(__file__))


def run():
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button('Professors'):
                get_people_data(df)
                shutil.make_archive('myfile', 'zip', os.path.join(main_path, 'people'))

                with open("myfile.zip", "rb") as fp:
                    with col3:
                        btn = st.download_button(
                            label="Download ZIP",
                            data=fp,
                            file_name="professors.zip",
                            mime="application/zip"
                        )

        with col2:
            if st.button('Classes'):
                get_subjects_data(df)
                shutil.make_archive('myfile', 'zip', os.path.join(main_path, 'subjects'))

                with col3:
                    with open("myfile.zip", "rb") as fp:
                        btn = st.download_button(
                            label="Download ZIP",
                            data=fp,
                            file_name="subjects.zip",
                            mime="application/zip"
                        )
                        

if __name__ == '__main__':
    run()
