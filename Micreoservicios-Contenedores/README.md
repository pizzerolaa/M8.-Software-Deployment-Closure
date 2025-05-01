# Microservicios para Cálculo de Áreas

Este proyecto implementa tres microservicios en contenedores Docker para calcular el área de diferentes figuras geométricas:

- Círculo
- Cuadrado
- Triángulo

## Estructura del Proyecto

```
.
├── docker-compose.yaml
├── README.md
├── circulo/
│   ├── app.py
│   └── Dockerfile
├── cuadrado/
│   ├── app.py
│   └── Dockerfile
└── triangulo/
    ├── app.py
    └── Dockerfile
```

## Cómo ejecutar

1. Asegúrate de tener Docker y Docker Compose instalados en tu sistema
2. Clona este repositorio
3. Navega a la carpeta del proyecto
4. Ejecuta: `docker-compose up --build`
5. Los servicios estarán disponibles en:
   - Círculo: http://localhost:5000/area?radio=5
   - Cuadrado: http://localhost:5001/area?lado=4
   - Triángulo: http://localhost:5002/area?base=6&altura=3

## API Endpoints

### Círculo
- URL: `/area`
- Método: GET
- Parámetros: `radio` (número positivo)
- Ejemplo: `curl "http://localhost:5000/area?radio=5"`

### Cuadrado
- URL: `/area`
- Método: GET
- Parámetros: `lado` (número positivo)
- Ejemplo: `curl "http://localhost:5001/area?lado=4"`

### Triángulo
- URL: `/area`
- Método: GET
- Parámetros: `base` y `altura` (números positivos)
- Ejemplo: `curl "http://localhost:5002/area?base=6&altura=3"`