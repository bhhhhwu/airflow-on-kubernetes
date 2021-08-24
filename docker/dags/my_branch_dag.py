import random

from airflow.models import DAG, Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import (BranchPythonOperator,
                                               PythonOperator)
from airflow.utils.dates import days_ago

args = {
    'owner': 'Airflow',
    'start_date': days_ago(2),
    'enabled': True
}

dag = DAG(
    dag_id='my_branch_dag',
    default_args=args,
    schedule_interval="@daily",
    tags=['example'],
    is_paused_upon_creation=False
)

run_this_first = DummyOperator(
    task_id='run_this_first',
    dag=dag,
)

options = ['branch_a', 'branch_b', 'branch_c', 'branch_d']

branching = BranchPythonOperator(
    task_id='branching',
    python_callable=lambda: random.choice(options),
    dag=dag,
)
run_this_first >> branching

join = DummyOperator(
    task_id='join',
    trigger_rule='one_success',
    dag=dag,
)


def my_function(*args, **kwargs):
    var1 = Variable.get('var1')
    print(f'var1= {var1}, args= {args}, kwargs= {kwargs}')
    Variable.set("key1", "1.2.3")
    return None


end_task = PythonOperator(
    task_id='end', dag=dag, python_callable=my_function, provide_context=True, op_args=[Variable.get("var1")],
    op_kwargs={"key": "string outside of {{ var.value.var1 }}"}
)

for option in options:
    t = DummyOperator(
        task_id=option,
        dag=dag,
    )

    dummy_follow = DummyOperator(
        task_id='follow_' + option,
        dag=dag,
    )

    branching >> t >> dummy_follow >> join >> end_task
