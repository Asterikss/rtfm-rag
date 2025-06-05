# RTFM (Read The Friendly Manual) RAG Assistant

### Preview

https://github.com/user-attachments/assets/32a712e3-b829-4a56-abb2-f06927a45c05

1. Enter the chosen documentation (index name) you want to embed into the assistant's knowledge base.
2. Proceed with your questions.

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
