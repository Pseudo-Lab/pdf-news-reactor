#!/bin/bash

kubectl delete configmap clickhouse-config
kubectl delete -f base/clickhouse.yaml
kubectl delete -f base/redis.yaml
kubectl delete -f base/zookeeper.yaml
kubectl delete -f base/broker.yaml
kubectl delete -f base/create_topic.yaml
kubectl delete -f base/producer.yaml
kubectl delete -f base/kafka_ui.yaml
