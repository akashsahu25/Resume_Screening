## 3. Forgot Password (POST)
Initiates a password reset process by sending a reset link or verification code to the user's registered email address.

**Endpoint:** `/auth/forgot-password`  
**Method:** `POST`  
**Auth Required:** No  

#### Request Body
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| email | String | Yes | The email address associated with the account. |

**Example Request:**
```json
{
  "email": "jane.doe@example.com"
}
```

#### Response
**Success (200 OK):**
```json
{
  "status": "success",
  "message": "Password reset instructions have been sent to your email."
}
```

**Error (404 Not Found):**
```json
{
  "status": "error",
  "message": "User with this email does not exist"
}
```