"""
Business logic for tools. For plain CRUD this is thin (mostly delegates to
the repo), but it's the right place to add rules later, e.g.:
  - can't set status back to 'available' if there's an open loan
  - can't delete a tool that has calibration history
Routers should never talk to the repo directly — always go through here.
"""

from fastapi import HTTPException, status
from sqlalchemy import Connection

from app.repositories import tool_repo
from app.schemas.tool import ToolCreate, ToolUpdate


def list_tools(conn: Connection) -> list[dict]:
    return tool_repo.list_all(conn)


def get_tool(conn: Connection, tool_id: int) -> dict:
    tool = tool_repo.get_by_id(conn, tool_id)
    if tool is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")
    return tool


def create_tool(conn: Connection, payload: ToolCreate) -> dict:
    return tool_repo.create(conn, payload.model_dump())


def update_tool(conn: Connection, tool_id: int, payload: ToolUpdate) -> dict:
    # exclude_unset so PATCH only touches fields the client actually sent
    data = payload.model_dump(exclude_unset=True)
    tool = tool_repo.update_fields(conn, tool_id, data)
    if tool is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")
    return tool


def delete_tool(conn: Connection, tool_id: int) -> None:
    deleted = tool_repo.delete_by_id(conn, tool_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")
