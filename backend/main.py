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

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve CSS and other static files
app.mount(
    "/static",
    StaticFiles(directory="frontend/static"),
    name="static"
)

# Load HTML templates
templates = Jinja2Templates(directory="frontend/templates")


# API routes
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


# Frontend
@app.get("/")
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )