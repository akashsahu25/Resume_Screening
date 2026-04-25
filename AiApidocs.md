
---

# 📘 ResumeScan API Documentation

**Base URL:** `https://api.resumescan.com`
**Content-Type:** `application/json`
**Authentication:** Bearer Token (JWT)

---

# 🔐 Authentication APIs

## 1. Sign Up

Create a new recruiter account.

**Endpoint:** `POST /auth/signup`
**Auth Required:** ❌ No

### Request Body

```json
{
  "fullName": "Jane Doe",
  "email": "jane.doe@example.com",
  "password": "SecurePassword123!"
}
```

### Response

**201 Created**

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

**409 Conflict**

```json
{
  "status": "error",
  "message": "Email already exists"
}
```

---

## 2. Login

Authenticate user and receive JWT token.

**Endpoint:** `POST /auth/login`
**Auth Required:** ❌ No

### Request

```json
{
  "email": "jane.doe@example.com",
  "password": "SecurePassword123!"
}
```

### Response

**200 OK**

```json
{
  "status": "success",
  "message": "Login successful",
  "token": "JWT_TOKEN",
  "user": {
    "userId": "usr_987654321",
    "fullName": "Jane Doe"
  }
}
```

---

## 3. Forgot Password

Send reset instructions to email.

**Endpoint:** `POST /auth/forgot-password`

### Request

```json
{
  "email": "jane.doe@example.com"
}
```

### Response

```json
{
  "status": "success",
  "message": "Password reset instructions sent"
}
```

---

## 4. Google Authentication

Login/signup using Google OAuth.

**Endpoint:** `POST /auth/google`

### Request

```json
{
  "idToken": "GOOGLE_ID_TOKEN"
}
```

### Response

```json
{
  "status": "success",
  "token": "JWT_TOKEN",
  "user": {
    "userId": "usr_google_123",
    "fullName": "Jane Doe",
    "email": "jane.doe@gmail.com",
    "isNewUser": false
  }
}
```

---

# 📂 Job Management APIs

## 5. Get Jobs

Retrieve all jobs.

**Endpoint:** `GET /jobs`
**Auth Required:** ✅ Yes

### Headers

```
Authorization: Bearer <JWT_TOKEN>
```

### Response

```json
{
  "status": "success",
  "data": [
    {
      "jobId": "job_001",
      "title": "Software Engineer",
      "applicants": 214,
      "shortlisted": 24,
      "postedDate": "2023-10-25"
    }
  ]
}
```

---

## 6. Get Jobs with Filter

Filter jobs by department.

**Endpoint:** `GET /jobs?department=Engineering`

### Query Params

| Param      | Type   | Description                |
| ---------- | ------ | -------------------------- |
| department | string | Optional department filter |

---

## 7. Create Job Requirement

Create job configuration for AI screening.

**Endpoint:** `POST /job-requirements`

### Request

```json
{
  "jobTitle": "Senior Software Developer",
  "department": "IT",
  "industryFocus": "Fintech",
  "responsibilities": ["Develop APIs"],
  "jobDescription": "Backend scaling role",
  "educationLevel": "Bachelors",
  "experienceRequired": 5,
  "mustHaveSkills": ["Node.js"],
  "goodToHaveSkills": ["AWS"],
  "softSkills": ["Communication"],
  "optionalSkills": {
    "languages": ["English"]
  }
}
```

### Fixes Applied

* ❌ Removed invalid fields: `total applicant`, `Shortlisted`
* ✔ Renamed `softSkill` → `softSkills`
* ✔ Standardized naming conventions

---

# 📄 Resume Processing APIs

## 8. Upload Resumes

Upload multiple resumes.

**Endpoint:**
`POST /job-requirements/{jobId}/resumes`

**Content-Type:** `multipart/form-data`

### Response

```json
{
  "status": "success",
  "message": "Upload successful",
  "jobId": "job_123456",
  "numberOfApplicants": 950
}
```

---

## 9. Start AI Processing

Trigger resume parsing and scoring.

**Endpoint:**
`POST /job-requirements/{jobId}/process`

### Response

```json
{
  "status": "success",
  "message": "Processing started"
}
```

---

## 10. Get Processing Progress

Track real-time progress.

**Endpoint:**
`GET /job-requirements/{jobId}/progress`

### Response

```json
{
  "status": "success",
  "data": {
    "totalResumes": 50,
    "processedCount": 15,
    "percentage": 30,
    "isCompleted": false
  }
}
```

---

# 👥 Candidate APIs

## 11. Get Candidates Summary

Paginated dashboard data.

**Endpoint:**
`GET /job-requirements/{jobId}/candidates-summary`

### Fix Applied

* ❌ Incorrect endpoint `/{jobId}/...` → ✔ corrected

---

## 12. Get Candidate Details

Full profile data.

**Endpoint:**
`GET /candidates/{candidateId}`

---

## 13. Update Candidate CTC

**Endpoint:**
`PATCH /candidates/{candidateId}/ctc`

```json
{
  "ctc": "15 LPA"
}
```

---

## 14. Update Candidate Note

**Endpoint:**
`PATCH /candidates/{candidateId}/note`

---

## 15. Get Candidate Resume

Returns secure S3 pre-signed URL.

**Endpoint:**
`GET /candidates/{candidateId}/resume`

---

## 16. Get Candidate External Profiles

### GitHub

`GET /candidates/{candidateId}/github`

### LinkedIn

`GET /candidates/{candidateId}/linkedin`

---

# ⚠️ Standard Error Format

```json
{
  "status": "error",
  "message": "Error description"
}
```

---

# ✅ Key Improvements Made

### 🔧 Structural Fixes

* Grouped APIs into logical sections (Auth, Jobs, Processing, Candidates)
* Fixed duplicate numbering
* Standardized endpoint naming

### 🧹 Data Consistency

* Converted numeric strings → integers (`"214"` → `214`)
* Unified naming (`aiScore`, `softSkills`, `candidateId`)
* Removed invalid/auto-generated request fields

### 🧠 Clarity Improvements

* Simplified descriptions
* Removed redundancy
* Standardized response formats

### ⚠️ Errors Fixed

* Trailing commas in JSON
* Duplicate endpoints
* Missing commas in responses
* Incorrect endpoint paths
* Inconsistent headers (JWT vs Bearer)

---

# 🚀 Suggestions for Next Iteration

To make this fully production-ready, you should add:

* 🔐 Rate limiting & API quotas
* 📦 Versioning (`/v1/...`)
* 📄 OpenAPI / Swagger spec
* 🧪 Error codes catalog
* 🔄 Webhooks (for async processing completion)
* 📊 Filtering/sorting for candidates
* 📥 Export API

---

If you want, I can also:

* Convert this into **Swagger/OpenAPI spec**
* Create **Postman collection**
* Design **backend folder structure**
* Or draw **API flow diagram**

Just tell me 👍
