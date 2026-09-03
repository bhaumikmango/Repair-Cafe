from fastapi import HTTPException, status
from sqlalchemy import Connection

from app.repositories import member_repo
from app.schemas.member import MemberCreate, MemberUpdate


def list_members(conn: Connection) -> list[dict]:
    return member_repo.list_all(conn)


def get_member(conn: Connection, member_id: int) -> dict:
    member = member_repo.get_by_id(conn, member_id)
    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    return member


def create_member(conn: Connection, payload: MemberCreate) -> dict:
    return member_repo.create(conn, payload.model_dump())


def update_member(conn: Connection, member_id: int, payload: MemberUpdate) -> dict:
    data = payload.model_dump(exclude_unset=True)
    member = member_repo.update_fields(conn, member_id, data)
    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    return member


def delete_member(conn: Connection, member_id: int) -> None:
    deleted = member_repo.delete_by_id(conn, member_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
