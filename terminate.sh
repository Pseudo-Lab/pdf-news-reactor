#!/bin/bash

kubectl delete configmap clickhouse-config
kubectl delete -f clickhouse.yaml
kubectl delete -f redis.yaml
kubectl delete -f zookeeper.yaml
kubectl delete -f broker.yaml
kubectl delete -f create_topic.yaml
kubectl delete -f producer.yaml
kubectl delete -f kafka_ui.yaml
