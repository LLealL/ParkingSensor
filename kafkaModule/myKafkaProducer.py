from kafka import KafkaProducer
from kafka.errors import KafkaError

class KProducer:

    def __init__(self, servers='localhost:9092',):
        self.producer = KafkaProducer(bootstrap_servers=[servers], value_serializer= lambda m: json.dumps(m).encode('ascii'))
        

    def sendData(self, data , topic ):
        future = self.producer.send(topic,data).add_callback(on_send_sucess).add_errback(on_send_error)

    def on_send_sucess(record_metadata):
        print(record_metadata)
        print(record_metada.partition)
        print(record_metadata.offset)

    def on_send_error(excp):
        log.error('I am an errback', exc_info =excp)
        
