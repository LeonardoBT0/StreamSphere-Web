# StreamSphere - Frontend Web

Interfaz web para probar el modulo de analisis de rendimiento de videos de StreamSphere.

Construido con React + Vite.

## Requisitos

- Node.js 18+
- npm 9+

## Instalacion y ejecucion (Arch Linux)

### 1. Instalar Node.js (si no esta instalado)

```bash
sudo pacman -S nodejs npm
```

### 2. Entrar al modulo e instalar dependencias

```bash
cd frontend-web
npm install
```

### 3. Iniciar el servidor de desarrollo

```bash
npm run dev
```

La aplicacion estara disponible en: http://localhost:5173

## Arquitectura

```
frontend-web (React :5173)
  │
  │ POST /api/analysis/predict
  ▼
api-gateway (:8080)
  │
  │ StripPrefix=2 → /predict
  ▼
analysis-service (:8095)
```

El proxy de Vite redirige `/api/*` hacia `http://localhost:8080` (API Gateway),
que a su vez aplica `StripPrefix=2` y reenvia a `http://localhost:8095/predict`.

## Uso

1. Asegurate de que estos servicios esten corriendo:
   - `analysis-service` en `:8095`
   - `api-gateway` en `:8080`

2. Abre http://localhost:5173

3. El formulario tiene valores de prueba precargados.

4. Haz clic en **Analizar rendimiento** para obtener la prediccion.

## Scripts disponibles

| Comando         | Descripcion                      |
|-----------------|----------------------------------|
| `npm run dev`   | Inicia servidor de desarrollo    |
| `npm run build` | Compila para produccion          |
| `npm run preview` | Preview de la build produccion |