import streamlit as st
import pandas as pd
from datetime import datetime
import traceback

from helpers.variables import Variables


def add_modify_dataset():
    # st.markdown("#### This page is not yet Ready. ####")
    st.markdown("#### Add/Modify Dataset Configs ####")
    with st.expander("**Dataset**", expanded=True):
        st.markdown("")
        try:
            provider_options = list(Variables.provider_names.keys())
            source_connection = ["S3_ID_CONN"]
            domain_options = list(Variables.domains.keys())
            target_connection = ["SNOWFLAKE"]


            st.session_state.dataset_form_data["rule_names"] = list(Variables.rule_names.keys())
            st.session_state.dataset_form_data["partition_names"] = list(Variables.rule_partitions.keys())


            col1, col2, col3, col4,col5,col6 = st.columns([0.25, 3, 2.5,2.5,1, 0.25])

            with col2:
                st.session_state.dataset_form_data['dataset_name'] = st.text_input("Dataset Name",
                                                                    st.session_state.dataset_form_data.get('dataset_name'))

            if st.session_state.dataset_form_data['dataset_name'] in [" ", None, ""]:
                st.error("Please enter Dataset Name")

            col1, col2, col3, col4, col5, col6 = st.columns([0.15, 1.5, 1.5, 1.5, 1, 0.15])

            with col2:
                default_domain_index = domain_options.index("MKT") if "MKT" in domain_options else 0
                st.session_state.dataset_form_data["domain_name"] = st.selectbox("Domain", domain_options,
                                                                                 index=domain_options.index(
                                                                                     st.session_state.dataset_form_data[
                                                                                         "domain_name"]) if st.session_state.dataset_form_data.get(
                                                                                     "domain_name") in domain_options else default_domain_index)

                st.session_state.dataset_form_data["dataset_source_conn"] = source_connection[0]
                # st.session_state.dataset_form_data["dataset_source_conn"] = st.selectbox("Dataset Source",
                #                                                                          source_connection,
                #                                                                          index=source_connection.index(
                #                                                                              st.session_state.dataset_form_data[
                #                                                                                  "dataset_source_conn"]) if st.session_state.dataset_form_data.get(
                #                                                                              "dataset_source_conn") in source_connection else 0)

                st.session_state.dataset_form_data['dag_start_date'] = datetime.today().strftime('%Y-%m-%d')
                # st.session_state.dataset_form_data['dag_start_date'] = st.date_input(
                #     "Dataset Start Date",
                #     value=st.session_state.dataset_form_data.get('dag_start_date', datetime.today())
                # )

                st.session_state.dataset_form_data['schedule_interval'] = st.text_input(
                    "Schedule Interval*",
                    value=st.session_state.dataset_form_data.get('schedule_interval', '30 15,17,19,20 * * 1-5')
                )

                st.markdown(" ")
                st.markdown("**Optional Pipeline Tasks**")
                col_1, col_2, col_3 = st.columns([0.5,3,0.5])
                with col_2:
                    st.session_state.dataset_form_data["pipeline_task_2"] = st.checkbox(
                        'Load Standard',
                        value=st.session_state.dataset_form_data.get("pipeline_task_2", True)
                    )
                    st.session_state.dataset_form_data["pipeline_task_1"] = st.checkbox(
                        'Check Parent DAG Execution Date',
                        value=st.session_state.dataset_form_data.get("pipeline_task_1", True)
                    )

            with col3:
                default_provider_index = provider_options.index("ALDN-EDP-AMALG") if "ALDN-EDP-AMALG" in provider_options else 0
                st.session_state.dataset_form_data["provider_name"] = st.selectbox("Provider", provider_options,
                                                                                   index=provider_options.index(
                                                                                       st.session_state.dataset_form_data[
                                                                                           "provider_name"]) if st.session_state.dataset_form_data.get(
                                                                                       "provider_name") in provider_options else default_provider_index)

                st.session_state.dataset_form_data["dataset_target_conn"] = target_connection[0]
                # st.session_state.dataset_form_data["dataset_target_conn"] = st.selectbox("Dataset Target",
                #                                                                          target_connection,
                #                                                                          index=target_connection.index(
                #                                                                              st.session_state.dataset_form_data[
                #                                                                                  "dataset_target_conn"]) if st.session_state.dataset_form_data.get(
                #                                                                              "dataset_target_conn") in target_connection else 0)
                st.markdown("")
                st.markdown("")
                st.session_state.dataset_form_data["dataset_active"] = st.checkbox(
                    'Active',
                    value=st.session_state.dataset_form_data.get("dataset_active", True)
                )


        except Exception as ex:
            st.error(f"Error occurred: {ex.__str__()}")

    with st.expander("**Schedule Interval Examples**", expanded=False):
        st.markdown("""
                Enter a schedule interval using a cron-like expression. For example:
                - 0 * * * * (Every Hour)
                - 0 0 * * * (Every day at 12:00 AM)
                - 30 20 * * 1-5 (At 08:30 PM, Monday through Friday)  
                - 30 20 10 * * (At 08:30 PM, on day 10 of the month) 
                """)
        st.markdown("For more examples, visit (https://crontab.guru/ or https://crontab.cronhub.io/)")

    # st.write(st.session_state.dataset_rule_partitions)
    # st.write(st.session_state.dataset_dependencies)
    # st.write(st.session_state.dataset_form_data)