from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime, timedelta

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
    return 'Hello from GKE Airflow!'

dag = DAG(
    'k8s_test_dag',
    default_args=default_args,
    description='A test DAG using Kubernetes executor',
    schedule_interval=timedelta(days=1),
    catchup=False
)

# Regular Python task
task1 = PythonOperator(
    task_id='hello_task',
    python_callable=print_hello,
    dag=dag
)

# Kubernetes Pod task
k8s_task = KubernetesPodOperator(
    task_id='kubernetes_pod_task',
    name='sample-pod-task',
    namespace='airflow',
    image='python:3.9-slim',
    cmds=["python", "-c"],
    arguments=["print('Hello from Kubernetes Pod!')"],
    labels={"app": "airflow"},
    resources={
        'request_cpu': '100m',
        'request_memory': '200Mi',
        'limit_cpu': '200m',
        'limit_memory': '500Mi'
    },
    is_delete_operator_pod=True,
    dag=dag
)

task1 >> k8s_task