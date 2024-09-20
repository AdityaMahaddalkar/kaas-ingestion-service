import json
import uuid

from models.chunk_entity import ChunkEntity


def test_serialization():

    _id = str(uuid.uuid4())
    chunk_content = 'Hello World'
    source = 'dev/null'

    chunk_entity = ChunkEntity(
        chunk_id=_id,
        chunk=chunk_content,
        source=source
    )

    serialized_object = ChunkEntity.serialize(chunk_entity)

    assert b'chunk_id' in ChunkEntity.serialize(chunk_entity)
    assert b'chunk' in ChunkEntity.serialize(chunk_entity)
    assert b'source' in ChunkEntity.serialize(chunk_entity)


def test_deserialize():

    _id = str(uuid.uuid4())
    chunk_content = 'Hello World'
    source = 'dev/null'

    chunk_json = json.dumps({
        'chunk_id': _id,
        'chunk': chunk_content,
        'source': source
    })

    assert 'chunk_id' in ChunkEntity.deserialize(chunk_json).__dict__
    assert 'chunk' in ChunkEntity.deserialize(chunk_json).__dict__
    assert 'source' in ChunkEntity.deserialize(chunk_json).__dict__

