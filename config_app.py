import streamlit as st

from helpers.css_styles import  addon_header_css, app_styling_css
from helpers.session_state import initialize_session
from helpers.utils import inject_css
import os


if __name__ == "__main__":

    inject_css(addon_header_css)
    logo_path = os.path.join(os.getcwd(), "logo.png")
    st.logo(image=logo_path, icon_image=None)
    inject_css(app_styling_css)


    initialize_session()

    datasets = st.Page("app_pages/1_dataset_configs.py", title=" Dataset Configs", icon=":material/arrow_forward:")
    rules = st.Page("app_pages/2_rules.py", title=" Rules", icon=":material/house:")

    pg = st.navigation([datasets,rules])
    pg.run()