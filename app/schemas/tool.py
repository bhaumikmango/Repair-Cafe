from enum import Enum

from pydantic import BaseModel, ConfigDict


class ToolStatus(str, Enum):
    available = "available"
    checked_out = "checked_out"
    in_repair = "in_repair"
    retired = "retired"


class ToolCreate(BaseModel):
    """Payload for POST /tools"""

    name: str
    category_id: int | None = None
    shelf_location: str
    calibration_interval_days: int
    status: ToolStatus = ToolStatus.available


class ToolUpdate(BaseModel):
    """Payload for PATCH /tools/{tool_id} — all fields optional."""

    name: str | None = None
    category_id: int | None = None
    shelf_location: str | None = None
    calibration_interval_days: int | None = None
    status: ToolStatus | None = None


class ToolOut(BaseModel):
    """What we return to clients."""

    tool_id: int
    name: str
    category_id: int | None
    status: ToolStatus
    shelf_location: str
    calibration_interval_days: int

    # Lets Pydantic build this straight from a SQLAlchemy Row / RowMapping
    model_config = ConfigDict(from_attributes=True)
