import json
import os
import uuid
from concurrent.futures import ThreadPoolExecutor

from kafka import KafkaProducer
from langchain_community.document_loaders import BSHTMLLoader

from config import Config


class ChunkingService:
    def __init__(self):
        self.config = Config().get_config()
        self.source_folder = self.config['local-storage']['temporary-directory']

        self.bootstrap_server = self.config['kafka']['bootstrap-server']
        self.chunk_topic = self.config['kafka']['chunk-processing-topic']
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_server,
            compression_type='gzip',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def run(self):
        files_to_chunk = list(os.walk(self.source_folder))[0][2]
        full_file_paths = [os.path.join(self.source_folder, file_path) for file_path in files_to_chunk]

        def load_and_split_threadsafe(full_file_path):
            docs = BSHTMLLoader(file_path=full_file_path).load_and_split()

            for doc in docs:
                unique_id = str(uuid.uuid4())
                doc_json = {
                    'chunk_id': unique_id,
                    'chunk': doc.page_content,
                    'source': doc.metadata['source']
                }

                self.kafka_producer.send(self.chunk_topic, unique_id, doc_json)

        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.submit(load_and_split_threadsafe, full_file_paths)
