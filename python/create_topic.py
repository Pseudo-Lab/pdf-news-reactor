from kafka.admin import KafkaAdminClient, NewTopic

# Kafka 관리자 클라이언트 생성
admin_client = KafkaAdminClient(
    bootstrap_servers=['broker-1:9092', 'broker-2:9092', 'broker-3:9092'],  # Kafka 브로커의 주소
    client_id='my_admin_client'  # 클라이언트 ID
)

# 생성할 새로운 토픽 설정
topic_list = []
topic_list.append(NewTopic(name="reaction", num_partitions=1, replication_factor=1))

# 토픽 생성
admin_client.create_topics(new_topics=topic_list, validate_only=False)

# 관리자 클라이언트 종료
admin_client.close()
