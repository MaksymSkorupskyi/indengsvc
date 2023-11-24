import requests

url = "https://indengsvc-1-u8804147.deta.app/employees"

headers = {"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="}


def get_employees_tokens():
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open("tokens.xlsx.zip", "wb") as f:
            f.write(response.content)
    else:
        print(f"Error: {response.status_code}")

    import zipfile

    with zipfile.ZipFile("tokens.xlsx.zip", "r") as z:
        z.extractall()
