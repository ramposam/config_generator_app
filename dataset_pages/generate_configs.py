import os
import shutil
import tempfile
import zipfile

import streamlit as st
from core_utils.dag_generator import DagGenerator

from core_utils.generate_configs import ConfigTemplate

from helpers.variables import Variables


class GenerateConfigs:

    def __init__(self,form_data):
        self.form_data = form_data

    def zip_files_with_long_names(self,directory, output_zip):
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, directory)
                    if len(file_path) > 255:
                        # Add file to the zip file with a shortened name
                        file_path = r'\\?\{}'.format(file_path)
                    zipf.write(file_path, relative_path)


    def zipit(self,config_dir, delete_configs):
        zip_name = os.path.join(os.path.dirname(config_dir), os.path.basename(config_dir))
        # shutil.make_archive(zip_name, 'zip', config_dir)
        self.zip_files_with_long_names(config_dir, zip_name + ".zip")
        if delete_configs:
            try:
                shutil.rmtree(config_dir)
            except Exception as ex:
                st.error(f"Failed to delete generated configs unzipped file:{config_dir},{ex.__str__()} ")
        return f"{zip_name}.zip"

    def get_long_file_path(self,file_path):
        result = file_path
        if len(file_path) > 255:
            result = r'\\?\{}'.format(file_path)
        return result


    def generate(self):
        bucket = self.form_data["s3_bucket"]
        file_path = self.form_data["file_pth"]
        start_date_str = self.form_data["start_date"].strftime("%Y,%m,%d")
        file_date_format = self.form_data["file_date_format"]
        dataset_name = self.form_data["dataset_name"]
        pipeline_type = self.form_data["pipeline_type"]
        schedule_interval = self.form_data["schedule_interval"]
        s3_dataset_path = self.form_data["s3_dataset_path"]
        aws_access_key = self.form_data.get("aws_access_key")
        aws_secret_key = self.form_data.get("aws_secret_key")
        snowflake_stage_name = self.form_data.get("snowflake_stage_name")

        configs_tmp_dir =  tempfile.mkdtemp()

        configs_gen = ConfigTemplate( bucket=bucket,pipeline_type=pipeline_type, file_path=file_path,
                                      dataset_name=dataset_name, start_date=start_date_str, catchup=True,
                                      datetime_format=file_date_format, aws_access_key = aws_access_key,
                                      aws_secret_key=aws_secret_key, schedule_interval=schedule_interval,
                                      s3_dataset_path=s3_dataset_path, snowflake_stage_name=snowflake_stage_name)

        configs_dir = configs_gen.generate_configs(configs_tmp_dir)

        if not pipeline_type == "SNOWPIPE":
            dag_gen = DagGenerator(configs_dir=configs_dir, dataset_name=dataset_name)
            dag_gen.generate_dag_ddls()

        zipped_file = self.zipit(configs_dir, True)

        if os.path.exists(zipped_file):
            st.success(f"Successfully Generated configs. Click on Download zip to download files.!")
            zip_name = os.path.basename(zipped_file)
            with open(zipped_file, "rb") as file:
                st.markdown("")
                st.download_button(
                    label="Download ZIP File",
                    data=file,
                    file_name=zip_name,
                    mime="application/zip")
