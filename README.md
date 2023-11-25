# indengsvc API

API service for working with Indeng Inc. employee data

## Getting Started

### Requirements
- Python 3.11+
- Poetry for dependency management

## Installation

Clone the repository and navigate to the project directory:
```
git clone https://github.com/MaksymSkorupskyi/indengsvc.git
cd indengsvc-api
```

Install dependencies with Poetry:
```
poetry config virtualenvs.in-project true
poetry install
```


## DEV setup

You need to set environment variables:
- `USERNAME` - User Name
- `PASSWORD`- User Password
- `DB_CONN` - Connection URI to the database 
- `LEGACY_ENDPOINT_EMPLOYEES` - Legacy API endpoint 
- `HTTP_AUTHORIZATION` - HTTP Basic Auth 

### Database environment variables setup
```
export USERNAME="<username>"
export PASSWORD="<password>"
export DB_CONN=postgresql://${USER}:<password>@localhost:5432/jbeambxm

export LEGACY_ENDPOINT_EMPLOYEES="https://indengsvc-1-u8804147.deta.app/employees"
export HTTP_AUTHORIZATION="<auth_string>"
```


## Usage

### Start the API server:
```
poetry run uvicorn app.main:app --reload --port 8003
```
The API will be available at http://127.0.0.1:8003

Documentation is available at http://127.0.0.1:8003/docs

## API endpoints:

#### Update Employees data from legacy API:
```
curl -X 'GET' \
  'http://localhost:8003/v1/employees' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic YWRtaW46cGFzc3dvcmQ='
```

#### Get all users:
```
curl -X 'GET' \
  'http://localhost:8003/v1/users' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic YWRtaW46cGFzc3dvcmQ='
```

#### Get user by id:
```
curl -X 'GET' \
  'http://localhost:8003/v1/users/1000' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic YWRtaW46cGFzc3dvcmQ='
 ```
## Testing
Run tests:
```
poetry run pytest -vv
```
