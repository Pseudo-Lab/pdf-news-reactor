#!/bin/bash

kubectl delete -f zookeeper.yaml
kubectl delete -f broker.yaml
kubectl delete -f create_topic.yaml
kubectl delete -f producer.yaml
kubectl delete -f consumer.yaml
kubectl delete -f kafka_ui.yaml