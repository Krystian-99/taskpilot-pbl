from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date

from .db import Base, engine, get_db
from .models import Task
from .schemas import TaskCreate, TaskUpdate, CommentCreate
from .services import create_task, update_task, delete_task, add_comment

app = FastAPI(title="TaskPilot PBL", version="1.0.0")

Base.metadata.create_all(bind=engine)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # folder app/

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def get_task_or_404(db: Session, task_id: int) -> Task:
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/", response_class=HTMLResponse)
def index(request: Request, status: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Task)
    if status:
        q = q.filter(Task.status == status.upper())
    tasks = q.order_by(Task.created_at.desc()).all()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "tasks": tasks,
            "status_filter": (status or "").upper(),
        },
    )


@app.post("/tasks")
def create_task_form(
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("MEDIUM"),
    due_date_str: str = Form(""),
    db: Session = Depends(get_db),
):
    due = None
    if due_date_str.strip():
        due = date.fromisoformat(due_date_str.strip())

    create_task(db, TaskCreate(title=title, description=description, priority=priority, due_date=due))
    return RedirectResponse(url="/", status_code=303)


@app.get("/tasks/{task_id}", response_class=HTMLResponse)
def task_detail(task_id: int, request: Request, db: Session = Depends(get_db)):
    task = get_task_or_404(db, task_id)
    # odśwież relacje
    task.comments.sort(key=lambda c: c.created_at, reverse=True)
    task.activities.sort(key=lambda a: a.created_at, reverse=True)
    return templates.TemplateResponse("task_detail.html", {"request": request, "task": task})


@app.post("/tasks/{task_id}/update")
def update_task_form(
    task_id: int,
    title: str = Form(""),
    description: str = Form(""),
    priority: str = Form("MEDIUM"),
    due_date_str: str = Form(""),
    status: str = Form("TODO"),
    db: Session = Depends(get_db),
):
    task = get_task_or_404(db, task_id)

    due = None
    if due_date_str.strip():
        due = date.fromisoformat(due_date_str.strip())

    update_task(
        db,
        task,
        TaskUpdate(
            title=title,
            description=description,
            priority=priority,
            due_date=due,
            status=status,
        ),
    )
    return RedirectResponse(url=f"/tasks/{task_id}", status_code=303)


@app.post("/tasks/{task_id}/delete")
def delete_task_form(task_id: int, db: Session = Depends(get_db)):
    task = get_task_or_404(db, task_id)
    delete_task(db, task)
    return RedirectResponse(url="/", status_code=303)


@app.post("/tasks/{task_id}/comments")
def add_comment_form(
    task_id: int,
    author: str = Form("Student"),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    task = get_task_or_404(db, task_id)
    add_comment(db, task, CommentCreate(author=author, content=content))
    return RedirectResponse(url=f"/tasks/{task_id}", status_code=303)