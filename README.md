# Travel-Test-Project
Backend service for managing travel projects and places to visit.

## Prerequisites

Before running the project, make sure you have:

Python 3.12+
PostgreSQL running locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Create a .env file in the project root (use .env.example as reference):

```bash
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/travel_project_db_1
```
- Replace user and password with your PostgreSQL credentials


## API Documentation (Swagger)
After starting the server, open:
- Swagger UI: http://127.0.0.1:8000/docs


## Postman collection
The Postman collection containing all API endpoints and example requests is available here:
https://igor29319965-4677466.postman.co/workspace/%D0%98%D0%B3%D0%BE%D1%80%D1%8C-%D0%9F%D0%BB%D0%B0%D1%85%D0%BE%D1%82%D0%BD%D1%8E%D0%BA's-Workspace~f466574e-62a8-413d-88de-7e0362b7b21d/collection/49379307-636b399c-d890-4109-9bf6-2acf1acff7e3?action=share&creator=49379307&active-environment=49379307-3bf8992b-d3ea-4687-8d82-cf4c902ebee3
