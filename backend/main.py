from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from app.database import connect_db, close_db, db
from app.routes import auth_routes, meals_routes, dashboard_routes, chat_routes, food_routes, cycle_routes, progress_routes, voice_routes
from seed_db import seed_database

load_dotenv()

app = FastAPI(title="SmartNutri Backend", version="1.0.0")

# CORS configuration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.detail.get("code", "UNKNOWN_ERROR") if isinstance(exc.detail, dict) else "HTTP_ERROR",
                "message": exc.detail.get("message", str(exc.detail)) if isinstance(exc.detail, dict) else str(exc.detail),
                "fields": exc.detail.get("fields") if isinstance(exc.detail, dict) else None,
            }
        }
    )

# Routes
app.include_router(auth_routes.router, prefix="/api/auth", tags=["auth"])
app.include_router(meals_routes.router, tags=["meals"])
app.include_router(dashboard_routes.router, tags=["dashboard"])
app.include_router(chat_routes.router, prefix="/api/chat", tags=["chat"])
app.include_router(food_routes.router, tags=["foods"])
app.include_router(cycle_routes.router, tags=["cycle"])
app.include_router(progress_routes.router, tags=["progress"])
app.include_router(voice_routes.router, prefix="/api", tags=["voice"])

@app.get("/health")
async def health():
    return {"status": "ok", "message": "SmartNutri Backend is running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

