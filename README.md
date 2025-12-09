## ChatBot — LLM-Powered Chatbot with FastAPI, PostgreSQL, and Docker

This project is a production-ready, microservices-based backend system for an LLM-powered chatbot built using FastAPI, PostgreSQL, and a Groq-hosted Large Language Model (LLM) such as Llama 3.1 or Mistral-7B.

The system accepts natural language queries, converts them into safe SQL queries using an LLM, executes them on a PostgreSQL database, and returns structured results via secure APIs. The entire platform is fully containerized with Docker and is deployable via Docker Hub.

# System Architecture
The application follows a microservices architecture consisting of the following components:

# Auth Service: Handles user registration, login, and JWT token generation
- Chatbot Service: Converts natural language queries into SQL using an LLM and executes them
- PostgreSQL (Auth Database): Stores user authentication data
- PostgreSQL (Chatbot Database): Stores customer-related data
- Each service runs in an isolated Docker container and communicates over an internal Docker network.

# Key Features
- Natural Language to SQL conversion using a Groq-hosted LLM
- Secure FastAPI-based backend
- PostgreSQL database integration using SQLAlchemy ORM
- JWT-based authentication and authorization
- Safe execution of read-only (SELECT) queries
-Structured logging of:
    - User queries
    - Generated SQL statements
    - Execution errors
- Comprehensive error handling for:
    - Invalid queries
    - SQL execution failures
    - Unauthorized access
    - Token expiration
- Fully Dockerized services
- Docker Hub-based image distribution
- Postman-ready API testing

# Technology Stack
- Component	-> Technology
1.Backend Framework ->	FastAPI (Python)
2.Database ->	PostgreSQL
3.ORM ->	SQLAlchemy
4.LLM Provider ->	Groq (Llama 3.1 / Mistral-7B)
5.Authentication ->	JWT
6.Containerization ->	Docker, Docker Compose
7.API Testing ->	Postman
8.Database Schema :
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT NOT NULL,
    location TEXT NOT NULL
);

## Running the Application Using Docker (Recommended)
This is the recommended production and client deployment method.

# Step 1: Install Docker Desktop
- Download and install Docker Desktop from:
- https://www.docker.com/products/docker-desktop/
- Ensure the Docker Engine is running after installation.

# Step 2: Create Project Directory
- mkdir chatbot-project
- cd chatbot-project

# Step 3: Create Environment File
- Create a file named .env in the project directory with the following content:

# Groq API Key
- GROQ_API_KEY=PASTE_YOUR_GROQ_KEY_HERE

# JWT Configuration
- JWT_SECRET_KEY=PASTE_YOUR_SECRET_KEY_HERE
- JWT_ALGORITHM=HS256
- ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database URLs (Docker Internal)
- AUTH_DATABASE_URL=postgresql://postgres:postgres@auth_db:5432/Chatbot_Auth
- CHATBOT_DATABASE_URL=postgresql://postgres:postgres@chat_db:5432/Chatbot_Chat

# Step 4: Create Docker Compose Configuration

- Create a file named docker-compose.yml with the following content:

services:
  auth_db:
    image: postgres:15
    container_name: auth_db
    restart: always
    environment:
      POSTGRES_DB: Chatbot_Auth
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - auth_db_data:/var/lib/postgresql/data

  chat_db:
    image: postgres:15
    container_name: chat_db
    restart: always
    environment:
      POSTGRES_DB: Chatbot_Chat
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5433:5432"
    volumes:
      - chat_db_data:/var/lib/postgresql/data

  auth_service:
    image: your_dockerhub_username/auth_service:latest
    container_name: auth_service
    env_file:
      - .env
    depends_on:
      - auth_db
    ports:
      - "8001:8001"

  chatbot_service:
    image: your_dockerhub_username/chatbot_service:latest
    container_name: chatbot_service
    env_file:
      - .env
    depends_on:
      - chat_db
      - auth_service
    ports:
      - "8002:8002"

volumes:
  auth_db_data:
  chat_db_data:


- Replace your_dockerhub_username with your actual Docker Hub username.

# Step 5: Start the System
- docker compose up
- Docker will automatically pull the required images and start all services.

## API Access Points
- Service	URL
  - Auth Service	http://localhost:8001/docs
  - Chatbot Service	http://localhost:8002/docs

## API Testing Using Postman
- Register User
POST
http://localhost:8001/register

Request Body
{
  "username": "ankit",
  "password": "123456"
}

- Login User
POST
http://localhost:8001/login

Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
  "token_type": "bearer"
}
Use the returned token for authenticated requests.

- Query the Chatbot
POST
http://localhost:8002/chat/query

Headers
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

Request Body
{
  "query": "Show me all female customers from Mumbai"
}

Sample Response
{
  "sql": "SELECT customer_id, name, gender, location FROM customers WHERE gender = 'female' AND location = 'Mumbai';",
  "rows": [
    {
      "customer_id": 1,
      "name": "Aisha Khan",
      "gender": "female",
      "location": "Mumbai"
    },
    {
      "customer_id": 3,
      "name": "Neha Patel",
      "gender": "female",
      "location": "Mumbai"
    }
  ]
}

# Sample Queries
- Show all customers from Delhi
- List all female customers
- Show male customers from Bangalore
- Show all customers
- Logging

# The system logs the following:
- User queries
- Generated SQL statements
- SQL execution errors
- Authentication and authorization failures

# Error Handling
- The application handles the following error conditions:
- Invalid SQL generated by the LLM
- Database connection failures
- Unauthorized access attempts
- Token expiration
- Empty result sets

# Notes
- Backend-focused system with no frontend UI
- Postman is used as the client interface
- LLM access is restricted to safe SELECT-only queries
- Fully containerized deployment
- Suitable for cloud deployment using Docker

# Author: 
- Ankit Raj
- Backend Developer
- GitHub: https://github.com/ankitraj20616

Ankit Raj
Backend Developer
GitHub: https://github.com/ankitraj20616
