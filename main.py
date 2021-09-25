import uvicorn
from fastapi import FastAPI
from controller import endpoints

app = FastAPI()


@app.get("/")
def read_root():
    return {"Welcome to dictionary"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="localhost", reload=True)
