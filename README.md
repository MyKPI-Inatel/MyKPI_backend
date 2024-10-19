# MyKPI Backend

## Overview

MyKPI is a backend application developed with FastAPI, providing an API for data management and associated operations.

## Running the API Locally

To run the API locally, follow the steps below:

1. Navigate to the application directory:
   ```bash
   cd app/
   ```

2. Load the environment variables:
   ```bash
   source .env.sh
   ```

3. Start the Uvicorn server:
   ```bash
   uvicorn main:appServer --reload
   ```

### Accessing the API

After starting the server, you can access your API at:
- **Base URL**: [http://localhost:8000](http://localhost:8000)
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

The interactive documentation (Swagger UI) allows you to explore and test the endpoints of your API.

### Note

Ensure that no other application is using port **8000** on your system, as this may cause conflicts. If necessary, you can change the port using the `--port` argument when starting the server.

If you encounter any issues or have questions while running the API locally, feel free to ask!

---

## Running the API with Docker

To run the API locally using Docker, you can use the following command at the root of the application (directory `mykpi-backend`):

```bash
docker-compose up --build
```

---

## Database Connection

To connect to the database, load the environment variables:

```bash
source .env.sh
```

**Note**: To use the database, you must have the `.env.sh` file created and the project running locally.