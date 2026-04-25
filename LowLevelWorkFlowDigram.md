flowchart TD
    A[User Login / Signup] --> B{Active Plan or Credits?}

    B -- No --> C[Locked Dashboard]
    C --> D[Choose Plan]
    D --> E[Payment Gateway]
    E --> F[Payment Success]
    F --> G[Unlock Dashboard]

    B -- Yes --> G[Full Dashboard Access]

    G --> H[Start New Screening]
    H --> I[Enter Job Description]
    I --> J[Define Must-Have Skills]
    J --> K[Define Nice-to-Have Skills]
    K --> L[Set Experience / Education Filters]

    L --> M[Bulk Upload Resumes]
    M --> N{Validate Files}

    N -- Invalid --> O[Show Error: Corrupt / Duplicate / Unsupported File]
    N -- Valid --> P{Enough Credits?}

    P -- No --> Q[Ask User to Upgrade / Buy Credits]
    P -- Yes --> R[Start Background AI Processing]

    R --> S[Parse Resume Text]
    S --> T[Extract Name, Contact, Skills, Experience, Education]
    T --> U[Detect Fraud / Keyword Stuffing]
    U --> V[Compare Resume with JD]
    V --> W[Calculate Match Score]
    W --> X[Identify Missing Skills]
    X --> Y[Generate AI Summary]
    Y --> Z[Store Candidate Result]

    Z --> AA[Update Progress Bar]
    AA --> AB{All Resumes Processed?}

    AB -- No --> R
    AB -- Yes --> AC[Redirect to Insights Dashboard]

    AC --> AD[Show Ranked Candidate Table]
    AD --> AE[Search / Filter Candidates]
    AD --> AF[Open Candidate Sidebar]
    AF --> AG[View Profile, Score Breakdown, Skill Gaps]
    AG --> AH[Add Recruiter Notes]
    AH --> AI[Update Status: Shortlist / Hold / Reject / Select]

    AI --> AJ[Export Final List to CSV / Excel]