import logging

import pandas as pd
import psycopg2
from kafka import KafkaConsumer
from psycopg2 import extras

from config import Config
from db.sql_scripts import CREATE_CHUNKS_TABLE, INSERT_CHUNKS_INTO_TABLE
from models.chunk_entity import ChunkEntity


class DatabaseService:
    def __init__(self):
        self.config = Config().get_config()

        self.host = self.config['postgres']['host']
        self.port = self.config['postgres']['port']
        self.username = self.config['postgres']['username']
        self.password = self.config['postgres']['password']
        self.database = self.config['postgres']['database']
        self.table = self.config['postgres']['table']
        self.insertion_batch_size = self.config['postgres']['insertion-batch-size']

        self.con = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.database,
        )

        self.create_table_if_not_exists()

        self.bootstrap_server = self.config['kafka']['bootstrap-server']
        self.chunk_topic = self.config['kafka']['chunk-processing-topic']

        self.kafka_consumer = KafkaConsumer(
            self.chunk_topic,
            bootstrap_servers=self.bootstrap_server,
            client_id='database-service',
            group_id='database-service',
            value_deserializer=ChunkEntity.deserialize
        )

    def create_table_if_not_exists(self):
        assert 'table' in self.__dict__ and self.table is not None, 'Table name is not specified'
        assert 'con' in self.__dict__ and self.con is not None, 'Connection to database is not instantiated'

        try:
            with self.con.cursor() as cursor:
                cursor.execute(
                    CREATE_CHUNKS_TABLE.format(table=self.table)
                )
                self.con.commit()
        except Exception as e:
            logging.error(f'Failed to create table = {self.table} in database = {self.database}', exc_info=e)

    def insert_chunks_into_table(self, chunk_list: list[ChunkEntity]):
        chunks_df = pd.DataFrame([chunk.__dict__ for chunk in chunk_list])
        query = INSERT_CHUNKS_INTO_TABLE.format(
            table=self.table,
            cols=','.join(list(chunks_df.columns))
        )
        try:
            tuples = [tuple(x) for x in chunks_df.to_numpy()]
            with self.con.cursor() as cursor:
                extras.execute_batch(cursor, query, tuples, self.insertion_batch_size)
            self.con.commit()
        except Exception as e:
            self.con.rollback()
            logging.error(f'Error inserting chunks with size = {len(chunk_list)} into table = {self.table}', exc_info=e)

    def run(self):

        chunk_list = [message.value for message in self.kafka_consumer]
        self.insert_chunks_into_table(chunk_list)
