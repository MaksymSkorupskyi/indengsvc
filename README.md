# indengsvc API

API service for working with Indeng Inc. employee data

## Getting Started

### Requirements
- Python 3.11+
- Poetry for dependency management

## Installation

Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/MaksymSkorupskyi/indengsvc.git
cd indengsvc-api
```

Install dependencies with Poetry:
```bash
poetry config virtualenvs.in-project true
poetry install
```

## Additional Information
The API supports HTTP Basic Authentication. 


## DEV setup

You need to set environment variables:
- `USERNAME` - User Name
- `PASSWORD`- User Password
- `DB_CONN` - Connection URI to the database 
- `LEGACY_ENDPOINT_EMPLOYEES` - Legacy API endpoint 
- `HTTP_AUTHORIZATION` - HTTP Basic Auth 
##### Note: For demo it's ok to use Enviroment variables, but for production we must use secrets.

### Environment variables setup
```bash
export USERNAME="<username>"
export PASSWORD="<password>"
export DB_CONN=postgresql://${USER}:<password>@localhost:5432/jbeambxm

export LEGACY_ENDPOINT_EMPLOYEES="https://indengsvc-1-u8804147.deta.app/employees"
export HTTP_AUTHORIZATION="<auth_string>"
```


## Usage

### Start the API server:
```bash
poetry run uvicorn app.main:app --reload --port 8003
```
The API will be available at http://127.0.0.1:8003

Documentation is available at http://127.0.0.1:8003/docs

## API endpoints:

#### Update Employees data from legacy API:
```bash
curl -X 'GET' \
  'http://localhost:8003/v1/employees' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic YWRtaW46cGFzc3dvcmQ='
```
Response:
```text
"Employees data from legacy API has been successfully updated in `users` table"
```
* Note: 
Make sure that you've fetch the last updated data from the Legacy API before calling 
folowing endpoints:

#### Get all users:
```bash
curl -X 'GET' \
  'http://localhost:8003/v1/users' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic YWRtaW46cGFzc3dvcmQ='
```
Response example:
```json
[
  {
    "id": 4675,
    "email": "kartoplya.greypfrutіvna@indeng.io",
    "phone": "+3809905751574",
    "full_name": "Картопля Грейпфрутівна",
    "first_name": "Картопля",
    "last_name": "Грейпфрутівна",
    "gender": "female",
    "birth": "1986-11-08",
    "reports": 1400,
    "position": "Support Engineer",
    "hired": "2019-01-15",
    "salary": "$1400",
    "team": "Support"
  },
  {
    "id": 8266,
    "email": "abrikos.mandarinovich@indeng.io",
    "phone": "+3809906892160",
    "full_name": "Абрикос Мандаринович",
    "first_name": "Абрикос",
    "last_name": "Мандаринович",
    "gender": "male",
    "birth": "1985-11-06",
    "reports": 1400,
    "position": "Support Engineer",
    "hired": "2021-07-16",
    "salary": "$1600",
    "team": "Support"
  },
    ...
  {
    "id": 6050,
    "email": "apelsin.greypfrutovich@indeng.io",
    "phone": "+3809907580312",
    "full_name": "Апельсин Грейпфрутович",
    "first_name": "Апельсин",
    "last_name": "Грейпфрутович",
    "gender": "male",
    "birth": "1993-12-08",
    "reports": 1400,
    "position": "Support Engineer",
    "hired": "2019-08-07",
    "salary": "$1100",
    "team": "Support"
  }
]
```

#### Get user by id:
```bash
curl -X 'GET' \
  'http://localhost:8003/v1/users/1000' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic YWRtaW46cGFzc3dvcmQ='
 ```
Response example:
```json
{
  "id": 1900,
  "email": "abrikos.vinogradovich@indeng.io",
  "phone": "+3809902324770",
  "full_name": "Абрикос Виноградович",
  "first_name": "Абрикос",
  "last_name": "Виноградович",
  "gender": "male",
  "birth": "1985-11-28",
  "reports": 1000,
  "position": "Head of Legal",
  "hired": "2021-12-07",
  "salary": "$5000",
  "team": "Legal"
}
```
## Testing
Run tests:
```
poetry run pytest -vv
```
