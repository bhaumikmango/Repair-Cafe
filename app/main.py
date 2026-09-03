from fastapi import FastAPI

from app.routers import members, reports, tools

app = FastAPI(title="Repair Cafe Backend", version="0.1.0")

app.include_router(tools.router)
app.include_router(members.router)
app.include_router(reports.router)


@app.get("/health")
def health():
    return {"status": "ok"}
