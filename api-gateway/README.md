# StreamSphere - API Gateway

API Gateway para StreamSphere Web construido con Spring Boot 3 y Spring Cloud Gateway.

## Requisitos

- Java 21 (JDK)
- Maven 3.8+

## Instalacion y ejecucion (Arch Linux)

### 1. Verificar versiones

```bash
java --version
mvn --version
```

### 2. Compilar el proyecto

```bash
cd api-gateway
mvn clean package -DskipTests
```

### 3. Ejecutar el Gateway

```bash
mvn spring-boot:run
```

O bien:

```bash
java -jar target/api-gateway-1.0.0.jar
```

El Gateway se iniciara en: http://localhost:8080

## Rutas configuradas

| Ruta del Gateway          | Destino                  |
|---------------------------|--------------------------|
| `/api/analysis/**`        | `http://localhost:8095`  |

### Ejemplo de uso

El frontend llama a:

```
POST http://localhost:8080/api/analysis/predict
```

El Gateway redirige a:

```
POST http://localhost:8095/predict
```

## Endpoints de Actuator

- `http://localhost:8080/actuator/health`
- `http://localhost:8080/actuator/info`

## CORS

Origenes permitidos:
- http://localhost:3000
- http://localhost:5173
- http://localhost:4200

## Prueba rapida

```bash
curl -X POST http://localhost:8080/api/analysis/predict \
  -H "Content-Type: application/json" \
  -d '{
    "duration_seconds": 300,
    "category": "Tecnologia",
    "publish_hour": 14,
    "publish_weekday": 3,
    "title_length": 50,
    "description_length": 250,
    "is_hd": 1,
    "creator_subscribers": 200000,
    "creator_avg_views_30d": 15000
  }'
```