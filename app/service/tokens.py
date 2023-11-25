import os
from zipfile import ZipFile

import requests
from fastapi import HTTPException

url = os.environ.get("LEGACY_ENDPOINT_EMPLOYEES")
auth = os.environ.get("HTTP_AUTHORIZATION")
headers = {"Authorization": auth}


def get_employees_tokens():
    if not url:
        raise HTTPException(400, "Employees endpoint URL is not provided!")

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(response.status_code)

    with open("tokens.xlsx.zip", "wb") as f:
        f.write(response.content)

    with ZipFile("tokens.xlsx.zip", "r") as z:
        z.extractall()
