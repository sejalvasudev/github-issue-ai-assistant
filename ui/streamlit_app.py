import streamlit as st
import requests
import json

st.title("🔍 GitHub Issue Analyzer")

repo_url = st.text_input("Enter GitHub Repo URL", "https://github.com/tiangolo/fastapi")
issue_number = st.number_input("Enter Issue Number", min_value=1, step=1)

if st.button("Analyze Issue"):
    with st.spinner("Analyzing issue..."):
        response = requests.post(
            "http://127.0.0.1:8000/analyze_issue",
            json={"repo_url": repo_url, "issue_number": int(issue_number)}
        )

        if response.status_code == 200:
            issue = response.json().get("issue")
            if issue:
                st.subheader(issue["title"])
                st.write(issue["body"][:500] + "...")
                st.markdown("### 🧠 LLM Summary")
                st.success(issue["summary"])

                st.markdown("### 📌 Metadata")
                st.markdown(f"- **Type**: `{issue['type']}`")
                st.markdown(f"- **Priority Score**: `{issue['priority_score']}`")
                st.markdown(f"- **Labels**: {', '.join(issue['suggested_labels'])}")
                st.markdown(f"- **Impact**: {issue['potential_impact']}")
                st.markdown(f"[🔗 View on GitHub]({issue['html_url']})", unsafe_allow_html=True)

                # Copyable JSON output
                st.markdown("### 📋 JSON Output")
                json_output = {
                    "summary": issue["summary"],
                    "type": issue["type"],
                    "priority_score": issue["priority_score"],
                    "suggested_labels": issue["suggested_labels"],
                    "potential_impact": issue["potential_impact"]
                }
                st.code(json.dumps(json_output, indent=2), language='json')
                st.button("📎 Copy JSON", on_click=st.toast, args=("Copied!",))
            else:
                st.warning("No issue found.")
        else:
            st.error("Failed to fetch or analyze issue.")
