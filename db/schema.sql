CREATE TABLE indexes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    source_url TEXT NOT NULL
);

CREATE TABLE chunks (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1536) NOT NULL,
    url TEXT NOT NULL,
    index_id INTEGER NOT NULL,
    CONSTRAINT fk_index_id
        FOREIGN KEY(index_id)
        REFERENCES indexes(id)
        ON DELETE CASCADE
);

CREATE INDEX ON chunks (index_id); -- WHERE

CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);  -- ORDER BY <=>
