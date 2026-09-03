from collections.abc import Generator

from sqlalchemy import Connection, create_engine

from app.config import settings

# One engine for the whole app process. pool_pre_ping avoids stale-connection
# errors if Postgres restarts or the connection times out while idle.
engine = create_engine(settings.database_url, pool_pre_ping=True, echo=settings.debug)


def get_conn() -> Generator[Connection, None, None]:
    """
    FastAPI dependency that yields a single DB connection wrapped in a
    transaction for the lifetime of the request. Commits on success,
    rolls back on any exception. Repositories receive this `conn` and
    just run `conn.execute(...)` — no commit/rollback logic in repos.

    Usage in a router:
        def list_tools(conn: Connection = Depends(get_conn)):
            return tool_repo.list_all(conn)
    """
    with engine.connect() as conn:
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
