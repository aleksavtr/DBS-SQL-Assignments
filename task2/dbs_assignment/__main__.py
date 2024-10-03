from fastapi import FastAPI
#from .router import router
from .database import database
from dbs_assignment.enpoints.query import router as router
app = FastAPI(title="DBS Assignment")

app.include_router(router)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
