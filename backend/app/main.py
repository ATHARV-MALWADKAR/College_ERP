from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import Form
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "app/templates"))

from app.core.config import settings
from app.api.v1.routes_auth import router as auth_router
from app.api.v1.routes_students import router as students_router
from app.api.v1.routes_faculty import router as faculty_router
from app.api.v1.routes_admin import router as admin_router
from app.api.v1.routes_attendance import router as attendance_router
from app.api.v1.routes_assignments import router as assignments_router
from app.api.v1.routes_results import router as results_router
from app.api.v1.routes_notices import router as notices_router
from app.api.v1.routes_timetable import router as timetable_router


app = FastAPI(
    title="College ERP API",
    version="0.1.0",
    description="Backend API for the College ERP system.",
)

# GLOBAL STORAGE
students_data = []

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok"}


api_prefix = "/api/v1"

app.include_router(auth_router, prefix=api_prefix, tags=["auth"])
app.include_router(students_router, prefix=api_prefix, tags=["students"])
app.include_router(faculty_router, prefix=api_prefix, tags=["faculty"])
app.include_router(admin_router, prefix=api_prefix, tags=["admin"])
app.include_router(attendance_router, prefix=api_prefix, tags=["attendance"])
app.include_router(assignments_router, prefix=api_prefix, tags=["assignments"])
app.include_router(results_router, prefix=api_prefix, tags=["results"])
app.include_router(notices_router, prefix=api_prefix, tags=["notices"])
app.include_router(timetable_router, prefix=api_prefix, tags=["timetable"])


# ------------------ Dashboard UI Route ------------------

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse(
        "admin_dashboard.html",
        {"request": request}
    )


@app.get("/faculty")
async def faculty_dashboard(request: Request):
    return templates.TemplateResponse(
        "faculty_dashboard.html",
        {"request": request}
    )


@app.get("/student")
async def student_dashboard(request: Request):
    return templates.TemplateResponse(
        "student_dashboard.html",
        {"request": request}
    )

    


@app.get("/students", response_class=HTMLResponse)
async def students_page(request: Request):

    return templates.TemplateResponse(
        "students.html",
        {
            "request": request,
            "students": students_data
        }
    )


@app.post("/students/add")
async def add_student(
    name: str = Form(...),
    email: str = Form(...),
    department: str = Form(...)
):

    students_data.append({
        "name": name,
        "email": email,
        "department": department
    })

    return {"message": "Student added"}

@app.get("/attendance", response_class=HTMLResponse)
async def attendance_page(request: Request):

    return templates.TemplateResponse(
        "attendance.html",
        {"request": request}
    )