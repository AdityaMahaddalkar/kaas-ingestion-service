import os

import pytest

from services.vectorization_service import VectorizationService


@pytest.mark.skipif("LOCAL_TESTING" not in os.environ, reason='Test Marqo locally')
def test_config_read():
    vectorization_service = VectorizationService()
    assert vectorization_service.config is not None
    assert vectorization_service.mq is not None
