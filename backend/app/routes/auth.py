from fastapi import APIRouter, HTTPException, status
from backend.app.database import get_db_connection
from backend.app.models import LoginRequest, UserResponse

router = APIRouter()


@router.post("/login", response_model=UserResponse)
def login(credentials: LoginRequest):

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT
                u.id,
                u.user_id,
                u.name,
                u.email,
                u.password_hash,
                u.role,
                u.designation,
                u.department_id,
                u.is_active,
                d.name AS department_name
            FROM users u
            LEFT JOIN departments d
                ON u.department_id = d.id
            WHERE u.user_id = ?
        """

        user = cursor.execute(
            query,
            (credentials.user_id,)
        ).fetchone()

        conn.close()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid User ID or Password"
            )

        if not user["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated. Contact Central Administration."
            )

        if user["password_hash"] != credentials.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid User ID or Password"
            )

        return {
            "id": user["id"],
            "user_id": user["user_id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "designation": user["designation"],
            "department_id": user["department_id"],
            "department_name": user["department_name"]
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Login backend error: {type(e).__name__}: {str(e)}"
        )