from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

app = FastAPI()

class Input(BaseModel):
    a: float
    b: float
    c: float
    d: float

@app.post('/resolver')
def resolver(valores: Input):
    try:
        sum_res = requests.post("http://suma:8000/sumar", json={"a": valores.a, "b": valores.b})
        rest_res = requests.post("http://resta:8000/restar", json={"c": valores.c, "d": valores.d})
        
        suma = sum_res.json().get("resultado")
        resta = rest_res.json().get("resultado")
        
        if suma is None or resta is None:
            raise HTTPException(status_code=500, detail="No se pudo obtener resultado de suma o resta")
        
        resultado = suma * resta
        
        datos_guardar = {
            "a": float(valores.a),
            "b": float(valores.b), 
            "c": float(valores.c),
            "d": float(valores.d),
            "resultado": float(resultado)
        }
        
        # linea para saber pq no se estaba guardando nada
        print(f"Enviando datos a division/guardar: {json.dumps(datos_guardar)}")
        
        try:
            guardar_res = requests.post("http://division:8000/guardar", json=datos_guardar)
            if guardar_res.status_code != 200:
                print(f"Error al guardar: Código {guardar_res.status_code}, Respuesta: {guardar_res.text}")
            guardar_res.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error al guardar el resultado: {e}")
        
        return {"resultado": resultado}
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al comunicarse con los microservicios: {str(e)}")