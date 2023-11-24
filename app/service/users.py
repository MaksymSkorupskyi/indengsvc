from fastapi import HTTPException

from app.dao.database import get_relativity_db_session


def get_users():
    with get_relativity_db_session() as session:
        users = session.execute("SELECT * FROM employees").all()

    return users


def get_user(user_id: str):
    with get_relativity_db_session() as session:
        query = f"""
        SELECT 
          employees.id,
          employees.email,
--           employees.phone,
--           employees.full_name,
--           employees.first_name,
--           employees.last_name,
--           employees.gender,
--           employees.birth,
          employees.reports,
          employees.position,
          employees.hired,
          employees.salary,
          teams.team_name    AS team
        FROM 
          employees 
        JOIN 
          teams
        ON
          employees.team_id = teams.id
        WHERE 
          employees.id = {user_id}
        """
        user = session.execute(query).one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id!r} not found!")

    return user
