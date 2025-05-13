FROM python:3.10-slim
WORKDIR /app
COPY multiplicacion.py .
RUN pip install fastapi uvicorn pydantic requests
CMD ["uvicorn", "multiplicacion:app", "--host", "0.0.0.0", "--port", "8000"]