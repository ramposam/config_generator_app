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
                    st.write(f"uploaded_file_path:{file_path}")

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
                st.session_state.dataset_form_data["s3_dataset_dir"] = st.text_input("S3 dataset folder")

                st.session_state.dataset_form_data["file_date_format"] = st.text_input("File Date Format",
                                                                               value="YYYYMMDD")


                st.session_state.dataset_form_data["catchup"] = st.checkbox("Historical Data load",
                                                                               value=False)

                st.session_state.dataset_form_data["start_date"] = st.date_input(
                    f'DAG Start Date'
                )
                st.session_state.dataset_form_data["schedule_interval"] = st.text_input("Schedule Interval",
                                                                                       value="* * * * *")

                st.session_state.dataset_form_data["pipeline_type"] = st.selectbox("Generate Pipelines Using:",
                                                                                options=pipelines_options,
                                                                               index=0)


                if st.session_state.dataset_form_data.get("dataset_name") is not None:
                    st.session_state.dataset_form_data["dataset_name"] = st.session_state.dataset_form_data["dataset_name"].replace(" ","_").lower()

        except Exception as ex:
            st.markdown("")
            print(traceback.format_exc())
            st.error(ex.__str__())
            return None