from fastapi import APIRouter, Depends, status
from sqlalchemy import Connection

from app.db.session import get_conn
from app.schemas.tool import ToolCreate, ToolOut, ToolUpdate
from app.services import tool_service

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("", response_model=list[ToolOut])
def list_tools(conn: Connection = Depends(get_conn)):
    return tool_service.list_tools(conn)


@router.get("/{tool_id}", response_model=ToolOut)
def get_tool(tool_id: int, conn: Connection = Depends(get_conn)):
    return tool_service.get_tool(conn, tool_id)


@router.post("", response_model=ToolOut, status_code=status.HTTP_201_CREATED)
def create_tool(payload: ToolCreate, conn: Connection = Depends(get_conn)):
    return tool_service.create_tool(conn, payload)


@router.patch("/{tool_id}", response_model=ToolOut)
def update_tool(tool_id: int, payload: ToolUpdate, conn: Connection = Depends(get_conn)):
    return tool_service.update_tool(conn, tool_id, payload)


@router.delete("/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tool(tool_id: int, conn: Connection = Depends(get_conn)):
    tool_service.delete_tool(conn, tool_id)
