#!/usr/bin/env bash

echo $BASH_VERSION

docker build --tag "bobwu/airflow:latest" . -f - <<EOF
FROM apache/airflow:2.1.2

COPY ./dags/ \${AIRFLOW_HOME}/dags/

EOF

