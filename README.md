#  User Authentication Service

A simple user management service built with FastAPI that provides user registration, login, and deletion functionality.

## Installation

1. To isolate the dependencies for this service, create and activate a new virtual environment. In this example, the virtual environment will be named `.venv`:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Update PIP and install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Run the service:
```bash
make start
```

The service will start on `http://localhost:8000`

## API Documentation

Once the service is running, you can access:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`

## API Endpoints

### 1. Register a New User

**Endpoint:** `POST /registration`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response (201 Created):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/registration/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

### 2. Login as a User

**Endpoint:** `POST /login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "user_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

### 3. Delete a User

**Endpoint:** `DELETE /users/{user_id}`

**Response (200 OK):**
```json
{
  "message": "User deleted successfully"
}
```

**cURL Example:**
```bash
curl -X DELETE "http://localhost:8000/users/123e4567-e89b-12d3-a456-426614174000"
```

## Error Responses

### 409 Conflict - Email Already Registered
```json
{
  "detail": "Email already registered"
}
```

### 401 Unauthorized - Invalid Login
```json
{
  "detail": "Invalid email or password"
}
```

### 404 Not Found - User Not Found
```json
{
  "detail": "User not found"
}
```

### 422 Unprocessable Entity - Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Testing with Postman

### Collection Setup

1. Create a new Postman collection called "User Auth API"
2. Set the base URL as a collection variable: `{{baseUrl}}` = `http://localhost:8000`

### Test Requests

#### 1. Register User
- **Method:** POST
- **URL:** `{{baseUrl}}/registration`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "email": "test@example.com",
  "password": "testpassword123"
}
```

#### 2. Login User
- **Method:** POST
- **URL:** `{{baseUrl}}/login`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "email": "test@example.com",
  "password": "testpassword123"
}
```

#### 3. Delete User
- **Method:** DELETE
- **URL:** `{{baseUrl}}/users/{{userId}}`
- **Note:** Replace `{{userId}}` with the actual user ID from registration response

## Running Tests

Run the unit tests using the `make` target:

```bash
# Run all tests
make unit-test
```

## Test Coverage

The test suite covers:

- **User Registration Tests:**
  - Successful registration
  - Duplicate email handling
  - Invalid email format
  - Missing required fields

- **User Login Tests:**
  - Successful login
  - Invalid email
  - Invalid password
  - Missing fields

- **User Deletion Tests:**
  - Successful deletion
  - Non-existent user
  - Invalid UUID format

- **Security Tests:**
  - Password hashing verification

## Data Storage

The service uses in-memory storage with two main data structures:

1. **`user_store`:** Dictionary with UUID keys storing complete user records
2. **`email_to_user_id`:** Dictionary mapping emails to user IDs for quick lookups

**Example data structure:**
```python
users_db = {
  "123e4567-e89b-12d3-a456-426614174000": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "password_hash": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
  }
}

email_to_user_id = {
  "user@example.com": "123e4567-e89b-12d3-a456-426614174000"
}
```

## Potential Next Steps
1. Add unit test coverage for user CRUD utilities
2. Add logging
3. Containerize the service


