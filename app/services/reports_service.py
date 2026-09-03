from sqlalchemy import Connection

from app.repositories import reports_repo


def overdue_tool_loans(conn: Connection):
    return reports_repo.overdue_tool_loans(conn)


def low_stock_parts(conn: Connection):
    return reports_repo.low_stock_parts(conn)


def volunteer_workload(conn: Connection):
    return reports_repo.volunteer_workload(conn)


def total_carbon_offset(conn: Connection):
    total = reports_repo.total_carbon_offset(conn)
    return {"total_carbon_offset_kg": float(total) if total is not None else 0.0}


def volunteers_by_specialty(conn: Connection, category_name: str):
    return reports_repo.volunteers_by_specialty(conn, category_name)


def tools_overdue_for_calibration(conn: Connection):
    return reports_repo.tools_overdue_for_calibration(conn)


def most_consumed_part(conn: Connection):
    return reports_repo.most_consumed_part(conn)


def member_repair_history(conn: Connection, member_id: int):
    return reports_repo.member_repair_history(conn, member_id)


def avg_turnaround_by_category(conn: Connection):
    return reports_repo.avg_turnaround_by_category(conn)


def members_with_late_returns(conn: Connection):
    return reports_repo.members_with_late_returns(conn)
