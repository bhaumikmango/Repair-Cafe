from fastapi import APIRouter, Depends, status
from sqlalchemy import Connection

from app.db.session import get_conn
from app.schemas.member import MemberCreate, MemberOut, MemberUpdate
from app.services import member_service

router = APIRouter(prefix="/members", tags=["members"])


@router.get("", response_model=list[MemberOut])
def list_members(conn: Connection = Depends(get_conn)):
    return member_service.list_members(conn)


@router.get("/{member_id}", response_model=MemberOut)
def get_member(member_id: int, conn: Connection = Depends(get_conn)):
    return member_service.get_member(conn, member_id)


@router.post("", response_model=MemberOut, status_code=status.HTTP_201_CREATED)
def create_member(payload: MemberCreate, conn: Connection = Depends(get_conn)):
    return member_service.create_member(conn, payload)


@router.patch("/{member_id}", response_model=MemberOut)
def update_member(member_id: int, payload: MemberUpdate, conn: Connection = Depends(get_conn)):
    return member_service.update_member(conn, member_id, payload)


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, conn: Connection = Depends(get_conn)):
    member_service.delete_member(conn, member_id)
