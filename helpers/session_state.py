import os

import streamlit as st

from helpers.css_styles import app_styling_css
from helpers.db_connection import SnowflakeSingleton
from helpers.variables import Variables


def initialize_session():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "page_1"

    if 'dataset_current_page' not in st.session_state:
        st.session_state.dataset_current_page = "page_1"

    if 'dataset_form_data' not in st.session_state:
        st.session_state.dataset_form_data = {}

    if 'dataset_rule_partitions' not in st.session_state:
        st.session_state.dataset_rule_partitions = []

    if 'dataset_dependencies' not in st.session_state:
        st.session_state.dataset_dependencies = []

    # if Variables.snowflake_conn is None:
    #     snowflake_instance = SnowflakeSingleton()
    #
    #     # Connect to Snowflake
    #     Variables.snowflake_conn = snowflake_instance.connect(
    #         user=os.getenv("SNOWFLAKE_USER"),
    #         password=os.getenv("SNOWFLAKE_PASSWORD"),
    #         account=os.getenv("SNOWFLAKE_ACCOUNT"),
    #         database=os.getenv("SNOWFLAKE_DATABASE"),
    #         schema=os.getenv("SNOWFLAKE_SCHEMA"),
    #         warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    #         role=os.getenv("SNOWFLAKE_ROLE"),
    #     )


