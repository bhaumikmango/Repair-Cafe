"""
Cross-table analytical queries — direct ports of practice.sql.

These use raw `text()` SQL rather than Core `select()` expressions because
the queries are complex enough (window-style aggregation, multi-join) that
hand-written SQL is clearer than building it up via the query builder.
This is a deliberate style choice, not a limitation — mix and match as you
like between tool_repo.py's Core style and this file's raw-SQL style.

Bugs fixed vs the original practice.sql:
  - Q5: '=' comparison used double quotes (Postgres identifier syntax) around
    'Electronics' instead of single quotes. Fixed, and category is now a
    bind parameter instead of a hardcoded literal.
  - Q3: WHERE rt.status IN (...) after a LEFT JOIN silently drops volunteers
    with zero tickets (turns it back into an inner join). Moved the status
    filter into the ON clause so idle volunteers still show up with 0.
"""

from sqlalchemy import Connection, text


def overdue_tool_loans(conn: Connection) -> list[dict]:
    """Q1: tools currently checked out and past due_date."""
    result = conn.execute(
        text("""
            SELECT tools.name AS tool_name,
                   members.full_name AS borrower_name,
                   (CURRENT_DATE - tool_loans.due_date) AS days_overdue
            FROM tools
            JOIN tool_loans ON tools.tool_id = tool_loans.tool_id
            JOIN members ON tool_loans.member_id = members.member_id
            WHERE tool_loans.return_date IS NULL
              AND tool_loans.due_date < CURRENT_DATE
        """)
    )
    return [row._mapping for row in result]


def low_stock_parts(conn: Connection) -> list[dict]:
    """Q2: parts below their minimum threshold."""
    result = conn.execute(text("SELECT * FROM parts WHERE stock_qty < min_threshold"))
    return [row._mapping for row in result]


def volunteer_workload(conn: Connection) -> list[dict]:
    """Q3: open ticket count per volunteer, including volunteers with zero."""
    result = conn.execute(
        text("""
            SELECT volunteers.volunteer_id,
                   volunteers.full_name,
                   COUNT(rt.ticket_id) AS open_tickets
            FROM volunteers
            LEFT JOIN repair_tickets AS rt
                ON rt.assigned_volunteer_id = volunteers.volunteer_id
                AND rt.status IN ('intake', 'diagnosing', 'in_progress', 'awaiting_parts')
            GROUP BY volunteers.volunteer_id, volunteers.full_name
            ORDER BY open_tickets DESC
        """)
    )
    return [row._mapping for row in result]


def total_carbon_offset(conn: Connection) -> float | None:
    """Q4: total kg CO2 offset from completed tickets."""
    result = conn.execute(
        text("""
            SELECT SUM(rt.weight_kg * categories.carbon_multiplier) AS total_carbon_offset
            FROM repair_tickets AS rt
            JOIN categories ON rt.category_id = categories.category_id
            WHERE rt.status = 'completed'
        """)
    )
    return result.scalar()


def volunteers_by_specialty(conn: Connection, category_name: str) -> list[dict]:
    """Q5: on-shift volunteers who specialize in the given category."""
    result = conn.execute(
        text("""
            SELECT volunteers.volunteer_id, volunteers.full_name, categories.name
            FROM volunteers
            JOIN volunteer_specialties AS vs ON volunteers.volunteer_id = vs.volunteer_id
            JOIN categories ON categories.category_id = vs.category_id
            WHERE volunteers.on_shift = TRUE AND categories.name = :category_name
        """),
        {"category_name": category_name},
    )
    return [row._mapping for row in result]


def tools_overdue_for_calibration(conn: Connection) -> list[dict]:
    """Q6: tools whose last calibration check exceeds their interval."""
    result = conn.execute(
        text("""
            SELECT tools.tool_id,
                   tools.name,
                   (CURRENT_DATE - latest.last_check) AS days_since_check
            FROM tools
            JOIN (
                SELECT tool_id, MAX(check_date) AS last_check
                FROM calibration_logs
                GROUP BY tool_id
            ) AS latest ON tools.tool_id = latest.tool_id
            WHERE (CURRENT_DATE - latest.last_check) > tools.calibration_interval_days
        """)
    )
    return [row._mapping for row in result]


def most_consumed_part(conn: Connection) -> dict | None:
    """Q7: single part with the highest total qty_used."""
    result = conn.execute(
        text("""
            SELECT part_id, SUM(qty_used) AS total_used
            FROM ticket_parts_used
            GROUP BY part_id
            ORDER BY total_used DESC
            LIMIT 1
        """)
    )
    row = result.first()
    return row._mapping if row else None


def member_repair_history(conn: Connection, member_id: int) -> list[dict]:
    """Q8: every repair ticket a given member has submitted."""
    result = conn.execute(
        text("""
            SELECT rt.ticket_id, rt.item_name, rt.status, volunteers.full_name AS assigned_to
            FROM repair_tickets AS rt
            JOIN members ON rt.member_id = members.member_id
            LEFT JOIN volunteers ON rt.assigned_volunteer_id = volunteers.volunteer_id
            WHERE members.member_id = :member_id
            ORDER BY rt.ticket_id
        """),
        {"member_id": member_id},
    )
    return [row._mapping for row in result]


def avg_turnaround_by_category(conn: Connection) -> list[dict]:
    """Q9: average completion time (days) for completed tickets, by category."""
    result = conn.execute(
        text("""
            SELECT categories.name,
                   AVG(rt.completed_at - rt.created_at) AS avg_turnaround
            FROM repair_tickets AS rt
            JOIN categories ON rt.category_id = categories.category_id
            WHERE rt.status = 'completed'
            GROUP BY categories.category_id, categories.name
        """)
    )
    return [row._mapping for row in result]


def members_with_late_returns(conn: Connection) -> list[dict]:
    """Q10: members with at least one returned-but-late loan."""
    result = conn.execute(
        text("""
            SELECT DISTINCT members.member_id, members.full_name
            FROM members
            JOIN tool_loans ON members.member_id = tool_loans.member_id
            WHERE tool_loans.return_date IS NOT NULL
              AND tool_loans.due_date < tool_loans.return_date
        """)
    )
    return [row._mapping for row in result]
