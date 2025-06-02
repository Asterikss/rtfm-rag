table "indexes" {
  schema = schema.public
  column "id" {
    null = false
    type = serial
  }
  column "name" {
    null = false
    type = text
  }
  column "source_url" {
    null = false
    type = text
  }
  primary_key {
    columns = [column.id]
  }
}

table "chunks" {
  schema = schema.public
  column "id" {
    null = false
    type = serial
  }
  column "content" {
    null = false
    type = text
  }
  column "embedding" {
    null = false
    type = sql("public.vector(1536)")
  }
  column "index_id" {
    null = false
    type = int
  }
  primary_key {
    columns = [column.id]
  }
  foreign_key "index_id" {
    columns = [column.index_id]
    ref_columns = [table.indexes.column.id]
    on_delete = CASCADE
  }
}
schema "public" {
  comment = "standard public schema"
}
