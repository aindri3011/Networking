# Django Networking API

This is a Django project that provides a networking API. The project includes Docker configuration for easy setup and deployment. Below, you will find step-by-step instructions on how to install and run this project locally.

## Features
- User signup/login with email and password
- User search by email or name with pagination (10 set as default)
- Sending, accepting, and rejecting friend requests
- Listing friends and pending friend requests
- Rate limiting for friend requests

## Requirements

- Python 3.8
- Docker Desktop

## Installation

### Clone the Repository

```bash
git clone https://github.com/aindri3011/Networking.git
```

# Setup Environment Variables
- Create a .env file in the root of the project directory with the following content:

# MongoDB settings (.env file)
mongo_username = your_mongodb_username, 
password = your_mongodb_password, 
cluster = your_mongodb_cluster, 
key = your_database_key

# Django secret key
SECRET_KEY= your_django_secret_key

# Build and Run the Docker Containers
Ensure you have Docker Desktop installed. Then, run the following command:

docker-compose up --build

## If you prefer to run the project without Docker, follow these steps:

### Setup Environment Variables

- Create a `.env` file as mentioned above.
  
- Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```

- Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

- Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```
- Run the Django development server:

    ```bash
    python manage.py runserver
    ```
## Access the Application
Once the containers are up and running, you can access the Django application at:

http://localhost:8000


Configuration
# MongoDB Configuration
The project uses MongoDB as the database. Ensure you have a MongoDB instance running and configure the .env file with your MongoDB credentials (Recommended) OR configure MongoDB file without env with credentials.

# Usage
# API Endpoints
Sign Up: POST api/create-user/

{
    "name": "username",
    "email_id": "user@example.com",
    "password": "userpassword"
}

Login User: GET api/login-user/?email_id=user@example.com&password=userpassword

Search Users: GET api/search/?keyword=search_value

Send Friend Request: POST /api/friend-request/

{
     "from_user": "user1@example.com",
     "to_user": "user2@example.com"
}

List Pending Friend Requests: GET /api/pending-requests/user@example.com/

List Friends: GET /api/friends/user@example.com

Accept Friend Request: PUT /api/friend-request/

{
    "from_user": "user1@example.com",
     "to_user": "user2@example.com",
     "action": "accept"
}
Reject Friend Request: PUT /api/friend-request/

{
    "from_user": "user1@example.com",
     "to_user": "user2@example.com",
     "action": "reject"
}

# Contributing
Contributions are welcome! Please fork the repository and submit a pull request.


### Additional Notes

1. **Replace Placeholders**: Ensure you replace placeholders like `yourusername`, `yourrepository`, `your_mongodb_username`, `your_mongodb_password`, `your_mongodb_cluster`, `your_database_name`, and `your_django_secret_key` with actual values.

2. **Running Without Docker**: If users prefer to run the project without Docker, follow instructions for setting up a virtual environment, installing dependencies, and running the Django development server.

- By following this `README.md`, users will have a clear and concise guide to setting up and running your Django Networking API project.
