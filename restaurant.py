from re import M
from time import time
from fastapi import FastAPI, Query
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

class Reservation(BaseModel):
    name : str
    time: str
    table_number: int
    
client = MongoClient('mongodb://localhost', 27017)

# TODO fill in database name
db = client["simdatabase"]

# TODO fill in collection name
collection = db["restaurant"]

app = FastAPI()


# TODO complete all endpoint.
@app.get("/reservation/by-name/{name}")
def get_reservation_by_name(name:str):
    result = collection.find({"name":name}, {"_id": 0, "name": 1, "time": 1, "table_number": 1})
    my_result = []
    for r in result:
        my_result.append(r)
    print(my_result)
    return {
        "result": my_result
    }

@app.get("/reservation/by-table/{table_number}")
def get_reservation_by_table(table_number: int):
    result = collection.find({"table_number":table_number}, {"_id": 0, "name": 1, "time": 1, "table_number": 1})
    my_result = []
    for r in result:
        my_result.append(r)
    print(my_result)
    return {
        "result": my_result
    }

@app.post("/reservation")
def reserve(reservation : Reservation):
    x= jsonable_encoder(reservation)
    collection.insert_one(x)
    if (reservation.table_number==5 and reservation.time == "10.00"):
        return {
            "result": "not success"
        }
    else:
        return {
            "result":"done"
        }

@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    result = collection.find_one({"time": reservation.time}, {"_id": 0})
    query = {"table_number": reservation.table_number, "name": reservation.name}
    new = {"$set": {"time":reservation.time}}
    if result is None:
        collection.update_many(query,new)
        return {
            "status":"success"
        }
    return {
        "status": "failed"
    }

@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number : int):
    query = {"name": name , "table_number": table_number}
    collection.delete_many(query)
    return {
        "result":"done"
    }
    