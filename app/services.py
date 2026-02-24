from sqlalchemy.orm import Session
from .models import Task, Comment, Activity
from .schemas import TaskCreate, TaskUpdate, CommentCreate


VALID_STATUSES = {"TODO", "DOING", "DONE"}
VALID_PRIORITIES = {"LOW", "MEDIUM", "HIGH"}


def log(db: Session, task_id: int, event_type: str, message: str) -> None:
    db.add(Activity(task_id=task_id, event_type=event_type, message=message))


def create_task(db: Session, data: TaskCreate) -> Task:
    priority = data.priority.upper()
    if priority not in VALID_PRIORITIES:
        priority = "MEDIUM"

    task = Task(
        title=data.title.strip(),
        description=(data.description or "").strip(),
        priority=priority,
        due_date=data.due_date,
        status="TODO",
    )
    db.add(task)
    db.flush()  # żeby mieć task.id
    log(db, task.id, "CREATED", f"Utworzono zadanie: {task.title}")
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task: Task, data: TaskUpdate) -> Task:
    changed = []
    if data.title is not None:
        task.title = data.title.strip()
        changed.append("title")
    if data.description is not None:
        task.description = data.description.strip()
        changed.append("description")
    if data.priority is not None:
        pr = data.priority.upper()
        if pr in VALID_PRIORITIES:
            task.priority = pr
            changed.append("priority")
    if data.due_date is not None or data.due_date is None:
        # pozwala wyczyścić termin
        task.due_date = data.due_date
        changed.append("due_date")
    if data.status is not None:
        st = data.status.upper()
        if st in VALID_STATUSES and st != task.status:
            old = task.status
            task.status = st
            log(db, task.id, "STATUS_CHANGED", f"Status: {old} → {st}")
            changed.append("status")

    if changed:
        log(db, task.id, "UPDATED", f"Zmieniono pola: {', '.join(changed)}")

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    log(db, task.id, "DELETED", f"Usunięto zadanie: {task.title}")
    db.delete(task)
    db.commit()


def add_comment(db: Session, task: Task, data: CommentCreate) -> Comment:
    c = Comment(task_id=task.id, author=data.author.strip() or "Student", content=data.content.strip())
    db.add(c)
    log(db, task.id, "COMMENT", f"Komentarz od: {c.author}")
    db.commit()
    db.refresh(c)
    return c