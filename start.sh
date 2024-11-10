#!/bin/bash

kubectl apply -f base/redis.yaml

kubectl apply -f base/zookeeper.yaml

sleep 20;

kubectl apply -f base/broker.yaml

sleep 20;

kubectl apply -f base/create_topic.yaml

sleep 20;

kubectl apply -f base/producer.yaml

sleep 60;

kubectl apply -f base/kafka_ui.yaml

kubectl create configmap clickhouse-config --from-file=./base/clickhouse/config.xml

sleep 10;

kubectl apply -f base/clickhouse.yaml