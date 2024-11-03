#!/bin/bash

kubectl apply -f redis.yaml

kubectl apply -f zookeeper.yaml

sleep 20;

kubectl apply -f broker.yaml

sleep 20;

kubectl apply -f create_topic.yaml

sleep 20;

kubectl apply -f producer.yaml

sleep 60;

kubectl apply -f kafka_ui.yaml

kubectl create configmap clickhouse-config --from-file=./clickhouse/config.xml

sleep 10;

kubectl apply -f clickhouse.yaml