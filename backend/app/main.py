from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api_routers
# from app.init_db import init_db , clode_db
from app.api.exception import APIException , api_exception_handler


app = FastAPI()
app.add_exception_handler(APIException, api_exception_handler) # Thêm custom để Raise status

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(api_routers, prefix="/api")


# NOT USE | USE CREATE WITH SQL SCRIPT/ALEMBIC
# @app.on_event("startup")
# async def prev_db():
#     await init_db()

# @app.on_event("shutdown")
# async def end_db():
#     await clode_db()