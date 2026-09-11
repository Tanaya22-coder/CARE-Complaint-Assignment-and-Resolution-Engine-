import sqlite3
import random
import os
from datetime import datetime
from faker import Faker

# Initialize Faker with Indian Locale (English - India)
fake = Faker('en_IN')

DB_PATH = os.path.join(os.path.dirname(__file__), "care.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def init_db():
    """Reads schema.sql and creates all tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read())
        
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def seed_data():
    """Seeds departments, manual test users, Indian Faker users, and mock complaints."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Seed Departments
    departments = [
        ("Hostel & Maintenance", "FIELD"),
        ("Campus IT & Network", "FIELD"),
        ("Academic Affairs", "ADMIN"),
        ("Canteen & Dining", "FIELD"),
        ("Registrar & Enrollment", "ADMIN"),
        ("Finance & Fees", "ADMIN")
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO departments (name, dept_type) VALUES (?, ?)", 
        departments
    )
    conn.commit()

    # 2. Seed Manual Core Users (Indian Context for College Defense)
    manual_users = [
        ("STU-2026-001", "Rahul Sharma (Test Student)", "rahul@college.edu", "pass123", "STUDENT", "Student", None),
        ("STF-101", "Ramesh Kumar (Hostel Warden)", "warden@college.edu", "pass123", "STAFF", "Warden", 1),
        ("STF-102", "Anil Patil (IT Specialist)", "it@college.edu", "pass123", "STAFF", "Technician", 2),
        ("ADM-01", "Dr. Priya Verma (HOD / Admin)", "admin@college.edu", "admin123", "ADMIN", "HOD", 3)
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO users 
        (user_id, name, email, password_hash, role, designation, department_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, manual_users)

    # 3. Seed Bulk Indian Users using Faker ('en_IN')
    faker_users = []
    
    # Generate 15 Fake Indian Students
    for i in range(2, 17):
        stu_id = f"STU-2026-{i:03d}"
        faker_users.append((
            stu_id, 
            fake.name(), # Generates realistic Indian names (e.g., Aarav Patel, Ananya Iyer)
            fake.unique.email(), 
            "pass123", 
            "STUDENT", 
            "Student", 
            None
        ))
    
    # Generate 6 Fake Indian Staff Members
    designations = ["Peon", "Cleaning Staff", "Assistant Cook", "Network Admin", "Electrician"]
    for i in range(103, 109):
        stf_id = f"STF-{i}"
        dept_id = random.randint(1, 6)
        faker_users.append((
            stf_id, 
            fake.name(), 
            fake.unique.email(), 
            "pass123", 
            "STAFF", 
            random.choice(designations), 
            dept_id
        ))

    cursor.executemany("""
        INSERT OR IGNORE INTO users 
        (user_id, name, email, password_hash, role, designation, department_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, faker_users)
    conn.commit()

    # 4. Fetch Student IDs for Complaint Seeding
    cursor.execute("SELECT id FROM users WHERE role = 'STUDENT'")
    student_ids = [row[0] for row in cursor.fetchall()]

    categories = [
        ("Hostel & Maintenance", ["Water Supply Issue", "Fan/Geyser Repair", "Washroom Cleanliness"], 1),
        ("Campus IT & Network", ["Campus Wi-Fi Down", "ERP Portal Login Error", "Lab Computer Glitch"], 2),
        ("Academic Affairs", ["Lecture Notes Missing", "Attendance Discrepancy", "Exam Timetable Overlap"], 3),
        ("Canteen & Dining", ["Food Hygiene Issue", "UPI Payment Failed", "Mess Rebate Dispute"], 4)
    ]
    
    priorities = ["LOW", "MEDIUM", "HIGH", "URGENT"]
    statuses = ["OPEN", "IN_PROGRESS", "PENDING_FEEDBACK", "RESOLVED"]

    # 5. Seed Bulk Complaints with Indian Campus Context
    complaints = []
    hostel_blocks = ["A-Block", "B-Block (Boys Hostel)", "C-Block (Girls Hostel)", "Mess Hall"]

    for i in range(1, 35):
        ticket_id = f"CARE-2026-{i:04d}"
        stu_id = random.choice(student_ids)
        cat_name, sub_cats, dept_id = random.choice(categories)
        sub_cat = random.choice(sub_cats)
        priority = random.choice(priorities)
        status = random.choice(statuses)
        title = f"{sub_cat}: {fake.sentence(nb_words=4)}"
        desc = fake.paragraph(nb_sentences=3)
        loc = f"{random.choice(hostel_blocks)}, Room {random.randint(101, 405)}"
        
        complaints.append((
            ticket_id, stu_id, dept_id, cat_name, sub_cat, priority, status, title, desc, loc
        ))

    cursor.executemany("""
        INSERT OR IGNORE INTO complaints 
        (ticket_id, student_id, department_id, category, sub_category, priority, status, title, description, location) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, complaints)

    conn.commit()
    conn.close()
    print("Database successfully seeded with Indian test data!")

if __name__ == "__main__":
    init_db()
    seed_data()