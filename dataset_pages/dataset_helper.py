
import json
import streamlit as st
from helpers.variables import Variables


def get_dataset_rule_partitions(index):
    rule_name = f"{index}_rule_name"
    partition_name = f"{index}_partition_name"
    primary_keys = f"{index}_primary_keys"
    src_table = f"{index}_src_table"
    tgt_table = f"{index}_tgt_table"
    rule_partition_active = f"{index}_rule_partition_active"
    return [rule_name, partition_name, primary_keys, src_table, tgt_table, rule_partition_active]


# Function to handle the addition of a new condition
def add_dataset_rule_partition():
    index = 1 if len(st.session_state.dataset_rule_partitions) == 0 else max(
        [item["partition_order_num"] for item in st.session_state.dataset_rule_partitions]) + 1

    st.session_state.dataset_rule_partitions.append({
        'rule_name': None,
        'rule_partition_name': None,
        'primary_keys': None,
        'src_table': None,
        "tgt_table": None,
        "partition_order_num": index,
        'dataset_rule_id': None,
        'rule_id': None,
        'rule_partition_id': None,
        'rule_partition_active': None})


# Function to handle the removal of a condition
def remove_dataset_rule_partitions(index):
    if index < len(st.session_state.dataset_rule_partitions) - 1:
        st.markdown("")
        st.markdown("")
        st.error("Removal of rule partition allowed only in descending(last to first) order.")
        return

    if st.session_state.dataset_rule_partitions[index].get("rule_partition_id"):
        st.session_state.dataset_form_data["delete_rule_partition_ids"].append(
            st.session_state.dataset_rule_partitions[index]["rule_partition_id"])

    st.session_state.dataset_rule_partitions.pop(index)


def get_dataset_dependencies(index):
    dataset_name = f"{index}_dataset_name"
    dataset_active = f"{index}_dataset_active"
    return [dataset_name, dataset_active]


# Function to handle the addition of a new condition
def add_dependent_dataset():
    index = 1 if len(st.session_state.dataset_dependencies) == 0 else max(
        [item["dataset_order_num"] for item in st.session_state.dataset_dependencies]) + 1
    st.session_state.dataset_dependencies.append({
        'dataset_name': None,
        'dataset_active': None,
        "dataset_dep_id": None,
        "edp_dataset_id": None,
        "dataset_order_num": index
    })


# Function to handle the removal of a condition
def remove_dependent_dataset(index):
    if index < len(st.session_state.dataset_dependencies) - 1:
        st.markdown("")
        st.markdown("")
        st.error("Removal of dependent dataset allowed only in descending(last to first) order.")
        return

    if st.session_state.dataset_dependencies[index].get("dataset_dep_id"):
        st.session_state.dataset_form_data["delete_dataset_dep_ids"].append(
            st.session_state.dataset_dependencies[index]["dataset_dep_id"])

    st.session_state.dataset_dependencies.pop(index)



def set_form_data(list_of_dict, form_data, dataset_rule_partitions, dataset_dependencies):
    for index, data_dict in enumerate(list_of_dict):
        form_data["dataset_id"] = data_dict["dataset_id"]
        form_data["edp_domain_id"] = data_dict["edp_domain_id"]
        form_data["provider_source_id"] = data_dict["provider_source_id"]
        form_data["dataset_name"] = data_dict["dataset_nm"]
        form_data["dataset_active"] = True if data_dict["active_fl"] == "Y" else False
        form_data["schedule_interval"] = data_dict["schedule_interval"]
        form_data["domain_name"] = data_dict["domain_nm"]
        form_data["provider_name"] = data_dict["provider_source_nm"]
        dep_dataset_details = json.loads(data_dict["dep_dataset_details"])
        rule_partition_details = json.loads(data_dict["rule_partition_details"])

        for index, dep_dataset_detail in enumerate(dep_dataset_details):
            for dep_dataset_name, dataset_detail in dep_dataset_detail.items():
                dep_dataset = {'dataset_name': dep_dataset_name,
                               'dataset_active': False if dataset_detail.get("ACTIVE_FL") == "N" else True,
                               "dataset_dep_id": dataset_detail.get("DEPENDENT_DATASET_ID"),
                               "edp_dataset_id": dataset_detail.get("EDP_DEPENDENT_DATASET_ID"),
                               "dataset_order_num": index + 1}
                dataset_dependencies.append(dep_dataset)

        for index, rule_partition_detail in enumerate(rule_partition_details):
            for rule_name, partition_detail in rule_partition_detail.items():
                dataset_rule_partitions.append({"rule_name": rule_name,
                                                "partition_name": partition_detail["PARTITION_NM"],
                                                "default_primary_keys": partition_detail["PRIMARY_KEYS"].split(","),
                                                "primary_keys": partition_detail["PRIMARY_KEYS"].split(","),
                                                "src_table": partition_detail["SRC_TABLE"],
                                                "tgt_table": partition_detail["TGT_TABLE"],
                                                "partition_order_num": index + 1,
                                                'dataset_rule_id': partition_detail["DATASET_RULE_ID"],
                                                'rule_id': partition_detail["RULE_ID"],
                                                'rule_partition_id': partition_detail["RULE_PARTITION_ID"],
                                                'rule_partition_active': partition_detail["ACTIVE_FL"]})


def set_dataset_details(dataset_name, form_data, dataset_rule_partitions, dataset_dependencies):
    dataset_query_result = get_data_from_query(dataset_query, dataset_name, "DATASET_NAME")
    set_form_data(dataset_query_result, form_data, dataset_rule_partitions, dataset_dependencies)

