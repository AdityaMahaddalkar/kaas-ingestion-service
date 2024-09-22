CREATE_CHUNKS_TABLE = '''
CREATE TABLE IF NOT EXISTS {table} (
    chunk_id VARCHAR(40) PRIMARY KEY,
    chunk TEXT NOT NULL,
    source TEXT NOT NULL
)
'''

INSERT_CHUNKS_INTO_TABLE = '''
INSERT INTO {table} ({cols})
VALUES (%s, %s, %s)
'''

SELECT_CHUNKS_WHERE_ID_IN = '''
SELECT chunk_id, chunk, source
FROM {table}
WHERE chunk_id IN {search_tuple_str}
'''