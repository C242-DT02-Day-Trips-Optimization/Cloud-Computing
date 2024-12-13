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
```
**Response:**
```json
{
  "message": "User registered successfully",
  "uid": "RhMCtVYCHXRxy3sni9zX8WhGwmG3"
}
```
### 2. Login User
**Endpoint:** `POST /user/login`  
**Description:** Log in an existing user using their email/username and password. 
**Request Body:**
```json
{
  "identifier": "peach@gmail.com",
  "password": "peach123"
}
```
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
```
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
```
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
```
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
```
### 5. Delete User
**Endpoint:** `DELETE /user/delete_user/{user_id}`  
**Description:** Delete a specific user account by their user ID. 
**Response:**
```json
{
  "message": "User deleted successfully"
}
```

# clustering API

This project provides a clustering and recommendation functionality. It allows users to group data into clusters and generate personalized recommendations based on the clustered results.

Base URL:
https://clustering-api-996559796971.asia-southeast2.run.app

## API Endpoints

### 1. Recomendation 
**Endpoint:** `POST /recommend`  
**Description:** This endpoint generates recommendations based on the user's input. It uses clustering results to suggest location or place that are most relevant to the user's preferences.
**Request Body:**
```json
{
    "points": [
        {"name": "Surabaya Zoo", "coordinates": [-7.3024, 112.7367]},
        {"name": "House of Sampoerna", "coordinates": [-7.2482, 112.7356]},
        {"name": "Submarine Monument", "coordinates": [-7.2656, 112.7461]},
        {"name": "Tugu Pahlawan", "coordinates": [-7.2458, 112.7374]},
        {"name": "Ciputra Waterpark", "coordinates": [-7.3167, 112.6308]},
        {"name": "Kenjeran Beach", "coordinates": [-7.2488, 112.8058]},
        {"name": "Galaxy Mall Surabaya", "coordinates": [-7.2940, 112.7700]},
        {"name": "Suroboyo Bridge", "coordinates": [-7.2475, 112.7802]},
        {"name": "Suro and Boyo Statue", "coordinates": [-7.3053, 112.7385]},
        {"name": "Pakuwon Mall", "coordinates": [-7.2916, 112.6429]}
	],
    "num_clusters": 3,
    "province": "jawa timur",
    "daily_start_time": "08:00",
    "daily_end_time": "18:00"
}

```
**Response:**
```json
{
  "grouped_clusters": [
	{
      "cluster": 0,
      "schedule": [
    	{
          "name": "Ciputra Waterpark",
          "avg_duration": 292,
          "travel_time": null,
          "mode": null
    	},
    	{
          "name": "Pakuwon Mall",
          "avg_duration": 292,
          "travel_time": 15,
          "mode": "driving"
    	}
  	],
      "avg_duration": 292
	},
	{
      "cluster": 1,
      "schedule": [
    	{
          "name": "Surabaya Zoo",
          "avg_duration": 58,
          "travel_time": null,
          "mode": null
    	},
    	{
          "name": "Suro and Boyo Statue",
          "avg_duration": 58,
          "travel_time": 15,
          "mode": "walking"
    	},
    	{
          "name": "Galaxy Mall Surabaya",
          "avg_duration": 58,
          "travel_time": 16,
          "mode": "driving"
    	},
    	{
          "name": "Submarine Monument",
          "avg_duration": 58,
          "travel_time": 18,
          "mode": "driving"
    	},
    	{
          "name": "House of Sampoerna",
          "avg_duration": 58,
          "travel_time": 10,
          "mode": "driving"
    	},
    	{
          "name": "Tugu Pahlawan",
          "avg_duration": 58,
          "travel_time": 6,
          "mode": "walking"
    	},
    	{
          "name": "Suroboyo Bridge",
          "avg_duration": 58,
          "travel_time": 16,
          "mode": "driving"
    	},
    	{
          "name": "Kenjeran Beach",
          "avg_duration": 58,
          "travel_time": 9,
          "mode": "driving"
    	}
  	],
      "avg_duration": 58
	}
  ],
  "final_unvisitable": [],
  "recommended_days": 2
}
```

### 2. Clustering 
**Endpoint:** `POST /cluster/`  
**Description:** This endpoint designed to optimize location-based data by grouping points of interest into clusters like travel planning or location-based recommendations, where grouping nearby locations can significantly improve efficiency and user experience
**Request Body:**
```json
 {
    "points": [
        {"name": "Surabaya Zoo", "coordinates": [-7.3024, 112.7367]},
        {"name": "House of Sampoerna", "coordinates": [-7.2482, 112.7356]},
        {"name": "Submarine Monument", "coordinates": [-7.2656, 112.7461]},
        {"name": "Tugu Pahlawan", "coordinates": [-7.2458, 112.7374]},
        {"name": "Ciputra Waterpark", "coordinates": [-7.3167, 112.6308]},
        {"name": "Kenjeran Beach", "coordinates": [-7.2488, 112.8058]},
        {"name": "Galaxy Mall Surabaya", "coordinates": [-7.2940, 112.7700]},
        {"name": "Suroboyo Bridge", "coordinates": [-7.2475, 112.7802]},
        {"name": "Suro and Boyo Statue", "coordinates": [-7.3053, 112.7385]},
        {"name": "Pakuwon Mall", "coordinates": [-7.2916, 112.6429]}
	],
    "num_clusters": 3,
    "province": "jawa timur",
    "daily_start_time": "08:00",
    "daily_end_time": "18:00"
}

```
**Response:**
```json
{
  "grouped_clusters": [
	{
      "cluster": 0,
      "avg_duration": 109,
      "schedule": [
    	{
          "name": "House of Sampoerna",
          "avg_duration": 109,
          "travel_time": null,
          "mode": null
    	},
    	{
          "name": "Tugu Pahlawan",
          "avg_duration": 109,
          "travel_time": 6,
          "mode": "walking"
    	},
    	{
          "name": "Submarine Monument",
          "avg_duration": 109,
          "travel_time": 9,
          "mode": "driving"
    	},
    	{
          "name": "Suroboyo Bridge",
          "avg_duration": 109,
          "travel_time": 19,
          "mode": "driving"
    	},
    	{
          "name": "Kenjeran Beach",
          "avg_duration": 109,
          "travel_time": 9,
          "mode": "driving"
    	}
  	]
	},
	{
      "cluster": 1,
      "avg_duration": 189,
      "schedule": [
    	{
          "name": "Surabaya Zoo",
          "avg_duration": 189,
          "travel_time": null,
          "mode": null
    	},
    	{
          "name": "Suro and Boyo Statue",
          "avg_duration": 189,
          "travel_time": 15,
          "mode": "walking"
    	},
    	{
          "name": "Galaxy Mall Surabaya",
          "avg_duration": 189,
          "travel_time": 16,
          "mode": "driving"
    	}
  	]
	},
	{
      "cluster": 2,
      "avg_duration": 292,
      "schedule": [
    	{
          "name": "Ciputra Waterpark",
          "avg_duration": 292,
          "travel_time": null,
          "mode": null
    	},
    	{
          "name": "Pakuwon Mall",
          "avg_duration": 292,
          "travel_time": 15,
          "mode": "driving"
    	}
  	]
	}
  ],
  "final_unvisitable": []
}
```




