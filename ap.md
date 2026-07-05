# ResumeScan API Documentation
**Base URL:** `https://api.resumescan.com`  
**Content-Type:** `application/json`

---
 
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
### 3. Forgot Password (POST)
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

---

### 4. Continue with Google (POST)
Authenticates or registers a user using a Google OAuth ID Token. If the user does not exist, a new account is created automatically.

**Endpoint:** `/auth/google`  
**Method:** `POST`  
**Auth Required:** No  

#### Request Body
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| idToken | String | Yes | The OAuth2 ID token received from Google’s authentication service. |

**Example Request:**
```json
{
  "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImY0Z..."
}
```

#### Response
**Success (200 OK):**
```json
{
  "status": "success",
  "message": "Authentication successful",
  "token": "eyJhbGciOiJSZ056IsInR5cCI6IkpXVCJ9...",
  "user": {
    "userId": "usr_google_123456",
    "fullName": "Jane Doe",
    "email": "jane.doe@gmail.com",
    "isNewUser": false
  }
}
```

**Error (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Invalid Google token"
}
```
---
### 1. Fetch Jobs (GET)
Retrieves a list of available jobs. 

*   **Endpoint:** `/jobs`
*   **Method:** `GET`
*   **Auth Required:** Yes (JWT)

#### Request Headers
| Field | Value | Description |
| :--- | :--- | :--- |
| **Authorization** | `JWT` | The token received from the Login API. |
| **Content-Type** | `application/json` | Standard JSON header. |


#### Response
**Success (200 OK):**
```json
{
  "status": "success",
  "message": "Jobs retrieved successfully",
  "data": [
    {
      "jobId": "job_001",
      "title": "Software Engineer",
      "applicants": "214",
      "shortlisted": "24",
      "postedDate": "2023-10-25"
    },
    {
      "jobId": "job_002",
      "title": "Product Designer",
     "applicants": "214",
      "shortlisted": "24",
      "postedDate": "2023-10-24"
    }
    .
    .
    .
    .
    .
    .
    .
    .
    .
    .
  ]
}
```

**Error (401 Unauthorized):**
*Occurs if the token is missing, expired, or invalid.*
```json
{
  "status": "error",
  "message": "Unauthorized access. Please login again."
}
```
---
### **1. Fetch Jobs with Filter (GET)**

Retrieves a list of available jobs. When a user selects a department from the dropdown menu, the selected value is passed as a query parameter in the URL to filter the results.

*   **Endpoint:** `/jobs`
*   **Method:** `GET`
*   **Auth Required:** Yes (JWT)

#### **Query Parameters**
| Field | Type | Description |
| :--- | :--- | :--- |
| `department` | `string` | **(Optional)** When a user selects a department from the dropdown, it is passed as a parameter (e.g., Engineering, Design, HR). If no department is selected, all jobs are returned. |

#### **Request Headers**
| Field | Value | Description |
| :--- | :--- | :--- |
| `Authorization` | `Bearer <JWT_TOKEN>` | The token received from the Login API. |
| `Content-Type` | `application/json` | Standard JSON header. |

#### **Example Request URL**
`GET /jobs?department=Engineering`

---

#### **Response**

**Success (200 OK):**
```json
{
  "status": "success",
  "message": "Jobs retrieved successfully",
  "departmentSelected": "Engineering",
  "data": [
    {
      "jobId": "job_001",
      "title": "Backend Developer",
      "department": "Engineering",
      "applicants": "150",
      "shortlisted": "15",
      "postedDate": "2023-11-01"
    },
    {
      "jobId": "job_005",
      "title": "Frontend Engineer",
      "department": "Engineering",
      "applicants": "98",
      "shortlisted": "10",
      "postedDate": "2023-11-05"
    }
  ]
}
```

**Error (401 Unauthorized):**
Occurs if the token is missing, expired, or invalid.
```json
{
  "status": "error",
  "message": "Unauthorized access. Please login again."
}
```

**Error (404 Not Found):**
Occurs if no jobs exist for the selected department.
```json
{
  "status": "error",
  "message": "No jobs found for the selected department."
}
```
---


## 1. Create Job Requirement (POST)
Saves the specific job requirements provided by HR to be used for AI matching.

*   **Endpoint:** `/job-requirements`
*   **Method:** `POST`
*   **Auth Required:** Yes (JWT)

### Request Body
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `jobTitle` | String | Yes | e.g., "Senior Software Developer" |
| `department` | Enum | Yes | e.g., "IT Department", "Sales", "HR" |
| `industryFocus` | String | Yes | e.g., "Health, Fitness", "Fintech" |
| `responsibilities` | Array[String]| Yes | List of job responsibilities. |
| `jobDescription` | String | Yes | Detailed description of the job. |
| `educationLevel` | Enum | Yes | e.g., "Bachelors", "Masters", "PhD" |
| `experienceRequired`| Integer | Yes | Required years of experience. |
| `mustHaveSkills` | Array[String]| Yes | Mandatory technical skills. |
| `goodToHaveSkills` | Array[String]| No | Preferred skills. |
| `softSkill` | Array[String]| No | e.g., "Leadership", "Communication" |
| `total applicant` | Integer | Yes | The number of shortlisted candidates. This is auto-fetched from the database and does not need to be provided in the request. |
| `Shortlisted` | Integer | Yes | The number of shortlisted candidates. This is auto-fetched from the database and does not need to be provided in the request.   |
| `optionalSkills` | JSONB | No | Key-value pairs of optional skills. |
| `jobPostDate` | date | No | auto fill |

**Example Request:**
```json
{
  "jobTitle": "Senior Software Developer",
  "department": "IT Department",
  "industryFocus": "Health, Fitness",
  "responsibilities": ["Develop APIs", "Cloud Management"],
  "jobDescription": "We need a developer for backend scaling.",
  "educationLevel": "Bachelors",
  "experienceRequired": 5,
  "mustHaveSkills": ["Node.js", "PostgreSQL"],
  "goodToHaveSkills": ["AWS", "Docker"],
  "softSkill": ["Communication"],
  "optionalSkills": {"languages": ["English", "Hindi"]}
}
```

### Response
*   **Success (201 Created):**
```json
{
  "status": "success",
  "message": "Job requirement created successfully",
  "jobId": "job_123456"
}
```
*   **Error (400 Bad Request):**
```json
{ "status": "error", "message": "Missing required fields" }
```
*   **Error (401 Unauthorized):**
```json
{ "status": "error", "message": "Invalid or expired JWT token" }
```

---

## 2. Bulk Resume Upload (POST)
Uploads multiple resumes to AWS S3 for the specific job.

*   **Endpoint:** `/job-requirements/{jobId}/resumes`
*   **Method:** `POST`
*   **Auth Required:** Yes (JWT)
*   **Content-Type:** `multipart/form-data`

### Request Body
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `files` | Files[] | Yes | Multiple PDF or Docx resume files. |

**Example Request:** 
`Form-Data: files=@resume1.pdf, files=@resume2.docx`

### Response
*   **Success (202 Accepted):**
```json
{
  "status": "success",
  "message": "Resumes uploaded to S3 successfully",
  "jobId": "job_123456"
  "numberOfApplicants": "950"
}
```

---

## 3. Start AI Extraction & Scoring (POST)
Triggers the background process where AI extracts data from resumes and compares them with the job requirement, nd saves the results to the `resume_extract_data_table`.

*   **Endpoint:** `/job-requirements/{jobId}/process`
*   **Method:** `POST`
*   **Auth Required:** Yes (JWT)

### AI Extraction Schema (Data points to be extracted from resumes):

| Field | Type | Description |
| :--- | :--- | :--- |
| `name` | String | Candidate's full name. |
| `candidate_id` | UUID / String | Unique identifier for the candidate.|
| `email` | String | Candidate's email address (Unique). |
| `phone number` | String | Candidate's contact/mobile number. |
| `college name` | String | Most recent educational institution. |
| `links` | JSON | Key-value pairs of social/portfolio links (e.g., GitHub, LinkedIn). |
| `company name` | String | Name of the most recent employer. |
| `year of experience`| Integer | Total years of professional experience calculated by AI. |
| `current role` | String | Candidate's latest job title. |
| `responsibilities` | String Array | List of key job responsibilities from previous roles. |
| `skills` | Array | Extracted technical and hard skills. |
| `soft skill` | Array | Extracted interpersonal/soft skills. |
| `key achievements` | Array | List of notable professional highlights or awards. |
| `work history` | String | Calculated details regarding the candidate's career progression. |
| `education` | Array | List of extracted degrees and certifications. |
| `projects` | Array | List of professional or personal projects mentioned. |
| `ctc` | Integer | Allows HR to manually add. |
| `notes` | String | Allows HR to manually add. |
| `resume_url` | String | S3 bucket path or public link of the uploaded resume. |
| `AI summary` | String | A brief candidate profile summary generated by the LLM. |
| `` | Integer | **(0-100)** Match score calculated based on the Job Requirements. |
| `AI score` | Integer | **(0-100)** Match score calculated based on the Job Requirements. |

### Response
*   **Success (202 Accepted):**
```json
{
  "status": "success",
  "message": "AI extraction and scoring has started in the background.",
  "jobId": "job_123456"
}
```
### Error Responses
*   **401 Unauthorized:**
```json
{
  "status": "error",
  "message": "Invalid or expired JWT token. Please login again."
}
```
*   **404 Not Found:**
```json
{
  "status": "error",
  "message": "Job ID not found. Ensure the job requirement is created before processing."
}
```

---

## 4. Get Processing Progress (GET)
Polling endpoint used by the "Processing Page" to show real-time progress.

*   **Endpoint:** `/job-requirements/{jobId}/progress`
*   **Method:** `GET`
*   **Auth Required:** Yes (JWT)

### Response
*   **Success (200 OK):**
```json
{
  "status": "success",
  "data": {
    "totalResumes": 50,
    "processedCount": 15,
    "percentage": 30,
    "isCompleted": false,
    "estimatedMinutesRemaining": 2
  }
}
```

---

## 5. Get Candidates Dashboard Summary (GET)
Retrieves a simplified list of candidates for the main dashboard view after processing is 100% complete.

*   **Endpoint:** `/{jobId}/candidates-summary`
*   **Method:** `GET`
*   **Auth Required:** Yes (JWT)

### Query Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `page` | Integer | No | 1 | The page number to retrieve (e.g., 1 for the first 10, 2 for the next 10). |
| `limit` | Integer | No | 10 | Number of candidates per page. |

### Response
*   **Success (200 OK):**
```json
{
  "status": "success",
  "metadata": {
    "totalCandidates": 45,
    "currentPage": 1,
    "totalPages": 5,
    "pageSize": 10,
    "hasNextPage": true,
    "hasPreviousPage": false
  },
  "data": [
    {
      "candidateId": "cand_001",
      "name": "John Smith",
      "currentRole": "Backend Developer",
      "companyName": "DevCorp",
      "yearOfExperience": 6,
      "aiScore": 95,
      "ctc": null
    },
    {
      "candidateId": "cand_002",
      "name": "Alice Wang",
      "currentRole": "Fullstack Engineer",
      "companyName": "TechSolutions",
      "yearOfExperience": 4,
      "aiScore": 92,
      "ctc": "null"
    },
    "... (8 more candidates)"
  ]
}
```

---

## 6. Update Candidate CTC (PATCH)
Allows HR to manually add, edit, or remove the CTC for a specific candidate.

*   **Endpoint:** `/candidates/{candidateId}/ctc`
*   **Method:** `PATCH`
*   **Auth Required:** Yes (JWT)

### Request Body
```json
{
  "ctc": "15 LPA" 
}
```
*(To remove CTC, send `{"ctc": null}`)*

### Response
*   **Success (200 OK):**
```json
{ "status": "success", "message": "CTC updated successfully" }
```

---

## 7. Get Full Candidate Details (GET)
Retrieves all 18+ extracted fields for a candidate when their profile is clicked.

*   **Endpoint:** `/candidates/{candidateId}/full-details`
*   **Method:** `GET`
*   **Auth Required:** Yes (JWT)

### Response Example
```json
{
  "status": "success",
  "data": {
    "name": "John Smith",
    "email": "john.smith@example.com",
    "phoneNumber": "+123456789",
    "collegeName": "University of Tech",
    "links": {"GitHub": "...", "LinkedIn": "..."},
    "companyName": "DevCorp",
    "yearOfExperience": 6,
    "currentRole": "Backend Developer",
    "responsibilities": ["API Dev", "Unit Testing"],
    "skills": ["Node.js", "PostgreSQL"],
    "softSkill": ["Leadership"],
    "keyAchievements": ["Top Performer 2022"],
    "workHistory": 2,
    "education": ["B.Tech CS"],
    "projects": ["E-commerce App"],
    "aiSummary": "Highly skilled backend developer...",
    "aiScore": 85
  }
}
```

---

## 8. Update Candidate Note (PATCH)
Allows HR to manually add, edit, or remove a note for a specific candidate.

**Endpoint:** `/candidates/{candidateId}/note`  
**Method:** `PATCH`  
**Auth Required:** `Yes (JWT)`

**Request Body**
```json
{
  "note": "Candidate has strong communication skills and relevant experience." 
}
```
*(To remove the note, send `{"note": null}`)*

**Response**

**Success (200 OK):**
```json
{ 
  "status": "success", 
  "message": "Note updated successfully" 
}
```

**Error (404 Not Found - If candidate doesn't exist):**
```json
{ 
  "status": "error", 
  "message": "Candidate not found" 
}
```

**Error (401 Unauthorized - If token is missing or invalid):**
```json
{ 
  "status": "error", 
  "message": "Unauthorized access" 
}
```

---

### 8. Get Candidate Resume (GET)
Retrieves a secure, temporary viewing link for a specific candidate's resume stored in AWS S3.

**Endpoint:** `/candidates/{candidateId}/resume`  
**Method:** `GET`  
**Auth Required:** `Yes (JWT)`

**Logic:**  
The backend retrieves the stored resume file path from the database and generates an **AWS S3 Pre-signed URL**. This URL provides time-limited access (e.g., valid for 5-10 minutes) to the file, ensuring that the resumes remain private and secure.

**Response**

**Success (200 OK):**
```json
{
  "status": "success",
  "resumeViewUrl": "https://s3.amazonaws.com/my-bucket/resumes/candidate_123.pdf?AWSAccessKeyId=AKIA...&Expires=1672531200&Signature=..."
}
```

**Error (404 Not Found):**
```json
{ 
  "status": "error", 
  "message": "Resume not found for this candidate" 
}
```

**Error (401 Unauthorized):**
```json
{ 
  "status": "error", 
  "message": "Invalid or expired JWT token" 
}
```



---


### 9. Get Candidate GitHub Profile (GET)
Retrieves the GitHub profile URL for a specific candidate from the database.

**Endpoint:** `/candidates/{candidateId}/github`  
**Method:** GET  
**Auth Required:** Yes (JWT)

**Response**

**Success (200 OK):**
```json
{
  "status": "success",
  "githubUrl": "https://github.com/candidate-username"
}
```

**Error (404 Not Found):**
```json
{ 
  "status": "error", 
  "message": "GitHub profile not found for this candidate" 
}
```

**Error (401 Unauthorized):**
```json
{ 
  "status": "error", 
  "message": "Invalid or expired JWT token" 
}
```

---


### 10. Get Candidate LinkedIn Profile (GET)
Retrieves the stored LinkedIn profile URL for a specific candidate.

**Endpoint:** `/candidates/{candidateId}/linkedin`  
**Method:** GET  
**Auth Required:** Yes (JWT)


**Response**

**Success (200 OK):**
```json
{
  "status": "success",
  "linkedinUrl": "https://www.linkedin.com/in/candidate-username"
}
```

**Error (404 Not Found):**
```json
{ 
  "status": "error", 
  "message": "LinkedIn profile not found for this candidate" 
}
```

**Error (401 Unauthorized):**
```json
{ 
  "status": "error", 
  "message": "Invalid or expired JWT token" 
}
```

---