# FlyRank Async Job Processing & Status Tracking Pipeline

An asynchronous backend task processing pipeline built with **FastAPI** and **In-Memory Job Tracking (`jobs_db`)**. This module enables non-blocking background execution for long-running AI inspection tasks and dynamic PDF report generation, providing instant `HTTP 202 Accepted` responses with real-time status polling.

---

## Key Features

* **Async Job Queue Pattern:** Offloads heavy computational tasks to background workers using FastAPI's `BackgroundTasks`.
* **Instant Non-blocking Response:** Returns `202 Accepted` with a unique `job_id` immediately upon job submission.
* **State Management:** In-memory job state tracking supporting transitions (`pending` ➔ `processing` ➔ `completed` / `failed`).
* **Status Polling API:** Dedicated endpoint to inspect job status and fetch final AI-generated results dynamically.

---

## System Architecture & Workflow

1. **Trigger Request (`POST /api/report/generate`)**:
   * Client submits a job prompt.
   * Server generates a unique 7-character `job_id`.
   * Enqueues the worker function `ai_inspect` to run asynchronously.
   * Returns an immediate JSON response with a status tracking URL.

2. **Background Execution (`ai_inspect`)**:
   * Updates state in `job_db[job_id]["status"] = "processing"`.
   * Simulates long-running AI analysis/task processing.
   * Saves execution results and transitions state to `"completed"`.
   * Handles errors gracefully with state set to `"failed"`.

3. **Status Polling (`GET /api/jobs/{job_id}`)**:
   * Client polls the status URL to verify execution state.
   * Returns current status (`processing` or `completed`) and the output result once finished.

---

## Project Structure

```text
.
├── main.py              # FastAPI application & Async Job endpoints
└── README.md            # Project documentation