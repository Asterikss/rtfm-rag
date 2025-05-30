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
  primary_key {
    columns = [column.id]
  }
}
schema "public" {
  comment = "standard public schema"
}
