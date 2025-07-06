@@ -0,0 +1,44 @@
# Kharjam Backend

This is the backend for the Kharjam project, built using FastAPI.

## Repository

GitHub Repository: [Kharjam](https://github.com/AhEsmaeili79/Kharjam)

## Features

- FastAPI framework for building APIs.
- Modular and scalable architecture.
- Easy integration with databases and external services.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/AhEsmaeili79/Kharjam.git
    cd Kharjam
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    uvicorn main:app --reload  
    ```
    OR 

    ```bash
    fastapi dev
    ```

## Usage

Access the API documentation at `http://127.0.0.1:8000/docs` after running the application.

## License

This project is licensed under the MIT License.