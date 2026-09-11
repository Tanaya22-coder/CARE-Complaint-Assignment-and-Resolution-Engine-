# Project CARE – Complaint Assignment and Resolution Engine

Project CARE is a full-stack, role-based grievance management system designed for educational institutions. It replaces slow and difficult-to-track physical complaint registers with a centralized digital platform for complaint submission, assignment, progress tracking, feedback, and resolution monitoring.

The system provides separate workflows for **Students, Staff, and Administrators**, with SQLite-based data management and a FastAPI REST API.

---

## Key Technical Highlights

* **Architecture:** FastAPI REST API with a lightweight HTML5, CSS3, and JavaScript frontend.
* **Database:** SQLite with relational tables for users, departments, complaints, complaint logs, and feedback.
* **Test Data Generation:** Faker is used to generate realistic Indian-style test users and complaint data.
* **Role-Based Access Control:** Separate access levels for Students, Staff, and Administrators.
* **Complaint Tracking:** Each complaint receives a unique CARE ticket ID and maintains its current status.
* **Assignment Workflow:** Complaints can be assigned or reassigned to appropriate staff members.
* **Resolution Verification:** Students can provide feedback after the resolution process and reopen complaints when they are not satisfied.
* **Audit Trail:** Complaint status changes are recorded in the complaint logs table.
* **Analytics:** Administrative endpoints provide complaint status and department performance metrics.

---

## Tech Stack

### Backend

* Python
* FastAPI
* Pydantic
* SQLite3
* Uvicorn

### Frontend

* HTML5
* CSS3
* JavaScript
* Fetch API

### Data Generation

* Faker

### Development Tools

* Visual Studio Code
* Git
* GitHub

---

## System Architecture

```text
Project CARE
│
├── Frontend
│   ├── HTML
│   ├── CSS
│   └── JavaScript
│
├── Backend
│   ├── FastAPI
│   ├── Authentication
│   ├── Complaint Management
│   └── Administrative Operations
│
├── Database
│   ├── SQLite
│   ├── Users
│   ├── Departments
│   ├── Complaints
│   ├── Complaint Logs
│   └── Feedback
│
└── Analysis
    └── Complaint and department metrics
```

---

## User Roles

| Role        | Main Features                                                                                                               |
| ----------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Student** | Login, submit complaints, view complaint history, track complaint status, and submit resolution feedback.                   |
| **Staff**   | View department complaints, work on assigned complaints, update complaint progress, and add resolution notes.               |
| **Admin**   | Monitor complaints across departments, assign/reassign staff, manage complaint progress, and view administrative analytics. |

---

## Complaint Lifecycle

```text
Student Submits Complaint
          ↓
      OPEN
          ↓
     ASSIGNED
          ↓
    IN_PROGRESS
          ↓
 PENDING_FEEDBACK
          ↓
   Student Feedback
       ↙       ↘
Satisfied       Not Satisfied
   ↓                 ↓
RESOLVED          REOPENED
```

This workflow helps maintain a closed-loop complaint resolution process instead of allowing a complaint to be considered successfully resolved without student feedback.

---

## Database

Project CARE uses SQLite for lightweight relational data storage.

The database contains five primary tables:

1. `users`
2. `departments`
3. `complaints`
4. `complaint_logs`
5. `feedbacks`

The database schema is stored in:

```text
database/schema.sql
```

Test data can be generated using:

```text
database/seed.py
```

The generated SQLite database is:

```text
database/care.db
```

The database file is excluded from Git using `.gitignore`.

---

## Project Structure

```text
Project Care/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   └── app/
│       ├── __init__.py
│       ├── database.py
│       ├── models.py
│       └── routes/
│           ├── __init__.py
│           ├── auth.py
│           ├── complaints.py
│           └── admin.py
│
├── frontend/
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   └── templates/
│       ├── login.html
│       └── student_dashboard.html
│
├── database/
│   ├── care.db
│   ├── schema.sql
│   └── seed.py
│
├── analysis/
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Getting Started

### 1. Clone the Repository

After creating the GitHub repository:

```bash
git clone <your-repository-url>
cd Project-Care
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

#### Windows Command Prompt

```cmd
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Database Initialization

Create the SQLite database and generate test data:

```bash
python database/seed.py
```

Expected output:

```text
Database initialized successfully.
Database successfully seeded with Indian test data!
```

---

## Running the Backend

Start the FastAPI server from the project root:

```bash
uvicorn backend.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

### API Documentation

FastAPI automatically provides Swagger UI:

```text
http://127.0.0.1:8000/docs
```

The API can be tested directly through Swagger UI.

---

## API Modules

### Authentication

```text
POST /api/auth/login
```

Used for Student, Staff, and Admin authentication.

### Complaints

```text
POST /api/complaints/create
GET  /api/complaints/student/{student_id}
POST /api/complaints/{complaint_id}/feedback
```

### Administration

```text
GET /api/admin/staff/department/{dept_id}

PUT /api/admin/complaints/{complaint_id}/progress

PUT /api/admin/complaints/{complaint_id}/reassign

GET /api/admin/analytics/metrics
```

---

## Default Test Credentials

These credentials are generated by the development seed script.

| Role    | User ID        | Password   |
| ------- | -------------- | ---------- |
| Student | `STU-2026-001` | `pass123`  |
| Staff   | `STF-101`      | `pass123`  |
| Staff   | `STF-102`      | `pass123`  |
| Admin   | `ADM-01`       | `admin123` |

> **Note:** These are development/demo credentials only. Production deployment should use securely hashed passwords and environment-based secrets.

---

## Current Development Status

### Database Layer

**Completed**

* SQLite database configured.
* Five relational tables implemented.
* Foreign-key relationships configured.
* Faker-based test data generation implemented.
* Departments, students, staff, admin, and complaints seeded.

### Backend REST API

**Implemented**

* FastAPI application configured.
* CORS configured for frontend integration.
* Authentication endpoint implemented.
* Student complaint submission implemented.
* Student complaint history implemented.
* Complaint feedback and reopening workflow implemented.
* Staff complaint progress endpoint implemented.
* Admin reassignment endpoint implemented.
* Administrative analytics endpoint implemented.

### Frontend

**In Development**

* Login interface implemented.
* Student dashboard structure implemented.
* Additional Staff and Admin interfaces can be expanded and tested as part of the final UI phase.

### Documentation & Delivery

**In Progress**

* `README.md`
* `requirements.txt`
* `.gitignore`
* Database schema
* Seed data
* API documentation through FastAPI Swagger

---

## Future Enhancements

* Secure password hashing using bcrypt/Argon2.
* JWT-based authentication.
* Complete Staff and Admin dashboard interfaces.
* Visual complaint timeline and roadmap.
* Advanced department analytics and charts.
* Email notifications for complaint status changes.
* Production database migration to PostgreSQL/MySQL.
* Deployment to a cloud platform.

---

## Purpose

Project CARE demonstrates the practical application of:

* REST API development
* Database management
* Role-based access control
* Complaint workflow automation
* CRUD operations
* API integration
* Data generation
* Software testing
* Git and GitHub project management

It is designed as an academic and portfolio project demonstrating full-stack software development concepts.
