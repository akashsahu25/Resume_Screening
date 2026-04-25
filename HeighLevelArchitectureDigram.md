flowchart TD
    User[Recruiter/User] --> WebApp[Web App / Dashboard]

    WebApp --> Auth[Authentication Service]
    WebApp --> Billing[Subscription & Billing]
    Billing --> Payment[Stripe / Razorpay]

    WebApp --> Upload[JD + Resume Upload]
    Upload --> Validation[File, Duplicate & Credit Validation]

    Validation --> AIEngine[AI Resume Screening Engine]

    AIEngine --> Parser[Resume Parser]
    AIEngine --> SkillMatch[Skill Matching]
    AIEngine --> Scoring[Match Score Engine]
    AIEngine --> Insights[AI Summary & Skill Gap Analysis]

    Parser --> DB[(Database)]
    SkillMatch --> DB
    Scoring --> DB
    Insights --> DB

    DB --> Dashboard[Recruitment Dashboard]

    Dashboard --> Filter[Search & Filters]
    Dashboard --> Sidebar[Candidate Detail Sidebar]
    Dashboard --> Decision[Shortlist / Hold / Reject / Select]
    Dashboard --> Export[CSV / Excel Export]