# Data Engineering Capstone Project

Data ingestion pipeline from the web to PostgreSQL, developed during the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp).

## Project Structure

```
.
├── docker-compose.yml      # Persistent services (PostgreSQL + pgAdmin)
├── Dockerfile              # Image for data ingestion
├── ingest_data.py          # Ingestion script
├── pyproject.toml          # Dependencies and project configuration
├── uv.lock                 # Exact dependency versions
├── .python-version         
├── .gitignore
└── README.md
```

## Prerequisites

- **Docker & Docker Compose** installed
- **Git** to clone this repository

## Quickstart

### 1. Start PostgreSQL + pgAdmin
In PowerShell (for Windows), navigate to the repository directory and execute:

```bash
docker-compose up
```

Verify that services are online:

```bash
docker-compose ps
```

**Expected output:**
```
NAME          IMAGE              STATUS
pgdatabase    postgres:16        Up 
pgadmin       dpage/pgadmin4     Up
```

### 2. Build the data ingestion image

```bash
docker build -t amazon_ingest:v001 ./
```

### 3. Run the data ingestion

```bash
docker run -it --rm --network=pipeline_default amazon_ingest:v001 --pg-host pgdatabase
```

The script will:
- Connect to PostgreSQL via `pgdatabase` (Docker network hostname)
- Download the raw data from [this repository](https://github.com/patternlover/amazon-raw-data/releases/tag/1.0.0)
- Elaborate the data
- Populate tables in `amazon_purchases`
- Terminate automatically (`--rm`)

**Expected output:**
```
Transactions ingested successfully
Demographics ingested successfully
```

### 4. Verify data in pgAdmin

1. Open http://localhost:8085
2. Login (admin@admin.com:pass)
3. Right click on Servers → Register → Server
4. Fill in the fields:
   - **Name:** `pg`
   - **Hostname:** `pgdatabase`
   - **Port:** `5432`
   - **Username:** `root`
   - **Password:** `root`
5. Navigate: **Servers → pg → Databases → amazon_purchases → Schemas → public → Tables**

## Tech Stack

- **Language:** Python 3.13
- **Package Manager:** `uv`
- **Database:** PostgreSQL 18
- **Database UI:** pgAdmin 4
- **Containerization:** Docker & Docker Compose
- **Main Dependencies:** (see `pyproject.toml`)