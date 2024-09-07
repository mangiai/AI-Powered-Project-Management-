from fastapi import APIRouter, Depends, File, UploadFile
from typing import List
import pandas as pd
import os
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from config import get_db
from models.users import User
from models.costs import Cost
from models.ftasks import FTask
from models.portfolios import Portfolio
from models.programs import Program
from models.projects import Project
from models.risks import Risk

from database.users import create_user
from database.costs import create_cost
from database.ftasks import create_ftask
from database.portfolios import create_portfolio
from database.programs import create_program
from database.projects import create_project
from database.risks import create_risk


upload_router = APIRouter(
    prefix="/uploadall",
)

class_mappings = {
    "costs": [
        "cost_per_hour",
        "total_hours",
        "fixed_cost",
        "actual_hours",
        "actual_fixed_cost",
        "cost_ftask_id",
        "cost_user_id",
        "cost_story_id",
        "location",
        "created_at",
        "updated_at",
    ],
    "ftasks": [
        "name",
        "description",
        "wbs",
        "current_status",
        "Resource",
        "PlannedStartDate",
        "PlannedEndDate",
        "ActualStartDate",
        "ActualEndDate",
        "action",
        "predecessor_successor",
        "progress",
        "assigned_to",
        "proj_id",
        "created_at",
        "updated_at",
        "ActualResource",
    ],
    "portfolios": [
        "name",
        "description",
        "company_id",
        "created_at",
        "updated_at",
        "status",
        "StartDate",
        "EndDate",
    ],
    "programs": [
        "name",
        "description",
        "portfolio_id",
        "created_at",
        "updated_at",
        "status",
        "StartDate",
        "EndDate",
    ],
    "projects": [
        "name",
        "description",
        "program_id",
        "portfolio_id",
        "created_at",
        "updated_at",
        "current_phase",
    ],
    "risks": [
        "title",
        "description",
        "impact",
        "probability",
        "project_id",
        "created_at",
        "updated_at",
        "type",
        "name",
        "is_completed",
        "risk_impact",
        "risk_probablitly",
    ],
    "users": [
        "email",
        "password",
        "username",
        "first_name",
        "last_name",
        "is_system_admin",
        "is_fte",
        "is_business_steward",
        "is_resource",
        "is_onshore",
        "access_level",
        "created_at",
        "updated_at",
    ],
}

db_functions = {
    "costs": create_cost,
    "ftasks": create_ftask,
    "portfolios": create_portfolio,
    "programs": create_program,
    "projects": create_project,
    "risks": create_risk,
    "users": create_user,
}

model_classes = {
    "costs": Cost,
    "ftasks": FTask,
    "portfolios": Portfolio,
    "programs": Program,
    "projects": Project,
    "risks": Risk,
    "users": User,
}

def identify_class(df, class_mappings):
    for class_name, columns in class_mappings.items():
        if set(columns).issubset(df.columns):
            return class_name
    return None

def process_uploaded_file(
    db: Session,
    file_path: str,
    class_mappings: dict,
    db_functions: dict,
    model_classes: dict,
):
    print(f"Processing file: {file_path}")
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded dataframe with columns: {df.columns.tolist()}")
    except Exception as e:
        print(f"Error loading CSV file {file_path}: {e}")
        return f"Error loading CSV file {file_path}: {e}"

    identified_class = identify_class(df, class_mappings)
    print(f"Identified class: {identified_class}")

    if not identified_class:
        print(
            f"Unable to identify the class of the uploaded file based on its columns: {df.columns.tolist()}"
        )
        return (
            f"Unable to identify the class of the uploaded file based on its columns."
        )

    db_function = db_functions[identified_class]
    model_class = model_classes[identified_class]
    try:
        for _, row in df.iterrows():
            # Remove the 'id' field if it exists in the row dictionary
            row_dict = row.to_dict()
            if 'id' in row_dict:
                del row_dict['id']
            
            # Create the model instance
            data = model_class(**row_dict)
            db_function(db, data)
    except Exception as e:
        print(f"Error saving data for class {identified_class}: {e}")
        return f"Error saving data for class {identified_class}: {e}"

    return f"Data successfully processed and saved for class: {identified_class}"

def extract_project_id(db: Session, file_path: str) -> int:
    # Retrieve the most recent project ID from the database
    project = db.query(Project).order_by(Project.id.desc()).first()
    return project.id if project else None


@upload_router.post("/upload_all_files")
async def upload_all_files(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    results = []
    project_id = None
    
    try:
        for file in files:
            file_path = f"temp_{file.filename}"
            with open(file_path, "wb") as f:
                f.write(await file.read())
            
            # Process each file and save data
            result = process_uploaded_file(db, file_path, class_mappings, db_functions, model_classes)
            results.append(result)
            
            # Dynamically check if the processed file corresponds to the 'projects' class
            if identify_class(pd.read_csv(file_path), class_mappings) == 'projects':
                project_id = extract_project_id(db, file_path)
            
            os.remove(file_path)
        
        # Ensure that the project_id was found
        if not project_id:
            return JSONResponse(
                status_code=400,
                content={"message": "Project ID could not be found. Ensure a project file was uploaded."}
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"message": f"Unexpected error: {str(e)}"}
        )

    # Return the project ID in the response
    return {"results": results, "project_id": project_id}
