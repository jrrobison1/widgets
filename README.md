# Widgets API

A CRUD REST API for managing Widgets.

## Features

- Create, read, update, and delete widgets
- A Widget consists of: name (max 64 chars), number of parts, created date, updated date
- The project:
  - Includes unit test coverage
  - Includes a generation script for OpenAPI spec
  - Is PEP8 compliant
  - Passes standard linter tests
  - Passes Bandit security analysis
  - Uses Python type annotations


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

## Configuration

The application can be configured using environment variables:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `HOST` | The host address to bind the server to | `127.0.0.1` (localhost) |
| `PORT` | The port number to run the server on | `8000` |

### Examples:

**Running the app:**
```bash
poetry run python app.py
# or
HOST=127.0.0.1 PORT=8000 poetry run python app.py
```

**The API will be available at:**
- http://localhost:8000


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

### Retrieve widget by id:
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