# Guía de estudio — Defensa oral del TP

Esta guía está pensada para que puedas explicar el proyecto con tus propias
palabras. No la memorices de corrido: entendé cada bloque y practicá decirlo
como si le explicaras a un compañero.

---

## 1. Conceptos base (te los pueden preguntar sueltos)

### ¿Qué es una API?
Es un programa que expone datos y funciones para que otros programas (en este
caso, tu página web) puedan usarlos sin necesidad de acceder directamente a
la base de datos. Funciona como un mozo entre el cliente (frontend) y la
cocina (los datos).

### ¿Qué son los métodos HTTP que usaste?
- **GET**: pedir datos (leer). No modifica nada.
- **POST**: crear un dato nuevo.
- **PUT**: editar un dato que ya existe.
- **DELETE**: eliminar un dato.

### ¿Qué es la asincronía y por qué la necesitás?
Pedirle datos a una API tarda un tiempo variable (depende de la red, del
servidor). JavaScript no se detiene a esperar: sigue ejecutando otras cosas
y "retoma" cuando la respuesta llega. Esto evita que la página se quede
congelada mientras espera al servidor.

### ¿Qué hacen `async` y `await`?
- `async` marca que una función va a manejar operaciones asincrónicas.
- `await` pausa **esa función puntual** (no la página entera) hasta que la
  operación (por ejemplo, un `fetch`) termine, y te da el resultado real en
  lugar de una promesa pendiente.

### ¿Qué es `fetch`?
La función de JavaScript que usás para hacer una petición HTTP desde el
navegador hacia una URL (en tu caso, hacia la API de FastAPI).

### ¿Qué es JSON y por qué se usa?
Es un formato de texto para representar datos (objetos, listas, números,
strings) que entienden tanto JavaScript como Python. La API responde en
JSON, y vos lo convertís a objetos de JS con `.json()`.

### ¿Qué es localStorage y en qué se diferencia de una variable normal?
Es un espacio de almacenamiento del navegador que persiste los datos aunque
cierres la pestaña o el navegador. Una variable de JS común se borra al
recargar la página; lo que está en localStorage, no.

### ¿Por qué tuviste que usar `JSON.stringify` y `JSON.parse`?
localStorage solo puede guardar **texto**. `JSON.stringify` convierte un
objeto/array de JS a texto para poder guardarlo. `JSON.parse` hace el
camino inverso: convierte ese texto guardado de nuevo en un objeto/array
que JS pueda usar.

---

## 2. Recorrido de tu propio código (para señalar en vivo)

### Backend (`main.py`)

- **Modelo `Pelicula` (clase con Pydantic)**: define qué forma deben tener
  los datos que llegan en un POST (título, género, año, sinopsis, imagen).
  Si falta un campo obligatorio o el tipo está mal, FastAPI rechaza la
  petición automáticamente, sin que tengas que validar a mano.
- **`leer_datos()` / `guardar_datos()`**: funciones helper que abren el
  archivo `data.json`, leen o escriben en él. Separar esto en funciones
  evita repetir el mismo código de abrir/cerrar archivo en cada endpoint.
- **Los 5 endpoints** (`@app.get`, `@app.post`, etc.): cada decorador le dice
  a FastAPI "esta función se ejecuta cuando llega una petición de tipo X a
  esta ruta". Adentro, cada función hace una operación distinta sobre los
  datos (leer todos, leer uno, agregar, modificar, borrar).
- **`CORSMiddleware`**: sin esto, el navegador bloquearía las peticiones del
  `index.html` hacia la API por una política de seguridad llamada CORS, que
  por defecto impide que una página le pida datos a un servidor con otro
  "origen" (otro dominio/puerto). Lo habilitamos explícitamente para
  permitir que el frontend hable con esta API.

### Frontend (`index.html`)

- **Las funciones `obtenerPeliculas`, `crearPelicula`, `editarPelicula`,
  `eliminarPelicula`**: cada una hace un `fetch` con el método HTTP que
  corresponde. Están separadas para que el resto del código no tenga que
  preocuparse de los detalles de la petición, solo llama a la función.
- **`mostrarVista()`**: la función que oculta todas las secciones y muestra
  solo una. Así toda la "navegación" pasa por JS, sin recargar la página ni
  cambiar de URL — por eso es "una sola ruta URL" como pide la consigna.
- **`crearFicha()`**: genera el HTML de una ficha de película, tanto para el
  catálogo como para favoritos (la reutilizás en los dos lugares, no
  duplicás código).
- **`obtenerFavoritos()` / `guardarFavoritos()` / `alternarFavorito()`**: los
  helpers de localStorage. `alternarFavorito` revisa si la película ya está
  en la lista: si está, la saca; si no está, la agrega.
- **Los `addEventListener`**: cada botón (ver detalle, favorito, crear,
  editar, eliminar) tiene un evento asociado que dispara la función
  correspondiente.

---

## 3. Preguntas típicas que te puede hacer el profesor

**¿Por qué separaste el backend del frontend?**
Porque son responsabilidades distintas: el backend maneja los datos y la
lógica de negocio, el frontend se encarga de mostrarlos e interactuar con
el usuario. Además es el patrón real que se usa en la industria (API +
cliente que la consume).

**¿Qué pasa si el backend no está corriendo?**
El `fetch` falla, y en tu código eso está manejado con `try/catch`: se
muestra un mensaje de error en pantalla en vez de romper la página.

**¿Por qué usaste un archivo JSON y no una base de datos real?**
Para mantenerlo simple a nivel de la consigna del TP. El archivo cumple la
misma función básica que una base de datos (persistir los datos entre
reinicios del servidor), pero sin la complejidad de configurar un motor de
base de datos.

**¿Qué diferencia hay entre guardar algo en la API y guardarlo en
localStorage?**
Lo que está en la API (`data.json`) es el catálogo "oficial", compartido,
que cualquiera que use la app puede ver. Lo que está en localStorage (los
favoritos) es local a tu navegador: es información personal de cada
usuario, no se comparte ni se manda al servidor.

**¿Por qué el botón de favoritos no manda nada al backend?**
Porque la consigna pide que favoritos se maneje con localStorage
específicamente (R3), no como parte de los datos del servidor.

**¿Qué pasaría si dos personas usan la app al mismo tiempo y las dos crean
una película?**
Como los datos viven en un archivo compartido en el servidor, ambas
peliculas se guardarían (cada una con un id distinto, calculado a partir
del máximo id existente). Si hicieran cambios al mismo tiempo de forma muy
simultánea podría haber una condición de carrera, pero para los fines de
este TP no se maneja ese caso avanzado.

**Mostrame que el PUT funciona.**
Sugerencia: abrí `/docs` (la interfaz de Swagger de FastAPI) y mostrá ahí
un PUT en vivo, o hacelo desde la app editando una película y mostrando que
el cambio persiste si recargás la página.

---

## 4. Checklist para practicar en voz alta

Practicá decir esto en orden, como si dieras un recorrido guiado:

1. "Esta es la página principal, acá se ve el catálogo que viene de la API."
   *(mostrás la vista de lista)*
2. "Si clickeo una película, pido su detalle con un GET a `/api/{id}`."
   *(mostrás la vista de detalle)*
3. "Desde el detalle puedo editar — esto dispara un PUT — o eliminar, que
   dispara un DELETE."
4. "Acá puedo agregar una nueva película — esto es un POST."
5. "Esta estrella guarda la película en localStorage, así que aunque
   recargue la página sigue apareciendo en 'Mis favoritos'."
   *(lo demostrás recargando la página en vivo)*
6. "Y en el código del backend, así están armados los 5 endpoints..."
   *(mostrás `main.py`)*

Si podés decir estos 6 puntos sin leer, ya estás más que preparado para la
defensa.
