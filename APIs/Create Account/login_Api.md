## 2. User Login (POST)
Authenticates a user and returns a Bearer Token for future requests.

*   **Endpoint:** `/auth/login`
*   **Method:** `POST`
*   **Auth Required:** No

### Request Body
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `email` | String | Yes | Registered email address. |
| `password` | String | Yes | User's password. |

**Example Request:**
```json
{
  "email": "jane.doe@example.com",
  "password": "SecurePassword123!"
}
```

### Response
*   **Success (200 OK):**
```json
{
  "status": "success",
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "userId": "usr_987654321",
    "fullName": "Jane Doe",
  }
}
```

*   **Error (401 Unauthorized):**
```json
{
  "status": "error",
  "message": "Invalid email or password"
}
```

---
