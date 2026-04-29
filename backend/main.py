
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
import os
from dotenv import load_dotenv

from app.database import connect_db, close_db, db
from app.routes import auth_routes, meals_routes, dashboard_routes, chat_routes, food_routes, cycle_routes, progress_routes, voice_routes, nutrition_routes, education_routes, parent_routes
from seed_db import seed_database

load_dotenv()

# Create FastAPI app first
app = FastAPI(title="SmartNutri Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Startup and shutdown events
@app.on_event("startup")
async def startup():
    await connect_db()
    print("[OK] Connected to MongoDB")
    
    # Auto-seed database if empty (mongomock only)
    try:
        from app.database import USE_MONGOMOCK, db as current_db
        print(f"DEBUG: USE_MONGOMOCK={USE_MONGOMOCK}, db type={type(current_db)}, has _db={hasattr(current_db, '_db')}")
        
        if USE_MONGOMOCK and hasattr(current_db, '_db'):
            # For mongomock with wrapper
            underlying_db = current_db._db
            user_count = underlying_db.users.count_documents({})
            print(f"DEBUG: User count in database: {user_count}")
            
            if user_count == 0:
                print("[INFO] Database is empty. Auto-seeding...")
                seed_database(underlying_db)
            else:
                print(f"[OK] Database already has {user_count} users")
    except Exception as e:
        import traceback
        print(f"Note: Could not auto-seed database: {e}")
        traceback.print_exc()

@app.on_event("shutdown")
async def shutdown():
    await close_db()
    print("[OK] Disconnected from MongoDB")

# Global error handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    origin = request.headers.get("Origin", "http://localhost:5173")
    
    # Validate origin is in allowed list
    allowed = ["http://localhost:5173", "http://localhost:5174"]
    if origin not in allowed:
        origin = "http://localhost:5173"
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.detail.get("code", "UNKNOWN_ERROR") if isinstance(exc.detail, dict) else "HTTP_ERROR",
                "message": exc.detail.get("message", str(exc.detail)) if isinstance(exc.detail, dict) else str(exc.detail),
                "fields": exc.detail.get("fields") if isinstance(exc.detail, dict) else None,
            }
        },
        headers={
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Credentials": "true",
        }
    )

# General exception handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    import traceback
    origin = request.headers.get("Origin", "http://localhost:5173")
    allowed = ["http://localhost:5173", "http://localhost:5174"]
    if origin not in allowed:
        origin = "http://localhost:5173"
    
    print(f"Unhandled exception: {exc}")
    traceback.print_exc()
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(exc),
            }
        },
        headers={
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Credentials": "true",
        }
    )

# Routes
app.include_router(auth_routes.router, prefix="/api/auth", tags=["auth"])
app.include_router(meals_routes.router, prefix="/api", tags=["meals"])
app.include_router(dashboard_routes.router, prefix="/api", tags=["dashboard"])
app.include_router(chat_routes.router, prefix="/api/chat", tags=["chat"])
app.include_router(food_routes.router, prefix="/api", tags=["foods"])
app.include_router(cycle_routes.router, prefix="/api/cycle", tags=["cycle"])
app.include_router(progress_routes.router, prefix="/api/progress", tags=["progress"])
app.include_router(voice_routes.router, prefix="/api/voice", tags=["voice"])
app.include_router(nutrition_routes.router, prefix="/api", tags=["nutrition"])
app.include_router(education_routes.router, prefix="/api", tags=["education"])
app.include_router(parent_routes.router, prefix="/api", tags=["parent"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "SmartNutri backend is running"}

@app.get("/health")
async def health():
    return {"status": "ok", "message": "SmartNutri Backend is running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

