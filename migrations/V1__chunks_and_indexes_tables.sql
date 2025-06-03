CREATE TABLE indexes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    source_url TEXT NOT NULL
);

CREATE TABLE chunks (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1536) NOT NULL,
    index_id INTEGER NOT NULL,
    CONSTRAINT fk_index_id
        FOREIGN KEY(index_id)
        REFERENCES indexes(id)
        ON DELETE CASCADE
);
