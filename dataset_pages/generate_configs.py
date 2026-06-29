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
        print("[INFO] Starting zip_files_with_long_names...")
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, directory)
                    if len(file_path) > 255:
                        # Add file to the zip file with a shortened name
                        file_path = r'\\?\{}'.format(file_path)
                    zipf.write(file_path, relative_path)
        print(f"[INFO] Completed zip_files_with_long_names: {output_zip}")


    def copy_dir_exclude(self, src, dst, exclude_dirs):
        """Copy directory excluding specified subdirectories"""
        print(f"[INFO] Starting copy_dir_exclude from {src} to {dst}, excluding {exclude_dirs}")
        if not os.path.exists(dst):
            os.makedirs(dst)
        
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dst_path = os.path.join(dst, item)
            
            if item in exclude_dirs:
                print(f"[INFO] Skipping excluded directory: {item}")
                continue
            
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path)
        print(f"[INFO] Completed copy_dir_exclude to {dst}")

    def zipit(self,config_dir, delete_configs):
        print(f"[INFO] Starting zipit for {config_dir}")
        zip_name = os.path.join(os.path.dirname(config_dir), "generated_configs")
        # shutil.make_archive(zip_name, 'zip', config_dir)
        self.zip_files_with_long_names(config_dir, zip_name + ".zip")
        if delete_configs:
            try:
                print(f"[INFO] Deleting temporary config directory: {config_dir}")
                shutil.rmtree(config_dir)
            except Exception as ex:
                st.error(f"Failed to delete generated configs unzipped file:{config_dir},{ex.__str__()} ")
        print(f"[INFO] Completed zipit: {zip_name}.zip")
        return f"{zip_name}.zip"


    def generate(self):
        print("[INFO] Starting config generation process...")
        bucket = self.form_data.get("bucket")
        file_path = self.form_data.get("file_path")
        if not file_path:
            st.error("file_path is required")
            return
        
        start_date = self.form_data.get("start_date")
        if not start_date:
            st.error("start_date is required")
            return
        start_date_str = start_date.strftime("%Y,%m,%d").replace(",0", ",")
        
        file_date_format = self.form_data.get("file_date_format")
        dataset_name = self.form_data.get("dataset_name")
        pipeline_type = self.form_data.get("pipeline_type")
        schedule_interval = self.form_data.get("schedule_interval")
        dataset_path = self.form_data.get("dataset_path")
        aws_access_key = self.form_data.get("aws_access_key")
        aws_secret_key = self.form_data.get("aws_secret_key")
        snowflake_stage_name = self.form_data.get("snowflake_stage_name")
        db_type =  self.form_data.get("db_type","SNOWFLAKE")
        encoding = self.form_data.get("encoding", "UTF-8")
        layer = self.form_data.get("layer", "Mirror -> Stage -> Standard")
        layer_0_db = self.form_data.get("layer_0_db", "MIRROR_DB")
        layer_1_db = self.form_data.get("layer_1_db", "STAGE_DB")

        print(f"[INFO] Dataset: {dataset_name}, Pipeline Type: {pipeline_type}")
        configs_tmp_dir = tempfile.mkdtemp()
        print(f"[INFO] Created temporary directory: {configs_tmp_dir}")
        
        try:
            print("[INFO] Initializing ConfigTemplate...")
            configs_gen = ConfigTemplate( bucket=bucket,pipeline_type=pipeline_type, file_path=file_path,db_type=db_type,
                                          dataset_name=dataset_name, start_date=start_date_str, catchup=True,
                                          datetime_format=file_date_format, aws_access_key = aws_access_key,
                                          aws_secret_key=aws_secret_key, schedule_interval=schedule_interval,
                                          dataset_path=dataset_path, snowflake_stage_name=snowflake_stage_name,
                                          encoding=encoding, layer=layer, layer_0_db=layer_0_db, layer_1_db=layer_1_db)

            print("[INFO] Generating configuration files...")
            configs_dir = configs_gen.generate_configs(configs_tmp_dir)
            print(f"[INFO] Configuration files generated in: {configs_dir}")

            if not pipeline_type == "SNOWPIPE":
                print("[INFO] Initializing DagGenerator...")
                dag_gen = DagGenerator(configs_dir=configs_dir, dataset_name=dataset_name)
                print("[INFO] Generating DAG DDLs...")
                dag_gen.generate_dag_ddls()
                print("[INFO] DAG DDLs generation completed")
            else:
                print("[INFO] Skipping DAG generation for SNOWPIPE pipeline")

            # Copy configs to dataset_path/dataset_configs/dev/ excluding generated_dag_ddls (only for Local load type)
            load_type = self.form_data.get("load_type")
            if load_type == "Local":
                try:
                    dataset_configs_dest = os.path.join(dataset_path, "dataset_configs", "dev")
                    self.copy_dir_exclude(configs_dir, dataset_configs_dest, exclude_dirs=["generated_dag_ddls"])
                except Exception as ex:
                    st.error(f"Failed to copy configs to {dataset_configs_dest}: {ex}")
                    return

            print("[INFO] Creating zip file...")
            zipped_file = self.zipit(configs_dir, False)
            print(f"[INFO] Zip file created: {zipped_file}")
        finally:
            if os.path.exists(configs_tmp_dir):
                if os.path.exists(zipped_file):
                    st.success(f"Successfully Generated configs. Click on Download zip to download files.!")
                    zip_name = os.path.basename(zipped_file)
                    with open(zipped_file, "rb") as file:
                        st.markdown("")
                        download_button = st.download_button(
                            label="Download ZIP File",
                            data=file,
                            file_name=zip_name,
                            mime="application/zip")
                if download_button:
                    print(f"[INFO] Cleaning up temporary directory: {configs_tmp_dir}")
                    shutil.rmtree(configs_tmp_dir)
        print("[INFO] Config generation process completed successfully")

        return zipped_file
