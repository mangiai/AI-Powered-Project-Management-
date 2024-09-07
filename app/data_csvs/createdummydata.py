import pandas as pd

# Dummy data for each table

# portfolios.csv
portfolios = {
    "id": [151],
    "name": ["Tech Portfolio"],
    "description": ["Description1"],
    "company_id": [1],
    "created_at": ["2024-08-01 12:00:00"],
    "updated_at": ["2024-08-01 12:00:00"],
    "status": [1],
    "StartDate": ["2024-01-01"],
    "EndDate": ["2024-12-31"]
}

# programs.csv
programs = {
    "id": [151],
    "name": ["Innovation Program"],
    "description": ["Description1"],
    "portfolio_id": [151],
    "created_at": ["2024-08-01 12:00:00"],
    "updated_at": ["2024-08-01 12:00:00"],
    "status": [1],
    "StartDate": ["2024-01-01"],
    "EndDate": ["2024-12-31"]
}

# projects.csv
projects = {
    "id": [151],
    "name": ["Project1"],
    "description": ["Description1"],
    "program_id": [151],
    "portfolio_id": [151],
    "created_at": ["2024-08-01 12:00:00"],
    "updated_at": ["2024-08-01 12:00:00"],
    "current_phase": ["Phase1"]
}

# ftasks.csv
ftasks = {
    "id": [10],
    "name": ["Task1"],
    "description": ["Description1"],
    "wbs": ["WBS1"],
    "current_status": ["InProgress"],
    "Resource": ["Resource1"],
    "PlannedStartDate": ["2024-01-01"],
    "PlannedEndDate": ["2024-01-15"],
    "ActualStartDate": ["2024-01-01"],
    "ActualEndDate": ["2024-01-10"],
    "action": ["Action1"],
    "predecessor_successor": ["1"],
    "progress": [50],
    "assigned_to": [151],
    "proj_id": [151],
    "created_at": ["2024-08-01 12:00:00"],
    "updated_at": ["2024-08-01 12:00:00"],
    "ActualResource": ["ActualResource1"]
}

# costs.csv
costs = {
    "id": [151],
    "cost_per_hour": [100],
    "total_hours": [200],
    "fixed_cost": [None],
    "actual_hours": [150],
    "actual_fixed_cost": [None],
    "cost_ftask_id": [10],
    "cost_user_id": [151],
    "cost_story_id": [10],
    "location": [1],
    "created_at": ["2024-08-01 12:00:00"],
    "updated_at": ["2024-08-01 12:00:00"]
}

# risks.csv
risks = {
    "id": [151],
    "title": ["Scope Creep"],
    "description": ["Description1"],
    "impact": ["High"],
    "probability": ["Medium"],
    "project_id": [151],
    "created_at": ["2024-08-01 12:00:00"],
    "updated_at": ["2024-08-01 12:00:00"],
    "type": ["Type1"],
    "name": ["Name1"],
    "is_completed": [0],
    "risk_impact": [1],
    "risk_probablitly": [2]
}

# users.csv
users = {
    "id": [151],
    "email": ["johndoe@example.com"],
    "password": ["password123"],
    "username": ["johndoe"],
    "first_name": ["John"],
    "last_name": ["Doe"],
    "is_system_admin": [1],
    "is_fte": [0],
    "is_business_steward": [1],
    "is_resource": [1],
    "is_onshore": [0],
    "access_level": [5],
    "created_at": ["2024-08-01 12:00:00"],
    "updated_at": ["2024-08-01 12:00:00"]
}

# Saving CSV files
pd.DataFrame(portfolios).to_csv("portfolios.csv", index=False)
pd.DataFrame(programs).to_csv("programs.csv", index=False)
pd.DataFrame(projects).to_csv("projects.csv", index=False)
pd.DataFrame(ftasks).to_csv("ftasks.csv", index=False)
pd.DataFrame(costs).to_csv("costs.csv", index=False)
pd.DataFrame(risks).to_csv("risks.csv", index=False)
pd.DataFrame(users).to_csv("users.csv", index=False)
