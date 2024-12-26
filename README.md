<h1 align="center" id="title">AI Girlfriend Backend</h1>

<p align="center"><img src="https://socialify.git.ci/manideepanasuri/ai_girlfriend_backend/image?language=1&amp;name=1&amp;owner=1&amp;stargazers=1&amp;theme=Auto" alt="project-image"></p>


This repository contains the backend API for an AI companion application, built using Django, Django REST Framework (DRF), Django Channels, and PostgreSQL. It provides the necessary endpoints and real-time communication infrastructure for the frontend to interact with.

## Technologies Used

*   Django: High-level Python web framework.
*   Django REST Framework (DRF): Toolkit for building RESTful APIs with Django.
*   Django Channels: Asynchronous framework for building real-time features with Django.
*   Daphne: ASGI server for deploying WebSocket applications built with Django Channels.
*   PostgreSQL: Relational database management system for persistent data storage.

## Features

*   **RESTful API:** Provides well-defined endpoints for the frontend to manage user data, AI interactions, and other application logic.
*   **Real-time Communication:** Implements WebSockets using Django Channels and Daphne, enabling seamless, low-latency communication with the frontend for interactive conversations.
*   **Data Persistence:** Utilizes PostgreSQL for reliable and scalable data storage.
*   **Asynchronous Handling:** Leverages Daphne to efficiently handle WebSocket connections and other asynchronous tasks.

## Installation and Usage

**(Please note:** This section will depend on your specific project setup. You'll need to fill in the details on how to install dependencies, configure the database, and run the development server.)

1.  Clone the repository:

    ```bash
    git clone https://github.com/manideepanasuri/ai_girlfriend_backend
    ```

2.  Navigate to the project directory:

    ```bash
    cd ai_girlfriend_backend
    ```

3.  Create a virtual environment (recommended):

    ```bash
    python -m venv venv  # For Python 3
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

4.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5.  Configure the database:

    *   Create a PostgreSQL database.
    *   Update the `DATABASES` settings in `settings.py` with your database credentials.

6.  Run database migrations:

    ```bash
    python manage.py migrate
    ```

7.  Run the development server:

    ```bash
    python manage.py runserver
    ```

    Or, for production-like WebSocket handling with Daphne:

    ```bash
    daphne ai_girlfriend_backend.asgi:application
    ```
