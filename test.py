from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Make sure dag_id is unique
dag_id = 'test_dag_v1'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['your-email@domain.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def print_hello():
    print("Hello from Airflow!")
    return 'Hello from GKE Airflow!'

# Make sure to assign the dag_id
dag = DAG(
    dag_id,
    default_args=default_args,
    description='A test DAG',
    schedule_interval=timedelta(days=1),
    catchup=False
)

# Create task
task1 = PythonOperator(
    task_id='hello_task',
    python_callable=print_hello,
    dag=dag
)

# Make sure this is at the end of the file
globals()[dag_id] = dag