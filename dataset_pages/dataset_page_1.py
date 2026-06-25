import os
import traceback


from helpers.constants import yes_no_options, bucket_list, pipelines_options, stage_name_options, encoding_options
from helpers.utils import get_df_from_query_with_error, dummy
import streamlit as st

from helpers.variables import Variables
import tempfile
def page_1():
    st.markdown("####  Datasets ####")
    st.markdown("")
    ui_errors = []
    with st.expander("**Datasets**", expanded=True):
        st.markdown("")
        st.markdown("##### Filter Datasets")
        try:
            st.session_state.dataset_form_data["file_path"] = None
            col1, col2, col3, col4 = st.columns([1,7 ,3, 1])
            with col3:
                st.markdown("")
                st.markdown("")
                st.session_state.dataset_form_data["has_file_path"] = st.checkbox(
                    "Has File path?",
                    value=False)


            with col2:
                if not st.session_state.dataset_form_data["has_file_path"]:
                    uploaded_file = st.file_uploader("Select File to upload", type=["TXT","CSV"])
                    if uploaded_file:
                        temp_dir = tempfile.mkdtemp()
                        file_path = os.path.join(temp_dir, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getvalue())

                            st.session_state.dataset_form_data["file_path"] = file_path
                else:
                    st.session_state.dataset_form_data["file_path"] = st.text_input("File Path",
                                                                                       value=None)
                    st.session_state.dataset_form_data["dataset_path"]= "/opt/airflow/datasets" if st.session_state.dataset_form_data["file_path"] else None

                st.session_state.dataset_form_data["file_has_dataset_name"] = st.checkbox("Use File Name for Dataset Configs",
                                                                               value=True)

                if not st.session_state.dataset_form_data["file_has_dataset_name"]:
                    st.session_state.dataset_form_data["dataset_name"] = st.text_input("Desired Dataset Name",
                                                                                   value=None)
                else:

                    if st.session_state.dataset_form_data["file_path"] is not None:
                        dataset_name = os.path.basename(st.session_state.dataset_form_data["file_path"])
                        st.session_state.dataset_form_data["dataset_name"] = dataset_name.split(".")[0]

                st.session_state.dataset_form_data["load_type"] = st.selectbox("Load From",
                                                                               options=["Local","AWS S3"],
                                                                               index=0)
                if st.session_state.dataset_form_data["load_type"] == "AWS S3":
                    st.session_state.dataset_form_data["bucket"] = st.selectbox("S3 Bucket",
                                                                               options=bucket_list,
                                                                               index=0)
                    st.session_state.dataset_form_data["dataset_path"] = st.text_input("S3 dataset Path")

                    if not st.session_state.dataset_form_data["dataset_path"]:
                        st.error("AWS S3 dataset Path is required.")
                        ui_errors.append("AWS S3 dataset Path is required.")
                        return ui_errors

                else:
                    st.session_state.dataset_form_data["bucket"] = None
                    st.info(f"Make sure you mounted your datasets, configs, and dags paths to docker container on /opt/airflow/ otherwise manually copy them")
                    st.session_state.dataset_form_data["dataset_path"] = st.text_input("Source dataset Path",value=st.session_state.dataset_form_data.get("dataset_path"))

                if st.session_state.dataset_form_data["dataset_path"]:
                    _, ext = os.path.splitext(st.session_state.dataset_form_data["dataset_path"])
                    ext = ext.lower().lstrip('.')
                else:
                    ext = None

                if ext in ["csv","dat","txt","zip","json",]:
                    st.error(
                        f"""Invalid path: '{st.session_state.dataset_form_data["dataset_path"]}' looks like a file with extension '.{ext}'. """
                        f"Expected a directory path only."
                    )
                    ui_errors.append("Invalid dataset path. Expected a directory path only.")
                    return ui_errors

                st.info(f"Remove File Date Format when file name doesn't have date or datetime")
                st.session_state.dataset_form_data["file_date_format"] = st.text_input("File Date Format",value="YYYY-DD-DD" )


                if st.session_state.dataset_form_data["file_date_format"]:
                    st.session_state.dataset_form_data["file_date_format"] = st.session_state.dataset_form_data["file_date_format"].upper()

                st.session_state.dataset_form_data["catchup"] = st.checkbox("Historical Data load",
                                                                               value=False)

                st.session_state.dataset_form_data["start_date"] = st.date_input(
                    f'DAG Start Date'
                )
                st.session_state.dataset_form_data["encoding"] = st.selectbox(
                    f'Encoding Type',
                    options=encoding_options,
                    index=0
                )
                st.session_state.dataset_form_data["schedule_interval"] = st.text_input("Schedule Interval",
                                                                                       value="0 23 * * 1-5")

                st.session_state.dataset_form_data["pipeline_type"] = st.selectbox("Generate Pipelines Using:",
                                                                                options=pipelines_options,
                                                                               index=0)
                st.session_state.dataset_form_data["db_type"] = "POSTGRES" if "POSTGRES" in st.session_state.dataset_form_data["pipeline_type"] else "SNOWFLAKE"

                if st.session_state.dataset_form_data["pipeline_type"] == "SNOWPIPE":
                    st.session_state.dataset_form_data["s3_credentials"] = st.checkbox("Want to Provide S3 Credentials?",
                                                                               value=False)
                    if st.session_state.dataset_form_data["s3_credentials"]:
                        st.session_state.dataset_form_data["aws_access_key"] = st.text_input("S3 Access Key")
                        st.session_state.dataset_form_data["aws_secret_key"] = st.text_input("S3 Secret Key")
                        if not (st.session_state.dataset_form_data["aws_access_key"] and st.session_state.dataset_form_data["aws_secret_key"]):
                            st.error("S3 Access/Secret Keys are required")
                            ui_errors.append("S3 Access/Secret Keys are required")
                            return ui_errors
                    else:
                        st.session_state.dataset_form_data["snowflake_stage_name"] = st.selectbox("Snowflake Stage Name:",
                                                                                           options=stage_name_options,
                                                                                           index=0)


                if st.session_state.dataset_form_data.get("dataset_name") is not None:
                    st.session_state.dataset_form_data["dataset_name"] = st.session_state.dataset_form_data["dataset_name"].replace(" ","_").lower()

            return ui_errors
        except Exception as ex:
            st.markdown("")
            print(traceback.format_exc())
            st.error(ex.__str__())
            ui_errors.append(ex.__str__())
            return ui_errors