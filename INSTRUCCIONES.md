# Cómo instalar y correr el proyecto — Guía paso a paso

Este TP tiene 2 partes que corren juntas:
1. **Backend** (FastAPI - Python) → es el TP01 de la materia PP1 - Python
2. **Frontend** (`index.html` - JavaScript) → es este TP Evaluativo

El frontend necesita que el backend esté corriendo para poder mostrar datos.

---

## PASO 1: Instalar Python

1. Entrá a https://www.python.org/downloads/
2. Descargá la última versión (cualquier 3.10 o superior funciona).
3. **IMPORTANTE (Windows):** al abrir el instalador, tildá la casilla que dice
   **"Add Python to PATH"** antes de hacer click en "Install Now". Si no la
   tildás, después no vas a poder usar el comando `python` desde la terminal.
4. Para confirmar que se instaló bien, abrí una terminal (en Windows: `cmd` o
   `PowerShell`; en Mac/Linux: `Terminal`) y escribí:
   ```
   python --version
   ```
   Te tiene que mostrar algo como `Python 3.12.x`. Si te da error, reiniciá la
   computadora y probá de nuevo (a veces el PATH no se actualiza hasta reiniciar).

---

## PASO 2: Ubicar la carpeta del proyecto

Vas a tener una carpeta `proyecto-peliculas` con esta estructura:

```
proyecto-peliculas/
├── backend/
│   ├── main.py          (el código de la API)
│   ├── data.json         (donde se guardan las películas)
│   └── requirements.txt  (lista de paquetes necesarios)
└── frontend/
    └── index.html         (la página web, este TP)
```

Movela a un lugar fácil de encontrar, como el Escritorio.

---

## PASO 3: Instalar las dependencias del backend

1. Abrí una terminal.
2. Navegá hasta la carpeta `backend`. Por ejemplo, si la pusiste en el
   Escritorio:
   ```
   cd Desktop/proyecto-peliculas/backend
   ```
   (en Windows puede ser `cd Desktop\proyecto-peliculas\backend`)

3. Instalá las dependencias con este comando:
   ```
   pip install -r requirements.txt
   ```
   Esto instala **FastAPI** (el framework para crear la API) y **uvicorn**
   (el servidor que la hace correr). Puede tardar uno o dos minutos.

   > Si `pip` no funciona, probá `pip3` o `python -m pip install -r requirements.txt`

---

## PASO 4: Levantar el backend (la API)

Desde la misma terminal, parado en la carpeta `backend`, ejecutá:

```
uvicorn main:app --reload
```

Si todo salió bien, vas a ver algo como:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

**Dejá esta terminal abierta y corriendo todo el tiempo** mientras usás la
página web. Si la cerrás, la API se apaga y el frontend deja de funcionar.

### Para comprobar que funciona

Abrí el navegador y entrá a:
- http://127.0.0.1:8000/api/ → te debería mostrar la lista de películas en formato JSON
- http://127.0.0.1:8000/docs → te abre una interfaz interactiva (Swagger) donde
  podés probar cada endpoint (GET, POST, PUT, DELETE) sin necesidad del frontend.
  **Esto es muy útil para la defensa oral**, podés mostrar ahí que la API funciona.

---

## PASO 5: Abrir el frontend

Con el backend corriendo (paso anterior), abrí el archivo `frontend/index.html`
haciendo doble click sobre él. Se va a abrir en tu navegador y debería mostrar
el catálogo de películas automáticamente.

> Si ves el mensaje "No se pudo conectar con la API", revisá que la terminal
> del backend siga abierta y sin errores.

---

## Resumen para el día de la defensa

Cada vez que quieras mostrar el proyecto funcionando:

1. Abrís una terminal, vas a la carpeta `backend`, y corrés:
   ```
   uvicorn main:app --reload
   ```
2. Dejás esa terminal abierta.
3. Abrís `frontend/index.html` en el navegador (o lo recargás si ya lo tenías abierto).

¡Listo! Con eso tenés todo funcionando para mostrar en vivo.
