from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import auth
from app.database import engine, Base
from app.face_recognition import init_model
import os

# Create uploads directory
os.makedirs("uploads", exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 Starting Face Recognition Server...")

    # Initialize database
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized")

    # Pre-load face recognition model
    init_model()

    print("✓ Server ready!")

    yield

    # Shutdown
    print("🛑 Shutting down...")


app = FastAPI(
    title="Face Recognition Auth API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Face Recognition Auth API", "status": "running"}
