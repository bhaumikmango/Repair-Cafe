from fastapi import APIRouter, Depends, Query
from sqlalchemy import Connection

from app.db.session import get_conn
from app.services import reports_service

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/overdue-tool-loans")
def overdue_tool_loans(conn: Connection = Depends(get_conn)):
    return reports_service.overdue_tool_loans(conn)


@router.get("/low-stock-parts")
def low_stock_parts(conn: Connection = Depends(get_conn)):
    return reports_service.low_stock_parts(conn)


@router.get("/volunteer-workload")
def volunteer_workload(conn: Connection = Depends(get_conn)):
    return reports_service.volunteer_workload(conn)


@router.get("/total-carbon-offset")
def total_carbon_offset(conn: Connection = Depends(get_conn)):
    return reports_service.total_carbon_offset(conn)


@router.get("/volunteers-by-specialty")
def volunteers_by_specialty(
    category_name: str = Query(..., description="e.g. 'Electronics'"),
    conn: Connection = Depends(get_conn),
):
    return reports_service.volunteers_by_specialty(conn, category_name)


@router.get("/tools-overdue-for-calibration")
def tools_overdue_for_calibration(conn: Connection = Depends(get_conn)):
    return reports_service.tools_overdue_for_calibration(conn)


@router.get("/most-consumed-part")
def most_consumed_part(conn: Connection = Depends(get_conn)):
    return reports_service.most_consumed_part(conn)


@router.get("/members/{member_id}/repair-history")
def member_repair_history(member_id: int, conn: Connection = Depends(get_conn)):
    return reports_service.member_repair_history(conn, member_id)


@router.get("/avg-turnaround-by-category")
def avg_turnaround_by_category(conn: Connection = Depends(get_conn)):
    return reports_service.avg_turnaround_by_category(conn)


@router.get("/members-with-late-returns")
def members_with_late_returns(conn: Connection = Depends(get_conn)):
    return reports_service.members_with_late_returns(conn)
