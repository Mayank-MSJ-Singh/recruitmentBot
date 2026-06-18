import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

app = FastAPI(title="Recruitment Bot API", version="1.0.0")

# CORS for Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Fake DB
DB_PATH = os.path.join(os.path.dirname(__file__), "fake_db.json")
def get_fake_db():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f:
            return json.load(f)
    return {"employees": [], "finalists_not_selected": []}

class JDPrompt(BaseModel):
    prompt: str

class JDResponse(BaseModel):
    job_title: str
    location: str
    description: str
    requirements: list[str]

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Recruitment Bot API is running"}

@app.get("/api/database")
async def get_database():
    return get_fake_db()

@app.post("/api/generate_jd")
async def generate_jd(data: JDPrompt):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not found in .env")

    client = genai.Client(api_key=api_key)
    
    # Contextualize with Employees Database
    db = get_fake_db()
    employees_context = json.dumps(db.get("employees", []))

    system_instruction = f"""
    You are an expert AI Recruiter. You generate engaging, inclusive job descriptions based on a short prompt.
    Additionally, align the requirements with the success vectors of our existing top-performing employees: {employees_context}
    Return the output in structured JSON.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=f"Prompt: {data.prompt}\n\n{system_instruction}",
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
                response_schema=JDResponse,
                temperature=0.4
            )
        )
        
        # Parse the JSON response
        jd_data = json.loads(response.text)
        return jd_data
        
    except Exception as e:
        print(f"Error generating JD: {e}")
        raise HTTPException(status_code=500, detail=str(e))
