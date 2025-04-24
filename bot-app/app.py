import sys
import os

if len(sys.argv) != 3:
    print("Uso: python app.py <usuario> <pregunta>")
    sys.exit(1)

usuario = sys.argv[1]
pregunta = sys.argv[2]

historial_path = "/app/historial/historial.txt"

with open(historial_path, "a") as f:
    f.write(f"{usuario}: {pregunta}\n")

print("Pregunta guardada correctamente.")
