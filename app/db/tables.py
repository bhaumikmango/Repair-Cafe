"""
SQLAlchemy Core table definitions mirroring create.sql 1:1.

These are NOT an ORM — no relationships, no sessions, no model instances.
They exist so repositories can write `select(tools).where(...)` with
autocomplete/typo-safety instead of raw f-strings, while still giving you
full control over joins and SQL shape (same spirit as practice.sql).

If you'd rather write pure `text("SELECT ...")` everywhere, that's fine too —
these Table objects are optional scaffolding, not a requirement.

NOTE: This file does NOT create the schema. Run create.sql directly against
your Postgres DB (psql -f create.sql) or wire it into an Alembic migration.
This metadata just needs to match what's actually in the DB.
"""

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    Text,
)

metadata = MetaData()

tool_status = Enum(
    "available", "checked_out", "in_repair", "retired",
    name="tool_status", metadata=metadata,
)
calibration_result = Enum("pass", "fail", name="calibration_result", metadata=metadata)
ticket_status = Enum(
    "intake", "diagnosing", "in_progress", "awaiting_parts", "completed",
    name="ticket_status", metadata=metadata,
)

categories = Table(
    "categories",
    metadata,
    Column("category_id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("carbon_multiplier", Numeric(6, 3), nullable=False),
)

members = Table(
    "members",
    metadata,
    Column("member_id", Integer, primary_key=True),
    Column("full_name", String(150), nullable=False),
    Column("email", String(255), nullable=False),
    Column("phone", String(30)),
    Column("joined_date", Date, nullable=False),
)

volunteers = Table(
    "volunteers",
    metadata,
    Column("volunteer_id", Integer, primary_key=True),
    Column("full_name", String(150), nullable=False),
    Column("email", String(255), nullable=False),
    Column("is_active", Boolean, nullable=False, default=True),
    Column("on_shift", Boolean, nullable=False, default=False),
)

volunteer_specialties = Table(
    "volunteer_specialties",
    metadata,
    Column("volunteer_id", Integer, ForeignKey("volunteers.volunteer_id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.category_id"), primary_key=True),
)

tools = Table(
    "tools",
    metadata,
    Column("tool_id", Integer, primary_key=True),
    Column("name", String(120), nullable=False),
    Column("category_id", Integer, ForeignKey("categories.category_id")),
    Column("status", tool_status, nullable=False, default="available"),
    Column("shelf_location", String(50), nullable=False),
    Column("calibration_interval_days", Integer, nullable=False),
)

calibration_logs = Table(
    "calibration_logs",
    metadata,
    Column("log_id", Integer, primary_key=True),
    Column("tool_id", Integer, ForeignKey("tools.tool_id"), nullable=False),
    Column("technician_id", Integer, ForeignKey("volunteers.volunteer_id"), nullable=False),
    Column("check_date", Date, nullable=False),
    Column("result", calibration_result, nullable=False),
    Column("notes", Text),
)

tool_loans = Table(
    "tool_loans",
    metadata,
    Column("loan_id", Integer, primary_key=True),
    Column("tool_id", Integer, ForeignKey("tools.tool_id"), nullable=False),
    Column("member_id", Integer, ForeignKey("members.member_id"), nullable=False),
    Column("checkout_date", Date, nullable=False),
    Column("due_date", Date, nullable=False),
    Column("return_date", Date),
)

repair_tickets = Table(
    "repair_tickets",
    metadata,
    Column("ticket_id", Integer, primary_key=True),
    Column("member_id", Integer, ForeignKey("members.member_id"), nullable=False),
    Column("category_id", Integer, ForeignKey("categories.category_id"), nullable=False),
    Column("assigned_volunteer_id", Integer, ForeignKey("volunteers.volunteer_id")),
    Column("item_name", String(150), nullable=False),
    Column("weight_kg", Numeric(8, 3), nullable=False),
    Column("status", ticket_status, nullable=False, default="intake"),
    Column("symptom_notes", Text),
    Column("created_at", DateTime, nullable=False),
    Column("completed_at", DateTime),
)

parts = Table(
    "parts",
    metadata,
    Column("part_id", Integer, primary_key=True),
    Column("name", String(120), nullable=False),
    Column("drawer_location", String(50), nullable=False),
    Column("stock_qty", Integer, nullable=False, default=0),
    Column("min_threshold", Integer, nullable=False),
)

ticket_parts_used = Table(
    "ticket_parts_used",
    metadata,
    Column("ticket_id", Integer, ForeignKey("repair_tickets.ticket_id"), primary_key=True),
    Column("part_id", Integer, ForeignKey("parts.part_id"), primary_key=True),
    Column("qty_used", Integer, nullable=False),
    Column("used_at", DateTime, nullable=False),
)
