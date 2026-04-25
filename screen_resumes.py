#!/usr/bin/env python3
"""
Resume Screening Script for Backend Developer Role
Company: Clinvvo (Healthcare SaaS Startup)

Usage:
    python screen_resumes.py --input ./resumes --output results.csv

Requirements:
    pip install google-genai pandas
"""

import os
import sys
import time
import json
import base64
import argparse
import pandas as pd
from pathlib import Path
from google import genai
from google.genai import types as genai_types
from google.oauth2.service_account import Credentials

# =============================================================================
# ENVIRONMENT VARIABLES - Fill these with your actual values
# =============================================================================
os.environ["GOOGLE_APPLICATION_CREDENTIALS_BASE64"] = "ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAiZ2VuLWxhbmctY2xpZW50LTA4OTE4NDk3OTAiLAogICJwcml2YXRlX2tleV9pZCI6ICI1YzM3YjAzZDU1MzViMGNmNmZkZDAwNjhjYzkxMTFmMmIzNDE2ZGQ4IiwKICAicHJpdmF0ZV9rZXkiOiAiLS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tXG5NSUlFdlFJQkFEQU5CZ2txaGtpRzl3MEJBUUVGQUFTQ0JLY3dnZ1NqQWdFQUFvSUJBUUMxQXJUekJnNzl2L2V6XG5OdU5EUHlJSWZEZCtnTmFOdzJOcFZOKzhjb2lDeXZkcmdNcUtjZWdsN2R3Sm9MT2RiVmlwM0JvRWhsa3gwbEdjXG5odHIxYWdJdCtIMHB0U2pkTVV6MHkyTXQvZ21NdkJuWXVBSmNBOEVuaTFQeWIrTThndHJONDlYRVRTaUZ3YmMvXG4zcmtMMVJpV1N0ckFiczlNbUJkVU9EQTE2ZFd1ZE03VXZ5bWJNUjV1dG4vazFRMUNSU05HaWdVTTlRYk1ZdWNZXG53R0Q5cFhtckFjUElyd0J6MUpEbnZhSkNXaDZLejVpNkVQa0ZUVTNvYUswa080Z2w4WS8xbnI2M3BXUVNaajZxXG5pUGRhUWNRbFpPSEFPajBwN1ZqYWhIZ0FtU0xJSmxxZFlSeE9aL0l1a2w1YXk0V2JTL3dZa2FsZUFHL29wVCttXG5memR0NHErZEFnTUJBQUVDZ2dFQUtKWHJTYVJkbnlLNFlOd1pOOTVEZk1DUlZ0Ri9pZmk1NVFldFJOMHZZNWdyXG53dFIxVlhaMTFXOVFTMjVYWjZCNVpWaWZFczJtMlNkdHVobDRwZGMzbHVRaytFR1E0SXVwMUNkNFhQc2RYQXRmXG5CanMzK0RhMVMrOFBDd2h3WElTQWwvS1NYem5uc0puL1F4aG15RkxtK09mZXhZL3k5aHNSL0FXL05ZOXhKSFRXXG51bzhwc1JQYXU3Y25zRTZDQmJqWWFIcUFabVE0RlVzenVKMjk2V3dZWm16TFVBN3JiNklxNlMvQjNEVEpJaXNtXG5lNHNNM3BSZmRXYlZTeEpORDlpcUpPbTJCeDN0Wm56MVA4b2hkc1hIWmtwbTZzQUduUkI0YndTWXlCV0c5TVo5XG4rN1RtaE9OZUVJSlRtem5FY3BUY21VNitibDk5c1d6MUtUMEM1aXpsdHdLQmdRRGhiRWNURVFGc3ZXak9kbmo1XG5pT3Z5M0pxdFE4Y3VDNis5OWx3SnZ2S2pzUFZTTTJRRHRmRFpTdVdncHY5czNJNmFadEJMenNWcktQTGFGdXVMXG4yOVZ2WnAyb21hV2xoWjYxWGhoTTJiYUVpQ2MzWnRxN3dNN3BqQ2FzcmRPZXVuKzYrWnZhOHY1Z0FWVTd5S21RXG5icHJNL0h6ZUorZmVmamxCL2FrY3BmcUJGd0tCZ1FETmtEb1FMVUFtNlczQ1RmR09iYURTOFNDUnhtN2hyQnlFXG5VQmJTeTVQSS8xVW9KVDRhcThLNm1DTVZWbHFjR0tSV093dC93aEthaC9OSUp2U0pyZ0F1NjlpSjl0OENVaXJWXG5xNG1RekdTUjNsa3lTNFlqMk5Md1Zxck0rYWZBSW44ZjVLcm13R3BZMm4wWWxDV2pxN2xsSmUrUmtmN2pPbnZuXG5aRFhLS3gzOWF3S0JnUUM5d1FhblB4Wmk4YUlLd2VHZHRDdGgyVjkrNEdJSEdhRkxGOWxyL3NlREVVL0FiVEFRXG5pNVA5WmJXY0lWYzd6UUZoYVpDSGI3dnhNNXdTQjE4cDhOaGVtUk8zdS9hYk9icGFVNlhDOHpWWHBNRFdPd2QvXG5LcE5DTjA3SzV0d1BibEJkRlFha0xRNEJ4TDE1d0xVenRsY3FuSk9EOGpXVnJjMEhCcjdYTmNTRDZ3S0JnRWo3XG5mK0htYnZSaHhCcE1XZ3JiV1ZJTFVpanZic2FvdUtjeFdDa1hKaTBpbWpWYW82WU1mV0tLU1VwMkVrMkJZamRMXG5WMVhRclpJMzJtUXZrSHFoVUdkWVROVU8xVGFadmFPRzk1eDFOTytsSmIzNW1uSjN0TXludUpSMXZ0MDBZallNXG5sYkMvZUFKNzhCWWQ0dzh0RlBHWWVtb1FqNUpWWFZCVi85TDdZL1pwQW9HQURuNWJtaUVnRFZ5VzZ1c2xod3g5XG53SUtubWZHTi9DaEhYUXUwbGMwbm5Sa3A2Q1hJL2lkNS9MVmNtR01DRnNhUEVDT3htSVdFUUdITFZoTUtQMXgrXG5YdkJMYnE4bFoxaEYvZDlnM2EwS2Z0MEtlYmFjWDRKTWdGNERhbzhEdklpNFkvNEFHRlN6L2d1bWxzK1pFYnRZXG4vUnZ4VDBYcWdvVnlzUFM4RXJtQm0vaz1cbi0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS1cbiIsCiAgImNsaWVudF9lbWFpbCI6ICJnZW1pbmktYXBpQGdlbi1sYW5nLWNsaWVudC0wODkxODQ5NzkwLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwKICAiY2xpZW50X2lkIjogIjExMTc2OTA5MjczMTIzODA0MTM0OSIsCiAgImF1dGhfdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoIiwKICAidG9rZW5fdXJpIjogImh0dHBzOi8vb2F1dGgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwKICAiYXV0aF9wcm92aWRlcl94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL29hdXRoMi92MS9jZXJ0cyIsCiAgImNsaWVudF94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL3JvYm90L3YxL21ldGFkYXRhL3g1MDkvZ2VtaW5pLWFwaSU0MGdlbi1sYW5nLWNsaWVudC0wODkxODQ5NzkwLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwKICAidW5pdmVyc2VfZG9tYWluIjogImdvb2dsZWFwaXMuY29tIgp9Cg==" 
os.environ["GCP_PROJECT_ID"] = "gen-lang-client-0891849790" 
os.environ["GCP_LOCATION"] = "europe-north1"
# =============================================================================
# CONFIGURATION - Edit this section for different job profiles
# =============================================================================

JOB_PROFILE = {
    "name": "Backend Engineer - Clinvvo",
    "skills": {
        "backend_programming": {"max_score": 25},
        "aws_cloud_infrastructure": {"max_score": 15},
        "databases_and_data": {"max_score": 12},
        "api_and_architecture": {"max_score": 15},
        "genai_integration": {"max_score": 8},
        "ownership_and_leadership": {"max_score": 12},
        "healthcare_regulated_domain": {"max_score": 5},
        "startup_and_communication": {"max_score": 8}, `````````````````````                                                                `           
    }
    # Total max score: 100
}

# Gemini model configuration
GEMINI_MODEL = "gemini-2.5-flash"
BATCH_SIZE = 5  # Number of PDFs per API request
RATE_LIMIT_RETRY_BASE = 5  # Base seconds to wait on rate limit
RATE_LIMIT_RETRY_MAX = 120  # Max seconds to wait

# =============================================================================
# ENVIRONMENT VARIABLES (set these before running)
# =============================================================================
# GOOGLE_APPLICATION_CREDENTIALS_BASE64 - Base64 encoded service account JSON
# GCP_PROJECT_ID - Your GCP project ID
# GCP_LOCATION - GCP region (e.g., "us-central1")
# =============================================================================


def get_genai_client() -> genai.Client:
    """
    Initializes and returns a Google Generative AI client using a
    base64 encoded service account from environment variables.
    """
    # Get environment variables
    creds_base64 = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_BASE64")
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")
    
    if not creds_base64:
        print("Error: GOOGLE_APPLICATION_CREDENTIALS_BASE64 environment variable not set")
        sys.exit(1)
    if not project_id:
        print("Error: GCP_PROJECT_ID environment variable not set")
        sys.exit(1)
    
    try:
        # Decode the base64 encoded service account JSON
        sa_info_decoded = base64.b64decode(creds_base64)
        sa_info = json.loads(sa_info_decoded)

        # Define the required scopes
        scopes = ["https://www.googleapis.com/auth/cloud-platform"]

        # Create credentials from the service account info
        creds = Credentials.from_service_account_info(sa_info, scopes=scopes)

        # Initialize the GenAI client for Vertex AI
        client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location,
            credentials=creds,
        )
        return client
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        print(f"Error: Failed to decode or parse service account credentials: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to initialize Google GenAI client: {e}")
        sys.exit(1)

# =============================================================================
# EVALUATION PROMPT
# =============================================================================

EVALUATION_PROMPT = """You are an expert technical recruiter evaluating resumes for a Backend Engineer position at a healthcare SaaS startup.

## Company Context
Clinvvo is a small Swedish healthtech startup (not a large enterprise). They need engineers who can:
- Own features end-to-end with minimal hand-holding
- Work with loose requirements and make good judgment calls
- Move fast while maintaining quality in a regulated healthcare domain
- Collaborate directly with stakeholders and partners

## Tech Stack
- **Primary**: Python (FastAPI), Node.js
- **Cloud**: AWS (EC2, S3, RDS, Lambda, IAM)
- **Database**: PostgreSQL
- **Bonus**: GenAI/LLM integration experience

## Your Task
Evaluate each resume and extract structured information. Be rigorous and evidence-based.

### CRITICAL EVALUATION RULES:
1. **Professional experience counts 3x more than personal projects, bootcamp projects, or coursework**
2. **Infer skills from specific project bullets and achievements, NOT from summary/objective sections or self-proclaimed skills lists**
3. **Look for EVIDENCE of claims**: "Led migration" should have details (what? how big? what was the outcome?)
4. **Production systems >> side projects >> tutorials/certifications**
5. **Depth over breadth**: 3 years focused Python experience > listing 10 languages superficially
6. **Ownership signals**: deployed to prod, oncall/incidents, architecture decisions, mentoring
7. **Startup fit**: ambiguity tolerance, wore multiple hats, resource constraints, fast iteration
8. **Be skeptical of vague claims**: "Improved performance" (by how much?), "Large scale" (what scale exactly?)

### Scoring Guidelines for Each Skill:

**backend_programming (0-25):**
- 20-25: 3+ years production Python/Node.js, shipped multiple systems, deep framework knowledge
- 15-19: 2+ years solid experience, production systems, good fundamentals
- 10-14: 1-2 years experience OR strong in Java/Go/C# but not Python/Node
- 5-9: Junior level, mostly personal projects, limited production exposure
- 0-4: Minimal backend experience, frontend-heavy, or no clear evidence

**aws_cloud_infrastructure (0-15):**
- 12-15: Hands-on AWS (multiple services), IaC, deployment pipelines, cost optimization
- 8-11: Good AWS experience, deployed production systems
- 4-7: Basic cloud usage, or strong in GCP/Azure but not AWS
- 0-3: Minimal cloud experience, localhost-only development

**databases_and_data (0-12):**
- 10-12: PostgreSQL expert, query optimization, migrations, data modeling at scale
- 6-9: Solid SQL skills, production database experience
- 3-5: Basic CRUD, limited optimization experience
- 0-2: Minimal database work, ORM-only, no direct SQL

**api_and_architecture (0-15):**
- 12-15: Designed APIs from scratch, async patterns, scalability decisions, system design
- 8-11: Built RESTful services, understands architecture patterns
- 4-7: Consumed/extended APIs, limited design responsibility
- 0-3: Minimal API experience

**genai_integration (0-8):**
- 6-8: Built production AI features, LLM APIs, RAG, embeddings, prompt engineering
- 3-5: Some AI/ML integration, experimented with LLMs
- 1-2: Awareness level, used ChatGPT API once
- 0: No evidence of AI/GenAI work (DO NOT penalize heavily - this is a bonus)

**ownership_and_leadership (0-12):**
- 10-12: Led projects end-to-end, architecture decisions, production deployments, oncall, mentored
- 6-9: Owned features, some leadership, deployed to prod independently
- 3-5: Contributed to team projects, some ownership
- 0-2: Mostly executed assigned tasks, no clear ownership evidence
- **IMPORTANT**: Infer this from project descriptions. Ignore self-proclaimed "leadership skills" in summary.

**healthcare_regulated_domain (0-5):**
- 4-5: Direct healthcare/fintech experience, HIPAA/GDPR, compliance-aware
- 2-3: Regulated industry experience, security-conscious patterns
- 1: Awareness of compliance, no direct experience
- 0: No regulated domain experience (DO NOT penalize too heavily)

**startup_and_communication (0-8):**
- 6-8: Startup experience, cross-functional work, ambiguous requirements, wore multiple hats
- 3-5: Some startup or small team experience, good collaboration signals
- 1-2: Mostly large company/structured environment
- 0: No signals either way

## Resumes to Evaluate
You will receive {num_resumes} resume(s). Evaluate each one and return a JSON array with one object per resume.

The filenames are: {filenames}

CRITICAL: For each evaluation, you MUST set "source_filename" to the EXACT filename of the resume you are evaluating (e.g., "john_doe.pdf"). This is used for verification.

Return your evaluation as a JSON array with exactly {num_resumes} objects - one per resume.
"""

# =============================================================================
# EXTRACTION SCHEMA
# =============================================================================

EXTRACTION_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "source_filename": {
                "type": "string",
                "description": "The exact filename of the resume being evaluated (e.g., 'john_doe.pdf'). MUST match one of the provided filenames exactly."
            },
            "candidate_name": {
                "type": "string",
                "description": "Full name of the candidate"
            },
            "email": {
                "type": "string",
                "description": "Email address if found, else empty string"
            },
            "phone": {
                "type": "string",
                "description": "Phone number if found, else empty string"
            },
            "years_of_experience": {
                "type": "number",
                "description": "Total years of professional software development experience (not including internships or personal projects). Use 0 if unclear."
            },
            "backend_programming": {
                "type": "integer",
                "description": "Score 0-25: Python/Node.js expertise preferred, Java/Go/C# acceptable. Based on production experience depth."
            },
            "aws_cloud_infrastructure": {
                "type": "integer",
                "description": "Score 0-15: AWS services (EC2, S3, RDS, Lambda, IAM), IaC, deployments."
            },
            "databases_and_data": {
                "type": "integer",
                "description": "Score 0-12: PostgreSQL preferred. SQL expertise, optimization, data modeling."
            },
            "api_and_architecture": {
                "type": "integer",
                "description": "Score 0-15: RESTful APIs, async processing, system design, scalability."
            },
            "genai_integration": {
                "type": "integer",
                "description": "Score 0-8: LLM APIs, RAG, embeddings, AI pipelines. Bonus skill."
            },
            "ownership_and_leadership": {
                "type": "integer",
                "description": "Score 0-12: Led projects E2E, architecture decisions, prod deployments. INFER from projects, NOT summary."
            },
            "healthcare_regulated_domain": {
                "type": "integer",
                "description": "Score 0-5: Healthcare, fintech, HIPAA, GDPR, compliance experience."
            },
            "startup_and_communication": {
                "type": "integer",
                "description": "Score 0-8: Startup experience, cross-functional work, ambiguity tolerance."
            },
            "key_strengths": {
                "type": "string",
                "description": "2-3 strongest qualifications with evidence (max 150 chars)"
            },
            "concerns": {
                "type": "string",
                "description": "Key gaps or red flags for this role (max 150 chars)"
            }
        },
        "required": [
            "source_filename", "candidate_name", "email", "phone", "years_of_experience",
            "backend_programming", "aws_cloud_infrastructure", "databases_and_data",
            "api_and_architecture", "genai_integration", "ownership_and_leadership",
            "healthcare_regulated_domain", "startup_and_communication",
            "key_strengths", "concerns"
        ]
    }
}

# =============================================================================
# PROGRESS TRACKER
# =============================================================================

# Global log file handle (set in main)
_log_file = None


def log(message: str, end: str = "\n"):
    """Print to console and write to log file."""
    print(message, end=end, flush=True)
    if _log_file:
        _log_file.write(message + end)
        _log_file.flush()


class ProgressTracker:
    """Simple progress tracker with timing information."""
    
    def __init__(self, total: int, batch_size: int):
        self.total = total
        self.batch_size = batch_size
        self.processed = 0
        self.failed = 0
        self.start_time = time.time()
        self.total_batches = (total + batch_size - 1) // batch_size
        self.current_batch = 0
    
    def update(self, success_count: int, fail_count: int = 0):
        """Update progress after a batch completes."""
        self.processed += success_count
        self.failed += fail_count
        self.current_batch += 1
    
    def get_elapsed(self) -> str:
        """Get elapsed time as formatted string."""
        elapsed = time.time() - self.start_time
        return self._format_time(elapsed)
    
    def get_eta(self) -> str:
        """Estimate remaining time based on current pace."""
        if self.processed == 0:
            return "calculating..."
        
        elapsed = time.time() - self.start_time
        rate = self.processed / elapsed  # resumes per second
        remaining = self.total - self.processed - self.failed
        
        if rate > 0:
            eta_seconds = remaining / rate
            return self._format_time(eta_seconds)
        return "unknown"
    
    def _format_time(self, seconds: float) -> str:
        """Format seconds into human readable string."""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            mins = seconds // 60
            secs = seconds % 60
            return f"{mins:.0f}m {secs:.0f}s"
        else:
            hours = seconds // 3600
            mins = (seconds % 3600) // 60
            return f"{hours:.0f}h {mins:.0f}m"
    
    def get_progress_bar(self, width: int = 30) -> str:
        """Generate a simple progress bar."""
        if self.total == 0:
            return "[" + "=" * width + "]"
        
        progress = (self.processed + self.failed) / self.total
        filled = int(width * progress)
        bar = "=" * filled + "-" * (width - filled)
        percentage = progress * 100
        return f"[{bar}] {percentage:.1f}%"
    
    def print_status(self):
        """Print current progress status."""
        bar = self.get_progress_bar()
        elapsed = self.get_elapsed()
        eta = self.get_eta()
        
        status = (
            f"\r📊 {bar} | "
            f"Batch {self.current_batch}/{self.total_batches} | "
            f"Done: {self.processed}/{self.total} | "
            f"Failed: {self.failed} | "
            f"Elapsed: {elapsed} | "
            f"ETA: {eta}    "
        )
        print(status, end="", flush=True)
        # Log without carriage return
        if _log_file:
            clean_status = status.replace("\r", "").strip()
            _log_file.write(f"{clean_status}\n")
            _log_file.flush()
    
    def print_newline(self):
        """Print newline to move past the progress bar."""
        print()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_processed_filenames(csv_path: Path) -> set:
    """Get set of already processed filenames from CSV."""
    if not csv_path.exists():
        return set()
    try:
        df = pd.read_csv(csv_path)
        return set(df['filename'].tolist())
    except Exception as e:
        log(f"Warning: Could not read existing CSV: {e}")
        return set()


def scan_folder(input_dir: Path) -> tuple[list[Path], dict[str, int]]:
    """
    Recursively scan folder for PDFs, track removed file types.
    Returns (list of PDF paths, dict of removed extensions with counts)
    """
    pdf_files = []
    removed = {}
    
    # Recursively find all files
    for file in input_dir.rglob('*'):
        if file.is_file():
            ext = file.suffix.lower()
            if ext == '.pdf':
                pdf_files.append(file)
            else:
                removed[ext] = removed.get(ext, 0) + 1
    
    return pdf_files, removed


def calculate_overall_score(evaluation: dict) -> int:
    """Calculate overall score by summing all skill scores."""
    skill_fields = [
        "backend_programming", "aws_cloud_infrastructure", "databases_and_data",
        "api_and_architecture", "genai_integration", "ownership_and_leadership",
        "healthcare_regulated_domain", "startup_and_communication"
    ]
    return sum(evaluation.get(field, 0) for field in skill_fields)


def call_gemini_with_retry(client, pdf_bytes_list: list[bytes], filenames: list[str]) -> list[dict]:
    """
    Call Gemini API with retry on rate limit.
    Sends PDFs as inline bytes data.
    Returns list of evaluation dicts.
    """
    prompt_text = EVALUATION_PROMPT.format(
        num_resumes=len(pdf_bytes_list),
        filenames=", ".join(filenames)
    )
    
    # Build content with PDFs as inline bytes and prompt
    parts = []
    for i, pdf_bytes in enumerate(pdf_bytes_list):
        # Add label as text part
        parts.append(genai_types.Part.from_text(text=f"=== RESUME {i+1}: {filenames[i]} ==="))
        # Add PDF as inline bytes
        parts.append(genai_types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"))
    
    # Add the evaluation prompt
    parts.append(genai_types.Part.from_text(text=prompt_text))
    
    # Single user message with all parts
    contents = [
        genai_types.Content(role="user", parts=parts)
    ]
    
    # Build config
    config = genai_types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=EXTRACTION_SCHEMA,
        temperature=0,
        top_k=1,
        seed=0,
        thinking_config=genai_types.ThinkingConfig(thinking_budget=0),
    )
    
    retry_count = 0
    wait_time = RATE_LIMIT_RETRY_BASE
    
    while True:
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=contents,
                config=config,
            )
            
            # Parse response using the same pattern as your invoke method
            result = response.to_json_dict().get("parsed", [])
            
            # Fallback to text parsing if parsed is empty
            if not result and hasattr(response, 'text') and response.text:
                result = json.loads(response.text)
            
            return result
            
        except Exception as e:
            error_str = str(e).lower()
            
            # Check if rate limit error
            if "rate" in error_str or "quota" in error_str or "429" in error_str or "resource_exhausted" in error_str:
                retry_count += 1
                log(f"  ⏳ Rate limit hit (attempt {retry_count}). Waiting {wait_time}s...")
                time.sleep(wait_time)
                wait_time = min(wait_time * 2, RATE_LIMIT_RETRY_MAX)
            else:
                # Non-rate-limit error, raise it
                raise


def process_batch(client, pdf_paths: list[Path], filenames: list[str]) -> list[dict]:
    """
    Process a batch of PDFs and return evaluations with filenames verified.
    Sends PDFs as inline bytes (no file upload needed for Vertex AI).
    """
    # Read PDF files as bytes
    pdf_data = []
    for pdf_path in pdf_paths:
        with open(pdf_path, "rb") as f:
            pdf_data.append(f.read())
    
    # Call API with inline PDF bytes
    evaluations = call_gemini_with_retry(client, pdf_data, filenames)
    
    # Build a map from source_filename to evaluation for matching
    eval_map = {}
    for eval_dict in evaluations:
        source = eval_dict.get('source_filename', '').strip()
        eval_map[source] = eval_dict
    
    # Match evaluations to filenames and verify
    results = []
    unmatched = []
    
    for filename in filenames:
        if filename in eval_map:
            eval_dict = eval_map[filename]
            eval_dict['filename'] = filename  # Use our filename as canonical
            eval_dict['overall_score'] = calculate_overall_score(eval_dict)
            # Remove source_filename from output (we have 'filename' now)
            eval_dict.pop('source_filename', None)
            results.append(eval_dict)
        else:
            unmatched.append(filename)
    
    # Handle unmatched files
    if unmatched:
        log(f"   ⚠️  Warning: Could not match evaluations for: {unmatched}")
        # If we have extra evaluations, try to assign by order as fallback
        used_sources = set(eval_map.keys()) & set(filenames)
        unused_evals = [e for s, e in eval_map.items() if s not in filenames]
        
        for i, filename in enumerate(unmatched):
            if i < len(unused_evals):
                log(f"      Fallback: assigning unmatched eval to {filename}")
                eval_dict = unused_evals[i]
                eval_dict['filename'] = filename
                eval_dict['overall_score'] = calculate_overall_score(eval_dict)
                eval_dict.pop('source_filename', None)
                results.append(eval_dict)
            else:
                log(f"      ❌ No evaluation found for {filename}, skipping")
    
    return results


def append_to_csv(results: list[dict], csv_path: Path):
    """Append results to CSV file."""
    # Define column order
    columns = [
        'filename', 'candidate_name', 'email', 'phone', 'years_of_experience',
        'backend_programming', 'aws_cloud_infrastructure', 'databases_and_data',
        'api_and_architecture', 'genai_integration', 'ownership_and_leadership',
        'healthcare_regulated_domain', 'startup_and_communication',
        'overall_score', 'key_strengths', 'concerns'
    ]
    
    df = pd.DataFrame(results)
    df = df[columns]  # Reorder columns
    
    # Append or create
    if csv_path.exists():
        df.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_path, index=False)


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Screen resumes for Backend Developer role")
    parser.add_argument("--input", "-i", required=True, help="Input folder containing PDF resumes")
    parser.add_argument("--output", "-o", default="results.csv", help="Output CSV file (default: results.csv)")
    parser.add_argument("--log", "-l", default="screening.log", help="Log file (default: screening.log)")
    args = parser.parse_args()
    
    input_dir = Path(args.input)
    csv_path = Path(args.output)
    log_path = Path(args.log)
    
    # Setup global log file
    global _log_file
    _log_file = open(log_path, "a", encoding="utf-8")
    
    if not input_dir.exists():
        log(f"Error: Input directory '{input_dir}' does not exist")
        _log_file.close()
        sys.exit(1)
    
    # Initialize Gemini client via Vertex AI
    client = get_genai_client()
    
    log(f"{'='*60}")
    log(f"Resume Screening - {JOB_PROFILE['name']}")
    log(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"{'='*60}")
    
    # Scan folder
    log(f"\n📁 Scanning folder: {input_dir}")
    pdf_files, removed = scan_folder(input_dir)
    
    log(f"   Found {len(pdf_files)} PDF files")
    if removed:
        log(f"   ⚠️  Skipped non-PDF files:")
        for ext, count in sorted(removed.items()):
            log(f"      {ext}: {count} file(s)")
    
    # Check already processed
    processed = get_processed_filenames(csv_path)
    log(f"\n📋 Already processed: {len(processed)} files")
    
    # Filter to unprocessed
    to_process = [(p, p.name) for p in pdf_files if p.name not in processed]
    log(f"   Remaining to process: {len(to_process)} files")
    
    if not to_process:
        log("\n✅ All files already processed!")
        _log_file.close()
        return
    
    # Process in batches
    total_batches = (len(to_process) + BATCH_SIZE - 1) // BATCH_SIZE
    log(f"\n🚀 Processing {len(to_process)} resumes in {total_batches} batches (batch size: {BATCH_SIZE})")
    log(f"   Output: {csv_path}")
    log(f"   Log: {log_path}")
    log("")
    
    # Initialize progress tracker
    progress = ProgressTracker(total=len(to_process), batch_size=BATCH_SIZE)
    failed_files = []
    
    for batch_num in range(total_batches):
        start_idx = batch_num * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, len(to_process))
        batch = to_process[start_idx:end_idx]
        
        batch_paths = [item[0] for item in batch]
        batch_names = [item[1] for item in batch]
        
        # Print progress bar
        progress.print_status()
        progress.print_newline()
        log(f"   📦 Processing: {batch_names}")
        
        try:
            results = process_batch(client, batch_paths, batch_names)
            append_to_csv(results, csv_path)
            
            # Print quick summary for this batch
            for r in results:
                log(f"      ✓ {r['filename']}: {r['candidate_name']} - Score: {r['overall_score']}/100")
            
            progress.update(success_count=len(results), fail_count=len(batch_names) - len(results))
            
        except Exception as e:
            log(f"      ❌ Batch failed: {e}")
            failed_files.extend(batch_names)
            progress.update(success_count=0, fail_count=len(batch_names))
        
        log("")
    
    # Final progress update
    progress.print_status()
    progress.print_newline()
    
    # Final summary
    log(f"\n{'='*60}")
    log(f"✅ COMPLETE")
    log(f"   Processed: {progress.processed} resumes")
    log(f"   Failed: {progress.failed} resumes")
    log(f"   Total time: {progress.get_elapsed()}")
    log(f"   Output: {csv_path}")
    log(f"   Finished at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if failed_files:
        log(f"\n   Failed files:")
        for f in failed_files:
            log(f"      - {f}")
    
    log(f"\n💡 Tip: Open {csv_path} and sort by 'overall_score' descending to see top candidates")
    
    # Close log file
    _log_file.close()


if __name__ == "__main__":
    main()