from enum import Enum
from uuid import uuid4
from datetime import datetime

class JobStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class Job:
    def __init__(self, job_type: str):
        self.job_id = str(uuid4())
        self.job_type = job_type
        self.status = JobStatus.PENDING
        self.retries = 0
        self.created_at = datetime.utcnow()
