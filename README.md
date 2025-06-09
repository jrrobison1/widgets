# Widgets API

A CRUD REST API for managing Widgets built with FastAPI and SQLite.

## Features

- Create, read, update, and delete widgets
- Widget properties: name (max 64 chars), number of parts, created date, updated date
- Automatic timestamp management
- SQLite database persistence
- Interactive API documentation

## Prerequisites

- Python 3.9 or later
- Poetry (for dependency management)

## Setup

1. **Clone the repository and navigate to the project directory:**
   ```bash
   cd widgets
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

## Running the Application

1. **Start the server:**
   ```bash
   poetry run uvicorn src.widgets.main:app --reload --port 8000
   ```

2. **The API will be available at:**
   - Main API: http://localhost:8000
   - Interactive docs (Swagger UI): http://localhost:8000/docs
   - Alternative docs (ReDoc): http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/widgets` | List all widgets |
| POST   | `/widgets` | Create a new widget |
| GET    | `/widgets/{id}` | Get a specific widget by ID |
| PUT    | `/widgets/{id}` | Update a specific widget |
| DELETE | `/widgets/{id}` | Delete a specific widget |

## Example Usage

### Create a widget:
```bash
curl -X POST "http://localhost:8000/widgets" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Widget", "number_of_parts": 10}'
```

### List all widgets:
```bash
curl -X GET "http://localhost:8000/widgets"
```

### Get a specific widget:
```bash
curl -X GET "http://localhost:8000/widgets/1"
```

### Update a widget:
```bash
curl -X PUT "http://localhost:8000/widgets/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Widget", "number_of_parts": 15}'
```

### Delete a widget:
```bash
curl -X DELETE "http://localhost:8000/widgets/1"
```

## Widget Schema

### Input (Create/Update):
```json
{
  "name": "string (max 64 characters)",
  "number_of_parts": "integer"
}
```

### Response:
```json
{
  "id": "integer",
  "name": "string",
  "number_of_parts": "integer",
  "created_date": "datetime",
  "updated_date": "datetime"
}
```

## Running Tests

Run the test suite:
```bash
poetry run pytest
```

Run tests with verbose output:
```bash
poetry run pytest -v
```

## Database

The application uses SQLite with a local database file (`widgets.db`) that will be created automatically when you first run the application.

## Development

The project follows a layered architecture:
- **Controllers** (`src/widgets/main.py`): HTTP request/response handling
- **Services** (`src/widgets/services.py`): Business logic and data conversion
- **Models** (`src/widgets/models.py`): Database models and configuration
- **Schemas** (`src/widgets/schemas.py`): API request/response models

To run the application in development mode with auto-reload:
```bash
poetry run uvicorn src.widgets.main:app --reload --host 0.0.0.0 --port 8000
```