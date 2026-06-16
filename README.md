# Football-CLI

A Python-based Command-Line Interface (CLI) for managing a relational PostgreSQL database seeded with real-world European football data. Built for CMPSC 431W — Database Management Systems originally.

## Project Background

This was an academic project with the following requirements:
- Source a real-world dataset from Kaggle
- Normalize the schema to Third Normal Form (3NF)
- Load the data into PostgreSQL via a staged ETL pipeline
- Build a non-engineer-friendly CLI supporting basic query operations

The source dataset was a European football dataset from Kaggle (transfermarkt). The CSV files had three transitive dependencies which I resolved: countries, stadiums, and positions — see [Normalization Decisions](#normalization-decisions).

## Features

- **Full CRUD support** — Insert, delete, update, and search records through an interactive menu
- **Advanced SQL operations** — Aggregate functions (SUM, AVG, COUNT, MIN, MAX), multi-type JOINs (INNER, LEFT, RIGHT, FULL OUTER), GROUP BY, ORDER BY, and nested subqueries
- **Normalized schema** — 8-table relational database in 3NF with enforced foreign key constraints
- **Staged ETL pipeline** — CSV data is loaded into staging tables, transformed, migrated to the normalized schema, then staging tables are dropped

## Database Schema

| Table | Description |
|---|---|
| `countries` | Country reference data — extracted from competitions CSV to resolve a 3NF violation |
| `competitions` | Football leagues/competitions per country |
| `stadiums` | Stadium names and seating capacity — extracted from clubs CSV to resolve a 3NF violation |
| `clubs` | Club details, squad size, and home stadium |
| `positions` | Player sub-position to position mapping — extracted from players CSV to resolve a 3NF violation |
| `players` | Player profiles linked to clubs and competitions |
| `games` | Match results with home/away scores and attendance |
| `game_lineups` | Player-club-game lineup records |

## Normalization Decisions

The raw Kaggle CSV files contained three transitive dependencies that violated 3NF:

**1. `countries` table**
In the raw `competitions.csv`, `country_name` was stored alongside `country_id` in the same row. This created a transitive dependency:

```
competition_id → country_id → country_name
```

`country_name` depended on `country_id`, not directly on `competition_id`. Extracting `countries` as its own table removes this dependency — `competitions` now stores only `country_id` as a foreign key.

**2. `stadiums` table**
In the raw `clubs.csv`, `stadium_seats` was stored as an attribute of each club. This created a transitive dependency:

```
club_id → stadium_name → stadium_seats
```

`stadium_seats` is a fact about the stadium, not the club. Keeping it in `clubs` would also duplicate the same seat count across every club that plays at the same venue. Extracting `stadiums` resolves both the 3NF violation and the redundancy.

**3. `positions` table**
In the raw `players.csv`, both `sub_position` and `position` were stored on each player row. This created a transitive dependency:

```
player_id → sub_position → position
```

`position` is always determined by `sub_position` (e.g., "Attacking Midfield" and "Defensive Midfield" both always map to "Midfield"). Storing `position` directly on each player row is redundant. Extracting `positions` as its own table removes this dependency — `players` now stores only `sub_position` as a foreign key, and `position` is retrieved via JOIN when needed. `sub_position` serves as the natural primary key since it is a fixed, unique vocabulary of values with no need for a surrogate ID.

**Tables dropped from the original dataset**
`game_events`, `club_games`, and `appearances` were present in the raw CSV files and staging tables but excluded from the normalized schema to keep scope focused on the core relational structure.

## ETL Pipeline

Data is loaded through a 5-step staged pipeline run manually in pgAdmin 4:

| Step | File | Description |
|---|---|---|
| 1 | `PSQL-commands/StagingTables.sql` | Creates staging tables that mirror the raw CSV structure |
| 2 | `PSQL-commands/IMPORT.sql` | Loads CSV data into staging tables via `\copy` — **edit file paths first** |
| 3 | `PSQL-commands/CREATE.sql` | Creates the normalized schema tables with FK constraints |
| 4 | `PSQL-commands/INSERT.sql` | Migrates and transforms data from staging into the normalized tables |
| 5 | `PSQL-commands/DROP.sql` | Drops all staging tables |

Key transformations in `INSERT.sql`:
- `countries` is derived from `staging_competitions` using `SELECT DISTINCT` — it did not exist as its own CSV
- Stadium deduplication is handled with `ROW_NUMBER() OVER (PARTITION BY stadium_name ORDER BY stadium_seats DESC)` — the raw data had multiple rows per stadium with varying seat counts
- A second stadium pass inserts venues that appeared in games but not in clubs (with `NULL` seat count)
- FK insertion order is respected: countries → competitions → stadiums → clubs → players → games → game_lineups

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/) with [pgAdmin 4](https://www.pgadmin.org/)
- `psycopg2` Python package

```bash
pip install psycopg2
```

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/andychokim/CMPSC431W-CLI.git
cd CMPSC431W-CLI
```

**2. Set up a PostgreSQL server in pgAdmin 4**
- Register a new server with your chosen server name, hostname, and password
- Navigate to: your server → Databases → postgres → Schemas → public

**3. Run the ETL pipeline** (run each script in pgAdmin 4's Query Tool in order)

> Use the PSQL Tool for `IMPORT.sql` — the `\copy` command requires it. Edit the file paths in `IMPORT.sql` to point to your local `csv_files/` directory before running.
> For other .sql commands, use Query Tool.

**4. Run the CLI**
```bash
python CLI.py
```

## Usage

On launch, the CLI prompts for your PostgreSQL password and connects to the local database. You are then presented with an interactive menu:

```
Welcome to my CLI interface

Please select an option:
0. Insert Data
1. Delete Data
2. Update Data
3. Search Data
4. Aggregate Functions
5. Sorting
6. Joins
7. Grouping
8. Subqueries
9. Exit
```

## Project Structure

```
CMPSC431W-CLI/
├── CLI.py                  # Entry point — connection and menu loop
├── queries.py              # Centralized SQL query templates
├── DMLs/                   # DML operations package
│   ├── crud.py             # Insert, delete, update (basic write ops)
│   ├── search.py           # Search with table/field/operator validation
│   ├── aggregation.py      # Aggregate functions, sorting, grouping
│   └── advanced.py         # Joins and subqueries
├── PSQL-commands/          # SQL scripts for the ETL pipeline
│   ├── StagingTables.sql
│   ├── IMPORT.sql
│   ├── CREATE.sql
│   ├── INSERT.sql
│   └── DROP.sql
└── csv_files/              # Raw Kaggle CSV source data
```
