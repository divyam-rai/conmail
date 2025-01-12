from uuid import uuid4
from confluent_kafka import Producer

from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer

# string_serializer = StringSerializer('utf8')
# producer = Producer({ "bootstrap.servers": "schema_registry_url" })
# schema_registry_client = SchemaRegistryClient({ "url": "schema_registry_url" })

def delivery_report(err, msg):
    """
    Reports the failure or success of a message delivery.

    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    """
    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return

    print('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))

def produce(topic, proto_value, key = None):
    # if key is None:
    #     key = str(uuid4())

    # protobuf_serializer = ProtobufSerializer(
    #     type(proto_value),
    #     schema_registry_client,
    #     {'use.deprecated.format': False}
    # )

    # producer.produce(
    #     topic= topic,
    #     key= string_serializer(key),
    #     value= protobuf_serializer(
    #         proto_value,
    #         SerializationContext(topic, MessageField.VALUE)
    #     ),
    #     on_delivery=delivery_report
    # )
    print(proto_value)
    print(key)
    print(topic)