from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import session, onboarding, prompts, entries, garden, threads, insights, memories
from app.db.database import init_db

app = FastAPI(
    title="Journal a Forest API",
    description="AI-powered journaling companion backend",
    version="0.1.0",
)

# CORS middleware for frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    await init_db()

# Include routers
app.include_router(session.router, prefix="/api", tags=["session"])
app.include_router(onboarding.router, prefix="/api", tags=["onboarding"])
app.include_router(prompts.router, prefix="/api/prompts", tags=["prompts"])
app.include_router(entries.router, prefix="/api", tags=["entries"])
app.include_router(garden.router, prefix="/api", tags=["garden"])
app.include_router(threads.router, prefix="/api/threads", tags=["threads"])
app.include_router(insights.router, prefix="/api/insights", tags=["insights"])
app.include_router(memories.router, prefix="/api", tags=["memories"])

@app.get("/")
async def root():
    return {"message": "Journal a Forest API", "version": "0.1.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

