from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import router as pdf_router
from contextlib import asynccontextmanager
from services.db import close_database, connect_database
from services.message_store import create_message_indexes
from services.conversation_store import create_conversation_indexes
from routers.conversation_router import router as conversation_router
from config import FRONTEND_DIR


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await connect_database()
        await create_conversation_indexes()
        await create_message_indexes()
        yield
    finally:
        await close_database()


app = FastAPI(
    title="DocRAG Agent PDF 文献阅读助手",
    lifespan=lifespan,
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(pdf_router)
app.include_router(conversation_router)

@app.get("/health")
def health_check() -> dict:
    return {"提示": "DocRAG 后端服务正在运行"}


app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend",
)