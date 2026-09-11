from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    user_id: str
    password: str


class UserResponse(BaseModel):
    id: int
    user_id: str
    name: str
    email: str
    role: str
    designation: Optional[str] = None
    department_id: Optional[int] = None
    department_name: Optional[str] = None


class ComplaintCreate(BaseModel):
    student_id: int
    category: str
    sub_category: str
    priority: str
    title: str
    description: str
    location: str


class FeedbackCreate(BaseModel):
    student_id: int
    rating: int
    comments: Optional[str] = None
    is_satisfied: bool


class StaffUpdateStatus(BaseModel):
    staff_id: int
    status: str
    resolution_notes: str


class AdminReassign(BaseModel):
    admin_id: int
    new_staff_id: int