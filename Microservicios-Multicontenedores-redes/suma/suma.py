from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Input(BaseModel):
    a: float
    b: float

@app.post('/sumar')
def sumar(valores:Input):
    res = valores.a + valores.b
    return {'resultado': res}