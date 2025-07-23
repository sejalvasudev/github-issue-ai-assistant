from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.github_utils import fetch_issue_with_comments
from app.llm_utils import summarize_issue  # now returns structured JSON

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model
class IssueRequest(BaseModel):
    repo_url: str
    issue_number: int

@app.post("/analyze_issue")
async def analyze_issue(req: IssueRequest):
    try:
        issue = fetch_issue_with_comments(req.repo_url, req.issue_number)
        if issue:
            summary_struct = summarize_issue(issue["title"], issue["body"] + "\n\n" + issue["comments"])
            issue.update(summary_struct)  # adds summary, type, priority_score, etc.
            return {"issue": issue}
        else:
            raise HTTPException(status_code=404, detail="Issue not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
