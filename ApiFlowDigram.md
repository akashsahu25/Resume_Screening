flowchart TD
    A[Client / Frontend App] --> B[Sign Up / Login / Google Auth API]

    B --> C{Authentication Successful?}
    C -- No --> C1[Return Auth Error]
    C -- Yes --> D[Receive JWT Token]

    D --> E[Authorized API Requests]

    E --> F[Create Job Requirement API]
    F --> G[Store Job Details in Database]

    G --> H[Upload Resumes API]
    H --> I[Store Resume Files in AWS S3]
    I --> J[Save Resume Metadata in Database]

    J --> K[Start AI Processing API]
    K --> L[Background AI Processing Engine]

    L --> M[Parse Resume]
    M --> N[Extract Candidate Data]
    N --> O[Match Resume with Job Requirement]
    O --> P[Calculate AI Score]
    P --> Q[Generate AI Summary]
    Q --> R[Save Candidate Results in Database]

    R --> S[Get Processing Progress API]
    S --> T{Processing Complete?}

    T -- No --> S
    T -- Yes --> U[Get Candidates Summary API]

    U --> V[Display Ranked Candidate Dashboard]

    V --> W[Get Full Candidate Details API]
    V --> X[Get Candidate Resume API]
    V --> Y[Get GitHub / LinkedIn Profile API]

    W --> Z[Update Candidate CTC API]
    W --> AA[Update Candidate Note API]

    Z --> AB[Save Updates in Database]
    AA --> AB

    AB --> V