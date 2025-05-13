FROM python:3.10-slim
WORKDIR /app
COPY division.py .
RUN pip install fastapi uvicorn pydantic requests mysql-connector-python
CMD ["uvicorn", "division:app", "--host", "0.0.0.0", "--port", "8000"]