from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.app.routes import auth, complaints, admin


app = FastAPI(
    title="CARE - Complaint Assignment and Resolution Engine",
    description="Campus Management Engine for University Students & Staff",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Static Files
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="frontend/static"),
    name="static"
)


# --------------------------------------------------
# HTML Templates
# --------------------------------------------------

templates = Jinja2Templates(
    directory="frontend/templates"
)


# --------------------------------------------------
# API Routes
# --------------------------------------------------

app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Authentication"]
)

app.include_router(
    complaints.router,
    prefix="/api/complaints",
    tags=["Complaints"]
)

app.include_router(
    admin.router,
    prefix="/api/admin",
    tags=["Admin & Onboarding"]
)


# --------------------------------------------------
# Login Page
# --------------------------------------------------

@app.get("/")
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


# --------------------------------------------------
# Student Dashboard
# --------------------------------------------------

@app.get("/student_dashboard.html")
def student_dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="student_dashboard.html"
    )


# --------------------------------------------------
# Staff Workspace
# --------------------------------------------------

@app.get("/staff_workspace.html")
def staff_workspace(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="staff_workspace.html"
    )


# --------------------------------------------------
# Admin Dashboard
# --------------------------------------------------

@app.get("/admin_dashboard.html")
def admin_dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html"
    )