"""
Seed script — wipes and repopulates all tables with small, deliberately-chosen
fake data so every /reports/* endpoint returns a non-empty, sensible result.

Run with:
    python -m app.db.seed

Safe to re-run: truncates all tables first (respecting FK order).
"""

from datetime import date, datetime, timedelta

from sqlalchemy import insert, text

from app.db.session import engine
from app.db.tables import (
    calibration_logs,
    categories,
    members,
    metadata,
    parts,
    repair_tickets,
    ticket_parts_used,
    tool_loans,
    tools,
    volunteer_specialties,
    volunteers,
)

TODAY = date.today()
NOW = datetime.now()


def truncate_all(conn):
    # Reverse dependency order so FKs don't block deletion.
    table_names = [
        "ticket_parts_used",
        "repair_tickets",
        "tool_loans",
        "calibration_logs",
        "volunteer_specialties",
        "tools",
        "parts",
        "volunteers",
        "members",
        "categories",
    ]
    for name in table_names:
        conn.execute(metadata.tables[name].delete())


def seed():
    with engine.begin() as conn:  # single transaction: commits at the end, rolls back on error
        truncate_all(conn)

        # --- categories ---
        conn.execute(
            insert(categories),
            [
                {"category_id": 1, "name": "Electronics", "carbon_multiplier": 12.500},
                {"category_id": 2, "name": "Textiles", "carbon_multiplier": 3.200},
                {"category_id": 3, "name": "Furniture", "carbon_multiplier": 8.000},
                {"category_id": 4, "name": "Small Appliances", "carbon_multiplier": 15.750},
            ],
        )
        _reset_seq(conn, "categories", "category_id")

        # --- members ---
        conn.execute(
            insert(members),
            [
                {"member_id": 1, "full_name": "Asha Patel", "email": "asha@example.com",
                 "phone": "555-0101", "joined_date": TODAY - timedelta(days=400)},
                {"member_id": 2, "full_name": "Ravi Shah", "email": "ravi@example.com",
                 "phone": "555-0102", "joined_date": TODAY - timedelta(days=200)},
                {"member_id": 3, "full_name": "Meera Joshi", "email": "meera@example.com",
                 "phone": None, "joined_date": TODAY - timedelta(days=90)},
            ],
        )
        _reset_seq(conn, "members", "member_id")

        # --- volunteers ---
        conn.execute(
            insert(volunteers),
            [
                {"volunteer_id": 1, "full_name": "Dev Kumar", "email": "dev@example.com",
                 "is_active": True, "on_shift": True},
                {"volunteer_id": 2, "full_name": "Priya Nair", "email": "priya@example.com",
                 "is_active": True, "on_shift": False},
                {"volunteer_id": 3, "full_name": "Sam Wilson", "email": "sam@example.com",
                 "is_active": True, "on_shift": True},
            ],
        )
        _reset_seq(conn, "volunteers", "volunteer_id")

        # --- volunteer_specialties ---
        conn.execute(
            insert(volunteer_specialties),
            [
                {"volunteer_id": 1, "category_id": 1},  # Dev: Electronics, on_shift -> should show up in Q5
                {"volunteer_id": 2, "category_id": 1},  # Priya: Electronics, NOT on_shift -> excluded from Q5
                {"volunteer_id": 3, "category_id": 2},  # Sam: Textiles
            ],
        )

        # --- tools ---
        conn.execute(
            insert(tools),
            [
                {"tool_id": 1, "name": "Soldering Iron", "category_id": 1, "status": "checked_out",
                 "shelf_location": "A1", "calibration_interval_days": 90},
                {"tool_id": 2, "name": "Sewing Machine", "category_id": 2, "status": "available",
                 "shelf_location": "B2", "calibration_interval_days": 180},
                {"tool_id": 3, "name": "Multimeter", "category_id": 1, "status": "available",
                 "shelf_location": "A2", "calibration_interval_days": 60},
            ],
        )
        _reset_seq(conn, "tools", "tool_id")

        # --- calibration_logs (tool 3 overdue: last check 100 days ago, interval 60) ---
        conn.execute(
            insert(calibration_logs),
            [
                {"log_id": 1, "tool_id": 1, "technician_id": 1,
                 "check_date": TODAY - timedelta(days=10), "result": "pass", "notes": "OK"},
                {"log_id": 2, "tool_id": 3, "technician_id": 1,
                 "check_date": TODAY - timedelta(days=100), "result": "pass", "notes": "Needs recheck"},
            ],
        )
        _reset_seq(conn, "calibration_logs", "log_id")

        # --- tool_loans (tool 1 overdue and unreturned; a past late-but-returned loan for member 2) ---
        conn.execute(
            insert(tool_loans),
            [
                {"loan_id": 1, "tool_id": 1, "member_id": 1,
                 "checkout_date": TODAY - timedelta(days=20),
                 "due_date": TODAY - timedelta(days=6), "return_date": None},  # currently overdue
                {"loan_id": 2, "tool_id": 2, "member_id": 2,
                 "checkout_date": TODAY - timedelta(days=60),
                 "due_date": TODAY - timedelta(days=50),
                 "return_date": TODAY - timedelta(days=45)},  # returned late
            ],
        )
        _reset_seq(conn, "tool_loans", "loan_id")

        # --- parts (one below threshold) ---
        conn.execute(
            insert(parts),
            [
                {"part_id": 1, "name": "Capacitor 220uF", "drawer_location": "D1",
                 "stock_qty": 2, "min_threshold": 10},   # low stock
                {"part_id": 2, "name": "Zipper 20cm", "drawer_location": "D2",
                 "stock_qty": 50, "min_threshold": 5},
            ],
        )
        _reset_seq(conn, "parts", "part_id")

        # --- repair_tickets ---
        conn.execute(
            insert(repair_tickets),
            [
                {"ticket_id": 1, "member_id": 3, "category_id": 1, "assigned_volunteer_id": 1,
                 "item_name": "Toaster", "weight_kg": 1.200, "status": "in_progress",
                 "symptom_notes": "Won't heat", "created_at": NOW - timedelta(days=5),
                 "completed_at": None},
                {"ticket_id": 2, "member_id": 3, "category_id": 2, "assigned_volunteer_id": 3,
                 "item_name": "Jacket", "weight_kg": 0.800, "status": "completed",
                 "symptom_notes": "Torn seam", "created_at": NOW - timedelta(days=10),
                 "completed_at": NOW - timedelta(days=7)},
                {"ticket_id": 3, "member_id": 1, "category_id": 1, "assigned_volunteer_id": None,
                 "item_name": "Lamp", "weight_kg": 0.500, "status": "intake",
                 "symptom_notes": "Flickers", "created_at": NOW - timedelta(days=1),
                 "completed_at": None},
            ],
        )
        _reset_seq(conn, "repair_tickets", "ticket_id")

        # --- ticket_parts_used ---
        conn.execute(
            insert(ticket_parts_used),
            [
                {"ticket_id": 2, "part_id": 2, "qty_used": 3, "used_at": NOW - timedelta(days=8)},
                {"ticket_id": 1, "part_id": 1, "qty_used": 1, "used_at": NOW - timedelta(days=4)},
            ],
        )

    print("Seed complete.")


def _reset_seq(conn, table_name: str, pk_column: str):
    """
    We inserted explicit primary keys above, which leaves each table's SERIAL
    sequence unaware of the max id already used. Bump it so the next
    auto-generated insert (e.g. via the API) doesn't collide with seed data.
    """
    conn.execute(
        text(
            f"SELECT setval(pg_get_serial_sequence('{table_name}', '{pk_column}'), "
            f"COALESCE((SELECT MAX({pk_column}) FROM {table_name}), 1))"
        )
    )


if __name__ == "__main__":
    seed()
