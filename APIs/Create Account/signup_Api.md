## 1. User Signup (POST)
Creates a new account for a Recruiter.

*   **Endpoint:** `/auth/signup`
*   **Method:** `POST`
*   **Auth Required:** No

### Request Body
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `fullName` | String | Yes | The user's full name. |
| `email` | String | Yes | A unique email address. |
| `password` | String | Yes | Must be at least 8 characters. |

**Example Request:**
```json
{
  "fullName": "Jane Doe",
  "email": "jane.doe@example.com",
  "password": "SecurePassword123!",
}
```

### Response
*   **Success (201 Created):**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "userId": "usr_987654321",
    "fullName": "Jane Doe",
    "email": "jane.doe@example.com",
    "createdAt": "2023-10-27T10:00:00Z"
  }
}
```

*   **Error (409 Conflict):**
```json
{
  "status": "error",
  "message": "Email already exists"
}
```


---

## 2. Continue with Google (POST)
Authenticates a user using their Google account. If the user doesn't exist, a new account is automatically created.

*   **Endpoint:** `/auth/google`
*   **Method:** `POST`
*   **Auth Required:** No

### Request Body
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `idToken` | String | Yes | The token received from Google after client-side login. |

**Example Request:**
```json
{
  "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg3Y..."
}
```

### Response
*   **Success (200 OK / 201 Created):**
```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "userId": "usr_123456789",
    "fullName": "Jane Doe",
    "email": "jane.doe@gmail.com",
    "isNewUser": true,
    "token": "backend_generated_jwt_token"
  }
}
```
*   **Error (401 Conflict):**
```json
{
  "status": "error",
  "message": "Invalid or expired Google token"
}
```
---
