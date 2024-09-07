from sqlalchemy.orm import Session
from models.portfolios import Portfolio
from schemas.portfolios import PortfolioCreateSchema, PortfolioUpdateSchema


def get_portfolios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Portfolio).offset(skip).limit(limit).all()


def get_portfolio_by_id(db: Session, portfolio_id: int):
    return db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()


def create_portfolio(db: Session, portfolio: PortfolioCreateSchema):
    db_portfolio = Portfolio(name=portfolio.name,
                   description=portfolio.description
                   , StartDate=portfolio.StartDate, EndDate=portfolio.EndDate)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


def delete_portfolio(db: Session, portfolio_id: int):
    db_portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    db.delete(db_portfolio)
    db.commit()


def update_portfolio(db: Session, portfolio_id: int, portfolio: PortfolioUpdateSchema):
    db_portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    db_portfolio.name = portfolio.name
    db_portfolio.description = portfolio.description
    db_portfolio.StartDate = portfolio.StartDate
    db_portfolio.EndDate = portfolio.EndDate
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

