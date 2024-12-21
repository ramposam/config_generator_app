import streamlit as st

from dataset_pages.dataset_page_1 import page_1
from dataset_pages.generate_configs import  GenerateConfigs
from helpers.utils import dummy
from pandas import DataFrame
from helpers.variables import Variables


def generate_configs(form_data, dataset_rule_partitions, dataset_dependencies):
    dummy()


# Function to navigate to the next page
def next_page(df: DataFrame = None):
    df_not_empty = False if df is None else True
    if st.session_state.dataset_current_page == 'page_1':
        st.session_state.dataset_current_page = 'page_2'


# Function to navigate to the previous page
def prev_page():
    if st.session_state.dataset_current_page == 'page_2':
        st.session_state.dataset_current_page = 'page_1'


def switch_dataset_pages(generate_standard_configs=None):
    # Page 1
    page_1()
    col1, col2, col3 = st.columns([3, 6, 3])

    with col3:
        dataset_configs = st.button("Generate Configs", key="dataset_configs_generate",use_container_width=True)

    if dataset_configs:
        GenerateConfigs(st.session_state.dataset_form_data).generate()
