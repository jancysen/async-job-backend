import time
from queue_store import job_queue, job_store
from models import JobStatus

def process_job(job):
    print(f"Processing job {job.job_id} ({job.job_type})")
    time.sleep(3)  # simulate work
    job.status = JobStatus.SUCCESS
    print(f"Job {job.job_id} completed")

def start_worker():
    print("Worker started. Waiting for jobs...")
    while True:
        job = job_queue.get()
        job.status = JobStatus.PROCESSING
        process_job(job)
        job_queue.task_done()

if __name__ == "__main__":
    start_worker()
