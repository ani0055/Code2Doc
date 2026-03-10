from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import user, project, documentation
from app.api import auth, code_analysis, history 
from app.api import auth, code_analysis, history, export
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Code2Doc API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(code_analysis.router, prefix="/api")
app.include_router(history.router, prefix="/api") 
app.include_router(export.router, prefix="/api") 

@app.get("/")
def root():
    return {"message": "Welcome to Code2Doc API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}