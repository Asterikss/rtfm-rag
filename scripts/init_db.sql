CREATE EXTENSION IF NOT EXISTS "vector";

DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles WHERE rolname = 'developer'
   ) THEN
      CREATE ROLE developer LOGIN PASSWORD 'password';
   END IF;
END
$$;

-- Grant privileges
GRANT USAGE ON SCHEMA public TO developer;
GRANT CREATE ON SCHEMA public TO developer;

-- Grant all privileges on all current tables/sequences
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO developer;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO developer;

-- Ensure future tables/sequences are accessible
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO developer;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO developer;
