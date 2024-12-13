## API
# CRUD User API

This project provides a simple CRUD (Create, Read, Update, Delete) API for user management. The API allows users to register, log in, update their profile, view user details, and delete accounts. It can be easily tested using Postman.

Base URL:
https://auth-api-996559796971.asia-southeast2.run.app

## API Endpoints

### 1. Register User
**Endpoint:** `POST /auth/register`  
**Description:** Register a new user account.  
**Request Body:**
```json
{
  "email": "peach@gmail.com",
  "username": "peach",
  "password": "peach123",
  "confirm_password": "peach123"
}

