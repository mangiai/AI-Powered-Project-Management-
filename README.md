
# AI Poweered Project Management

This project is a FastAPI application that integrates various AI models and a database to handle user authentication and serve responses for cost, project, and risk management queries. It also supports chat functionality, allowing the creation and retrieval of chat messages and conversations.

## Key Features

- **User Authentication**: OAuth2 password-based authentication with token generation.
- **Cost, Project, and Risk Bots**: AI-powered responses for cost, project, and risk-related queries using a FewShotPromptTemplate and LLMs.
- **Database Integration**: Uses SQLAlchemy ORM with PostgreSQL (or other databases) for handling users, chats, and messages.
- **VectorStore Integration**: Enables query-based responses through vector embeddings.
- **Modular Code**: All APIs and functions are built in a reusable and modular way.

## Project Structure

```bash
.
├── app/
│   ├── main.py               # FastAPI entry point
│   ├── database.py           # SQLAlchemy database configuration
│   ├── models.py             # Database models for users, chats, and messages
│   ├── schemas.py            # Pydantic schemas for request and response validation
│   ├── auth.py               # User authentication and token handling
│   ├── cost_agent.py         # Logic for cost bot response
│   ├── project_agent.py      # Logic for project bot response
│   ├── risk_agent.py         # Logic for risk bot response
│   ├── chat.py               # Chat bot utilities and tools
└── README.md                 # This file
```

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/ai-powered-proj-management.git
   cd AI-POWERED-PROJ-MANAGEMENT
   ```

2. **Set up a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:

   Create a `.env` file in the project root and add the necessary database and security credentials:

   ```bash
   DATABASE_URL=your_database_url
   SECRET_KEY=your_secret_key
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run database migrations**:

   ```bash
   alembic upgrade head
   ```

## Running the Application

Start the FastAPI application using `uvicorn`:

```bash
uvicorn main:app --reload
```

This will start the server on `http://127.0.0.1:8000`.

## API Endpoints

### Authentication

- **POST** `/token`: Get an access token by providing username and password.

### User Management

- **POST** `/users/`: Create a new user.
- **GET** `/users/me/`: Get details of the current authenticated user.

### Bots

- **POST** `/cost-bot`: Get a response from the cost bot.
- **POST** `/project-bot`: Get a response from the project bot.
- **POST** `/risk-bot`: Get a response from the risk bot.

### Chats

- **POST** `/chats/`: Create a new chat.
- **GET** `/chats/{chat_id}`: Retrieve a chat by ID.

### Messages

- **POST** `/msgs/`: Create a new message.
- **GET** `/msgs/{msg_id}`: Retrieve a message by ID.

## Dependencies

- **FastAPI**: Web framework.
- **SQLAlchemy**: ORM for database interaction.
- **Pydantic**: Data validation.
- **OAuth2**: Authentication and token handling.
- **LLMs and VectorStore**: For AI-driven query responses.

## Testing

To run tests, you can use:

```bash
pytest
```

## Future Improvements

- Add more detailed logging.
- Expand bot functionality with additional AI models.
- Improve error handling.

