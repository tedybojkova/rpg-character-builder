# ☠️ Grand Line Character Builder

A production-grade One Piece themed RPG character builder REST API built with Flask, SQLAlchemy, and Streamlit.

## What it does

Build and manage your pirate crew for the Grand Line. Create characters with classes like Swordsman, Navigator, and Devil Fruit User, choose from races like Fishman, Giant, and Mink, roll random stats, set your bounty, and write your backstory.

## Project Structure
## Requirements

- Python 3.11+
- pip

## Installation

```bash
git clone https://github.com/tedybojkova/grand-line-builder.git
cd grand_line_builder
pip install -r requirements.txt
```

## Running the API

```bash
py run.py
```

API runs at `http://localhost:5000`

## Running the Frontend

```bash
streamlit run frontend/app.py
```

Open `http://localhost:8501` in your browser.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/characters/` | List all characters |
| POST | `/characters/` | Create a character |
| GET | `/characters/<id>` | Get a character |
| PUT | `/characters/<id>` | Update a character |
| DELETE | `/characters/<id>` | Delete a character |
| GET | `/characters/roll` | Roll random stats |
| GET | `/classes/` | List all classes |
| GET | `/races/` | List all races |

## Running Tests

```bash
pytest
```

Coverage report is generated automatically. Current coverage: **90%**

## Code Quality

```bash
black app/
pylint app/
mypy app/
```

## CI/CD Pipeline

GitHub Actions runs on every push to `main`:
1. Installs dependencies
2. Runs pylint (minimum score 7.0)
3. Runs pytest with coverage (minimum 80%)
4. Uploads coverage report as artifact
5. Builds Docker container

## Architecture

The app follows a layered architecture:

- **Routes** — handle HTTP requests and responses
- **Services** — contain all business logic and validation
- **Models** — SQLAlchemy ORM models with computed properties
- **Exceptions** — custom exception classes for clean error handling

## Technologies

- Flask — REST API framework
- SQLAlchemy — ORM and database management
- Streamlit — frontend UI
- pytest + pytest-cov — testing and coverage
- pylint + mypy + black — code quality
- Sphinx — documentation
- Docker — containerisation
- GitHub Actions — CI/CD pipeline