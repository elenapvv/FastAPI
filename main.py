from fastapi import FastAPI

from models import InputData
from models import Data
from models import GeneralData
from database import Database

from starlette.responses import Response


app = FastAPI(title="REST service")
db = Database()


@app.post(
    "/add",
    response_description="Add new data in database",
)
async def add(data: InputData):
    return db.add(data)


@app.get(
    "/get?limit={lim}&offset={offs}",
    response_description="Get general data",
    description="Get several rows data from database using LIMIT and OFFSET",
    response_model=GeneralData,
)
async def get(lim=10, offs=0):
    return db.get_general_data(lim, offs)


@app.put(
    "/edit",
    response_description="Edit database",
    description="Change data in the database by ID"
)
async def edit(record: Data):
    return db.edit(record)


@app.get(
    "/product/{data_id}/{data_type}/",
    response_description="Get single data",
    description="Get JSON or XML data from database using ID",
    response_model=Data,
)
async def get_single_data(data_id, data_type):
    if data_type.lower() == "xml":
        return Response(content=db.get_single_data(data_id, data_type), media_type="application/xml")
    return db.get_single_data(data_id, data_type)