from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'nfl_data_pipeline',
    default_args=default_args,
    description='NFL Play-by-Play Data Pipeline',
    schedule_interval=None,
    catchup=False,
    max_active_runs=1,
)

def upload_to_gcs(bucket_name, source_files):
    gcs_hook = GCSHook(gcp_conn_id='google_cloud_default')
    for file in source_files:
        local_file_path = f"/Users/AKooner/Desktop/coding/data_engineering_zoomcamp/project1/nfl-raw-data/{file}"
        gcs_file_path = f"{file}"
        gcs_hook.upload(bucket_name, gcs_file_path, local_file_path)

source_files = [
    'pbp-2013.csv',
    'pbp-2014.csv',
    'pbp-2015.csv',
    'pbp-2016.csv',
    'pbp-2017.csv',
    'pbp-2018.csv',
    'pbp-2019.csv',
    'pbp-2020.csv',
    'pbp-2021.csv',
    'pbp-2022.csv',
    'pbp-2023.csv'
]

upload_to_gcs_task = PythonOperator(
    task_id='upload_to_gcs',
    python_callable=upload_to_gcs,
    op_kwargs={
        'bucket_name': 'sincere-nirvana-340100-nfl-data-lake-20230601',
        'source_files': source_files,
    },
    dag=dag,
)

gcs_to_bq_task = GCSToBigQueryOperator(
    task_id='gcs_to_bq',
    bucket='sincere-nirvana-340100-nfl-data-lake-20230601',
    source_objects=['*.csv'],
    destination_project_dataset_table='sincere-nirvana-340100.nfl_dataset.nfl_play_by_play',
    schema_fields=[
        {'name': 'GameId', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'GameDate', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'Quarter', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'Minute', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'Second', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'OffenseTeam', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'DefenseTeam', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'Down', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'ToGo', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'YardLine', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'SeriesFirstDown', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'NextScore', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'Description', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'TeamWin', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'SeasonYear', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'Yards', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'Formation', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'PlayType', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'IsRush', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'IsPass', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'IsIncomplete', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'IsTouchdown', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'PassType', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'IsSack', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'IsChallenge', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'IsChallengeReversed', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'Challenger', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'IsMeasurement', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'IsInterception', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'IsFumble', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'IsPenalty', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'IsTwoPointConversion', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'IsTwoPointConversionSuccessful', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'RushDirection', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'YardLineFixed', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'YardLineDirection', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'IsPenaltyAccepted', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'PenaltyTeam', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'IsNoPlay', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'PenaltyType', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'PenaltyYards', 'type': 'INTEGER', 'mode': 'NULLABLE'},
    ],
    write_disposition='WRITE_TRUNCATE',
    dag=dag,
)

upload_to_gcs_task >> gcs_to_bq_task