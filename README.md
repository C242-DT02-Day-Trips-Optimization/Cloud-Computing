## API
# CRUD User API

This project provides a simple CRUD (Create, Read, Update, Delete) API for user management. The API allows users to register, log in, update their profile, view user details, and delete accounts. It can be easily tested using Postman.

Base URL:
https://auth-api-996559796971.asia-southeast2.run.app

## API Endpoints

### 1. Register User
**Endpoint:** `POST /user/register`  
**Description:** Register a new user account.  
**Request Body:**
```json
{
  "email": "peach@gmail.com",
  "username": "peach",
  "password": "peach123",
  "confirm_password": "peach123"
}

**Response:**
```json
{
  "message": "User registered successfully",
  "uid": "RhMCtVYCHXRxy3sni9zX8WhGwmG3"
}

### 2. Login User
**Endpoint:** `POST /user/login`  
**Description:** Log in an existing user using their email/username and password. 
**Request Body:**
```json
{
  "identifier": "peach@gmail.com",
  "password": "peach123"
}

**Response:**
```json
{
  "email": "peach_updated@gmail.com",
  "expiresIn": "3600",
  "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6...",
  "message": "Login successful",
  "refreshToken": "AMf-vBz954Q-CnP-gX1MLGcP8w6faNHZzcKW8HgLRN...",
  "userId": "RhMCtVYCHXRxy3sni9zX8WhGwmG3",
  "username": "peach_updated"
}

### 3. Update User
**Endpoint:** `PUT /user/update_user/{user_id}`  
**Description:** Update an existing user's information (username, email, password). 
**Request Body:**
```json
{
  "username": "peach_updated",
  "email": "peach_updated@gmail.com",
  "password": "peach456"
}

**Response:**
```json
{
  "message": "User updated successfully",
  "user": {
    "created_at": "2024-12-11T11:27:40.355362",
    "email": "jambu@gmail.com",
    "password": "$2b$12$nDHKnr6OkkYGqLcdM0iVW.khsiSQj8s/zq56MMOB6NyfmmhMRrPca",
    "updated_at": "2024-12-11T11:29:22.153267",
    "username": "jambu"
  }
}

### 4. Get User Details
**Endpoint:** `GET /user/get_user/{user_id}`  
**Description:** Retrieve the details of a specific user by their user ID. 
**Response:**
```json
{
  "created_at": "2024-12-11T11:27:40.355362",
  "email": "jambu@gmail.com",
  "password": "$2b$12$nDHKnr6OkkYGqLcdM0iVW.khsiSQj8s/zq56MMOB6NyfmmhMRrPca",
  "updated_at": "2024-12-11T11:29:22.153267",
  "username": "jambu"
}

### 5. Delete User
**Endpoint:** `DELETE /user/delete_user/{user_id}`  
**Description:** Delete a specific user account by their user ID. 
**Response:**
```json
{
  "message": "User deleted successfully"
}






