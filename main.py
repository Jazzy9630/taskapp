"""
TaskFlow - a small task management web app.
Author: Jahanzaib Muhammad
Contact: Jahanzebsiyal4@gmail.com
"""
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import models
import schemas

# Resolve paths relative to this file, not the process's working directory —
# Vercel's serverless runtime doesn't guarantee cwd == project root.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = FastAPI(
    title="TaskFlow API",
    description="A simple to-do list API built by Jahanzaib Muhammad",
    version="1.0.0",
)

# create the SQLite tables on startup
models.init_db()

# serve the css/js assets
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def serve_homepage():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/health")
def health_check():
    """Simple deployment health check."""
    return {"status": "ok"}


@app.get("/api/todos", response_model=list[schemas.TodoOut])
def list_todos(db: Session = Depends(models.get_session)):
    """Return every to-do item, most recently created first."""
    return db.query(models.TodoItem).order_by(models.TodoItem.id.desc()).all()


@app.post("/api/todos", response_model=schemas.TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(payload: schemas.TodoCreatePayload, db: Session = Depends(models.get_session)):
    """Create a new to-do item."""
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=422, detail="Title cannot be blank")

    item = models.TodoItem(title=title, notes=(payload.notes or "").strip())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.patch("/api/todos/{item_id}", response_model=schemas.TodoOut)
def update_todo(item_id: int, payload: schemas.TodoUpdatePayload, db: Session = Depends(models.get_session)):
    """Partially update a to-do item (title, notes, and/or done status)."""
    item = db.query(models.TodoItem).filter(models.TodoItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="That task doesn't exist")

    changes = payload.model_dump(exclude_unset=True)
    if "title" in changes:
        changes["title"] = changes["title"].strip()
        if not changes["title"]:
            raise HTTPException(status_code=422, detail="Title cannot be blank")
    if "notes" in changes and changes["notes"] is not None:
        changes["notes"] = changes["notes"].strip()
    for field, value in changes.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@app.delete("/api/todos/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(item_id: int, db: Session = Depends(models.get_session)):
    """Remove a to-do item permanently."""
    item = db.query(models.TodoItem).filter(models.TodoItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="That task doesn't exist")

    db.delete(item)
    db.commit()
    return None
