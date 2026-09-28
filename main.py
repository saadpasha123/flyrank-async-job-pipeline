from fastapi import FastAPI, BackgroundTasks,status
from fastapi.responses import FileResponse
import uuid
import time
app = FastAPI(title="Report Generation Pipeline API")
job_db={}
def ai_inspect(job_id:str,prompt:str):
    job_db[job_id]["status"]="processing"
    try:
        time.sleep(4)
        job_db[job_id]["status"]="completed"
        job_db[job_id]["result"]=f"AI Generated Insight for: {prompt}"
    except Exception as e:
        job_db[job_id]["status"]="failed"
        job_db[job_id]["error"]=str(e)
@app.post("/api/report/generate",status_code=status.HTTP_202_ACCEPTED)
def trigger_report_generation(prompt:str,backgroundtasks:BackgroundTasks):
    job_id=str(uuid.uuid4())[:7]        
    job_db[job_id]={
        "job_id":job_id,
        "status":"pending",
        "result":None,
        "error":None
    }
    backgroundtasks.add_task(
        ai_inspect,
        job_id,
        prompt,                
    )
    return{
        "status": "Job Enqueued",
        "message": "Report generation has started in the background.",
        "job_id":job_id,            
        "check_status":f"/api/jobs/{job_id}"
    }
@app.get("/api/jobs/{job_id}")
def download_report(job_id:str):
    job=job_db.get(job_id)
    if not job:
        return{"error":"Invalid Job ID"}
    return job        