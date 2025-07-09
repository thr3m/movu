[English](#english) | [Español](#español)

## Español

### Descripción del Proyecto
Este proyecto es un servicio backend/API construido con Django, diseñado para la gestión de flotas. Proporciona funcionalidades para registrar conductores y autos, y obtener la ubicación de un conductor específico, la cual es obtenida de una API externa ([CountriesNow](https://countriesnow.space)).


### Tecnologías Utilizadas

*   **Backend:** Django 4.2 (utilizado por compatibilidad con las dependencias), Django REST Framework
*   **Base de Datos:** PostgreSQL
*   **Contenedorización:** Docker, Docker Compose
*   **Pruebas:** pytest, pytest-django
*   **Clientes HTTP:** `requests`
*   **Documentación API:** drf-spectacular (Swagger UI, Redoc)

### Estructura del Proyecto

*   `src/apps/`: Contiene las aplicaciones Django (`fleet`, `administration`).
*   `src/config/`: Configuración general del proyecto (settings, urls, wsgi, asgi).
*   `src/lib/`: Librerías y utilidades compartidas (clientes API, helpers, email).
*   `entrypoint.sh`: Script de inicialización del contenedor Docker.
*   `docker-compose.yaml`: Definición de servicios Docker.
*   `.env`: Archivo para variables de entorno.

### Requisitos Previos
Antes de configurar y ejecutar este proyecto:

*   **Docker:** [Instalar Docker](https://docs.docker.com/get-docker/)
*   **Docker Compose:** [Instalar Docker Compose](https://docs.docker.com/compose/install/)

### Configuración y Ejecución

Para configurar y ejecutar este proyecto, sigue los siguientes pasos:

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/thr3m/movu.git
    cd movu
    ```

2.  **Crear el archivo de variables de entorno:**
    Crea un archivo llamado `.env` en la raíz del proyecto con la siguiente estructura. Este archivo contiene la configuración necesaria para la base de datos, la API y otros ajustes de la aplicación.

    ```text
        SECRET_KEY=XXXXXXXXX
        ENV=dev

        DB_NAME=postgres
        DB_USER=postgres
        DB_PASSWORD=postgres
        DB_HOST = movu-db-dev
        DB_PORT=5432
        DB_SCHEMA=public

        BASE_URL_COUNTRIES_NOW=https://countriesnow.space/api/v0.1/

        EMAIL_HOST="smtp-mail.outlook.com"
        EMAIL_PORT=587
        EMAIL_HOST_USER="xxxxxxx@outlook.com"
        EMAIL_HOST_PASSWORD="xxxxxxx"
    ```

3.  **Construir y ejecutar los contenedores Docker:**
    Ejecuta el siguiente comando en la raíz del proyecto. Este comando construirá las imágenes Docker (si no existen) e iniciará los servicios `api` y `db` definidos en el archivo `docker-compose.yaml`.

    ```bash
        docker compose up -d --build
    ```
    *   La API estará disponible en `http://localhost:8000`.
    *   La base de datos PostgreSQL estará disponible en el puerto `5432`.

4.  **Proceso de Inicialización del Contenedor:**
    El script `entrypoint.sh` se ejecuta automáticamente al iniciar el contenedor de la API. `Es importante que este archivo esté formateado usando saltos de línea LF (Line Feed) en lugar de CRLF (Carriage Return + Line Feed) para evitar errores de ejecución en entornos Linux dentro de Docker`. Este script se encarga de:
    *   Recolectar archivos estáticos.
    *   Crear y aplicar migraciones de base de datos.
    *   Ejecutar el script `init_data.py` para la configuración inicial de datos, incluyendo la creación de un superusuario.
    *   Iniciar el servidor de la aplicación con Gunicorn.

5.  **Superusuario por Defecto:**
    Durante el proceso de inicialización, se crea automáticamente un superusuario con las siguientes credenciales para facilitar el acceso inicial como admin, si se requiere:

    ```text
        username: admin
        email: admin@admin.com
        password: admin123456
    ```

6.  **Acceder a la Documentación de la API:**
    Una vez que los contenedores estén en funcionamiento, puedes interactuar con la API y ver la documentación interactiva (Swagger UI) en el siguiente endpoint:

    - [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
    - [http://localhost:8000/api/docs/redoc/](http://localhost:8000/api/docs/redoc/)

### Ejecución de Pruebas

Para ejecutar las pruebas dentro del contenedor, utiliza el siguiente comando:

```bash
    docker compose exec api sh -c "DJANGO_SETTINGS_MODULE=config.settings.test pytest"
```

### Endpoints

El proyecto expone los siguientes endpoints principales:

*   **`/api/admin/`**: Incluye los endpoints para la gestión de `Car` y `Driver` a través de ViewSets. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre estos recursos.
*   **`/api/driver/<uuid:pk>/location`**: Permite obtener la ubicación (ciudad) de un conductor específico utilizando su ID (`pk`). Esta información se obtiene de una API externa de la siguiente manera:
    1.  El endpoint utiliza el `DriverCityLocationRetrieveAPIView`.
    2.  Se inicializa un servicio (`CountryDataService`) que interactúa con un cliente (`CountriesNowClient`) para la API externa CountriesNow.
    3.  El servicio solicita al cliente una lista de ciudades para un país y estado específicos, por defecto se usa como pais Colombia y estado Bogota.
    4.  El cliente realiza una solicitud HTTP GET a la API de CountriesNow (`/countries/state/cities/q`).
    5.  La API externa responde con una lista de ciudades.
    6.  El servicio selecciona una ciudad aleatoria de la lista recibida.
    7.  Esta ciudad aleatoria se devuelve como la ubicación del conductor y se asigna a la variable city_location.
    8.  En caso de fallo en la comunicación con la API externa, se registra el error y se envía una notificación por correo electrónico y se retorna `None`.
*   **`/api/user/`**: Incluye los endpoints para la gestión de `User` a través de un ViewSet. Permite realizar operaciones CRUD sobre los usuarios.

Para una documentación detallada de todos los endpoints y sus parámetros, consulta la documentación (Swagger UI) en [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/).

## English

### Project Description
This project is a backend/API service built with Django, designed for fleet management. It provides functionalities to register drivers and cars, and to retrieve the location of a specific driver, which is obtained from an external API ([CountriesNow](https://countriesnow.space)).

### Technologies Used
*   **Backend:** Django 4.2 (used for dependency compatibility), Django REST Framework
*   **Database:** PostgreSQL
*   **Containerization:** Docker, Docker Compose
*   **Testing:** pytest, pytest-django
*   **HTTP Clients:** `requests`
*   **API Documentation:** drf-spectacular (Swagger UI, Redoc)

### Project Structure
*   `src/apps/`: Contains the Django applications (`fleet`, `administration`).
*   `src/config/`: General project configuration (settings, urls, wsgi, asgi).
*   `src/lib/`: Shared libraries and utilities (API clients, helpers, email).
*   `entrypoint.sh`: Docker container initialization script.
*   `docker-compose.yaml`: Docker services definition.
*   `.env`: Environment variables file.

### Prerequisites
Before setting up and running this project:
*   **Docker:** [Install Docker](https://docs.docker.com/get-docker/)
*   **Docker Compose:** [Install Docker Compose](https://docs.docker.com/compose/install/)

### Setup and Execution
To set up and run this project, follow these steps:
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/thr3m/movu.git
    cd movu
    ```
2.  **Create the environment variables file:**
    Create a file named `.env` in the project root with the following structure. This file contains the necessary configuration for the database, API, and other application settings.
    ```text
        SECRET_KEY=XXXXXXXXX
        ENV=dev
        DB_NAME=postgres
        DB_USER=postgres
        DB_PASSWORD=postgres
        DB_HOST = movu-db-dev
        DB_PORT=5432
        DB_SCHEMA=public
        BASE_URL_COUNTRIES_NOW=https://countriesnow.space/api/v0.1/
        EMAIL_HOST="smtp-mail.outlook.com"
        EMAIL_PORT=587
        EMAIL_HOST_USER="xxxxxxx@outlook.com"
        EMAIL_HOST_PASSWORD="xxxxxxx"
    ```
3.  **Build and run Docker containers:**
    Execute the following command in the project root. This command will build the Docker images (if they don't exist) and start the `api` and `db` services defined in the `docker-compose.yaml` file.
    ```bash
        docker compose up -d --build
    ```
    *   The API will be available at `http://localhost:8000`.
    *   The PostgreSQL database will be available on port `5432`.
4.  **Container Initialization Process:**
    The `entrypoint.sh` script automatically runs when the API container starts.`It is important that this file is formatted using LF (Line Feed) line endings instead of CRLF (Carriage Return + Line Feed) to avoid execution errors in Linux environments within Docker`. This script is responsible for:
    *   Collecting static files.
    *   Creating and applying database migrations.
    *   Executing the `init_data.py` script for initial data setup, including superuser creation.
    *   Starting the application server with Gunicorn.
5.  **Default Superuser:**
    During the initialization process, a superuser is automatically created with the following credentials to facilitate initial admin access, if required:
    ```text
        username: admin
        email: admin@admin.com
        password: admin123456
    ```
6.  **Access API Documentation:**
    Once the containers are running, you can interact with the API and view the interactive documentation (Swagger UI) at the following endpoint:
    - [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
    - [http://localhost:8000/api/docs/redoc/](http://localhost:8000/api/docs/redoc/)

### Running Tests
To run tests inside the container, use the following command:
```bash
    docker compose exec api sh -c "DJANGO_SETTINGS_MODULE=config.settings.test pytest"
```

### Endpoints
The project exposes the following main endpoints:
*   **`/api/admin/`**: Includes endpoints for `Car` and `Driver` management via ViewSets. Allows for CRUD (Create, Read, Update, Delete) operations on these resources.
*   **`/api/driver/<uuid:pk>/location`**: Allows retrieving the location (city) of a specific driver using their ID (`pk`). This information is obtained from an external API as follows:
    1.  The endpoint uses the `DriverCityLocationRetrieveAPIView`.
    2.  A service (`CountryDataService`) is initialized that interacts with a client (`CountriesNowClient`) for the external CountriesNow API.
    3.  The service requests a list of cities for a specific country and state from the client; by default, Colombia and Bogotá are used as the country and state.
    4.  The client makes an HTTP GET request to the CountriesNow API (`/countries/state/cities/q`).
    5.  The external API responds with a list of cities.
    6.  The service selects a random city from the received list.
    7.  This random city is returned as the driver's location.
    8.  In case of communication failure with the external API, the error is logged, an email notification is sent, and `None` is returned.
*   **`/api/user/`**: Includes endpoints for `User` management via a ViewSet. Allows for CRUD operations on users.

For detailed documentation of all endpoints and their parameters, please refer to the documentation (Swagger UI) at [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/).