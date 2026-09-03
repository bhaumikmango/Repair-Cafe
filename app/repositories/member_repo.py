from sqlalchemy import Connection, delete, insert, select, update

from app.db.tables import members


def list_all(conn: Connection) -> list[dict]:
    result = conn.execute(select(members))
    return [row._mapping for row in result]


def get_by_id(conn: Connection, member_id: int) -> dict | None:
    result = conn.execute(select(members).where(members.c.member_id == member_id))
    row = result.first()
    return row._mapping if row else None


def create(conn: Connection, data: dict) -> dict:
    result = conn.execute(insert(members).values(**data).returning(*members.c))
    return result.first()._mapping


def update_fields(conn: Connection, member_id: int, data: dict) -> dict | None:
    if not data:
        return get_by_id(conn, member_id)
    result = conn.execute(
        update(members).where(members.c.member_id == member_id).values(**data).returning(*members.c)
    )
    row = result.first()
    return row._mapping if row else None


def delete_by_id(conn: Connection, member_id: int) -> bool:
    result = conn.execute(delete(members).where(members.c.member_id == member_id))
    return result.rowcount > 0
