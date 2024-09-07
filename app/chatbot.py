from langchain_chroma import Chroma
from langchain.chains import create_sql_query_chain
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate
)

from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from dotenv import load_dotenv

import os

load_dotenv()


def load_env_variables():
    load_dotenv()
    return os.getenv("DATABASE_URL")

def setup_db(db_uri: str):
    db = SQLDatabase.from_uri(db_uri, sample_rows_in_table_info=0)
    table_info = db.table_info
    return db, table_info

def initialize_llms():
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    llm2 = ChatOpenAI(model="gpt-4o", temperature=0.5)
    return llm, llm2

def create_sql_tools(llm, db):
    generate_query = create_sql_query_chain(llm, db)
    execute_query = QuerySQLDataBaseTool(db=db)
    return generate_query, execute_query

def integrate_vector_store():
    vectorstore = Chroma()
    vectorstore.delete_collection()
    example_selectors = SemanticSimilarityExampleSelector.from_examples(
        examples, OpenAIEmbeddings(), vectorstore, k=3, input_keys=["input"]
    )
    return vectorstore, example_selectors

def create_few_shot_prompt(example_selectors):
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
    return few_shot_prompt



# Cost Agent


def get_cost_response(User_Question, few_shot_prompt, llm, llm2, db, execute_query):
    Cost_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL Query, and SQL results, answer the user question with respect to cost being in $ Dollars with the value of deviation and you must need elaborate the negative or positive hours.
        Objective: Track and analyze project costs.
        Metrics to Track: Planned vs. actual costs, cost overruns, cost performance index (CPI).
        Identify tasks and projects where actual costs exceed planned costs.
        Highlight tasks and projects with significant cost deviation
    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    Answer: """
    )

    final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a PostgreSQL expert. Given an input question, create a syntactically correct PostgreSQL query that identifies deviations and violations against key performance indicators (KPIs) such as time, cost, and resource availability. Your response should cover the following aspects: For a program: Analyze multiple projects by phase, highlighting percentage deviations across all three KPIs. For a project: Evaluate a single project's phases, detailing percentage deviations across all KPIs. Identify and predict points of failure across KPIs, summarizing key learnings from the data. Provide definitions and values for each identified deviation and violation clearly. Here is the relevant table information: {table_info} Below are several examples of questions and their corresponding SQL queries to guide your format.",
            ),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )

    generate_query = create_sql_query_chain(llm, db, final_prompt)
    rephrase_answer = Cost_prompt | llm2 | StrOutputParser()
    chain = (
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | rephrase_answer
    )

    response = chain.invoke({"question": f"{User_Question}", "top_k": 5})
    return response




# Project Agent


def get_project_response(User_Question, few_shot_prompt, llm, llm2, db, execute_query):
    Project_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL Query, and SQL results, answer the user question in a human understandable context with respect to the project through the name of the project given by the user
        and then all the ftasks for the given project then utilze the hourly cost multiply with total hours for the planned hours then hourly cost multiply with actual cost then find the deviation.
        Objective: Track and analyze project costs.

    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    Answer: """
    )

    final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a PostgreSQL expert. Given an input question, create syntactically correct PostgreSQL queries that finds the project name and its id according to what user has asked for utilizing the 'ftask' and 'cost' table.Here is the relevant table information: {table_info}, you need access the column names from here, Below are several examples of questions and their corresponding SQL queries to guide your format.",
            ),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )

    generate_query = create_sql_query_chain(llm, db, final_prompt)
    rephrase_answer = Project_prompt | llm2 | StrOutputParser()
    chain = (
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | rephrase_answer
    )

    response = chain.invoke({"question": f"{User_Question}", "top_k": 5})

    return response


# Risk Agent
def get_risk_response(User_Question, few_shot_prompt, llm, llm2, db, execute_query):
    Risk_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL Query, and SQL results, answer the user question with respect to providing Risk Mitigation Analysis according to the User/Assignee, Project, Risk, Type, Probablity, Impact for the given project and provide analysis over the user/assignee.

    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    Answer: """
    )

    final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a PostgreSQL expert. Given an input question, create syntactically correct PostgreSQL queries that fetch the risk table for the given 'project' by finding its id then using the 'assigned_to' column and get the anaysis for the concerned Risk . Here is the relevant table information: {table_info}, you need access the column names from here, Below are several examples of questions and their corresponding SQL queries to guide your format.",
            ),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )

    generate_query = create_sql_query_chain(llm, db, final_prompt)
   
    rephrase_answer = Risk_prompt | llm2 | StrOutputParser()
    chain = (
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | rephrase_answer
    )

    response = chain.invoke({"question": f"{User_Question}", "top_k": 3})

    return response



examples = [
    {
        "input": "Calculate time deviation for each project:",
        "query": """SELECT
    proj_id,
    EXTRACT(day FROM ("ActualEndDate" - "PlannedEndDate")) AS time_deviation_days
FROM ftasks
WHERE "ActualEndDate" IS NOT NULL AND "PlannedEndDate" IS NOT NULL;"""
    },
        {
        "input": "Calculate time deviation for each project phase",
        "query": """SELECT
    proj_id,
    COUNT(DISTINCT assigned_to) AS unique_resources_assigned
FROM ftasks
GROUP BY proj_id;"""
    },
    {
        "input": "Calculate cost deviation for each project:",
        "query": """SELECT
    p.id AS project_id,
    SUM((c.actual_hours * c.cost_per_hour + c.actual_fixed_cost) - (c.total_hours * c.cost_per_hour + c.fixed_cost)) AS cost_deviation
FROM projects p
JOIN ftasks f ON p.id = f.proj_id
JOIN costs c ON f.id = c.cost_ftask_id
GROUP BY p.id;"""
    },
        {
        "input": "Calculate resource allocation deviation for each project",
        "query": """SELECT
    proj_id,
    COUNT(DISTINCT "ActualResource") - COUNT(DISTINCT "Resource") AS resource_deviation_count
FROM ftasks
GROUP BY proj_id;"""
    },
            {
        "input": "Calculate average time deviation across all projects",
        "query": """SELECT
    AVG(EXTRACT(day FROM ("ActualEndDate" - "PlannedEndDate"))) AS avg_time_deviation_days
FROM ftasks
WHERE "ActualEndDate" IS NOT NULL AND "PlannedEndDate" IS NOT NULL;"""
    },
    {
        "input": "Calculate resource allocation deviation for each project:",
        "query": """SELECT
    proj_id,
    COUNT(DISTINCT "ActualResource") - COUNT(DISTINCT "Resource") AS resource_deviation_count
FROM ftasks
GROUP BY proj_id;"""
    },
    {
        "input": "Calculate average time deviation across all projects:",
        "query": """SELECT
    AVG(EXTRACT(day FROM ("ActualEndDate" - "PlannedEndDate"))) AS avg_time_deviation_days
FROM ftasks
WHERE "ActualEndDate" IS NOT NULL AND "PlannedEndDate" IS NOT NULL;"""
    },
    {
        "input": "This query counts the unique user IDs (representing individual resources) assigned to tasks within each project, giving an insight into how many different resources (people) were engaged per project",
        "query": """SELECT
    proj_id,
    COUNT(DISTINCT assigned_to) AS unique_resources_assigned
FROM ftasks
GROUP BY proj_id;"""
    },
{
    "input": "Calculate time deviation for each project phase:",
"query": """SELECT
    proj_id,
    EXTRACT(day FROM ("ActualEndDate" - "PlannedEndDate")) AS time_deviation_days
FROM ftasks
WHERE "ActualEndDate" IS NOT NULL AND "PlannedEndDate" IS NOT NULL;"""
},
    {
        "input": "Calculate cost deviation for each project:",
"query": """SELECT
    p.id AS project_id,
    SUM((c.actual_hours * c.cost_per_hour + c.actual_fixed_cost) - (c.total_hours * c.cost_per_hour + c.fixed_cost)) AS cost_deviation
FROM projects p
JOIN ftasks f ON p.id = f.proj_id
JOIN costs c ON f.id = c.cost_ftask_id
GROUP BY p.id;"""
    },
{
    "input": "Calculate resource allocation deviation for each project:",
"query": """SELECT
    proj_id,
    COUNT(DISTINCT "ActualResource") - COUNT(DISTINCT "Resource") AS resource_deviation_count
FROM ftasks
GROUP BY proj_id;"""
},
    {
        "input": "Calculate average time deviation across all projects:",
"query": """SELECT
    AVG(EXTRACT(day FROM ("ActualEndDate" - "PlannedEndDate"))) AS avg_time_deviation_days
FROM ftasks
WHERE "ActualEndDate" IS NOT NULL AND "PlannedEndDate" IS NOT NULL;"""
    },
    {
     "input": "List all projects with a positive cost deviation",
"query": """SELECT
    proj_id,
    SUM((c.actual_hours * c.cost_per_hour + c.actual_fixed_cost) - (c.total_hours * c.cost_per_hour + c.fixed_cost)) AS cost_deviation
FROM ftasks f
JOIN costs c ON f.id = c.cost_ftask_id
GROUP BY proj_id
HAVING SUM((c.actual_hours * c.cost_per_hour + c.actual_fixed_cost) - (c.total_hours * c.cost_per_hour + c.fixed_cost)) > 0;"""

    },
    {
        "input": "List all projects with a negative resource allocation deviation:",
"query": """SELECT
    proj_id,
    COUNT(DISTINCT "ActualResource") - COUNT(DISTINCT "Resource") AS resource_deviation_count
FROM ftasks
GROUP BY proj_id
HAVING COUNT(DISTINCT "ActualResource") - COUNT(DISTINCT "Resource") < 0;"""

    },
    {
        "input": "Calculate total cost for planned vs actual across a specific project:",
"query": """SELECT
    proj_id,
    SUM(c.total_hours * c.cost_per_hour + c.fixed_cost) AS planned_cost,
    SUM(c.actual_hours * c.cost_per_hour + c.actual_fixed_cost) AS actual_cost
FROM ftasks f
JOIN costs c ON f.id = c.cost_ftask_id
WHERE proj_id = 1
GROUP BY proj_id;"""

    },
    {
        "input": "Show the timeline deviation per phase in a specific project:",
"query": """SELECT
    l.phase,
    EXTRACT(day FROM (f."ActualEndDate" - f."PlannedEndDate")) AS time_deviation_days
FROM ftasks f
JOIN projects p ON f.proj_id = p.id
JOIN lifecycle l ON p.project_lifecycle_id = l.id  -- Assuming projects table links to lifecycle via a lifecycle ID
WHERE f.proj_id = 1 AND f."ActualEndDate" IS NOT NULL AND f."PlannedEndDate" IS NOT NULL
ORDER BY l.phase;"""
    },
{
    "input": "Percentage cost deviation per project:",
"query": """SELECT
    proj_id,
    100.0 * SUM((c.actual_hours * c.cost_per_hour + c.actual_fixed_cost) - (c.total_hours * c.cost_per_hour + c.fixed_cost)) / SUM(c.total_hours * c.cost_per_hour + c.fixed_cost) AS cost_deviation_percent
FROM ftasks f
JOIN costs c ON f.id = c.cost_ftask_id
GROUP BY proj_id;"""
},
    {
        "input": "Aggregate resource deviation for all projects in a programs:",
"query": """SELECT
    p.program_id,
    SUM(CASE WHEN "ActualResource" IS NOT NULL THEN 1 ELSE 0 END) - SUM(CASE WHEN "Resource" IS NOT NULL THEN 1 ELSE 0 END) AS resource_deviation
FROM ftasks
JOIN projects p ON ftasks.proj_id = p.id
WHERE p.program_id = 1
GROUP BY p.program_id;"""
    },
    {

"input": "List projects with no time deviations:",
"query": """SELECT
    proj_id
FROM ftasks
WHERE "ActualEndDate" = "PlannedEndDate"; """

    },
    {
        "input": "Show resource allocation per phase in a project:",
"query": """SELECT
    l.phase,
    COUNT(DISTINCT f."ActualResource") AS actual_resources,
    COUNT(DISTINCT f."Resource") AS planned_resources
FROM ftasks f
JOIN projects p ON f.proj_id = p.id
JOIN lifecycle l ON p.project_lifecycle_id = l.id
WHERE f.proj_id = 1
GROUP BY l.phase;"""

    },

    {
        "input": "Time deviation for each task in a project:",
"query": """SELECT
    id,
    name,
    EXTRACT(day FROM ("ActualEndDate" - "PlannedEndDate")) AS time_deviation_days
FROM ftasks
WHERE proj_id = 1 AND "ActualEndDate" IS NOT NULL AND "PlannedEndDate" IS NOT NULL;"""

    },

    {

     "input": "Sum of all positive cost deviations across projects:",
"query": """SELECT
    SUM(cost_deviation) AS total_positive_cost_deviation
FROM (
    SELECT
        proj_id,
        (c.actual_hours * c.cost_per_hour + c.actual_fixed_cost) - (c.total_hours * c.cost_per_hour + c.fixed_cost) AS cost_deviation
    FROM ftasks f
    JOIN costs c ON f.id = c.cost_ftask_id
    WHERE (c.actual_hours * c.cost_per_hour + c.actual_fixed_cost) - (c.total_hours * c.cost_per_hour + c.fixed_cost) > 0
) sub;"""


    },
    {
        "input": "Percentage resource deviation for each project:",
"query": """SELECT
    proj_id,
    100.0 * (COUNT(DISTINCT "ActualResource") - COUNT(DISTINCT "Resource")) / COUNT(DISTINCT "Resource") AS resource_deviation_percent
FROM ftasks
GROUP BY proj_id;"""   },

    {
        "input": "List projects with time deviations greater than a specific threshold:",
"query": """SELECT
    proj_id,
    MAX(EXTRACT(day FROM ("ActualEndDate" - "PlannedEndDate"))) AS max_time_deviation_days
FROM ftasks
GROUP BY proj_id
HAVING MAX(EXTRACT(day FROM ("ActualEndDate" - "PlannedEndDate"))) > 10;"""
    },
    {
        "input": "Show all resources used more than planned in any project:",
"query": """SELECT
    proj_id,
    COUNT(DISTINCT "Resource") AS planned_resource_count,
    COUNT(DISTINCT "ActualResource") AS actual_resource_count,
    COUNT(DISTINCT "ActualResource") - COUNT(DISTINCT "Resource") AS resource_deviation
FROM ftasks
GROUP BY proj_id;"""
    },
    {
        "input": "Detailed resource allocation comparison for a single project:",
"query": """SELECT
    name,
    "Resource" AS planned_resource,
    "ActualResource" AS actual_resource
FROM ftasks
WHERE proj_id = 1;"""

    },
    {
        "input": "Evaluate overall program performance by summing deviations:",
"query": """SELECT
    pj.program_id,
    SUM(EXTRACT(day FROM (f."ActualEndDate" - f."PlannedEndDate"))) AS total_time_deviation_days,
    SUM((c.actual_hours * c.cost_per_hour + c.actual_fixed_cost) - (c.total_hours * c.cost_per_hour + c.fixed_cost)) AS total_cost_deviation,
    SUM(CASE WHEN f."ActualResource" IS NOT NULL THEN 1 ELSE 0 END) - SUM(CASE WHEN f."Resource" IS NOT NULL THEN 1 ELSE 0 END) AS total_resource_deviation
FROM programs p
JOIN projects pj ON p.id = pj.program_id
JOIN ftasks f ON pj.id = f.proj_id
JOIN costs c ON f.id = c.cost_ftask_id
GROUP BY pj.program_id;"""
    },

]
