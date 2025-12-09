from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text


from database import get_db
from models import Customer
from schemas import QueryRequest, QueryResult, UserInfo
from llm_client import generate_sql_from_nl
from auth import get_current_user
from logging_config import logger


router = APIRouter()




@router.post("/chat/query", response_model= QueryResult)
def query_customers(
    body: QueryRequest,
    current_user: UserInfo= Depends(get_current_user),
    db: Session= Depends(get_db)
):
    logger.info(f"User {current_user.username} requested_query: {body.query}")
    # Only admin can query *all* customers with no constraints
    if "all customers" in body.query.lower() and current_user.role != "admin":
        logger.info("Authorization: user not allowed to fetch all customers")
        raise HTTPException(status_code=403, detail="Not allowed to fetch all customers")
    
    try:
        sql = generate_sql_from_nl(body.query)
    except Exception as e:
        logger.info("Error in calling LLM.")
        raise HTTPException(status_code= 500, detail= "Error generating SQL from query.")
    
    if not sql.lower().strip().startswith("select"):
        logger.error(f"Generated SQL is not a SELECT query: {sql}")
        raise HTTPException(status_code= 500, detail= "LLM produced invalid SQL.")

    try:
        result= db.execute(text(sql))
        rows = [dict(row) for row in result]
    except Exception as e:
        logger.exception(f"SQL execution error for query: {sql}")
        raise HTTPException(status_code=400, detail=f"SQL error: {str(e)}")
    logger.info(f"Returning {len(rows)} rows")
    return QueryResult(rows= rows, sql= sql)