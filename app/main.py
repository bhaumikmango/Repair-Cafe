from fastapi import FastAPI

from app.routers import reports, tools

app = FastAPI(title="Repair Cafe Backend", version="0.1.0")

app.include_router(tools.router)
app.include_router(reports.router)
# As you build out members/volunteers/parts/repair_tickets, add them here:
# app.include_router(members.router)
# app.include_router(volunteers.router)
# app.include_router(parts.router)
# app.include_router(repair_tickets.router)


@app.get("/health")
def health():
    return {"status": "ok"}
