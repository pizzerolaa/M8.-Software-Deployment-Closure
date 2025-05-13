from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Input(BaseModel):
    c: float
    d: float

@app.post('/restar')
def sumar(valores:Input):
    res = valores.c - valores.d
    return {'resultado': res}