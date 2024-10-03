from fastapi import FastAPI
from dbs_assignment.enpoints.query import router as endpoints_router

app = FastAPI()

app.include_router(endpoints_router)
