import uvicorn
from fastapi import FastAPI, HTTPException
from model.file_model import File

app = FastAPI()
COEF = 0.5
MIN_SIZE = 20


fake_files_db = [
    {"filename:": "file", "size": 40, "is_archived": True},
    {"filename:": "essay", "size": 30, "is_archived": False},
    {"filename:": "game", "size": 10000, "is_archived": False}
    ]


@app.get("/")
def read_root():
    return {"Welcome to file archiver"}


@app.get("/files/{file_id}")
def read_file(file_id: int):
    if 0 <= file_id < 3:
        return fake_files_db[file_id]
    return {"file_id": file_id}


@app.post("/files/create/")
def post_item(file: File):
    if file.is_archived:
        raise HTTPException(status_code=400, detail="File is archived already")
    new_size = file.size * COEF
    if new_size >= MIN_SIZE:
        file.is_archived = True
        return {"filename": file.filename + ".zip", "file_size": new_size, "is_archived": file.is_archived}
    raise HTTPException(status_code=400, detail="File size is too low to compress")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="localhost", reload=True)
