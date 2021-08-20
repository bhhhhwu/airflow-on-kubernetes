kubectl scale --replicas=0 deployment/airflow-scheduler
kubectl scale --replicas=1 deployment/airflow-scheduler

kubectl scale --replicas=0 deployment/airflow-webserver
kubectl scale --replicas=1 deployment/airflow-webserver


