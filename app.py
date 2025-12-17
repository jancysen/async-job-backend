from fastapi import FastAPI, BackgroundTasks
import time
from models import Job, JobStatus
from database import get_connection, init_db
init_db()


app = FastAPI()

MAX_RETRIES = 3

def process_job(job: Job):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE jobs SET status=? WHERE job_id=?",
            (JobStatus.PROCESSING, job.job_id)
        )
        conn.commit()

        time.sleep(3)

        if job.job_type == "fail":
            raise Exception("Simulated failure")

        cursor.execute(
            "UPDATE jobs SET status=? WHERE job_id=?",
            (JobStatus.SUCCESS, job.job_id)
        )

    except Exception:
        job.retries += 1

        if job.retries >= MAX_RETRIES:
            cursor.execute(
                "UPDATE jobs SET status=?, retries=? WHERE job_id=?",
                (JobStatus.FAILED, job.retries, job.job_id)
            )
        else:
            cursor.execute(
                "UPDATE jobs SET retries=? WHERE job_id=?",
                (job.retries, job.job_id)
            )
            process_job(job)

    conn.commit()
    conn.close()

@app.get("/")
def root():
    return {"message": "Backend API is running"}

@app.post("/jobs")
def create_job(job_type: str, background_tasks: BackgroundTasks):
    job = Job(job_type)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO jobs VALUES (?, ?, ?, ?, ?)",
        (job.job_id, job.job_type, job.status, job.retries, job.created_at.isoformat())
    )
    conn.commit()
    conn.close()

    background_tasks.add_task(process_job, job)

    return {
        "job_id": job.job_id,
        "status": job.status
    }


@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT job_id, job_type, status, retries FROM jobs WHERE job_id=?",
        (job_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "Job not found"}

    return {
        "job_id": row[0],
        "job_type": row[1],
        "status": row[2],
        "retries": row[3]
    }

