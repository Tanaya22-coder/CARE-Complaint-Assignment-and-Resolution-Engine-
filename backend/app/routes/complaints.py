from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from backend.app.database import get_db_connection

router = APIRouter()

class ComplaintCreate(BaseModel):
    student_id: int
    category: str
    sub_category: str
    priority: str
    location: str
    title: str
    description: str

class FeedbackSubmit(BaseModel):
    student_id: int
    rating: int = Field(..., ge=1, le=5, description="CSAT rating must be between 1 and 5")
    comments: Optional[str] = None
    is_satisfied: bool

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_complaint(complaint: ComplaintCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    dept = cursor.execute(
        "SELECT id FROM departments WHERE name = ?", (complaint.category,)
    ).fetchone()
    
    if not dept:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Invalid category/department: '{complaint.category}'")

    dept_id = dept["id"]

    count = cursor.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
    ticket_id = f"TCK-{2026000 + count + 1}"

    cursor.execute("""
        INSERT INTO complaints (ticket_id, student_id, department_id, sub_category, priority, location, title, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, complaint.student_id, dept_id, complaint.sub_category, 
          complaint.priority, complaint.location, complaint.title, complaint.description))

    conn.commit()
    conn.close()

    return {"message": "Complaint created successfully", "ticket_id": ticket_id}


@router.get("/student/{student_id}")
def get_student_complaints(student_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    student = cursor.execute("SELECT id FROM users WHERE id = ? AND role = 'STUDENT'", (student_id,)).fetchone()
    if not student:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")

    query = """
        SELECT c.*, d.name AS department_name
        FROM complaints c
        JOIN departments d ON c.department_id = d.id
        WHERE c.student_id = ?
        ORDER BY c.created_at DESC
    """
    rows = cursor.execute(query, (student_id,)).fetchall()
    conn.close()

    return [dict(row) for row in rows]


@router.post("/{complaint_id}/feedback")
def submit_feedback(complaint_id: int, feedback: FeedbackSubmit):
    conn = get_db_connection()
    cursor = conn.cursor()

    complaint = cursor.execute("SELECT * FROM complaints WHERE id = ?", (complaint_id,)).fetchone()
    if not complaint:
        conn.close()
        raise HTTPException(status_code=404, detail="Complaint not found")

    if complaint["student_id"] != feedback.student_id:
        conn.close()
        raise HTTPException(status_code=403, detail="Unauthorized: You can only give feedback on your own complaints")

    # Determine status transition based on True Resolution Gate
    new_status = "RESOLVED" if feedback.is_satisfied else "REOPENED"

    cursor.execute("""
        INSERT INTO feedbacks (complaint_id, rating, comments)
        VALUES (?, ?, ?)
    """, (complaint_id, feedback.rating, feedback.comments))

    cursor.execute("""
        UPDATE complaints 
        SET status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (new_status, complaint_id))

    cursor.execute("""
        INSERT INTO complaint_logs (complaint_id, updated_by, old_status, new_status, remarks)
        VALUES (?, ?, ?, ?, ?)
    """, (complaint_id, feedback.student_id, complaint["status"], new_status, 
          f"Student submitted feedback (Satisfied: {feedback.is_satisfied}, Rating: {feedback.rating}/5)"))

    conn.commit()
    conn.close()

    return {
        "message": "Feedback submitted successfully",
        "final_status": new_status
    }