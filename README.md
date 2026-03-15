# Data Monitor AI Python Backend

Production-ready FastAPI base structure.

## Project Structure and Purpose

```text
.
├── app/
│   ├── main.py                 # FastAPI app creation and router registration
│   ├── api/
│   │   └── v1/                 # Versioned API layer (HTTP routes only)
│   ├── core/                   # App-wide config, logging, shared infrastructure
│   ├── db/                     # Database connection/client setup by database type
│   │   ├── mysql/
│   │   ├── oracle/
│   │   ├── mongodb/
│   │   └── mssql/
│   ├── repositories/           # DB query/data-access layer (SQL/NoSQL operations)
│   │   ├── mysql/
│   │   ├── oracle/
│   │   ├── mongodb/
│   │   └── mssql/
│   ├── services/               # Business logic layer (uses repositories)
│   │   ├── mysql/
│   │   ├── oracle/
│   │   ├── mongodb/
│   │   └── mssql/
│   └── schemas/                # Pydantic request/response models
├── tests/                      # Unit/integration tests
├── requirements.txt            # Runtime + dev dependencies
├── pyproject.toml              # Tooling config (ruff, mypy, pytest)
├── .env.example                # Environment variable template
└── run.py                      # Local entrypoint for uvicorn
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
python run.py
```

Or:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Test

```bash
pytest
```

## Lint

```bash
ruff check .
```

## Folder Usage Rules

- `app/api/v1/`: Keep route handlers thin. No direct DB queries here.
- `app/services/`: Put business logic and orchestration here.
- `app/repositories/`: Put raw data access/query logic here.
- `app/db/`: Only connection/session/client initialization and helpers.
- `app/schemas/`: Put request/response payload models and validation.
- `tests/`: Mirror `app/` structure for predictable test discovery.

## Docker Setup
```bash
##for windows
wsl --install

## Download docker from docker official website
## After Downloading and completing the setup run the following 

## Here is the link btw https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-win-amd64


docker comopose version ##To check the version and verify the install
##Navigate to your project root and open cmd there(can be done using the top path display tab and run the following
docker compose up --build -d


#for linux

sudo pacman -S docker docker-compose
sudo systemctl enable --now docker.service
docker compose up --build -d

```

## How to Maintain This Repository

When creating new folders or files, follow this checklist:

1. Decide layer first:
   - API endpoint file -> `app/api/v1/`
   - Business rule -> `app/services/<db>/`
   - Data access -> `app/repositories/<db>/`
   - DB connector/client code -> `app/db/<db>/`
   - Request/response model -> `app/schemas/`
2. Keep naming consistent:
   - Use lowercase snake_case for filenames.
   - Name by feature, e.g. `user_routes.py`, `user_service.py`, `user_repository.py`.
3. Register new routers:
   - Add route module in `app/api/v1/`.
   - Include it from `app/api/v1/router.py`.
4. Add configuration safely:
   - Add new env keys in `app/core/config.py`.
   - Add matching placeholders in `.env.example`.
5. Add tests with each change:
   - Create tests under `tests/` matching the feature path.
   - Cover both success and failure cases for APIs/services.
6. Validate before commit:
   - `pytest`
   - `ruff check .`

## Recommended Development Flow for New Features

1. Add/extend schema in `app/schemas/`.
2. Add repository method in `app/repositories/<db>/`.
3. Add service method in `app/services/<db>/`.
4. Add API endpoint in `app/api/v1/`.
5. Register router in `app/api/v1/router.py`.
6. Add tests in `tests/`.
