"""
Dashboard and home page routes
Endpoints for fetching dashboard data, user stats, etc.
"""
from fastapi import APIRouter, Request
from datetime import datetime, timedelta
from bson import ObjectId
from app.database import get_db
from app.routes.auth_routes import get_current_user
from app.json_encoder import to_json_serializable

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard(request: Request):
    """Get complete dashboard data for home page"""
    user = get_current_user(request)
    db = get_db()
    user_id = user["userId"]
    
    # Get user profile
    profile = await db.profiles.find_one({"user_id": user_id})
    
    # Get user document
    try:
        user_oid = ObjectId(user_id) if len(user_id) == 24 else user_id
        user_doc = await db.users.find_one({"_id": user_oid})
    except:
        user_doc = await db.users.find_one({"email": user.get("email", "")})
    
    # Get nutrition targets
    targets = await db.nutrition_targets.find_one({"user_id": user_id})
    
    # Get today's meals
    today = datetime.utcnow().strftime("%Y-%m-%d")
    today_meals = await db.meal_logs.find({"user_id": user_id, "date": today}).to_list(None)
    
    # Calculate today's nutrition
    total_calories = sum(m.get("total_calories", 0) for m in today_meals)
    total_protein = sum(m.get("total_protein_g", 0) for m in today_meals)
    total_carbs = sum(m.get("total_carbs_g", 0) for m in today_meals)
    total_fats = sum(m.get("total_fats_g", 0) for m in today_meals)
    
    # Get progress data for streak calculation
    progress_logs = await db.progress_logs.find({"user_id": user_id}).sort("date", -1).limit(30).to_list(None)
    
    # Calculate streak
    streak = 0
    current_date = datetime.utcnow().date()
    for _ in range(30):
        check_date = (current_date - timedelta(days=streak)).strftime("%Y-%m-%d")
        if any(p.get("date") == check_date for p in progress_logs):
            streak += 1
        else:
            break
    
    # Get achievements
    achievements = await db.achievements.find({"user_id": user_id}).to_list(None)
    badges = [
        {
            "id": a.get("badge_id"),
            "emoji": a.get("icon"),  # Icon maps to emoji in frontend
            "label": a.get("name"),   # Name maps to label in frontend
            "description": a.get("description"),
            "earned": a.get("unlocked", False),  # unlocked maps to earned
            "earned_at": to_json_serializable(a.get("earned_at")),
        }
        for a in achievements if a.get("unlocked", False)  # Only show unlocked badges
    ]
    
    # Get cycle summary if applicable
    cycle_summary = None
    if profile and profile.get("segment") in ["teen-girl-h", "teen-girl-a"]:
        if profile and profile.get("cycle_data"):
            from app.routes.cycle_routes import calculate_cycle_phase
            phase_info = calculate_cycle_phase(
                profile["cycle_data"].get("lastPeriodDate", "2024-01-01"),
                profile["cycle_data"].get("cycleLength", 28)
            )
            cycle_summary = {
                "phase": phase_info["phase"],
                "label": phase_info["label"],
                "emoji": phase_info["emoji"]
            }
        else:
            cycle_summary = { "phase": "not_started", "label": "Not Started", "emoji": "⚪" }
    
    # AI Nudge (placeholder)
    ai_nudge = {
        "text": f"You're doing great! Keep your protein intake consistent at {(targets or {}).get('protein_g', 110)}g daily.",
        "chips": ["💪 Protein", "🎯 Consistency"],
    }
    
    # Greeting based on time
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good Morning"
    elif hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
    
    return {
        "success": True,
        "data": {
            "user": {
                "name": user_doc.get("name") if user_doc else "User",
                "segment": profile.get("segment") if profile else "adult",
                "streak": streak,
            },
            "greeting": greeting,
            "date": datetime.now().strftime("%a %d %b"),
            "nutrition": {
                "calories": {
                    "current": total_calories,
                    "goal": (targets or {}).get("calories", 2000),
                },
                "protein": {
                    "current": total_protein,
                    "goal": (targets or {}).get("protein_g", 110),
                },
                "carbs": {
                    "current": total_carbs,
                    "goal": (targets or {}).get("carbs_g", 250),
                },
                "water": {
                    "current": 1.5,  # Would calculate from logs
                    "goal": 2.5,
                },
            },
            "cycleSummary": cycle_summary,
            "aiNudge": ai_nudge,
            "badges": badges,
        }
    }

@router.get("/progress/summary")
async def get_progress_summary(request: Request, days: int = 7):
    """Get progress summary for the last N days"""
    user = get_current_user(request)
    db = get_db()
    user_id = user["userId"]
    
    # Get progress logs for the selected period
    start_date = (datetime.utcnow() - timedelta(days=days))
    cursor = db.progress_logs.find({"user_id": user_id, "created_at": {"$gte": start_date}})
    progress_logs = await cursor.to_list(None)
    
    # Group by date and calculate trends
    daily_data = {}
    for log in progress_logs:
        date = log.get("date")
        if date not in daily_data:
            # Remove _id field for JSON serialization
            log_clean = {k: v for k, v in log.items() if k != "_id"}
            daily_data[date] = log_clean
    
    sorted_data = sorted(daily_data.values(), key=lambda x: x.get("date", ""))
    
    return {
        "success": True,
        "data": {
            "period_days": days,
            "total_logs": len(progress_logs),
            "daily_data": sorted_data,
            "average_weight": sum(d.get("weight_kg", 0) for d in sorted_data) / len(sorted_data) if sorted_data else 0,
            "average_exercises": sum(d.get("exercise_minutes", 0) for d in sorted_data) / len(sorted_data) if sorted_data else 0,
        }
    }
