from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config import *


kpi_router = APIRouter(
    prefix="/kpi",
)
@kpi_router.get("/story")
async def getCostPerUser(userId:int):
    try:
        connection = await connect_to_db()
        query = f'\
            SELECT costs.*\
                FROM stories\
                inner join costs on stories.id = costs.cost_story_id\
                where stories.assigned_to= {userId}'
        costList = await connection.fetch(query)
        await close_db_connection(connection)
        plannedCost = 0
        actualCost = 0

        for cost in costList:
            location = cost['location']
            if cost['fixed_cost'] is not None and cost['fixed_cost'] != 0:
                plannedCost += cost['fixed_cost']
                actualCost += cost['actual_fixed_cost']
            else:
                plannedCost += cost['cost_per_hour'] * cost['total_hours']
                actualCost += cost['cost_per_hour'] * cost['actual_hours']
        return JSONResponse(status_code=200, content={
            "plannedCost": plannedCost,
            "actualCost": actualCost,
            "location": location
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
@kpi_router.get("/sprint")
async def getSprintCost(sprintId:int, startingPhase:int, endingPhase:int):
    if startingPhase > endingPhase:
        tmp = startingPhase
        startingPhase = endingPhase
        endingPhase = tmp

    try:
        connection = await connect_to_db()
        query = f'\
            SELECT costs.*\
                FROM stories\
                inner join costs on stories.id = costs.cost_story_id\
                where stories.sprint_id = {sprintId} and stories.current_status between {startingPhase} and {endingPhase}\
            '
        costList = await connection.fetch(query)
        await close_db_connection(connection)
        plannedCost = 0
        actualCost = 0

        for cost in costList:
            if cost['fixed_cost'] is not None and cost['fixed_cost'] != 0:
                plannedCost += cost['fixed_cost']
                actualCost += cost['actual_fixed_cost']
            else:
                plannedCost += cost['cost_per_hour'] * cost['total_hours']
                actualCost += cost['cost_per_hour'] * cost['actual_hours']
        return JSONResponse(status_code=200, content={
            "plannedCost": plannedCost,
            "actualCost": actualCost
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@kpi_router.get("/release")
async def getReleaseCost(releaseId:int, startingPhase:int, endingPhase:int):
    if startingPhase > endingPhase:
        tmp = startingPhase
        startingPhase = endingPhase
        endingPhase = tmp

    try:
        connection = await connect_to_db()
        query = f'\
            SELECT sprints.id\
                FROM sprints\
                where sprints.release_id = {releaseId}\
            '
        sprintIdList = await connection.fetch(query)
        plannedCost = 0
        actualCost = 0
        for sprint in sprintIdList:
            sprintId = sprint['id']
            query = f'\
                    SELECT costs.*\
                    FROM stories\
                    inner join costs on stories.id = costs.cost_story_id\
                    where stories.sprint_id = {sprintId} and stories.current_status between {startingPhase} and {endingPhase}\
                '
            costList = await connection.fetch(query)
            for cost in costList:
                if cost['fixed_cost'] is not None and cost['fixed_cost'] != 0:
                    plannedCost += cost['fixed_cost']
                    actualCost += cost['actual_fixed_cost']
                else:
                    plannedCost += cost['cost_per_hour'] * cost['total_hours']
                    actualCost += cost['cost_per_hour'] * cost['actual_hours']
        await close_db_connection(connection)
        
        return JSONResponse(status_code=200, content={
            "plannedCost": plannedCost,
            "actualCost": actualCost
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@kpi_router.get("/product")
async def getProductCost(productId:int, startingPhase:int, endingPhase:int):
    if startingPhase > endingPhase:
        tmp = startingPhase
        startingPhase = endingPhase
        endingPhase = tmp

    try:
        connection = await connect_to_db()
        query = f'\
            SELECT sprints.id\
                FROM sprints\
                inner join releases on sprints.release_id = releases.id\
                where releases.product_id = {productId}\
            '
        sprintIdList = await connection.fetch(query)
        plannedCost = 0
        actualCost = 0
        for sprint in sprintIdList:
            sprintId = sprint['id']
            query = f'\
                    SELECT costs.*\
                    FROM stories\
                    inner join costs on stories.id = costs.cost_story_id\
                    where stories.sprint_id = {sprintId} and stories.current_status between {startingPhase} and {endingPhase}\
                '
            costList = await connection.fetch(query)
            for cost in costList:
                if cost['fixed_cost'] is not None and cost['fixed_cost'] != 0:
                    plannedCost += cost['fixed_cost']
                    actualCost += cost['actual_fixed_cost']
                else:
                    plannedCost += cost['cost_per_hour'] * cost['total_hours']
                    actualCost += cost['cost_per_hour'] * cost['actual_hours']
        await close_db_connection(connection)
        
        return JSONResponse(status_code=200, content={
                "plannedCost": plannedCost,
                "actualCost": actualCost
            })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@kpi_router.get("/project")
async def getProjectCost(projectId:int, startingPhase:int, endingPhase:int):
    if startingPhase > endingPhase:
        tmp = startingPhase
        startingPhase = endingPhase
        endingPhase = tmp

    try:
        connection = await connect_to_db()
        query = f'\
            SELECT costs.*\
                FROM ftasks\
                inner join costs on ftasks.id = costs.cost_ftask_id\
                where ftasks.proj_id = {projectId} and ftasks.current_status between {startingPhase} and {endingPhase}\
            '
        costList = await connection.fetch(query)
        await close_db_connection(connection)
        plannedCost = 0
        actualCost = 0

        for cost in costList:
            if cost['fixed_cost'] is not None and cost['fixed_cost'] != 0:
                plannedCost += cost['fixed_cost']
                actualCost += cost['actual_fixed_cost']
            else:
                plannedCost += cost['cost_per_hour'] * cost['total_hours']
                actualCost += cost['cost_per_hour'] * cost['actual_hours']
        return JSONResponse(status_code=200, content={
                "plannedCost": plannedCost,
                "actualCost": actualCost
            })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@kpi_router.get("/program")
async def getProgramCost(programId:int, startingPhase:int, endingPhase:int):
    if startingPhase > endingPhase:
        tmp = startingPhase
        startingPhase = endingPhase
        endingPhase = tmp

    try:
        connection = await connect_to_db()
        query = f'\
            SELECT projects.id\
                FROM projects\
                where projects.program_id = {programId}\
            '
        projectIdList = await connection.fetch(query)
        plannedCost = 0
        actualCost = 0
        for project in projectIdList:
            projectId = project['id']
            query = f'\
                    SELECT costs.*\
                    FROM ftasks\
                    inner join costs on ftasks.id = costs.cost_ftask_id\
                    where ftasks.proj_id = {projectId} and ftasks.current_status between {startingPhase} and {endingPhase}\
                '
            costList = await connection.fetch(query)
            for cost in costList:
                if cost['fixed_cost'] is not None and cost['fixed_cost'] != 0:
                    plannedCost += cost['fixed_cost']
                    actualCost += cost['actual_fixed_cost']
                else:
                    plannedCost += cost['cost_per_hour'] * cost['total_hours']
                    actualCost += cost['cost_per_hour'] * cost['actual_hours']
        await close_db_connection(connection)
        
        return JSONResponse(status_code=200, content={
                "plannedCost": plannedCost,
                "actualCost": actualCost
            })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    
@kpi_router.get("/portfolio")
async def getPortfolioCost(portfolioId:int, startingPhase:int, endingPhase:int):
    if startingPhase > endingPhase:
        tmp = startingPhase
        startingPhase = endingPhase
        endingPhase = tmp

    try:
        connection = await connect_to_db()
        query = f'\
            SELECT projects.id\
                FROM projects\
                inner join programs on projects.program_id = programs.id\
                where programs.portfolio_id = {portfolioId}\
            '
        projectIdList = await connection.fetch(query)
        plannedCost = 0
        actualCost = 0
        for project in projectIdList:
            projectId = project['id']
            query = f'\
                    SELECT costs.*\
                    FROM ftasks\
                    inner join costs on ftasks.id = costs.cost_ftask_id\
                    where ftasks.proj_id = {projectId} and ftasks.current_status between {startingPhase} and {endingPhase}\
                '
            costList = await connection.fetch(query)
            for cost in costList:
                if cost['fixed_cost'] is not None and cost['fixed_cost'] != 0:
                    plannedCost += cost['fixed_cost']
                    actualCost += cost['actual_fixed_cost']
                else:
                    plannedCost += cost['cost_per_hour'] * cost['total_hours']
                    actualCost += cost['cost_per_hour'] * cost['actual_hours']
        await close_db_connection(connection)
        
        return JSONResponse(status_code=200, content={
                    "plannedCost": plannedCost,
                    "actualCost": actualCost
                })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@kpi_router.get("/timeline")
async def getTimeline(projectId:int, startingPhase:int, endingPhase:int):
    if startingPhase > endingPhase:
        tmp = startingPhase
        startingPhase = endingPhase
        endingPhase = tmp

    try:
        connection = await connect_to_db()
        query = f'\
            SELECT \"PlannedStartDate\", \"PlannedEndDate\", \"ActualStartDate\", \"ActualEndDate\"\
                FROM ftasks\
                where ftasks.proj_id = {projectId} and ftasks.current_status between {startingPhase} and {endingPhase}\
            '
        periodsList = await connection.fetch(query)
        await close_db_connection(connection)
        if len(periodsList) > 0:
            plannedStartDate = periodsList[0]['PlannedStartDate']
            plannedEndDate = periodsList[0]['PlannedEndDate']
            actualStartDate = periodsList[0]['ActualStartDate']
            actualEndDate = periodsList[0]['ActualEndDate']
        else:
            return JSONResponse(status_code=200, content={"message": "No results!"})
        
        for period in periodsList:
            if plannedStartDate > period['PlannedStartDate']:
                plannedStartDate = period['PlannedStartDate']
            if plannedEndDate < period['PlannedEndDate']:
                plannedEndDate = period['PlannedEndDate']
            if actualStartDate > period['ActualStartDate']:
                actualStartDate = period['ActualStartDate']
            if actualEndDate < period['ActualEndDate']:
                actualEndDate = period['ActualEndDate']
            
        return JSONResponse(status_code=200, content={
                "plannedStartDate": str(plannedStartDate),
                "plannedEndDate": str(plannedEndDate),
                "actualStartDate": str(actualStartDate),
                "actualEndDate": str(actualEndDate)
            })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@kpi_router.get("/resource")
async def getResource(projectId:int, startingPhase:int, endingPhase:int):
    if startingPhase > endingPhase:
        tmp = startingPhase
        startingPhase = endingPhase
        endingPhase = tmp

    try:
        connection = await connect_to_db()
        query = f'\
            SELECT \"Resource\", \"ActualResource\"\
                FROM ftasks\
                where ftasks.proj_id = {projectId} and ftasks.current_status between {startingPhase} and {endingPhase}\
            '
        resourcesList = await connection.fetch(query)
        await close_db_connection(connection)
        plannedResource = []
        actualResource = []

        for resource in resourcesList:
            if resource['Resource'] != None and resource['Resource'] != '':
                plannedResource.append(resource['Resource'])
            if resource['ActualResource'] != None and resource['ActualResource'] != '':
                actualResource.append(resource['ActualResource'])
            
        return JSONResponse(status_code=200, content={
                "plannedResource": plannedResource,
                "actualResource": actualResource
            })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    
@kpi_router.get("/timelineforjira")
async def getTimeline(sprintId:int, startingPhase:int, endingPhase:int):
    if startingPhase > endingPhase:
        tmp = startingPhase
        startingPhase = endingPhase
        endingPhase = tmp

    try:
        connection = await connect_to_db()
        query = f'\
            SELECT \"plannedStartDate\", \"plannedEndDate\", \"actualStartDate\", \"actualEndDate\"\
                FROM stories\
                where stories.sprint_id = {sprintId} and stories.current_status between {startingPhase} and {endingPhase}\
            '
        periodsList = await connection.fetch(query)
        await close_db_connection(connection)
        if len(periodsList) > 0:
            plannedStartDate = periodsList[0]['plannedStartDate']
            plannedEndDate = periodsList[0]['plannedEndDate']
            actualStartDate = periodsList[0]['actualStartDate']
            actualEndDate = periodsList[0]['actualEndDate']
        else:
            return JSONResponse(status_code=200, content={"message": "No results!"})
        
        for period in periodsList:
            if plannedStartDate > period['plannedStartDate']:
                plannedStartDate = period['plannedStartDate']
            if plannedEndDate < period['plannedEndDate']:
                plannedEndDate = period['plannedEndDate']
            if actualStartDate > period['actualStartDate']:
                actualStartDate = period['actualStartDate']
            if actualEndDate < period['actualEndDate']:
                actualEndDate = period['actualEndDate']
            
        return JSONResponse(status_code=200, content={
                "plannedStartDate": str(plannedStartDate),
                "plannedEndDate": str(plannedEndDate),
                "actualStartDate": str(actualStartDate),
                "actualEndDate": str(actualEndDate)
            })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@kpi_router.get("/resourceforjira")
async def getResource(sprintId:int, startingPhase:int, endingPhase:int):
    if startingPhase > endingPhase:
        tmp = startingPhase
        startingPhase = endingPhase
        endingPhase = tmp

    try:
        connection = await connect_to_db()
        query = f'\
            SELECT \"resource\", \"actualResource\"\
                FROM stories\
                where stories.sprint_id = {sprintId} and stories.current_status between {startingPhase} and {endingPhase}\
            '
        resourcesList = await connection.fetch(query)
        await close_db_connection(connection)
        plannedResource = []
        actualResource = []

        for resource in resourcesList:
            if resource['resource'] != None and resource['resource'] != '':
                plannedResource.append(resource['resource'])
            if resource['actualResource'] != None and resource['actualResource'] != '':
                actualResource.append(resource['actualResource'])
            
        return JSONResponse(status_code=200, content={
                "plannedResource": plannedResource,
                "actualResource": actualResource
            })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})