from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pickle
import pandas as pd
from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKey

from starlette.status import HTTP_403_FORBIDDEN

app = FastAPI(title="Examen Final API",
              description="Esta API responde si un proyecto va a ser patrocinado o no con base en una descripción"
                          " del proyecto dada.",
              version="0.0.1")

API_KEY = "1234567asdfgh"
API_KEY_NAME = "access_token"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)


def get_api_key(api_key_query: str = Security(api_key_query)):

    if api_key_query == API_KEY:
        return api_key_query
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


class Funded(BaseModel):
    description: str


@app.on_event("startup")
def load_matrix():
    global model_funded
    with open("../model/funded_logmodel.sav", "rb") as openfile:
        model_funded = pickle.load(openfile)


@app.get("/api/v1/recommend")
def classify_funded(funded: Funded, api_key: APIKey = Depends(get_api_key)):
    params = [[funded.description]]
    text = "Our project is amazing compared to other projects because our team has the best people on Earth, you should definitely fund us"
    text_tfidf = tfidf.transform([text]).toarray()

    dict_funded = {0: "Not Funded",
                   1: "Funded"}

    return {"Result": dict_funded.get(pred[0]),
            "Desc": "Predicción hecha correctamente."}


@app.get("/")
def home():
    return{"Desc": "Health Check"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
