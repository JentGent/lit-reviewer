from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from schemas import RewriteQueryRequest
from google import genai
from google.genai import types
from services.search_openalex import search_openalex
from services.read_paper import read_paper
import secrets
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(
    vertexai=True,
)

RUNS = {}

@app.get("/")
def root():
    return {"message": "Running"}

@app.post("/api/run")
async def get_references(body: RewriteQueryRequest):
    if not body.query or not body.query.strip():
        raise HTTPException(status_code=400, detail="No query")
    
    state = {
        "run_id": secrets.token_urlsafe(16),
        "query": body.query,
        "references": [],
    }
    RUNS[state["run_id"]] = state

    system_prompt = f"""
You are an autonomous agent acting as a literature review assistant. Your task is to find relevant scientific literature based on a given research problem, extract key direct quotes, and use those quotes to write a comprehensive literature review section.

Rules:
- Do not write from your own knowledge; only use the information you find.
- Do not hallucinate. Do not make anything up. Stick to the facts.
- Do not try to communicate with a user.

You have access to the following tools:
- {search_openalex.__name__}: Use this to search for relevant scientific literature based on a keyword search. Please filter for the following: is_retracted:false,is_oa:true,has_doi:true
- {read_paper.__name__}: Use this to attempt to read the text of a paper given its title. This is likely to fail, so please retry with a different paper in the search result (or try another search) if it does. Do not attempt to read the same paper twice. This is also likely to give extraneous text (e.g., HTML code). Look for the paper's abstract and results.
"""
    
    def stream():
        try:
            stream = client.models.generate_content_stream(
                model="gemini-2.5-flash-lite",
                contents="Research problem: " + body.query,
                config=types.GenerateContentConfig(
                    tools=[search_openalex, read_paper],
                    system_instruction=system_prompt,
                )
            )

            for chunk in stream:
                if chunk.text:
                    data = json.dumps({"type": "chunk", "text": chunk.text})
                    yield f"data: {data}\n\n"
            
            data = json.dumps({"type": "end"})
            yield f"data: {data}\n\n"
        except Exception as e:
            data = json.dumps({"type": "error", "message": str(e)})
            yield f"data: {data}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
