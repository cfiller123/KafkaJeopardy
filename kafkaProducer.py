import kafka

def publish_message(producer_instance, topic_name, key, value):
    key_bytes = bytes(key, encoding='utf-8')
    value_bytes = 