# Requirements
# Interpreter Python3 >= 3.7
# API framework: FastAPI / https://fastapi.tiangolo.com/
# ASGI server: uvicorn / https://www.uvicorn.org/
# Async MongoDB driver: motor / https://motor.readthedocs.io/en/stable/
# Validations and settings: pydantic / https://pydantic-docs.helpmanual.io/
# Mongo core for udpate after doc: pymongo / https://pymongo.readthedocs.io/en/stable/
# Async networking library for : tornado / https://www.tornadoweb.org/en/stable/

# pip3 install fastapi uvicorn motor pydantic pymongo tornado

# Import
from fastapi import FastAPI
from motor import motor_asyncio
from motor.motor_tornado import MotorCursor
from pymongo import ReturnDocument
from pydantic import BaseModel
import uuid
import pprint
import json

# Constants
MONGODB_ENDPOINT = "localhost"
MONGODB_PORT = 27017
MYDOKTOR_DATABSE = "MyDoktor"
PATIENTS_COLLECTION = "Patients"

PATIENTS_ROUTE = "/patients"
PATIENT_ID_FIELD = "id"

# Models
class Patient(BaseModel):
    id: str
    name: str
    age: int
    address: str


# Init
app = FastAPI()
client = motor_asyncio.AsyncIOMotorClient(MONGODB_ENDPOINT, MONGODB_PORT)
my_doktor_database = client[MYDOKTOR_DATABSE]
patients_collection = my_doktor_database[PATIENTS_COLLECTION]

# API definition
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get(PATIENTS_ROUTE + "/{patient_id}")
async def get_patient(patient_id: str):
    return await fetch_patient(patient_id)

@app.delete(PATIENTS_ROUTE + "/{patient_id}")
async def remove_patient(patient_id: str):
    return await remove_patient(patient_id)

@app.get(PATIENTS_ROUTE)
async def options_patient():
    return await list_patients()

@app.post(PATIENTS_ROUTE)
async def post_patient(patient: Patient):
    return await create_patient(patient)

@app.put(PATIENTS_ROUTE + "/{patient_id}")
async def put_patient(patient_id: str, patient: Patient):
    return await update_patient(patient_id, patient)



# Library
async def fetch_patient(patient_id: str):
    patient_data = await patients_collection.find_one({PATIENT_ID_FIELD: patient_id})
    if not patient_data:
        return {"Status": "NotFound"}
    patient:Patient = Patient(id=patient_data["id"], name=patient_data["name"], age=patient_data["age"], address=patient_data["address"])
    return {"Status": "Found", "Patient": patient}

async def remove_patient(patient_id: str):
    patient_data = await patients_collection.find_one_and_delete({PATIENT_ID_FIELD: patient_id})
    if not patient_data:
        return {"Status": "NotFound"}
    patient:Patient = Patient(id=patient_data["id"], name=patient_data["name"], age=patient_data["age"], address=patient_data["address"])
    return {"Status": "Found", "Patient": patient}

async def list_patients():
    cursor:MotorCursor = patients_collection.find()
    patients = list()
    results = await cursor.to_list(length=10)
    while results:
        for patient_data in results:
            patients.insert(-1, Patient(id=patient_data["id"], name=patient_data["name"], age=patient_data["age"], address=patient_data["address"]))
        results = await cursor.to_list(length=10)
    return {"Status": "Listed", "Patients": patients}

async def create_patient(patient: Patient):
    my_uuid:str = str(uuid.uuid4())
    my_patient:dict = {
        "id": my_uuid,
        "name": patient.name,
        "age": patient.age,
        "address": patient.address
    }
    returned_patient = await patients_collection.insert_one(my_patient)
    response = {"Status": "Created", "id": my_uuid, "Acknowledged": str(returned_patient.acknowledged), "DocId": str(returned_patient.inserted_id)}
    return response

async def update_patient(patient_id: str, patient: Patient):
    my_patient:dict = {
        "id": patient_id,
        "name": patient.name,
        "age": patient.age,
        "address": patient.address
    }
    # print("before update: {}".format(my_patient))
    patient_data = await patients_collection.find_one_and_replace({PATIENT_ID_FIELD: patient_id}, my_patient, return_document=ReturnDocument.AFTER)
    # print("after update: {}".format(patient_data))
    if not patient_data:
        return {"Status": "Not found"}
    patientRes:Patient = Patient(id=patient_data["id"], name=patient_data["name"], age=patient_data["age"], address=patient_data["address"])
    # print("before return: {}".format(patientRes))
    return {"Status": "Updated", "Patient": patientRes}
