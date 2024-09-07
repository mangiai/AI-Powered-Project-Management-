from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import join
from schemas import chatbot as schema

from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_chroma import Chroma


from config import  DATABASE_URL, engine, connect_to_db, close_db_connection, SessionLocal, POSTGRES_CONNECTION, get_db
from decouple import config
import chatbot as cb


openai_key = config("OPENAI_API_KEY")
chatbot_router = APIRouter(
    prefix="/chatbot",
)

db = SQLDatabase.from_uri(DATABASE_URL,sample_rows_in_table_info=0)
table_info = db.table_info


llm = ChatOpenAI(api_key=openai_key,model="gpt-4", temperature=0)
llm2 = ChatOpenAI(api_key=openai_key,model="gpt-4o", temperature=0.5)
generate_query = create_sql_query_chain(llm, db)
execute_query = QuerySQLDataBaseTool(db=db)
vectorstore = Chroma()

vectorstore.delete_collection()
example_selectors = SemanticSimilarityExampleSelector.from_examples(
    cb.examples, OpenAIEmbeddings(), vectorstore, k=3, input_keys=["input"]
)

example_prompt = ChatPromptTemplate.from_messages(
[
    ("human", "{input}\nSQLQuery:"),
    ("ai", "{query}"),
]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
example_prompt=example_prompt,
example_selector=example_selectors,
input_variables=["input", "top_k"],
) 


@chatbot_router.post("/cost-bot")
def cost_bot(query: schema.QueryRequest):
    response = cb.get_cost_response(
        query.question, few_shot_prompt, llm, llm2, db, execute_query
    )
    return {"response": response}

@chatbot_router.post("/project-bot")
def project_bot(query: schema.QueryRequest,):
    response = cb.get_project_response(
        query.question, few_shot_prompt, llm, llm2, db, execute_query
    )
    return {"response": response}

@chatbot_router.post("/risk-bot" )
def risk_bot(query: schema.QueryRequest):
    response = cb.get_risk_response(
        query.question, few_shot_prompt, llm, llm2, db, execute_query
    )
    return {"response": response}