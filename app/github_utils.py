# app/github_utils.py (or app/issue_fetcher.py if you prefer)

import requests

def fetch_issue_with_comments(repo_url: str, issue_number: int):
    try:
        # Parse repo path
        parts = repo_url.strip("/").split("/")
        owner, repo = parts[-2], parts[-1]
    except Exception:
        raise ValueError("Invalid GitHub repo URL")

    issue_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    comments_url = f"{issue_url}/comments"
    headers = {"Accept": "application/vnd.github.v3+json"}

    issue_resp = requests.get(issue_url, headers=headers)
    comments_resp = requests.get(comments_url, headers=headers)

    if issue_resp.status_code != 200:
        raise Exception(f"Failed to fetch issue #{issue_number}. GitHub returned: {issue_resp.status_code}")

    issue_data = issue_resp.json()
    comments_data = comments_resp.json() if comments_resp.status_code == 200 else []

    # Combine all comment bodies into one string
    comments_text = "\n".join(c["body"] for c in comments_data if "body" in c)

    return {
        "title": issue_data.get("title", ""),
        "body": issue_data.get("body", ""),
        "comments": comments_text,
        "html_url": issue_data.get("html_url", "")
    }
