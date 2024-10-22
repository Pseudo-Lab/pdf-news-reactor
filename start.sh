#!/bin/bash

kubectl apply -f redis.yaml

kubectl apply -f zookeeper.yaml
sleep 20

kubectl apply -f broker.yaml
sleep 20

kubectl apply -f create_topic.yaml
sleep 20

kubectl apply -f producer.yaml
sleep 20

kubectl apply -f consumer.yaml
sleep 20

kubectl apply -f kafka_ui.yaml
