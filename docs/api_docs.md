# AI Resume Analyzer — API Documentation

> API documentation for the AI Resume Analyzer backend built with FastAPI.

---

## 1. API Overview

The AI Resume Analyzer provides a RESTful API for uploading resumes, extracting resume content, analyzing resumes using AI/LLM services, and returning structured feedback.

### Backend Technology

* **Framework:** FastAPI
* **Language:** Python
* **API Style:** REST
* **Data Format:** JSON
* **File Format:** PDF
* **Validation:** Pydantic
* **AI Layer:** LLM-based analysis
* **API Version:** `v1`

---

# 2. Base URL

### Local Development

```text
http://localhost:8000
```

### API Base Path

```text
/api/v1
```

Therefore, the current API base URL is:

```text
http://localhost:8000/api/v1
```

---

# 3. API Versioning

The API uses URL-based versioning.

Current version:

```text
v1
```

Example:

```text
/api/v1/resume/analyze
```

Future versions can be introduced without breaking existing clients:

```text
/api/v2/resume/analyze
```

---

# 4. Content Types

### JSON Request

```http
Content-Type: application/json
```

### File Upload

Resume uploads use multipart form data:

```http
Content-Type: multipart/form-data
```

### JSON Response

Successful API responses generally use:

```http
Content-Type: application/json
```

---

# 5. Authentication

Authentication is currently optional and can be introduced when user accounts are implemented.

Future authenticated requests may use:

```http
Authorization: Bearer <access_token>
```

Example:

```http
Authorization: Bearer eyJhbGciOi...
```

Authentication-related functionality should be implemented through:

```text
backend/app/core/security.py
```

---

# 6. Resume Analysis API

## Analyze Resume

Analyzes an uploaded resume and returns structured AI-generated feedback.

### Endpoint

```http
POST /api/v1/resume/analyze
```

### Full URL

```text
http://localhost:8000/api/v1/resume/analyze
```

### Request Type

```text
multipart/form-data
```

### Request Parameter

| Parameter | Type | Required | Description     |
| --------- | ---- | -------: | --------------- |
| `file`    | File |      Yes | Resume PDF file |

### Example Request

Using cURL:

```bash
curl -X POST "http://localhost:8000/api/v1/resume/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@resume.pdf"
```

---

# 7. Successful Response

### Status Code

```http
200 OK
```

### Example Response

```json
{
  "score": 82,
  "summary": "The resume demonstrates a strong technical background with relevant project experience.",
  "skills": [
    "Python",
    "FastAPI",
    "React",
    "Machine Learning",
    "SQL"
  ],
  "strengths": [
    "Strong technical skill section",
    "Relevant project experience",
    "Clear educational background"
  ],
  "weaknesses": [
    "Limited measurable achievements",
    "Some sections could be more concise"
  ],
  "suggestions": [
    "Add measurable results to project descriptions",
    "Improve keyword alignment with target job descriptions",
    "Use stronger action verbs"
  ]
}
```

---

# 8. Response Schema

The expected response can be represented using a Pydantic model.

Example:

```python
from pydantic import BaseModel


class ResumeAnalysisResponse(BaseModel):
    score: float
    summary: str
    skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    suggestions: list[str]
```

The actual schema may evolve as additional analysis features are introduced.

---

# 9. API Processing Flow

The resume analysis request follows this architecture:

```text
Client
  │
  │ POST /api/v1/resume/analyze
  ▼
resume.py
  │
  ▼
analyzer.py
  │
  ├──► pdf_parser.py
  │       │
  │       ▼
  │    Extract Text
  │
  ├──► text_cleaner.py
  │       │
  │       ▼
  │    Clean Text
  │
  └──► ai_service.py
          │
          ▼
       AI / LLM
          │
          ▼
    Structured Result
          │
          ▼
       API Response
```

---

# 10. Request Lifecycle

The backend processes a resume through the following stages.

### Step 1 — Upload

The client uploads a PDF resume.

```text
Frontend → FastAPI
```

### Step 2 — Validation

The API validates the uploaded file.

Potential checks include:

* File exists
* File type
* File extension
* File size
* File readability

### Step 3 — PDF Parsing

The PDF parser extracts text from the uploaded document.

```text
PDF → Raw Text
```

### Step 4 — Text Cleaning

Extracted text is normalized and cleaned.

```text
Raw Text → Clean Text
```

### Step 5 — AI Analysis

The cleaned resume text is sent to the AI/LLM service.

```text
Clean Text → AI/LLM → Analysis
```

### Step 6 — Structured Response

The AI result is validated and returned as structured JSON.

```text
Analysis → JSON → Client
```

---

# 11. Error Handling

The API uses standard HTTP status codes to indicate request results.

| Status Code | Meaning                         |
| ----------- | ------------------------------- |
| `200`       | Request successful              |
| `400`       | Invalid request                 |
| `401`       | Authentication required/invalid |
| `403`       | Access denied                   |
| `404`       | Resource not found              |
| `413`       | Uploaded file is too large      |
| `415`       | Unsupported file type           |
| `422`       | Validation error                |
| `429`       | Rate limit exceeded             |
| `500`       | Internal server error           |
| `502`       | External AI service failure     |

---

# 12. Validation Errors

FastAPI may return a `422 Unprocessable Entity` response when request validation fails.

Example:

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "file"
      ],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

---

# 13. Invalid File Example

If the API receives an unsupported file:

```json
{
  "detail": "Only PDF files are supported."
}
```

Recommended status:

```http
415 Unsupported Media Type
```

---

# 14. Empty Resume Example

If the uploaded PDF contains no extractable text:

```json
{
  "detail": "Unable to extract readable text from the uploaded resume."
}
```

Recommended status:

```http
400 Bad Request
```

---

# 15. AI Service Error

If the external AI/LLM service fails:

```json
{
  "detail": "Resume analysis service is temporarily unavailable."
}
```

Recommended status:

```http
502 Bad Gateway
```

The API should avoid exposing internal API keys, provider errors, stack traces, or other sensitive information.

---

# 16. Health Check API

A health check endpoint is recommended for monitoring the backend.

### Endpoint

```http
GET /health
```

### Example Response

```json
{
  "status": "healthy"
}
```

### Status Code

```http
200 OK
```

This endpoint can be used by:

* Docker
* Deployment platforms
* Load balancers
* Monitoring services
* CI/CD pipelines

---

# 17. Root API Endpoint

The backend can expose a basic root endpoint.

### Endpoint

```http
GET /
```

### Example Response

```json
{
  "message": "AI Resume Analyzer API",
  "version": "1.0.0"
}
```

---

# 18. API Endpoint Summary

| Method | Endpoint                 | Purpose                 |
| ------ | ------------------------ | ----------------------- |
| `GET`  | `/`                      | API information         |
| `GET`  | `/health`                | Health check            |
| `POST` | `/api/v1/resume/analyze` | Analyze uploaded resume |

Future endpoints may include:

| Method   | Endpoint                    | Purpose                             |
| -------- | --------------------------- | ----------------------------------- |
| `POST`   | `/api/v1/auth/register`     | Create account                      |
| `POST`   | `/api/v1/auth/login`        | Authenticate user                   |
| `GET`    | `/api/v1/resumes`           | Get user's resumes                  |
| `GET`    | `/api/v1/resumes/{id}`      | Get analysis result                 |
| `DELETE` | `/api/v1/resumes/{id}`      | Delete resume                       |
| `POST`   | `/api/v1/job-match/analyze` | Compare resume with job description |
| `GET`    | `/api/v1/profile`           | Get user profile                    |

These endpoints should only be implemented when the corresponding functionality exists.

---

# 19. Interactive API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI

```text
http://localhost:8000/docs
```

Swagger UI allows developers to:

* View available endpoints
* Inspect request schemas
* Test API endpoints
* Upload resume files
* View responses
* Inspect status codes

### ReDoc

```text
http://localhost:8000/redoc
```

ReDoc provides an alternative documentation interface for the OpenAPI specification.

---

# 20. OpenAPI Specification

FastAPI automatically generates an OpenAPI specification.

```text
http://localhost:8000/openapi.json
```

This specification can be used by:

* API documentation tools
* Frontend developers
* API clients
* Testing tools
* Code generators

---

# 21. Example FastAPI Route

The resume endpoint is located at:

```text
backend/app/api/v1/resume.py
```

Example:

```python
from fastapi import APIRouter, UploadFile, File

from app.services.analyzer import analyze_resume

router = APIRouter()


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    result = await analyze_resume(file)
    return result
```

---

# 22. Example Application Setup

The main FastAPI application is located at:

```text
backend/app/main.py
```

Example:

```python
from fastapi import FastAPI

from app.api.v1.resume import router as resume_router


app = FastAPI(
    title="AI Resume Analyzer API",
    version="1.0.0"
)


app.include_router(
    resume_router,
    prefix="/api/v1/resume",
    tags=["Resume"]
)
```

The resulting endpoint becomes:

```text
POST /api/v1/resume/analyze
```

---

# 23. API Tags

API routes should be grouped using tags.

Recommended tags:

```text
Resume
Authentication
Users
Job Matching
Health
```

Example:

```python
router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)
```

---

# 24. Frontend API Integration

The React frontend communicates with the FastAPI backend through:

```text
frontend/src/services/api.js
```

Example:

```javascript
const API_URL = "http://localhost:8000/api/v1";


export async function analyzeResume(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_URL}/resume/analyze`,
    {
      method: "POST",
      body: formData
    }
  );

  if (!response.ok) {
    throw new Error("Resume analysis failed");
  }

  return response.json();
}
```

---

# 25. File Upload Rules

The backend should enforce reasonable upload restrictions.

Recommended initial rules:

```text
Allowed format: PDF
Maximum file size: configurable
```

Example:

```text
resume.pdf
```

Unsupported examples:

```text
resume.exe
resume.zip
resume.jpg
resume.docx
```

Support for additional formats can be added later.

---

# 26. Security Considerations

The API should follow basic security practices.

### API Keys

Never expose API keys in source code.

Use environment variables:

```env
OPENAI_API_KEY=your_key_here
```

### Git

Never commit:

```text
.env
```

### File Uploads

Uploaded files should be:

* Validated
* Size-limited
* Processed safely
* Stored only when necessary
* Deleted when temporary processing is complete

### AI Requests

Sensitive user information should be handled carefully when sending resume content to external AI services.

---

# 27. CORS

If the React frontend and FastAPI backend run on different origins during development, configure CORS.

Example:

```python
from fastapi.middleware.cors import CORSMiddleware


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

In production, replace the development origin with the actual frontend domain.

---

# 28. Environment Configuration

Example `.env.example`:

```env
OPENAI_API_KEY=your_api_key_here
DATABASE_URL=your_database_url_here
SECRET_KEY=your_secret_key_here
```

Environment-specific configuration should not be hardcoded into the application.

---

# 29. Local Development

### Start Backend

From the `backend` directory:

```bash
uv run uvicorn app.main:app --reload
```

Or, when the virtual environment is activated:

```bash
uvicorn app.main:app --reload
```

The backend will normally run at:

```text
http://localhost:8000
```

### Open API Documentation

```text
http://localhost:8000/docs
```

---

# 30. Testing the API

Example using cURL:

```bash
curl -X POST \
  "http://localhost:8000/api/v1/resume/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@resume.pdf"
```

Example using Python:

```python
import requests


with open("resume.pdf", "rb") as file:
    response = requests.post(
        "http://localhost:8000/api/v1/resume/analyze",
        files={"file": file}
    )


print(response.status_code)
print(response.json())
```

---

# 31. Automated Testing

API tests should be located in:

```text
backend/tests/
```

Example:

```text
backend/tests/test_resume.py
```

Tests should cover:

* Successful resume upload
* Invalid file type
* Empty file
* Corrupted PDF
* PDF text extraction
* AI service failure
* Invalid API requests
* Response schema validation

Example test structure:

```python
def test_resume_analysis():
    # Arrange
    # Act
    # Assert
    pass
```

---

# 32. Rate Limiting

Rate limiting can be introduced when the API is publicly deployed.

Possible limits:

```text
Anonymous users:
5 analyses / hour

Authenticated users:
20 analyses / hour
```

Actual limits should be determined based on infrastructure, AI provider costs, and product requirements.

---

# 33. Future API Expansion

The API can be expanded to support additional resume intelligence features.

### Resume Analysis

```text
POST /api/v1/resume/analyze
```

### Resume History

```text
GET /api/v1/resumes
```

### Resume Details

```text
GET /api/v1/resumes/{resume_id}
```

### Job Matching

```text
POST /api/v1/job-match/analyze
```

### Skill Extraction

```text
POST /api/v1/resume/skills
```

### ATS Analysis

```text
POST /api/v1/resume/ats-score
```

### Recommendations

```text
GET /api/v1/resumes/{resume_id}/recommendations
```

These endpoints should be added incrementally as the corresponding application features are implemented.

---

# 34. API Design Guidelines

The API should follow these principles:

1. Use appropriate HTTP methods.
2. Use meaningful resource names.
3. Keep API versioning consistent.
4. Validate all incoming data.
5. Return predictable JSON responses.
6. Use appropriate HTTP status codes.
7. Keep business logic outside route handlers.
8. Never expose secrets or internal errors.
9. Document new endpoints.
10. Add tests when introducing new functionality.

---

# 35. Backend Directory Reference

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── v1/
│   │       └── resume.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── services/
│   │   ├── pdf_parser.py
│   │   ├── ai_service.py
│   │   └── analyzer.py
│   │
│   ├── schemas/
│   │   └── resume_schema.py
│   │
│   ├── utils/
│   │   └── text_cleaner.py
│   │
│   └── db/
│       ├── models.py
│       └── session.py
│
├── tests/
│   └── test_resume.py
│
├── requirements.txt
└── README.md
```

---

# 36. Current API Contract

At the initial development stage, the primary API contract is:

```text
POST /api/v1/resume/analyze

Request:
    multipart/form-data
    file: PDF resume

Response:
    application/json

Response contains:
    - score
    - summary
    - skills
    - strengths
    - weaknesses
    - suggestions
```

The API contract should remain stable as much as possible. Breaking changes should be introduced through a new API version.

---

# 37. API Documentation Checklist

When adding a new endpoint, document:

* [ ] HTTP method
* [ ] Endpoint path
* [ ] Authentication requirement
* [ ] Request parameters
* [ ] Request body
* [ ] Content type
* [ ] Response structure
* [ ] Success status code
* [ ] Error status codes
* [ ] Example request
* [ ] Example response
* [ ] Test coverage

---

# 38. Summary

The AI Resume Analyzer API provides a modular interface between the React frontend and FastAPI backend.

The primary request flow is:

```text
React
  ↓
POST /api/v1/resume/analyze
  ↓
FastAPI
  ↓
Resume API Route
  ↓
Analyzer Service
  ↓
PDF Parser
  ↓
Text Cleaner
  ↓
AI/LLM Service
  ↓
Structured JSON
  ↓
React Frontend
```

The API is designed to evolve as additional features such as authentication, resume history, ATS scoring, job matching, and personalized recommendations are introduced.
