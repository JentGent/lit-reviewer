from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

@app.get("/")
def root():
    return {"message": "Running"}

@app.post("/get-references")
async def get_references(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    contents = await file.read()
    
    if not contents.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="Invalid PDF file")

    return {"message": "References"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
