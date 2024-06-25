# Chat Messenger Project

This is a chat messenger project built with Django and Django Channels. It supports both private and group chats with real-time messaging.

## Features

- User registration and authentication
- Profile management
- Private and group chat functionality
- Real-time messaging using WebSockets

## Requirements

- Python
- Django
- Django Channels
- Redis (for channel layers)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Brigeman/messenger_project
   cd messenger_project
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run Redis server:**

   Make sure Redis server is running. You can start it using the following command:

   ```bash
   redis-server
   ```

7. **Run the Daphne server:**

   Daphne is an HTTP, HTTP2, and WebSocket protocol server for ASGI and ASGI-HTTP, which will handle the WebSocket connections.

   ```bash
   daphne -p 8000 messenger_project.asgi:application
   ```

8. **Access the application:**

   Open your web browser and go to `http://127.0.0.1:8000`.

## Usage

1. **Register and log in:**

   Create a new account or log in with the superuser account you created.

2. **Create and join chats:**

   - You can create new group chats and add members to them.
   - Start private chats with other users.

3. **Real-time messaging:**

   Send and receive messages in real-time.

## License

This project is licensed under the MIT License.
