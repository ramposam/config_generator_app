import streamlit as st
import pandas as pd
import traceback

from dataset_pages.dataset_dependencies import add_dataset_dependencies
from dataset_pages.dataset_helper import add_dataset_rule_partition, add_dependent_dataset
from dataset_pages.dataset_rule_partitions import add_dataset_rule_partitions
from helpers.variables import Variables

def rule_partition_details():
    # st.markdown("#### This page is not yet Ready. ####")
    st.markdown("#### Add/Modify Dataset Configs ####")
    with st.expander("**Dataset Dependency Details**", expanded=True):
        try:
            for index, dependent_dataset in enumerate(sorted(st.session_state.dataset_dependencies,key=lambda x: 100 if x['dataset_order_num'] is None else x['dataset_order_num'])):
                add_dataset_dependencies( index, dependent_dataset)

            col1, col2, col3, col4, col5, col6,col7 = st.columns([2,2,2,2,2,2,2])
            with col1:
                st.button('Add Dataset', on_click=add_dependent_dataset)

            # if len(st.session_state.dataset_dependencies) ==0 :
            #     st.error("At least one Dataset Dependency Details are required")

            st.markdown("")
        except Exception as ex:
            print(traceback.format_exc())
            st.error(ex.__str__())



    with st.expander("**Rule/Partition Details**", expanded=True):
        st.markdown("")
        try:
            for index, partition in enumerate(sorted(st.session_state.dataset_rule_partitions,key=lambda x: 100 if x['partition_order_num'] is None else x['partition_order_num'])):
                add_dataset_rule_partitions( index, partition)

            col1, col2, col3, col4, col5, col6,col7 = st.columns([2,2,2,2,2,2,2])
            with col1:
                st.button('Add Rule / Partition', on_click=add_dataset_rule_partition)

            if len(st.session_state.dataset_rule_partitions) ==0 :
                st.error("At least one Rule/Partition Details are required")

            st.markdown("")
        except Exception as ex:
            print(traceback.format_exc())
            st.error(ex.__str__())