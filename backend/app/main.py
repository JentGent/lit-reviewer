from fastapi import FastAPI
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
def get_references():
    return {"message": "References"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
