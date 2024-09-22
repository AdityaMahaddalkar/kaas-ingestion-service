import marqo
from kafka import KafkaConsumer

from config import Config
from models.chunk_entity import ChunkEntity


class VectorizationService:
    def __init__(self):
        self.config = Config().get_config()

        self.connection_string = self.config['marqo']['connection-string']
        self.index_name = self.config['marqo']['index-name']
        self.model = self.config['marqo']['embedding-model']
        self.insertion_batch_size = self.config['marqo']['insertion-batch-size']
        self.tensor_field = self.config['marqo']['tensor-field']

        self.mq = marqo.Client(
            url=self.connection_string
        )

        self.create_index_if_not_exists()

        self.bootstrap_server = self.config['kafka']['bootstrap-server']
        self.chunk_topic = self.config['kafka']['chunk-processing-topic']

        self.kafka_consumer = KafkaConsumer(
            self.chunk_topic,
            bootstrap_servers=self.bootstrap_server,
            client_id='vectorization-service',
            group_id='vectorization-service',
            value_deserializer=ChunkEntity.deserialize
        )

    def create_index_if_not_exists(self):

        assert 'index_name' in self.__dict__ and self.index_name is not None, 'Index name is not set'
        assert 'model' in self.__dict__ and self.model is not None, 'Embedding model is not set'
        assert 'mq' in self.__dict__ and self.mq is not None, 'Marqo client is not instantiated'

        indices = set(result['indexName'] for result in self.mq.get_indexes()['results'])

        if self.index_name not in indices:
            self.mq.create_index(
                index_name=self.index_name,
                model=self.model
            )

    def run(self):

        docs = []

        for message in self.kafka_consumer:
            chunk_entity = message.value

            docs.append(ChunkEntity.serialize(chunk_entity))

            if len(docs) >= self.insertion_batch_size:
                self.mq.index(self.index_name).add_documents(
                    documents=docs,
                    tensor_fields=[self.tensor_field]
                )
                docs = []

        if len(docs) > 0:
            self.mq.index(self.index_name).add_documents(
                documents=docs,
                tensor_fields=[self.tensor_field]
            )
