from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from schemas import RewriteQueryRequest
from google import genai
from google.genai import types
from services.search_openalex import search_openalex
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

@app.get("/")
def root():
    return {"message": "Running"}

@app.post("/api/rewrite-query")
async def get_references(body: RewriteQueryRequest):
    system_prompt = f"""
You are an autonomous agent acting as a literature review assistant. Your task is to find relevant scientific literature based on a given research problem, extract key direct quotes, and use those quotes to write a comprehensive literature review section.

Do not write anything from your own perspective; just use the information you find.
Do not halluciate. Do not make anything up. Stick to the facts.
Do not try to communicate with a user.
"""
    
    def stream():
        try:
            stream = client.models.generate_content_stream(
                model="gemini-2.5-flash-lite",
                contents="Research problem: " + body.query,
                config=types.GenerateContentConfig(
                    tools=[search_openalex],
                    system_instruction=system_prompt,
                )
            )

            for chunk in stream:
                print(chunk)
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
