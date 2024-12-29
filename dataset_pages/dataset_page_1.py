import os
import traceback


from helpers.constants import yes_no_options, bucket_list, pipelines_options, stage_name_options
from helpers.utils import get_df_from_query_with_error, dummy
import streamlit as st

from helpers.variables import Variables
import tempfile
def page_1():
    st.markdown("####  Datasets ####")
    st.markdown("")
    with st.expander("**Datasets**", expanded=True):
        st.markdown("")
        st.markdown("##### Filter Datasets")
        try:
            st.session_state.dataset_form_data["file_pth"] = None
            col1, col2, col3 = st.columns([1,8,1])
            with col2:
                uploaded_file = st.file_uploader("Select File to upload", type=["TXT","CSV"])
                if uploaded_file:
                    temp_dir = tempfile.mkdtemp()
                    file_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getvalue())

                    st.session_state.dataset_form_data["file_pth"] = file_path

                st.session_state.dataset_form_data["file_has_dataset_name"] = st.checkbox("Use File Name for Dataset Configs",
                                                                               value=True)

                if not st.session_state.dataset_form_data["file_has_dataset_name"]:
                    st.session_state.dataset_form_data["dataset_name"] = st.text_input("Desired Dataset Name",
                                                                                   value=None)
                else:

                    if st.session_state.dataset_form_data["file_pth"] is not None:
                        dataset_name = os.path.basename(st.session_state.dataset_form_data["file_pth"])
                        st.session_state.dataset_form_data["dataset_name"] = dataset_name.split(".")[0]

                st.session_state.dataset_form_data["s3_bucket"] = st.selectbox("S3 Bucket",
                                                                               options=bucket_list,
                                                                               index=0)
                st.session_state.dataset_form_data["s3_dataset_path"] = st.text_input("S3 dataset Path")

                if not st.session_state.dataset_form_data["s3_dataset_path"]:
                    st.error("S3 dataset Path is required.")

                st.session_state.dataset_form_data["file_date_format"] = st.text_input("File Date Format" )


                st.session_state.dataset_form_data["catchup"] = st.checkbox("Historical Data load",
                                                                               value=False)

                st.session_state.dataset_form_data["start_date"] = st.date_input(
                    f'DAG Start Date'
                )
                st.session_state.dataset_form_data["schedule_interval"] = st.text_input("Schedule Interval",
                                                                                       value="0 23 * * 1-5")

                st.session_state.dataset_form_data["pipeline_type"] = st.selectbox("Generate Pipelines Using:",
                                                                                options=pipelines_options,
                                                                               index=0)

                if st.session_state.dataset_form_data["pipeline_type"] == "SNOWPIPE":
                    st.session_state.dataset_form_data["s3_credentials"] = st.checkbox("Want to Provide S3 Credentials?",
                                                                               value=False)
                    if st.session_state.dataset_form_data["s3_credentials"]:
                        st.session_state.dataset_form_data["aws_access_key"] = st.text_input("S3 Access Key")
                        st.session_state.dataset_form_data["aws_secret_key"] = st.text_input("S3 Secret Key")
                        if not (st.session_state.dataset_form_data["aws_access_key"] and st.session_state.dataset_form_data["aws_secret_key"]):
                            st.error("S3 Access/Secret Keys are required")
                    else:
                        st.session_state.dataset_form_data["snowflake_stage_name"] = st.selectbox("Snowflake Stage Name:",
                                                                                           options=stage_name_options,
                                                                                           index=0)


                if st.session_state.dataset_form_data.get("dataset_name") is not None:
                    st.session_state.dataset_form_data["dataset_name"] = st.session_state.dataset_form_data["dataset_name"].replace(" ","_").lower()

        except Exception as ex:
            st.markdown("")
            print(traceback.format_exc())
            st.error(ex.__str__())
            return None