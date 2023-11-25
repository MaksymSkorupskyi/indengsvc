from fastapi import HTTPException

from app.dao.database import get_relativity_db_session

BASIC_QUERY = """
        SELECT 
          employees.id,
          COALESCE(employees.email, users.email)    AS email,
          users.phone,
          users.full_name,
          users.first_name,
          users.last_name,
          users.gender,
          users.birth,
          employees.reports,
          employees.position,
          employees.hired,
          employees.salary,
          teams.team_name    AS team

        FROM 
          employees 

        LEFT JOIN 
          users
        USING
          (id)

        LEFT JOIN 
          teams
        ON
          employees.team_id = teams.id
        """


def get_users():
    with get_relativity_db_session() as session:
        users = session.execute(BASIC_QUERY).all()

    return users


def get_user(user_id: str):
    with get_relativity_db_session() as session:
        query = f"""
        {BASIC_QUERY}
        WHERE 
          employees.id = {user_id}
        """
        user = session.execute(query).one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id!r} not found!")

    return user
