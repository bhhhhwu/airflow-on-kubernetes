#!/usr/bin/env bash

echo $BASH_VERSION

helm upgrade airflow apache-airflow/airflow \
  --namespace=airflow \
  --set images.airflow.repository=bobwu/airflow \
  --set images.airflow.tag=latest \
  --set images.airflow.pullPolicy=Always