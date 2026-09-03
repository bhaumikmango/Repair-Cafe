from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr


class MemberCreate(BaseModel):
    """Payload for POST /members"""

    full_name: str
    email: EmailStr
    phone: str | None = None
    joined_date: date


class MemberUpdate(BaseModel):
    """Payload for PATCH /members/{member_id} — all fields optional."""

    full_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    joined_date: date | None = None


class MemberOut(BaseModel):
    member_id: int
    full_name: str
    email: str
    phone: str | None
    joined_date: date

    model_config = ConfigDict(from_attributes=True)
