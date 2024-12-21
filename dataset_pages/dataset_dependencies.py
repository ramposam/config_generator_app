
import traceback

import streamlit as st

from dataset_pages.dataset_helper import get_dataset_rule_partitions, remove_dataset_rule_partitions, \
    get_dataset_dependencies, remove_dependent_dataset
from helpers.variables import Variables


def add_dataset_dependencies(index, dependent_dataset):
    try:
        [dataset_name, dataset_active] = get_dataset_dependencies(index)

        col1, col2, col3, col4 = st.columns([3, 1.5, 3, 1.5])

        if len(st.session_state.dataset_dependencies) - 1 == index:
            disable_remove = False
        else:
            disable_remove = True

        dataset_names = list(Variables.dataset_names.keys())

        with col1:
            dependent_dataset["dataset_name"] = st.selectbox("Upstream Dataset Name", key=dataset_name,
                                                             options=dataset_names,
                                                             index=dataset_names.index(
                                                                 dependent_dataset[
                                                                     "dataset_name"]) if dependent_dataset.get(
                                                                 "dataset_name") in dataset_names else None)

        with col2:
            st.markdown("")
            st.markdown("")
            dependent_dataset["dataset_active"] = st.checkbox("Active", key=dataset_active,
                                                              value=dependent_dataset.get("dataset_active", True))

        if dependent_dataset["dataset_name"]:
            dependent_dataset["edp_dataset_id"] = Variables.dataset_names[dependent_dataset["dataset_name"]].get("id")

        with col4:
            st.markdown("")
            st.markdown("")
            st.button('Remove', key=f'remove_dependent_dataset_{index}', on_click=remove_dependent_dataset,
                      disabled=disable_remove, args=(index,))


    except Exception as ex:
        with col4:
            st.markdown("")
            st.markdown("")
            st.button('Remove', key=f'remove_dependent_dataset_{index}', on_click=remove_dependent_dataset,
                      disabled=disable_remove, args=(index,))

        print(traceback.format_exc())
        st.error(ex.__str__())

