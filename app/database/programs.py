from sqlalchemy.orm import Session
from models.programs import Program
from schemas.programs import ProgramCreateSchema, ProgramUpdateSchema


def get_programs(db: Session, skip: int = 0, limit: int = 100, portfolio_id: int = None):
    query = db.query(Program)
    if portfolio_id:
        query = query.filter(Program.portfolio_id == portfolio_id)
    return query.offset(skip).limit(limit).all()

def get_program_by_id(db: Session, program_id: int):
    return db.query(Program).filter(Program.id == program_id).first()


def create_program(db: Session, program: ProgramCreateSchema):
    db_program = Program(name=program.name,
                   description=program.description
                   , StartDate=program.StartDate, EndDate=program.EndDate,
                   program_lifecycle_id = program.program_lifecycle_id, portfolio_id = program.portfolio_id)
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program


def delete_program(db: Session, program_id: int):
    db_program = db.query(Program).filter(Program.id == program_id).first()
    db.delete(db_program)
    db.commit()


def update_program(db: Session, program_id: int, program: ProgramUpdateSchema):
    db_program = db.query(Program).filter(Program.id == program_id).first()
    db_program.name = program.name
    db_program.description = program.description
    db_program.StartDate = program.StartDate
    db_program.EndDate = program.EndDate
    db_program.program_lifecycle_id = program.program_lifecycle_id
    db_program.portfolio_id = program.portfolio_id
    db.commit()
    db.refresh(db_program)
    return db_program

