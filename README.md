# speer_assignment

## prerequisite softwares
- Python
- Postgres

## How to run

### Download the required python modules
```pip3 install -r requirements.txt```

### To migrate the databases for this project
```alembic upgrade head```
this will create all the tables required for the project

### How to run
Run this command to start the api server
```uvicorn main:app --reload```

Open this page
```http://127.0.0.1:8000/docs```

The above page contains all the APIs
