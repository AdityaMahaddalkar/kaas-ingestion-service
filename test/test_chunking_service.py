import os

import pytest

from services.chunking_service import ChunkingService


@pytest.mark.skipif("LOCAL_TESTING" not in os.environ, reason='Test Kafka connection locally')
def test_config_read():
    chunking_service = ChunkingService()
    assert chunking_service.config is not None
    assert chunking_service.kafka_producer is not None
