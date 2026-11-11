from fastapi import FastAPI
from dotenv import load_dotenv
import os
import requests

load_dotenv()

application = FastAPI(title=os.getenv("APP_NAME"))

@application.get("/health")
def healthstatus():
    return{
        "Status" : "Okay",
        "environment" : os.getenv("ENV")
        }
@application.get("/gitlab/status")
def gitlabstatus():
    header = {

        "PRIVATE_TOKEN" : os.getenv("GITLAB_TOKEN")

    }

    response = requests.get(

        f"{os.getenv('GITLAB_URL')}/api/v4/projects", headers=header

    )


    if (response.status_code != 200):

        return {"Error" : "Gitlab authentication failed !!!"}
    
    return{

        "Status" : "Connected",
        "Project_Count" : len(response.json())
    }

@application.get("/gitlab/pipeline/status")
def pipeline_status():

    project_id = os.getenv("GITLAB_PROJECT_ID").strip()

    header = {
        "Authorization": f"Bearer {os.getenv('GITLAB_TOKEN')}"
    }

    #header = {"PRIVATE_TOKEN" : os.getenv("GITLAB_TOKEN")}

    url = f"{os.getenv('GITLAB_URL')}/api/v4/projects/{project_id}/pipelines?per_page=2"

    response = requests.get (url, headers = header)

    if(response.status_code != 200):

        #return {"Error" : "Failed to fetch Pipelines !!!"}
        return{
            
            "status_code": response.status_code,
            "response_text": response.text
        }
    pipelines = response.json()

    if not pipelines:
        return {"status" : "No pipelines found !!!"}
    
    
    latest_pipeline = pipelines[0]

    return {

        "pipeline_id" : latest_pipeline["id"],
        "status" : latest_pipeline["status"],
        "ref" : latest_pipeline["ref"]
    }

@application.get("/release/decision")
def release_decision():

    project_id = os.getenv("GITLAB_PROJECT_ID").strip()

    header = { "Authorization" : f"Bearer {os.getenv('GITLAB_TOKEN')}"}

    url = f"{os.getenv('GITLAB_URL')}/api/v4/projects/{project_id}/pipelines?per_page=2"

    response = requests.get (url,headers = header)

    if(response.status_code != 200):
        #return{"Error" : "Failed to fetch pipelines !!!"}
    
        return{
            
            "status_code": response.status_code,
            "response_text": response.text
        }
    
    pipelines = response.json()

    latest_pipeline = pipelines[1]
    status = latest_pipeline["status"]

    if(status == "success"):
        decision = "allow"
        reason = "latest pipeline completed successfully"
    elif(status == "running"):
        decision = "wait"
        reason = "latest pipeline is still running"

    else:
        decision = "block"
        reason = f"Pipeline status is {status}"

    prompt = f"""
    You are a DevOps release advisor.

    Pipeline status: {status}
    Decision: {decision}
    Reason: {reason}

    Explain this decision in simple, clear terms.
    """

    ai_explanation = ask_llama(prompt)

    return {
        "decision": decision,
        "pipeline_status": pipeline_status,
        "pipeline_id": latest_pipeline["id"],
        "ai_explanation": ai_explanation
    }

    return {
        "decision": decision,
        "pipeline_status": status,
        "pipeline_id": latest_pipeline["id"],
        "reason": reason
    }

def ask_llama(prompt:str) -> str: #Indicating the parameter inside calling should be string and return type of function should be string

    url = "http://127.0.0.1:11434/api/generate"

    payload = {

        "model" : "llama3",
        "prompt" : prompt,
        "stream" : False

    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"AI explanation unavailable: {str(e)}"
