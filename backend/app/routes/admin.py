from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from backend.app.database import get_db_connection

router = APIRouter()

class StaffUpdateStatus(BaseModel):
    staff_id: int
    status: str
    resolution_notes: str

class AdminReassign(BaseModel):
    admin_id: int
    new_staff_id: int

@router.get("/staff/department/{dept_id}")
def get_department_tickets(dept_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    dept = cursor.execute("SELECT id FROM departments WHERE id = ?", (dept_id,)).fetchone()
    if not dept:
        conn.close()
        raise HTTPException(status_code=404, detail="Department not found")

    query = """
        SELECT c.*, u.name AS student_name, s.name AS staff_name
        FROM complaints c
        JOIN users u ON c.student_id = u.id
        LEFT JOIN users s ON c.assigned_staff_id = s.id
        WHERE c.department_id = ?
        ORDER BY c.created_at DESC
    """
    rows = cursor.execute(query, (dept_id,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.put("/complaints/{complaint_id}/progress")
def staff_update_ticket(complaint_id: int, data: StaffUpdateStatus):
    # Enforce mandatory resolution notes for resolution stage
    if data.status == "PENDING_FEEDBACK" and not data.resolution_notes.strip():
        raise HTTPException(
            status_code=400, 
            detail="Resolution notes are mandatory when marking a ticket as resolved."
        )

    conn = get_db_connection()
    cursor = conn.cursor()

    complaint = cursor.execute("SELECT * FROM complaints WHERE id = ?", (complaint_id,)).fetchone()
    if not complaint:
        conn.close()
        raise HTTPException(status_code=404, detail="Complaint not found")

    old_status = complaint["status"]

    cursor.execute("""
        UPDATE complaints 
        SET status = ?, assigned_staff_id = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (data.status, data.staff_id, complaint_id))

    cursor.execute("""
        INSERT INTO complaint_logs (complaint_id, updated_by, old_status, new_status, remarks)
        VALUES (?, ?, ?, ?, ?)
    """, (complaint_id, data.staff_id, old_status, data.status, data.resolution_notes))

    conn.commit()
    conn.close()

    return {"message": "Ticket status updated successfully", "new_status": data.status}


@router.put("/complaints/{complaint_id}/reassign")
def admin_reassign_ticket(complaint_id: int, data: AdminReassign):
    conn = get_db_connection()
    cursor = conn.cursor()

    complaint = cursor.execute("SELECT * FROM complaints WHERE id = ?", (complaint_id,)).fetchone()
    if not complaint:
        conn.close()
        raise HTTPException(status_code=404, detail="Complaint not found")

    cursor.execute("""
        UPDATE complaints 
        SET assigned_staff_id = ?, status = 'ASSIGNED', updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (data.new_staff_id, complaint_id))

    cursor.execute("""
        INSERT INTO complaint_logs (complaint_id, updated_by, old_status, new_status, remarks)
        VALUES (?, ?, ?, 'ASSIGNED', 'Ticket manually reassigned by Admin')
    """, (complaint_id, data.admin_id, complaint["status"]))

    conn.commit()
    conn.close()

    return {"message": "Ticket successfully reassigned"}


@router.get("/analytics/metrics")
def get_admin_analytics():
    conn = get_db_connection()
    cursor = conn.cursor()

    status_counts = cursor.execute("""
        SELECT status, COUNT(*) as count FROM complaints GROUP BY status
    """).fetchall()

    dept_ratings = cursor.execute("""
        SELECT d.name AS department, AVG(f.rating) as avg_rating, COUNT(f.id) as total_feedbacks
        FROM departments d
        LEFT JOIN complaints c ON c.department_id = d.id
        LEFT JOIN feedbacks f ON f.complaint_id = c.id
        GROUP BY d.id
    """).fetchall()

    conn.close()

    return {
        "status_breakdown": {row["status"]: row["count"] for row in status_counts},
        "department_performance": [dict(row) for row in dept_ratings]
    }
# --- ADD THIS TO THE BOTTOM OF backend/app/routes/admin.py ---

class CreateUserRequest(BaseModel):
    user_id: str
    name: str
    email: str
    password: str
    role: str  # 'STUDENT', 'STAFF', or 'ADMIN'
    department_id: Optional[int] = None
    designation: Optional[str] = None


@router.post("/users/create", status_code=status.HTTP_201_CREATED)
def create_user_by_admin(data: CreateUserRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if user_id or email already exists
    existing = cursor.execute(
        "SELECT id FROM users WHERE user_id = ? OR email = ?", (data.user_id, data.email)
    ).fetchone()

    if existing:
        conn.close()
        raise HTTPException(status_code=400, detail="User ID or Email already registered.")

    cursor.execute("""
        INSERT INTO users (user_id, name, email, password, role, department_id, designation)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (data.user_id, data.name, data.email, data.password, data.role, data.department_id, data.designation))

    conn.commit()
    conn.close()

    return {"message": f"Successfully created {data.role} account: {data.name}"}