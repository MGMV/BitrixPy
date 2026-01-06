from fastapi import FastAPI

from src.router.bitrix import router as bitrix_router

app = FastAPI(title="BitrixPy API")


app.include_router(bitrix_router)


@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"status": "ok"}
