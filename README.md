# Read the Friendly Manual RAG Assistant

### Setup locally
1. Have [nix](https://docs.determinate.systems/) and [devenv](https://devenv.sh/) on your system.
2. Enter shell.
```bash
devenv shell
```
  - Or setup an automatic shell by creating `.envrc` based on `.envrc.example.` Then run
    `direnv allow` (requires direnv).
3. Spin up postgres database.
```bash
devenv up # devenv up -d to do it in the background
```
  - If running for the first time run:
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
  or
  ```bash
  uv run -m src.main
  ```
  or
  ```bash
  python -m src.main # assuming venv is actiavted
  ```
