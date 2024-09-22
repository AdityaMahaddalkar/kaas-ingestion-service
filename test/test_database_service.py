import os
import uuid

import pytest

from models.chunk_entity import ChunkEntity
from services.database_service import DatabaseService


@pytest.mark.skipif("LOCAL_TESTING" not in os.environ, reason='Test Postgres locally')
def test_config_read():
    database_service = DatabaseService()
    assert database_service.config is not None
    assert database_service.con is not None


@pytest.mark.skipif("LOCAL_TESTING" not in os.environ, reason='Test Postgres locally')
def test_table_insertion():
    database_service = DatabaseService()

    chunk_list = [
        ChunkEntity(
            chunk_id=str(index),
            chunk='Hello World',
            source='Hello World from ' + str(uuid.uuid4())
        ) for index in range(10)
    ]

    database_service.insert_chunks_into_table(chunk_list)
