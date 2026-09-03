"""
All SQL touching the `tools` table lives here. Routers and services never
import sqlalchemy.select/insert directly — they call these functions.

Every function takes `conn: Connection` as its first arg (supplied by the
caller, which got it from the `get_conn` FastAPI dependency). This repo
does NOT commit/rollback — that's handled once per-request in db/session.py.
"""

from sqlalchemy import Connection, delete, insert, select, update

from app.db.tables import tools


def list_all(conn: Connection) -> list[dict]:
    result = conn.execute(select(tools))
    return [row._mapping for row in result]


def get_by_id(conn: Connection, tool_id: int) -> dict | None:
    result = conn.execute(select(tools).where(tools.c.tool_id == tool_id))
    row = result.first()
    return row._mapping if row else None


def create(conn: Connection, data: dict) -> dict:
    result = conn.execute(insert(tools).values(**data).returning(*tools.c))
    return result.first()._mapping


def update_fields(conn: Connection, tool_id: int, data: dict) -> dict | None:
    if not data:
        return get_by_id(conn, tool_id)
    result = conn.execute(
        update(tools).where(tools.c.tool_id == tool_id).values(**data).returning(*tools.c)
    )
    row = result.first()
    return row._mapping if row else None


def delete_by_id(conn: Connection, tool_id: int) -> bool:
    result = conn.execute(delete(tools).where(tools.c.tool_id == tool_id))
    return result.rowcount > 0
