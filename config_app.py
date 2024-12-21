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

    rules = st.Page("pages/1_rules.py", title=" Rules", icon=":material/house:")
    datasets = st.Page("pages/2_dataset_configs.py", title=" Dataset Configs", icon=":material/arrow_forward:")

    pg = st.navigation([rules,datasets])
    pg.run()