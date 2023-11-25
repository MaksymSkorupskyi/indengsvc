import os
from zipfile import ZipFile

import pandas as pd
import requests
from fastapi import HTTPException

from app.dao.database import get_relativity_db_session

url = os.environ.get("LEGACY_ENDPOINT_EMPLOYEES")
auth = os.environ.get("HTTP_AUTHORIZATION")
headers = {"Authorization": auth}


def update_employees_data() -> list[dict]:
    # Fetch the employee data from legacy endpoint
    df: pd.DataFrame = get_employees_tokens()

    employees: list[dict] = [
        get_employee_by_token(row["Token"]) for _, row in df.iterrows()
    ]

    create_users_table()
    write_employees_to_db(employees)

    return employees


def get_employees_tokens() -> pd.DataFrame:
    if not url:
        raise HTTPException(400, "Employees endpoint URL is not provided!")

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(response.status_code)

    employees_excel_table_name = (
        os.environ.get("EMPLOYEES_EXCEL_TABLE_NAME") or "tokens.xlsx"
    )
    # File path for the zip file
    zip_file_path = f"{employees_excel_table_name}.zip"

    with open(zip_file_path, "wb") as f:
        f.write(response.content)

    # Unzip the file
    with ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall()

    # Delete the zip file
    os.remove(zip_file_path)

    # Return the Excel file as Pandas DataFrame
    return pd.read_excel(employees_excel_table_name)


def get_employee_by_token(token: str):
    if not url:
        raise HTTPException(400, "Employees endpoint URL is not provided!")

    response = requests.get(f"{url}/{token}", headers=headers)
    if response.status_code != 200:
        raise HTTPException(response.status_code)

    return response.json()


def create_users_table():
    query = """
    CREATE TABLE IF NOT EXISTS public.users
    (
        id          INTEGER NOT NULL primary key,
        email       varchar(255),
        phone       varchar(255),
        full_name   varchar(255),
        first_name  varchar(255),
        last_name   varchar(255),
        gender      varchar(255),
        birth       DATE
    );

    ALTER TABLE public.users
        OWNER TO jbeambxm;
    """
    with get_relativity_db_session() as session:
        session.execute(query)


def write_employees_to_db(employees: list[dict]):
    # Convert list of dict to dataframe
    df = pd.DataFrame(employees)

    with get_relativity_db_session() as session:
        # Get engine from session
        engine = session.get_bind()

        # Write dataframe to sql
        df.to_sql("users", engine, if_exists="replace", index=False)
