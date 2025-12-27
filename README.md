## Overview
This project demonstrates an asynchronous job processing backend built using FastAPI.
It allows clients to submit jobs that are processed in the background without blocking API requests.
## Why this project?
Built to understand how real-world backend systems handle background tasks, scalability,
and non-blocking request processing using FastAPI.
## Key Concepts
- Asynchronous background task execution
- RESTful API design
- Database interaction
## How to Run
1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
   pip install -r requirements.txt
4. Run the server:
   uvicorn app:app --reload
## 📦 API Endpoints

### Create Job
**POST /jobs**

**Request**
```json
{
  "job_type": "email"
}
