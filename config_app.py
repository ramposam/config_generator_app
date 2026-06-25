import streamlit as st

from helpers.css_styles import  addon_header_css, app_styling_css
from helpers.session_state import initialize_session
from helpers.utils import inject_css
import os


if __name__ == "__main__":

    st.set_page_config(
        page_title="Automated ETL Pipeline",
        layout="wide")
    
    st.html(
        """
        <style>
            .stMainBlockContainer {
                max-width: 1200px; /* Adjust this value to your preferred pixel width */
                margin: auto;       /* Optional: Centers the layout on widescreen displays */
            }
        </style>
        """
    )
    inject_css(addon_header_css)
    logo_path = os.path.join(os.getcwd(), "logo.png")
    st.logo(image=logo_path, icon_image=None)
    inject_css(app_styling_css)


    initialize_session()

    datasets = st.Page("app_pages/1_dataset_configs.py", title=" Dataset Configs", icon=":material/arrow_forward:")

    pg = st.navigation([datasets])
    pg.run()