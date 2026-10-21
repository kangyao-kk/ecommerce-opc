from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def read_root():
    return {"Status": "Running...."}

from ecommerce_opc.api.sessions import router as sessions_router

app.include_router(sessions_router)