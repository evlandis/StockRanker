import pandas as pd
from kafka import KafkaProducer
from time import sleep
from json import dumps
import json

producer = KafkaProducer(bootstrap_server=['18.222.147.73:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

producer.send('demo_testing',value="{'hello':'world'}")


df = pd.read_csv("data/indexProcessed.csv")
df.head()