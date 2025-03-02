import datetime

from dataset_pages.generate_configs import GenerateConfigs

page_inputs = {'file_pth': r'C:\\Users\\Asus\\Downloads\\data\\archive\\sales.csv', 'file_has_dataset_name': True, 's3_bucket': 'rposam-etl-source-datasets-s3', 's3_dataset_path': 'datasets/sales/', 'file_date_format': '', 'catchup': False, 'start_date': datetime.date(2025, 2, 1), 'schedule_interval': '@once', 'pipeline_type': 'Airflow with POSTGRES', 'db_type': 'POSTGRES', 'dataset_name': 'sales', 'has_file_path': True}

GenerateConfigs(page_inputs).generate()