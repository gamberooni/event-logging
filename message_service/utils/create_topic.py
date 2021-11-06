from confluent_kafka.admin import AdminClient, NewTopic
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import config

def main():
    a = AdminClient({'bootstrap.servers': config.bootstrap_server})

    new_topics = [NewTopic(topic, num_partitions=3, replication_factor=1) for topic in [config.topic]]
    # Note: In a multi-cluster production scenario, it is more typical to use a replication_factor of 3 for durability.

    # Call create_topics to asynchronously create topics. A dict
    # of <topic,future> is returned.
    fs = a.create_topics(new_topics)

    # Wait for each operation to finish.
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))

if __name__ == "__main__":
    main()