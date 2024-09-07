import uvicorn
import httpx, base64
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from models.users import User
from models.projects import Project
from models.programs import Program
from models.portfolios import Portfolio
from models.risks import Risk 
from models.roadmaps import Roadmap
from models.steward import Steward
from models.wbs import WBS
from models.baseline import Baseline
from models.lifecycle import Lifecycle
from models.ftasks import FTask
from models.costs import Cost
from models.products import Product
from models.releases import Release
from models.sprints import Sprint
from models.stories import Story
from models.epics import Epic
from models.bots import Bot
from models.chats import Chat
from models.msgs import Msg
from models.uploadedcsvs import UploadedCSV
from models.userqueries import UserQuery
from models.generatedsqls import GeneratedSql
from models.rephrasedresponses import RephrasedResponse
from models.kpiresults import KPIResult

from config import engine, connect_to_db, close_db_connection, SessionLocal, POSTGRES_CONNECTION, get_db
from routes.ftasks import ftask_router
from routes.users import user_router
from routes.kpi import kpi_router
from routes.lifecycle import lifecycle_router
from routes.projects import project_router
from routes.programs import program_router
from routes.portfolios import portfolio_router
from routes.steward import steward_router
from routes.risks import risk_router
from routes.roadmaps import roadmap_router
from routes.costs import cost_router
from routes.products import product_router
from routes.releases import release_router
from routes.sprints import sprint_router
from routes.stories import story_router
from routes.epics import epic_router
from routes.bots import bot_router
from routes.msgs import msg_router
from routes.chats import chat_router
from routes.uploadedcsvs import uploadedcsv_router
from routes.generatedsqls import generatedsql_router
from routes.kpiresults import kpiresult_router
from routes.userqueries import userquery_router
from routes.uploadallcsv import upload_router


from routes.chatbot import chatbot_router

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from jira.auth import *
import requests,json
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker
import asyncio
import psycopg2
import jpype
import os
from datetime import datetime
from typing import Dict, List

from auth.auth_handler import sign_jwt
from schemas.users import UserCreateSchema, UserLoginSchema
import mpxj
import csv

if not jpype.isJVMStarted():
    jpype.startJVM()

metadata = MetaData(schema='public')

User.metadata.create_all(bind=engine)
Lifecycle.metadata.create_all(bind=engine)
Project.metadata.create_all(bind=engine)
Program.metadata.create_all(bind=engine)
Portfolio.metadata.create_all(bind=engine)
Roadmap.metadata.create_all(bind=engine)
Risk.metadata.create_all(bind=engine)
Steward.metadata.create_all(bind=engine)
WBS.metadata.create_all(bind=engine)
Baseline.metadata.create_all(bind=engine)
FTask.metadata.create_all(bind=engine)
Cost.metadata.create_all(bind=engine)
Product.metadata.create_all(bind=engine)
Release.metadata.create_all(bind=engine)
Sprint.metadata.create_all(bind=engine)
Story.metadata.create_all(bind=engine)
Epic.metadata.create_all(bind=engine)
Bot.metadata.create_all(bind=engine)
Chat.metadata.create_all(bind=engine)
Msg.metadata.create_all(bind=engine)
UploadedCSV.metadata.create_all(bind=engine)
UserQuery.metadata.create_all(bind= engine)
GeneratedSql.metadata.create_all(bind= engine)
RephrasedResponse.metadata.create_all(bind= engine)
KPIResult.metadata.create_all(bind= engine)

def init_app():

    origins= [
        "*"
    ]

    app = FastAPI(
        title="StewardIQ App",
        description="A simple API to manage tasks",
        version="1.0.0",
        docs_url="/docs",
        redoc_url='/redoc',
        openapi_url="/api/openapi.json",

    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"]
    )

  
    app.include_router(user_router, prefix='/api', tags=['users'])
    app.include_router(lifecycle_router, prefix='/api', tags=['lifecycle'])
    app.include_router(kpi_router, prefix='/api', tags=['kpi'])
    app.include_router(project_router, prefix='/api', tags=['projects'])
    app.include_router(program_router, prefix='/api', tags=['programs'])
    app.include_router(portfolio_router, prefix='/api', tags=['portfolios'])
    app.include_router(risk_router, prefix='/api', tags=['risks'])
    app.include_router(roadmap_router, prefix='/api', tags=['roadmaps'])
    app.include_router(steward_router, prefix='/api', tags=['steward'])
    app.include_router(ftask_router, prefix='/api', tags = ['ftasks'])
    app.include_router(cost_router, prefix = '/api', tags = ['costs'])
    app.include_router(product_router, prefix = '/api', tags=['products'])
    app.include_router(release_router, prefix = '/api', tags=['releases'])
    app.include_router(sprint_router, prefix='/api', tags=['sprints'])
    app.include_router(story_router, prefix='/api', tags=['stories'])
    app.include_router(epic_router, prefix='/api', tags=['epics'])
    app.include_router(chatbot_router,prefix='/api',tags=['chatbot'])
    app.include_router(bot_router,prefix='/api', tags=['bots'])
    app.include_router(msg_router,prefix='/api',tags=['messages'])
    app.include_router(chat_router,prefix='/api', tags=['chats'])
    app.include_router(uploadedcsv_router,prefix='/api', tags=['uploadedcsvs'])
    app.include_router(userquery_router,prefix='/api',tags=['userqueries'])
    app.include_router(generatedsql_router,prefix='/api', tags=['generatedsqls'])
    app.include_router(kpiresult_router,prefix='/api',tags=['kpiresults'])
    app.include_router(upload_router, prefix='/api', tags=['uploadallcsvs'])






    @app.get("/")
    async def read_root():
        return {"message": "Hello from FastAPI!"}
    
    baseURL = 'http://localhost:8000'
    headers = {"Content-Type": "application/json", "Accept": "*/*"}
    
    @app.post("/signup")
    async def signup(user:UserCreateSchema):
        async with httpx.AsyncClient() as client:
            json_data = user.__dict__
            try:
                await client.post(f'{baseURL}/api/users/', json=json_data, headers=headers)
            
                return {
                    "token": sign_jwt(user.email),
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_system_admin": user.is_system_admin,
                    "is_fte": user.is_fte,
                    "is_business_steward": user.is_business_steward,
                    "is_resource": user.is_resource,
                    "is_onshore": user.is_onshore,
                    "access_level": user.access_level
                    }
            except Exception as e:
                return {
                    "Error ": str(e)
                }
    
    async def check_user(data: UserLoginSchema):
        users = []
        async with httpx.AsyncClient() as client:
            users = (await client.get(f'{baseURL}/api/users/', headers=headers)).json()['response']
            
        for user in users:
            print(user)
            if user['email'] == data.email and user['password'] == data.password:
                return user
        return None
    
    @app.post("/login")
    async def login(user: UserLoginSchema):
        exist_user = await check_user(user)
        if exist_user == None:
            return {
                "error": "Email or Password is incorrect!"
            }
        return {
            "token": sign_jwt(user.email),
            "email": exist_user['email'],
            "username": exist_user['username'],
            "first_name": exist_user['first_name'],
            "last_name": exist_user['last_name'],
            "is_system_admin": exist_user['is_system_admin'],
            "is_fte": exist_user['is_fte'],
            "is_business_steward": exist_user['is_business_steward'],
            "is_resource": exist_user['is_resource'],
            "is_onshore": exist_user['is_onshore'],
            "access_level": exist_user['access_level']
        }
    
    async def get_file_Content(file: str):
        from net.sf.mpxj.reader import UniversalProjectReader
        project = UniversalProjectReader().read(file)
        url = f'{baseURL}/api/ftasks/'  # Fixed typo "taks" to "tasks"
        proj_id = -1
        async with httpx.AsyncClient() as client:
            for id, task in enumerate(project.getTasks()):
                if id == 0:
                    continue
                if id == 1:
                    ele = {
                        'name': str(task.getName()),
                        'description': str(task.getNotes()),
                        'retro': '',
                        'is_completed': False,
                        'StartDate': str(task.getStart().toLocalDate().toString()),  # Converts Java String to Python String
                        'EndDate': str(task.getFinish().toLocalDate().toString()),  # Converts Java String to Python String                    
                    }
                    proj_id = (await client.post(url = f'{baseURL}/api/project/', json=ele, headers=headers)).json()['response']['id']
                    print(proj_id)
                    continue
                ele = {
                    'wbs': str(task.getWBS()),  # Converts Java String to Python String
                    'name': str(task.getName()),  # Converts Java String to Python String
                    'description': str(task.getNotes()),  # Converts Java String to Python String
                    'current_status': 1,
                    # 'Resource': str(task.getResourceAssignments()[0].getTask().getName().toString()),  # Converts Java String to Python String
                    'Resource': '',
                    'ActualResource': '',
                    'PlannedStartDate': str(task.getStart().toString()),  # Converts Java String to Python String
                    'PlannedEndDate': str(task.getFinish().toString()),  # Converts Java String to Python String
                    'ActualStartDate': str(task.getStart().toString()),  # Converts Java String to Python String
                    'ActualEndDate': str(task.getFinish().toString()),  # Converts Java String to Python String
                    'action': '',
                    'predecessor_successor': '',
                    'progress': 0,
                    'proj_id': proj_id
                }
                await client.post(url, json=ele, headers=headers)
        return JSONResponse(status_code=200, content={"message": "Successfully dumped the data from MPP file!"})

    def get_file_info(path: str, filename: str) -> Dict[str, str]:
        """
        Get information about a file
        """
        file_path = os.path.join(path, filename)
        file_info = os.stat(file_path)

        # Get file extension
        file_ext = os.path.splitext(filename)[1]
        if file_ext == '':
            file_ext = 'unknown'

        return {
            "filename": filename,
            "last_modified": datetime.fromtimestamp(file_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            "extension": file_ext
        }

    async def get_xls_file_content(file: str):
        with open(file, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            list_from_csv = list(reader)
            async with httpx.AsyncClient() as client:
        
                for row in list_from_csv:
                    dict_from_csv = dict(row)
                    print(dict_from_csv)
                    username = dict_from_csv['Assignee (doing the work)']
                    projectPhase = dict_from_csv['Project Phase']
                    ele = {
                        'username': username
                    }
                    user_id = None
                    current_status = 1
                    try:
                        connection = await connect_to_db()
                        query = f'select id from users where username = \'{username}\''
                        user_id = await connection.fetch(query)
                        query = f'select id from lifecycle where phase = \'{projectPhase}\''
                        current_status = (await connection.fetch(query))[0]['id']
                        await close_db_connection(connection)
                    except Exception as e:
                        return JSONResponse(status_code=500, content={"message2": str(e)})
                    # print(user_id)
                    assinged_to = None
                    if len(user_id) == 0:
                        assinged_to = (await client.post(f'{baseURL}/api/users/', json=ele, headers=headers)).json()['response']['id']
                    else:
                        assinged_to = user_id[0]['id']
                    
                    date_format = "%m/%d/%Y"

                    ele = {
                        'type': dict_from_csv['Log Type'],
                        'name': 'Issue',
                        'iwantto': dict_from_csv['Description (needs to read: "I need this...so I can accomplish this...)'],
                        'assigned_to': assinged_to,
                        'current_status': current_status,
                        'velocityPoints': dict_from_csv['Velocity Points in Sprint (Story points Dynamic): 1 day effort = 1 point; a SPRINT = 10 days'],
                        'sprint': dict_from_csv['Sprint (usually 2 weeks): 1 FTE = 5 working days (1 day = 1 velocity point, e.g. 5 days = 5 v-points)'],
                        'taskDuration': dict_from_csv['Task Duration'],
                        'actualStartDate': str(datetime.strptime(dict_from_csv['Sprint Start date(2week sprint)'], date_format).date()),
                        'actualEndDate': str(datetime.strptime(dict_from_csv['End date'], date_format).date()),
                        'plannedStartDate': str(datetime.strptime(dict_from_csv['Scheduled Start Date(perfect senario)'], date_format).date()),
                        'plannedEndDate': str(datetime.strptime(dict_from_csv['Scheduled End Date'], date_format).date()),                        
                    }
                    
                    print(ele)
                    await client.post(f'{baseURL}/api/stories/', json = ele, headers=headers)
            
        return JSONResponse(status_code=200, content={"message": "Successfully Dumped the data from csv format jira file!"})
                
    @app.post("/api/uploadjira")
    async def create_upload_jirafile(file: UploadFile = File(...)):
        try:
            date_today = datetime.now().strftime('%Y-%m-%d')
            directory = f'./uploads/{date_today}'
            if not os.path.exists(directory):
                os.makedirs(directory)
            # Save the file with the date and time included in the filename
            date_time_now = datetime.now().strftime('%H%M%S%f')
            filename = f"{date_time_now}_{file.filename}"
            file_location = f"{directory}/{filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(await file.read())
            
            return await get_xls_file_content(file_location)
        
        except Exception as e:
            return JSONResponse(status_code=500, content={"message1": str(e)})

    @app.post("/api/upload", summary="Upload mpp file")
    async def create_upload_file(file: UploadFile = File(...)):
        try:
            # Create a directory named with today's date
            date_today = datetime.now().strftime('%Y-%m-%d')
            directory = f'./uploads/{date_today}'

            if not os.path.exists(directory):
                os.makedirs(directory)

            # Save the file with the date and time included in the filename
            date_time_now = datetime.now().strftime('%H%M%S%f')
            filename = f"{date_time_now}_{file.filename}"
            file_location = f"{directory}/{filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(await file.read())
            
            return await get_file_Content(file_location)
            
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": str(e)})
    
    async def get_csvfile_Content(file: str):
        url = f'{baseURL}/api/ftasks/'  # Fixed typo "taks" to "tasks"
        with open(file, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            list_from_csv = list(reader)

            async with httpx.AsyncClient() as client:
                
                for row in list_from_csv:
                    dict_from_csv = dict(row)
                    print(dict_from_csv)
                    # if id == 1:
                    #     ele = {
                    #         'name': str(task.getName()),
                    #         'description': str(task.getNotes()),
                    #         'retro': '',
                    #         'is_completed': False,
                    #         'StartDate': str(task.getStart().toLocalDate().toString()),  # Converts Java String to Python String
                    #         'EndDate': str(task.getFinish().toLocalDate().toString()),  # Converts Java String to Python String                    
                    #     }
                    #     proj_id = (await client.post(url = f'{baseURL}/api/project/', json=ele, headers=headers)).json()['response']['id']
                    #     print(proj_id)
                    #     continue
                    date_format = "%m/%d/%Y"
                    ele = {
                        'wbs': dict_from_csv['wbs'],  # Converts Java String to Python String
                        'name': dict_from_csv['name'],  # Converts Java String to Python String
                        'description': dict_from_csv['description'],  # Converts Java String to Python String
                        'current_status': dict_from_csv['current_status'],
                        'Resource': dict_from_csv['Resource'],
                        'ActualResource': dict_from_csv['ActualResource'],
                        'PlannedStartDate': str(datetime.strptime(dict_from_csv['PlannedStartDate'], date_format).date()),  # Converts Java String to Python String
                        'PlannedEndDate': str(datetime.strptime(dict_from_csv['PlannedEndDate'], date_format).date()),  # Converts Java String to Python String
                        'ActualStartDate': str(datetime.strptime(dict_from_csv['ActualStartDate'], date_format).date()),  # Converts Java String to Python String
                        'ActualEndDate': str(datetime.strptime(dict_from_csv['ActualEndDate'], date_format).date()),  # Converts Java String to Python String
                        'action': dict_from_csv['action'],
                        'predecessor_successor': dict_from_csv['predecessor_successor'],
                        'progress': dict_from_csv['progress'],
                        'proj_id': dict_from_csv['proj_id']
                    }
                    await client.post(url, json=ele, headers=headers)
        return JSONResponse(status_code=200, content={"message": "Successfully dumped the data from MPP file!"})

    @app.post("/api/uploadcsv", summary="Upload csv file for microsoft project")
    async def create_upload_csvfile(file: UploadFile = File(...)):
        try:
            # Create a directory named with today's date
            date_today = datetime.now().strftime('%Y-%m-%d')
            directory = f'./uploads/{date_today}'

            if not os.path.exists(directory):
                os.makedirs(directory)

            # Save the file with the date and time included in the filename
            date_time_now = datetime.now().strftime('%H%M%S%f')
            filename = f"{date_time_now}_{file.filename}"
            file_location = f"{directory}/{filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(await file.read())
            
            return await get_csvfile_Content(file_location)
            
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": str(e)})
        
    def create_postgres_table(table_name, columns):
        conn = psycopg2.connect(**POSTGRES_CONNECTION)
        cur = conn.cursor()

        drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
        cur.execute(drop_table_query)
        conn.commit()
            
        column_definitions = []
        for column in columns:
            column_name = column["name"]
            column_type = column["type"]
            
            if column_type == "any":
                # Treat "any" type fields as JSONB
                column_definitions.append(f'"{column_name}" JSONB')
            else:
                column_definitions.append(f'"{column_name}" {column_type}')
        
        columns_sql = ', '.join(column_definitions)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
        
        cur.execute(create_table_query)
        conn.commit()
        conn.close()


    def insert_into_postgres(table_name, data):
        conn = psycopg2.connect(**POSTGRES_CONNECTION)
        cur = conn.cursor()

        # Constructing SQL query for inserting data dynamically
        placeholders = ', '.join(['%s' for _ in range(len(data[0]))])
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"

        for i, row in enumerate(data):
            for j, value in enumerate(row):
                if isinstance(value, dict) or isinstance(value, list):
                    data[i][j] = json.dumps(value)

        # Execute the insert query
        cur.executemany(insert_query, data)
        conn.commit()
        conn.close()

    @app.get("/dump_projects_data")
    async def dump_projects_from_jira(authorization: str):
        
        try:
            # Decode the base64 encoded authorization string
            decoded_auth = base64.b64decode(authorization).decode('utf-8')

            # Extract email and API token from decoded string
            email, api_token = decoded_auth.split(":", 1)
        except ValueError:
            return {"error": "Invalid authorization header format"}

        projects = await get_projects_from_jira(email, api_token)
        for project in projects:
            project_detail = await get_project_from_jira(email, api_token, project["id"])
            url = f'{baseURL}/api/project/'
            async with httpx.AsyncClient() as client:
                data = {
                    'name': project_detail['name'],
                    'description': project_detail['description']
                }
                # id = project_detail['id']
                print(data)
                await client.post(url, json = data, headers=headers)

        return {"message": "Projects data dumped successfully!"}

    @app.post("/dump_issues_data")
    async def dump_issues_data(authorization: str):
        try:
            # Decode the base64 encoded authorization string
            decoded_auth = base64.b64decode(authorization).decode('utf-8')

            # Extract email and API token from decoded string
            email, api_token = decoded_auth.split(":", 1)
        except ValueError:
            return {"error": "Invalid authorization header format"}

        # Fetching data from Jira
        issues = (await get_issues_from_jira(email, api_token))['issues']

        url = f'{baseURL}/api/stories/'
        for issue in issues:
            async with httpx.AsyncClient() as client:
                data = {
                    'type': issue['fields']['issuetype']['name'],
                    'name': issue['fields']['summary'],
                    'description': None if  not issue['fields'].get('description') else issue['fields']['description']['content'][0]['content'][0]['text'],
                    'assigned_to': None if not issue['fields'].get('assignee') else issue['fields']['assignee']['accountId'],
                    'DueDate': issue['fields']['duedate'],
                    # 'proj_id': issue['fields']['project']['id']
                }
                print(data)
                await client.post(url, json = data, headers=headers)

        return {"message": "Issues data dumped successfully!"}


    return app

app = init_app()

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)