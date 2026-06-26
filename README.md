# Config Generator App

A Streamlit-based application for automated ETL pipeline configuration generation. This tool helps generate configuration templates, Airflow DAGs, and database DDLs for building data pipelines with support for multiple database platforms including Snowflake and PostgreSQL.

## Features

- **Pipeline Configuration Generation**: Generate configuration templates for building ETL pipelines
- **Airflow DAG Generation**: Automatically create Airflow DAGs for scheduled data pipeline execution
- **Database DDL Generation**: Generate Postgres Table DDLs for:
  - Mirror tables
  - Mirror append-only tables for historical data
  - Stage tables for SCD (Slowly Changing Dimensions) type 2 data
- **Multi-Platform Support**: Support for Snowflake and PostgreSQL databases
- **Flexible Data Loading**: Support for local file loading and AWS S3 integration
- **Snowpipe Integration**: Native support for Snowflake Snowpipe for continuous data loading
- **DBT Model Generation**: Uses `generate_models.py` to generate dbt models from generated configs/templates
- **Custom Operators**: Utilizes custom operators library to pass data from mirror to stage layer

## Architecture

The application follows a modular architecture with clear separation of concerns:

### Core Components

- **Streamlit UI**: Multi-page interface for dataset configuration and management
- **Config Generation**: Backend logic for generating pipeline configurations
- **DAG Generation**: Airflow DAG creation using the `DagGenerator` class
- **DDL Generation**: Database schema definition generation
- **DBT Integration**: Model generation for dbt-based transformations

## Directory Structure

```
config_generator_app/
├── app_pages/                    # Streamlit application pages
│   ├── 1_dataset_configs.py     # Main dataset configuration page
│   └── __init__.py
├── dataset_pages/               # Dataset-specific pages and logic
│   ├── dataset_page.py          # Main dataset page controller
│   ├── dataset_page_1.py        # Dataset file and path configuration
│   ├── dataset_page_2.py        # Dataset metadata configuration
│   ├── dataset_page_3.py        # Dependencies and rule/partition details
│   ├── generate_configs.py      # Config generation and zip creation
│   ├── dataset_helper.py        # Helper functions for dataset management
│   ├── dataset_dependencies.py  # Dataset dependency management
│   └── dataset_rule_partitions.py # Rule and partition configuration
├── helpers/                     # Utility modules
│   ├── constants.py             # Application constants
│   ├── css_styles.py           # UI styling
│   ├── db_connection.py        # Database connection utilities
│   ├── session_state.py       # Streamlit session state management
│   ├── utils.py               # General utility functions
│   └── variables.py           # Global variables
├── dags/                       # Generated Airflow DAGs directory
├── config_app.py              # Main Streamlit application entry point
├── logo.png                   # Application logo
└── README.md                  # This file
```

## Key Modules

### `config_app.py`
Main entry point for the Streamlit application. Initializes session state, applies CSS styling, and sets up navigation.

### `dataset_pages/generate_configs.py`
Core module for configuration generation:
- `GenerateConfigs`: Main class for generating pipeline configurations
- `copy_dir_exclude()`: Copies directories while excluding specified subdirectories
- `zipit()`: Creates zip archives of generated configurations
- `generate()`: Orchestrates the entire config generation process

### `dataset_pages/dataset_page.py`
Page controller that manages navigation between different dataset configuration pages.

### `dataset_pages/dataset_page_1.py`
First configuration page for:
- File upload or path specification
- Dataset naming
- Load type selection (Local/AWS S3)
- S3 bucket and path configuration
- File date format specification
- Historical data load options
- Schedule interval configuration
- Pipeline type selection (Airflow with Snowflake/Postgres, Snowpipe)
- Encoding type selection

### `dataset_pages/dataset_page_2.py`
Second configuration page for:
- Dataset metadata (name, domain, provider)
- Schedule interval configuration
- Optional pipeline tasks (Load Standard, Check Parent DAG Execution)
- Dataset activation

### `dataset_pages/dataset_page_3.py`
Third configuration page for:
- Dataset dependency management
- Rule and partition details configuration
- Primary key specification
- Source and target table mapping

## Pipeline Types

### 1. Airflow with Snowflake
Generates Airflow DAGs for Snowflake data pipelines with support for:
- Mirror tables
- Mirror append-only tables
- Stage tables for SCD type 2

### 2. Airflow with PostgreSQL
Generates Airflow DAGs for PostgreSQL data pipelines with similar table types as Snowflake.

### 3. Snowpipe
Native Snowflake Snowpipe integration for continuous data loading from S3 with optional:
- S3 credential configuration
- Snowflake stage name specification

## Data Flow

1. **Configuration**: User provides dataset configuration through Streamlit UI
2. **Generation**: `ConfigTemplate` generates configuration files in a temporary directory
3. **DAG Generation**: `DagGenerator` creates Airflow DAGs (except for Snowpipe)
4. **Copy to Destination**: Configs are copied to `{dataset_path}/dataset_configs/dev/` excluding `generated_dag_ddls`
5. **Zip Creation**: All configs are zipped into `generated_configs.zip` for download
6. **DBT Model Generation**: `generate_models.py` generates dbt models from the configs

## Configuration Parameters

### Required Parameters
- **Dataset Name**: Name for the dataset (can be auto-generated from filename)
- **Dataset Path**: Source data location (local or S3)
- **File Date Format**: Date format pattern in filenames
- **Schedule Interval**: Cron expression for pipeline scheduling
- **Pipeline Type**: Target platform (Snowflake/Postgres/Snowpipe)

### Optional Parameters
- **AWS S3 Credentials**: Access key and secret key for S3 access
- **Snowflake Stage Name**: Stage name for Snowpipe integration
- **Encoding Type**: File encoding (UTF-8, ASCII, ISO-8859-1, Windows-1252)
- **Historical Data Load**: Enable catchup for historical data
- **Start Date**: DAG execution start date

## Dependencies

The application requires the following Python packages:
- `streamlit`: Web application framework
- `core_utils`: Custom utility library containing:
  - `DagGenerator`: For Airflow DAG generation
  - `ConfigTemplate`: For configuration template generation
- `pandas`: Data manipulation
- Additional database-specific libraries for Snowflake and PostgreSQL

## Usage

### Running the Application

```bash
streamlit run config_app.py
```

### Generating Configurations

1. **Upload File or Specify Path**: Choose to upload a file or provide a file path
2. **Configure Dataset**: Set dataset name, load type, and path
3. **Set Schedule**: Configure schedule interval using cron expressions
4. **Choose Pipeline Type**: Select target platform (Snowflake/Postgres/Snowpipe)
5. **Generate Configs**: Click "Generate Configs" to create the configuration package
6. **Download**: Download the generated `generated_configs.zip` file

### Output Structure

Generated configs are copied to:
```
{dataset_path}/dataset_configs/dev/
```

The zip file includes:
- Configuration files
- Airflow DAGs (in `generated_dag_ddls` directory)
- DDL scripts
- DBT model definitions

## Schedule Interval Examples

- `0 * * * *` - Every hour
- `0 0 * * *` - Every day at 12:00 AM
- `30 20 * * 1-5` - At 8:30 PM, Monday through Friday
- `30 20 10 * *` - At 8:30 PM, on day 10 of the month

For more examples, visit [crontab.guru](https://crontab.guru/) or [crontab.cronhub.io](https://crontab.cronhub.io/)

## Notes

- Ensure dataset paths are properly mounted to the Docker container at `/opt/airflow/` for local file loading
- The application automatically excludes the `generated_dag_ddls` directory when copying configs to the dataset path
- File paths with extensions like `.csv`, `.dat`, `.txt`, `.zip`, `.json` are treated as invalid (directory paths expected)
- Dataset names are automatically converted to lowercase with spaces replaced by underscores

## License

[Add your license information here]