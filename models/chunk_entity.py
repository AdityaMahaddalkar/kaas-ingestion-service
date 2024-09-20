import json

from pydantic import BaseModel


class ChunkEntity(BaseModel):
    chunk_id: str
    chunk: str
    source: str

    @classmethod
    def serialize(cls, obj):
        return json.dumps(obj.__dict__).encode('utf-8')

    @classmethod
    def deserialize(cls, data):
        return ChunkEntity(**json.loads(data))
