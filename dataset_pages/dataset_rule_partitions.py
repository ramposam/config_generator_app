import traceback

import streamlit as st

from dataset_pages.dataset_helper import get_dataset_rule_partitions, remove_dataset_rule_partitions
from helpers.variables import Variables


def add_dataset_rule_partitions(index,partition):
    try:
        [rule_name,partition_name,primary_keys,src_table,tgt_table,rule_partition_active] =  get_dataset_rule_partitions(index)

        col1, col2, col3, col4, col5, col6 = st.columns([3, 1.5, 3, 3, 0.5,1])

        if len(st.session_state.dataset_rule_partitions)-1==index:
            disable_remove = False
        else:
            disable_remove = True

        rule_names = st.session_state.dataset_form_data["rule_names"]
        partition_names =  st.session_state.dataset_form_data["partition_names"]

        with col1:
            partition["rule_name"] = st.selectbox("Rule Name", key=rule_name,options=rule_names,
                                                                           index=rule_names.index(
                                                                               partition[
                                                                                   "rule_name"]) if partition.get(
                                                                               "rule_name") in rule_names else None)



        if partition["rule_name"] in ["",None," "]:
            st.error("Rule Name is required")

        with col2:
            partition["partition_name"] = st.selectbox("Rule Partition",key=partition_name,options= partition_names,
                                                                           index=partition_names.index(
                                                                               partition[ "partition_name"]) if partition.get(
                                                                               "partition_name") in partition_names else None)

        with col3:
            st.markdown("")
            st.markdown("")
            partition["rule_partition_active"] = st.checkbox("Active",key=rule_partition_active,value= partition.get( "rule_partition_active",True))

        if partition["rule_name"]:
            partition["primary_keys"] = Variables.rule_names[partition["rule_name"]].get("primary_keys")
            partition["src_table"] = Variables.rule_names[partition["rule_name"]].get("src_table")
            partition["tgt_table"] = Variables.rule_names[partition["rule_name"]].get("tgt_table")
            partition["rule_id"] = Variables.rule_names[partition["rule_name"]].get("id")

        if partition["partition_name"]:
            partition["rule_partition_id"] = Variables.rule_partitions[partition["partition_name"]].get("id")

        with col6:
            st.markdown("")
            st.markdown("")
            st.button('Remove', key=f'remove_dataset_rule_partition_{index}', on_click=remove_dataset_rule_partitions,disabled=disable_remove, args=(index,))


    except Exception as ex:
        with col6:
            st.markdown("")
            st.markdown("")
            st.button('Remove', key=f'remove_dataset_rule_partition_{index}', on_click=remove_dataset_rule_partitions,
                      disabled=disable_remove, args=(index,))

        print(traceback.format_exc())
        st.error(ex.__str__())