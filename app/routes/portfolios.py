from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import get_db
from sqlalchemy.orm import Session
from schemas.portfolios import PortfolioCreateSchema, PortfolioReadSchema, PortfolioUpdateSchema, ResponsePortfolioSchema, ListResponsePortfolioSchema
import database.portfolios as lc


portfolio_router = APIRouter(
    prefix="/portfolio",
)


@portfolio_router.get("/", response_model=ListResponsePortfolioSchema)
def get_portfolios(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    portfolios = lc.get_portfolios(db, skip=skip, limit=limit)
    return {"code": "success", "status": status.HTTP_200_OK, "response": portfolios}


@portfolio_router.post("/", response_model=ResponsePortfolioSchema, status_code=status.HTTP_201_CREATED)
def create_portfolio(portfolio: PortfolioCreateSchema, db: Session = Depends(get_db)):
    returned_data = PortfolioReadSchema.model_validate(lc.create_portfolio(db, portfolio))
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}


@portfolio_router.get("/{portfolio_id}", response_model=ResponsePortfolioSchema)
def retrieve_portfolio(portfolio_id: int = Path(...), db: Session = Depends(get_db)):
    db_portfolio = lc.get_portfolio_by_id(db, portfolio_id=portfolio_id)
    if db_portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="portfolio not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_portfolio}


@portfolio_router.put("/{portfolio_id}", response_model=ResponsePortfolioSchema)
def update_portfolio(portfolio_id: int = Path(...), portfolio: PortfolioUpdateSchema = None, db: Session = Depends(get_db)):
    db_portfolio = lc.get_portfolio_by_id(db, portfolio_id=portfolio_id)
    if db_portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="portfolio not found")
    returned_data = PortfolioReadSchema.model_validate(lc.update_portfolio(db, portfolio_id=portfolio_id, portfolio=portfolio))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}


@portfolio_router.delete("/{portfolio_id}", response_model=ResponsePortfolioSchema)
def delete_portfolio(portfolio_id: int = Path(...), db: Session = Depends(get_db)):
    db_portfolio = lc.get_portfolio_by_id(db, portfolio_id=portfolio_id)
    if db_portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="portfolio not found")
    lc.delete_portfolio(db, portfolio_id=portfolio_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "portfolio deleted"}