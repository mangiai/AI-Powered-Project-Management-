from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import engine, connect_to_db, close_db_connection, SessionLocal, POSTGRES_CONNECTION, get_db
from sqlalchemy.orm import Session, joinedload
from schemas.msgs import MsgCreateSchema, MsgReadSchema, MsgUpdateSchema, ResponseMsgSchema, ListResponseMsgSchema
import database.msgs as tc

msg_router = APIRouter(
    prefix="/msgs",
)

@msg_router.get("/", response_model=ListResponseMsgSchema)
def get_msgs(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    msgs = tc.get_msgs(db, skip=skip, limit=limit)
    return {"code": "success", "status": status.HTTP_200_OK, "response": msgs}

@msg_router.post("/", response_model=ResponseMsgSchema, status_code=status.HTTP_201_CREATED)
def create_msg(msg: MsgCreateSchema, db: Session = Depends(get_db)):
    returned_data = MsgReadSchema.model_validate(tc.create_msg(db, msg))
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}

@msg_router.get("/{msg_id}", response_model=ResponseMsgSchema)
def retrieve_msg(msg_id: int = Path(...), db: Session = Depends(get_db)):
    db_msg = tc.get_msg_by_id(db, msg_id=msg_id)
    if db_msg is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Msg not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_msg}

@msg_router.put("/{msg_id}", response_model=ResponseMsgSchema)
def update_msg(msg_id: int = Path(...), msg: MsgUpdateSchema = None, db: Session = Depends(get_db)):
    db_msg = tc.get_msg_by_id(db, msg_id=msg_id)
    if db_msg is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Msg not found")
    returned_data = MsgReadSchema.model_validate(tc.update_msg(db, msg_id=msg_id, msg=msg))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}

@msg_router.delete("/{msg_id}", response_model=ResponseMsgSchema)
def delete_msg(msg_id: int = Path(...), db: Session = Depends(get_db)):
    db_msg = tc.get_msg_by_id(db, msg_id=msg_id)
    if db_msg is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Msg not found")
    tc.delete_msg(db, msg_id=msg_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "Msg deleted"}
