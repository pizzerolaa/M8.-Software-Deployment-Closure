#  Deploy de Microservicios en Kubernetes

Este proyecto implementa un sistema de cálculo distribuido utilizando una arquitectura de microservicios, donde diferentes operaciones matemáticas (suma, resta, división y ecuación) están separadas en servicios independientes que se comunican entre sí. El despliegue se realiza utilizando Kubernetes para la orquestación de contenedores.

## Descripción de la Arquitectura

El sistema está compuesto por los siguientes microservicios:

- **Suma**: Realiza operaciones de suma entre dos números
- **Resta**: Realiza operaciones de resta entre dos números
- **División**: Realiza operaciones de división y almacena resultados en MySQL
- **Ecuación**: Coordina las operaciones entre los demás servicios para resolver ecuaciones

Además, incluye:
- **Base de datos MySQL**: Almacena los resultados de las ecuaciones
- **Ingress Controller**: Proporciona acceso externo a los servicios

## Requisitos Previos

- Docker
- Kubernetes (minikube, Docker Desktop con Kubernetes, o un clúster real)
- kubectl
- Git

## Estructura del Proyecto

```
Microservicios-Multicontenedores-redes/
├── suma/
│   ├── suma.py
│   └── Dockerfile
├── resta/
│   ├── resta.py
│   └── Dockerfile
├── division/
│   ├── division.py
│   └── Dockerfile
├── ecuacion/
│   ├── multiplicacion.py
│   └── Dockerfile
├── kubernetes/
│   ├── suma-deployment.yaml
│   ├── resta-deployment.yaml
│   ├── division-deployment.yaml
│   ├── ecuacion-deployment.yaml
│   ├── mysql-deployment.yaml
│   ├── mysql-secrets.yaml
│   └── ingress.yaml
└── compose.yaml
```

## Instrucciones de Despliegue

### 1. Clonar el Repositorio

```bash
git clone https://github.com/pizzerolaa/M8.-Software-Deployment-Closure.git
cd Microservicios-Multicontenedores-redes
```

### 2. Construir las Imágenes Docker

Primero, construye las imágenes de Docker para cada microservicio:

```bash
# Configurar Docker para usar el daemon de Minikube (solo si usas Minikube)
eval $(minikube docker-env)  # En PowerShell: & minikube -p minikube docker-env | Invoke-Expression

# Construir imágenes
docker build -t suma:latest ./suma
docker build -t resta:latest ./resta
docker build -t division:latest ./division
docker build -t ecuacion:latest ./ecuacion
```

### 3. Desplegar en Kubernetes

Aplica los archivos YAML para crear los recursos en Kubernetes:

```bash
# Crear secretos para MySQL
kubectl apply -f kubernetes/mysql-secrets.yaml

# Desplegar MySQL
kubectl apply -f kubernetes/mysql-deployment.yaml

# Esperar a que MySQL esté listo (opcional pero recomendado)
echo "Esperando a que MySQL esté listo..."
kubectl wait --for=condition=ready pod -l app=mysql --timeout=120s

# Desplegar los microservicios
kubectl apply -f kubernetes/suma-deployment.yaml
kubectl apply -f kubernetes/resta-deployment.yaml
kubectl apply -f kubernetes/division-deployment.yaml
kubectl apply -f kubernetes/ecuacion-deployment.yaml

# Configurar Ingress (asegúrate de tener el controlador de Ingress instalado)
kubectl apply -f kubernetes/ingress.yaml
```

### 4. Configurar Acceso con Ingress

Si estás usando Minikube, habilita el complemento de Ingress:

```bash
minikube addons enable ingress
```

Edita tu archivo hosts para asociar el nombre de host con la IP:

```bash
# Obtener la IP de Minikube
minikube ip

# Añadir al archivo hosts (como administrador)
# En Windows: C:\Windows\System32\drivers\etc\hosts
# En Linux/Mac: /etc/hosts
# Añadir: <IP-MINIKUBE> microservicios.local
```

### 5. Verificar que todo funciona

```bash
# Verificar que todos los pods están ejecutándose
kubectl get pods

# Verificar los servicios
kubectl get services

# Verificar el Ingress
kubectl get ingress
```

## Pruebas

Una vez desplegado, puedes probar los servicios:

### Usando Ingress

```bash
# Operación de suma
curl -X POST http://microservicios.local/suma/sumar -H "Content-Type: application/json" -d '{"a": 5, "b": 3}'

# Operación de resta
curl -X POST http://microservicios.local/resta/restar -H "Content-Type: application/json" -d '{"c": 10, "d": 4}'

# Operación de división
curl -X POST http://microservicios.local/division/dividir -H "Content-Type: application/json" -d '{"dividendo": 8, "divisor": 2}'

# Resolver ecuación completa
curl -X POST http://microservicios.local/ecuacion/resolver -H "Content-Type: application/json" -d '{"a": 2, "b": 3, "c": 8, "d": 2}'

# Ver historial de operaciones
curl http://microservicios.local/division/historial
```

### Usando NodePort (alternativa a Ingress)

El servicio ecuación también está expuesto con NodePort (puerto 30003):

```bash
# Obtener la URL en Minikube
minikube service ecuacion --url

# O usar directamente la IP del nodo con el puerto 30003
curl -X POST http://<IP-NODO>:30003/resolver -H "Content-Type: application/json" -d '{"a": 2, "b": 3, "c": 8, "d": 2}'
```

## Componentes del Sistema

### Microservicios Backend

- **Suma**: Proporciona la API `/sumar` que acepta dos números (a, b) y devuelve su suma
- **Resta**: Proporciona la API `/restar` que acepta dos números (c, d) y devuelve su resta
- **División**: Proporciona la API `/dividir` para división y `/guardar` para almacenar resultados
- **Ecuación**: Coordina operaciones complejas con los demás servicios

### Base de Datos

El servicio MySQL almacena los resultados en la tabla `resultados` con los siguientes campos:
- id (clave primaria)
- a, b, c, d (operandos de la ecuación)
- resultado
- fecha_creación

## Solución de Problemas

- **Pods con estado `ImagePullBackOff`**: Asegúrate de construir las imágenes localmente y usar `imagePullPolicy: IfNotPresent`
- **Servicio de Ingress sin dirección IP**: Verifica que el controlador de Ingress esté instalado y funcionando
- **Error de conexión a MySQL**: El microservicio division esperará hasta que MySQL esté disponible

## Desarrollo Adicional

Para desarrollar nuevas funcionalidades:

1. Modifica o crea nuevos microservicios
2. Construye las imágenes Docker
3. Actualiza o crea nuevos archivos de configuración de Kubernetes
4. Aplica los cambios con `kubectl apply`

## Arquitectura con Docker Compose (alternativa a Kubernetes)

El proyecto también incluye un archivo compose.yaml para desplegar con Docker Compose:

```bash
docker-compose up --build
```

