# import:
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field # (to be able to use further pydantic validation)

# to be able to use further pydantic validation
from typing import Optional

# command that enables the framework/terminal used to display a user-friendly UI
app = FastAPI(
# change the Swagger page name in FastAPI UI display
    title='Airports',
    description='This is a sampling APIs for Airport.'
)
# text values for the Swagger method group name/tags in FastAPI UI display
tags_metadata = [
    {
        "name": "Airports",
        "description": "Airport list. Link on the documentation on the right.",
        "externalDocs": {
            "description": "Sampling Test automation documentation",
            "url": "https://github.com/njmlopez17/Python_VBCode_PyTest/blob/99f193d74e9729fb4b5fc8d38c81c3592de453c1/Test%20Automation%20End-to-End%20documentation.pdf",
        },
    },
]

# sample data library
airport_db = {
    'a': {'airport_id': 'aa', 'airport_name': 'To Sky Airport', 'city': 'Flying Lake AK', 'country_state': 'US Alaska'},
    'b': {'airport_id': 'bb', 'airport_name': 'Bear Creek Mining Strip', 'city': 'Granite Mountain CA',
          'country_state': 'US California'},
    'c': {'airport_id': 'cc', 'airport_name': 'Little Squaw Airport', 'city': 'Little Squaw FL',
          'country_state': 'US Florida'}
}

# the class used to create a data into the data library or db
class Airport(BaseModel):
    airport_id: str = Field(min_length=2, max_length=20) # (utilizing further pydantic validation)
    airport_name: str = Field(min_length=3, max_length=20) # (utilizing further pydantic validation)
    city: str = Field(min_length=3, max_length=20) # (utilizing further pydantic validation)
    country_state: Optional[str] = None # (this makes the field not mandatory)

# functions that raise error response(s) that can be use and reuse in various methods

# check if data exist
def check_airport_id_in_db (airport_id: str):
    if airport_id in airport_db:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail=f'Airport_ID {airport_id} exist in database.')
# check if data does not exist
def check_airport_id_not_in_db (airport_id: str):
    if airport_id not in airport_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Airport_ID {airport_id} not found.')

# change the Swagger method group name/tags in FastAPI UI display
app.openapi_tags=tags_metadata

#==========Method calls below===============

# GET method (returning ALL results)
@app.get('/airports', tags=["Airports"])
def get_airport():
    # return result as a list
    airport_list = list(airport_db.values())
    return airport_list

#GET method (returning DEFAULT LIMITED results)
@app.get('/airports', tags=["Airports"])
def get_airport_query(limit: int = 20):
    # return limited result as a list
    airport_list = list(airport_db.values())
    return airport_list [:limit]

# POST method (creating data in the data library or db)
@app.post('/airports', tags=["Airports"])
def create_airport(airport: Airport):
    airport_id = airport.airport_id
    check_airport_id_in_db(airport_id) #validation
    airport_db[airport_id] = airport.model_dump()
    return {'message': f'Successfully created airport: {airport_id}'}

# PUT method (updating data in the data library or db)
@app.put('/airports', tags=["Airports"])
def update_airport(airport: Airport):
    airport_id = airport.airport_id
    airport_db[airport_id] = airport.model_dump()
    return {'message': f'Successfully updated airport: {airport_id}'}

# PATCH method (updating specific/partial data in the data library or db)
@app.patch('/airports', tags=["Airports"])
def update_airport_partial(airport: Airport):
    airport_id = airport.airport_id
    check_airport_id_not_in_db(airport_id)  # validation
    airport_db[airport_id].update(airport.model_dump(exclude_unset=True))
    return {'message': f'Successfully updated specific data of the airport: {airport_id}'}

# DELETE method (deleting data from the data library or db)
@app.delete('/airports/{airport_id}', tags=["Airports"])
def delete_airport(airport_id: str):
    check_airport_id_not_in_db(airport_id)  # validation
    del airport_db[airport_id]
    return {'message': f'Successfully deleted airport: {airport_id}'}

























