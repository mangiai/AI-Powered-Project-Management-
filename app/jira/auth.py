from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from requests.auth import HTTPBasicAuth
import httpx

# Configuration for Jira API
JIRA_BASE_URL = "https://robertwilkpro.atlassian.net"
JIRA_API_URL = f"{JIRA_BASE_URL}/rest/api/3/project"
# email = "robert.wilk.pro@gmail.com"
# api_token = "ATATT3xFfGF0Tuspql4vEQ1t1c7qyeXt89llF0D9xNh3Jk-EWwHwZFvDUAV6xttci3MTqDeJDhMdoC4c-5oSzooH7SXoHnb7n7TPWHn7p26f6rbiQkdTo7ML9T0934U3Yz4QHxYBrtqBrnTuSEtiF4Pm3Ri8GZG2mpNvaRRnIUfAL3HdyTdrWZw=C9D1C712"
JIRA_PROJECT_KEY = "EK"
payload = {
        "maxResults": 2000,  # Adjust as per your needs
        "fields": "*all"
    }

async def get_projects_from_jira(email, api_token):
    async with httpx.AsyncClient(auth=(email, api_token)) as client:
        response = await client.get(f"{JIRA_BASE_URL}/rest/api/3/project")
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

async def get_project_from_jira(email, api_token, projectIDorKey):
    async with httpx.AsyncClient(auth=(email, api_token)) as client:
        response = await client.get(f"{JIRA_BASE_URL}/rest/api/3/project/{projectIDorKey}")
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

async def get_issues_from_jira(email, api_token):
    async with httpx.AsyncClient(auth=(email, api_token)) as client:
        response = await client.get(f"{JIRA_BASE_URL}/rest/api/3/search", params=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

