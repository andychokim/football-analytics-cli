# CMPSC431W-CLI

A Python-based Command-Line Interface (CLI) for managing a relational PostgreSQL database seeded with real-world European football data. Built for CMPSC 431W — Database Management Systems.

## Features

- **Full CRUD support** — Insert, delete, update, and search records through an interactive menu
- **Advanced SQL operations** — Aggregate functions (SUM, AVG, COUNT, MIN, MAX), multi-type JOINs (INNER, LEFT, RIGHT, FULL OUTER), GROUP BY, ORDER BY, and nested subqueries
- **Normalized schema** — 9-table relational database with enforced foreign key constraints and no data redundancy
- **Staged ETL pipeline** — CSV data is loaded into staging tables, migrated to the normalized schema, then staging tables are dropped

## Database Schema

| Table | Description |
|---|---|
| `countries` | Country reference data |
| `competitions` | Football leagues/competitions per country |
| `clubs` | Club details, squad size, and home stadium |
| `stadiums` | Stadium names and seating capacity |
| `players` | Player profiles linked to clubs and competitions |
| `games` | Match results with home/away scores and attendance |
| `game_lineups` | Player-club-game lineup records |
| `game_events` | In-game events (goals, cards, substitutions) |
| `appearances` | Individual player appearance statistics |

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

**3. Build the schema and import data** (run each script in pgAdmin 4's Query Tool in order)

| Step | File | Description |
|---|---|---|
| 1 | `PSQL-commands/StagingTables.sql` | Creates 9 staging tables for raw CSV import |
| 2 | `PSQL-commands/IMPORT.sql` | Imports CSV data into staging tables — **edit the file paths first** |
| 3 | `PSQL-commands/CREATE.sql` | Creates the normalized schema tables |
| 4 | `PSQL-commands/INSERT.sql` | Migrates data from staging into the normalized tables |
| 5 | `PSQL-commands/DROP.sql` | Drops the staging tables |

> After step 1, refresh the `public` schema in pgAdmin to confirm `Tables (9)` appears. Use the PSQL Tool (right-click the Tables tab) to run the IMPORT script.

**4. Run the CLI**
```bash
python CLI.py
```

## Usage

On launch, the CLI prompts for your PostgreSQL password and connects to the local database. You are then presented with an interactive menu:

```
Welcome to my CLI interface

Please select an option:
1. Insert Data
2. Delete Data
3. Update Data
4. Search Data
5. Aggregate Functions
6. Sorting
7. Joins
8. Grouping
9. Subqueries
10. Exit
```
