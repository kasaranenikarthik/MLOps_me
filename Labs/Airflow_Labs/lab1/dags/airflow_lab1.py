from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.lab import load_data, data_preprocessing, build_save_model, load_model_elbow

default_args = {
    'owner': 'Geeta Venkata Siva Karthik Kasaraneni',
    'start_date': datetime(2025, 1, 15),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='Airflow_Lab1',
    default_args=default_args,
    description='DAG example for Lab 1 of Airflow series',
    schedule=None,
    catchup=False,
    tags=['lab', 'example'],
) as dag:

    # Task: Load Data
    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )

    # Task: Data Preprocessing
    data_preprocessing_task = PythonOperator(
        task_id='data_preprocessing',
        python_callable=data_preprocessing,
        op_args=[load_data_task.output],
    )

    # Task: Build and Save Model
    build_save_model_task = PythonOperator(
        task_id='build_save_model',
        python_callable=build_save_model,
        op_args=[data_preprocessing_task.output, "model.sav"],
    )

    # Task: Load Model with Elbow Method
    load_model_task = PythonOperator(
        task_id='load_model',
        python_callable=load_model_elbow,
        op_args=["model.sav", build_save_model_task.output],
    )

    # Set task dependencies using bitshift operator
    load_data_task >> data_preprocessing_task >> build_save_model_task >> load_model_task

# Enable CLI interaction when run directly
if __name__ == "__main__":
    dag.cli()
