# RTFM (Read The Friendly Manual) RAG Assistant (api)

### Preview

https://github.com/user-attachments/assets/e0907418-378f-42df-a252-3580ce08e9bf

1. Choose the documentation (index name) you want to embed into the assistant's knowledge base.
2. Proceed with your questions.

(UI is at - [repo](https://github.com/Asterikss/rtfm-rag-ui))

### Embeddings Visualization

<div align="center">
  <img src="https://github.com/user-attachments/assets/0ce34f6c-eb71-43db-a7a9-047844e930d0" alt="embeddings_visualization" width="560" height="460"/>
</div>

### Setup Locally
1. Make sure you have [nix](https://docs.determinate.systems/) and [devenv](https://devenv.sh/getting-started/) on your system.
2. Enter shell.
```bash
devenv shell
```
  - Or setup an automatic shell by creating `.envrc` based on `.envrc.example`. Then run
    `direnv allow` (requires `direnv`).
3. Spin up the PostgreSQL database.
```bash
devenv up # devenv up -d to do it in the background
```
- If running for the first time, run:
    ```bash
    psql -h localhost -U $USER -d rtfm-rag -f scripts/init_db.sql
    ```
- Then:
    ```bash
    flyway migrate
    ```
4. Launch the api.
  ```bash
  run
  ```
  - or
    ```bash
    run-prod
    ```
  - or
    ```bash
    uvicorn src.main:app --port 8032
    ```
  - or
    ```bash
    uv run -m src.main
    ```
  - or
    ```bash
    python -m src.main # assuming venv is activated
    ```

### Local Processing
- Process links and store data locally:
```python
uv run -m scripts.scrape_data <url> [--debug] [--max-depth N] [--max-pages N]
```
- Ingest locally scraped data:
```python
uv run -m scripts.manual_ingest <index_name> [--debug] [--max-chunks N]
```
