"""
Progress tracking and analytics endpoints
Endpoints for tracking weight, achievements, streaks, and progress analytics
"""
from fastapi import APIRouter, HTTPException, Request, Query
from datetime import datetime, timedelta
from typing import Optional
from bson import ObjectId

from app.models import ProgressLogRequest
from app.database import get_db
from app.routes.auth_routes import get_current_user

router = APIRouter()

@router.post("/api/progress/log")
async def log_progress(req: ProgressLogRequest, request: Request):
    """Log daily progress (weight, mood, exercise, water, etc.)"""
    try:
        user = get_current_user(request)
        db = get_db()
        user_id = user.get("userId") or user.get("sub")
        
        # Get today's date
        today = datetime.utcnow().strftime("%Y-%m-%d")
        
        # Check if already logged today
        existing = await db.progress_logs.find_one({
            "user_id": user_id,
            "date": today
        })
        
        progress_log = {
            "user_id": user_id,
            "date": today,
            "weight_kg": req.weight,
            "mood": req.mood or "neutral",
            "energy_level": req.energy_level or 5,
            "water_glasses": req.water_glasses or 0,
            "exercise_minutes": req.exercise_minutes or 0,
            "notes": req.notes or "",
            "created_at": datetime.utcnow(),
        }
        
        if existing:
            # Update existing entry
            result = await db.progress_logs.update_one(
                {"_id": existing["_id"]},
                {"$set": progress_log}
            )
            return {
                "success": True,
                "data": {"message": "Progress updated"}
            }
        else:
            # Create new entry
            result = await db.progress_logs.insert_one(progress_log)
            
            # Check for streak achievement
            await check_and_award_streak(db, user_id)
            
            return {
                "success": True,
                "data": {
                    "id": str(result.inserted_id),
                    "message": "Progress logged"
                }
            }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": "PROGRESS_ERROR", "message": str(e)}
        )

@router.get("/api/progress/summary")
async def get_progress_summary(request: Request, days: int = 7):
    """Get progress data for the specified period"""
    try:
        user = get_current_user(request)
        db = get_db()
        user_id = user.get("userId") or user.get("sub")
        
        # Get start date
        start_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        # Fetch progress logs
        logs = []
        cursor = db.progress_logs.find({
            "user_id": user_id,
            "date": {"$gte": start_date}
        }).sort("date", 1)
        logs_list = await cursor.to_list(None)
        for log in logs_list:
            logs.append({
                "date": log.get("date"),
                "weight": log.get("weight_kg"),
                "mood": log.get("mood"),
                "energy": log.get("energy_level"),
                "water": log.get("water_glasses"),
                "exercise": log.get("exercise_minutes"),
            })
        
        # Calculate statistics
        if logs:
            weights = [l["weight"] for l in logs if l["weight"]]
            weight_change = round(weights[-1] - weights[0], 2) if len(weights) > 1 else 0
            avg_weight = round(sum(weights) / len(weights), 2) if weights else 0
            
            exercise_total = sum(l["exercise"] or 0 for l in logs)
            water_total = sum(l["water"] or 0 for l in logs)
            
            # Mood distribution
            mood_counts = {}
            for log in logs:
                mood = log.get("mood", "neutral")
                mood_counts[mood] = mood_counts.get(mood, 0) + 1
            
            most_common_mood = max(mood_counts, key=mood_counts.get) if mood_counts else "neutral"
            
            return {
                "success": True,
                "data": {
                    "period": f"{days} days",
                    "logs": logs,
                    "stats": {
                        "currentWeight": weights[-1] if weights else None,
                        "avgWeight": avg_weight,
                        "weightChange": weight_change,
                        "exerciseMinutes": exercise_total,
                        "waterGlasses": water_total,
                        "mostCommonMood": most_common_mood,
                        "mood Distribution": mood_counts,
                    }
                }
            }
        
        return {
            "success": True,
            "data": {
                "period": f"{days} days",
                "logs": [],
                "stats": {
                    "message": "No progress data yet. Start logging!",
                    "exerciseMinutes": 0,
                    "waterGlasses": 0,
                }
            }
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": "SUMMARY_ERROR", "message": str(e)}
        )

@router.get("/api/progress/streak")
async def get_streak(request: Request):
    """Get current logging streak"""
    try:
        user = get_current_user(request)
        db = get_db()
        user_id = user.get("userId") or user.get("sub")
        
        # Get all progress logs sorted by date descending
        logs = []
        cursor = db.progress_logs.find({"user_id": user_id}).sort("date", -1)
        logs_list = await cursor.to_list(None)
        logs = logs_list
        
        if not logs:
            return {
                "success": True,
                "data": {
                    "currentStreak": 0,
                    "bestStreak": 0,
                    "daysLogged": 0,
                    "message": "Start logging to build a streak!"
                }
            }
        
        # Calculate current streak
        current_streak = 0
        today = datetime.utcnow().strftime("%Y-%m-%d")
        yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Check if logged today or yesterday
        first_log_date = logs[0]["date"] if logs else None
        
        if first_log_date == today or first_log_date == yesterday:
            current_streak = 1
            
            # Count back from yesterday
            current_date = datetime.strptime(first_log_date, "%Y-%m-%d") - timedelta(days=1)
            
            for log in logs[1:]:
                log_date = datetime.strptime(log["date"], "%Y-%m-%d")
                if log_date.date() == current_date.date():
                    current_streak += 1
                    current_date -= timedelta(days=1)
                else:
                    break
        
        # Find best streak (scan all logs)
        best_streak = 0
        temp_streak = 1
        
        for i in range(len(logs) - 1):
            current_log_date = datetime.strptime(logs[i]["date"], "%Y-%m-%d")
            next_log_date = datetime.strptime(logs[i + 1]["date"], "%Y-%m-%d")
            
            if (current_log_date - next_log_date).days == 1:
                temp_streak += 1
            else:
                best_streak = max(best_streak, temp_streak)
                temp_streak = 1
        
        best_streak = max(best_streak, temp_streak)
        
        return {
            "success": True,
            "data": {
                "currentStreak": current_streak,
                "bestStreak": best_streak,
                "daysLogged": len(logs),
                "emoji": get_streak_emoji(current_streak)
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": "STREAK_ERROR", "message": str(e)}
        )

@router.get("/api/progress/goals")
async def check_goals(request: Request):
    """Check progress towards nutrition and fitness goals"""
    try:
        user = get_current_user(request)
        db = get_db()
        user_id = user.get("userId") or user.get("sub")
        
        today = datetime.utcnow().strftime("%Y-%m-%d")
        
        # Get today's meals
        meals = []
        cursor = db.meal_logs.find({
            "user_id": user_id,
            "date": today
        })
        meals_list = await cursor.to_list(None)
        meals = meals_list
        
        # Get today's progress log
        progress = await db.progress_logs.find_one({
            "user_id": user_id,
            "date": today
        })
        
        # Get nutrition targets
        targets = await db.nutrition_targets.find_one({"user_id": user_id})
        
        # Calculate totals
        total_calories = sum(m.get("total_calories", 0) for m in meals)
        total_protein = sum(m.get("total_protein_g", 0) for m in meals)
        total_water = progress.get("water_glasses", 0) if progress else 0
        exercise = progress.get("exercise_minutes", 0) if progress else 0
        
        # Set targets
        calorie_target = targets.get("calories", 2000) if targets else 2000
        protein_target = targets.get("protein_g", 110) if targets else 110
        water_target = 8
        exercise_target = 30
        
        # Calculate progress percentages
        goals = {
            "calories": {
                "current": total_calories,
                "goal": calorie_target,
                "percent": round((total_calories / calorie_target * 100) if calorie_target else 0),
                "icon": "🔥"
            },
            "protein": {
                "current": round(total_protein, 1),
                "goal": protein_target,
                "percent": round((total_protein / protein_target * 100) if protein_target else 0),
                "icon": "💪"
            },
            "water": {
                "current": total_water,
                "goal": water_target,
                "percent": round((total_water / water_target * 100) if water_target else 0),
                "icon": "💧"
            },
            "exercise": {
                "current": exercise,
                "goal": exercise_target,
                "percent": round((exercise / exercise_target * 100) if exercise_target else 0),
                "icon": "⚡"
            },
        }
        
        return {
            "success": True,
            "data": goals
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": "GOALS_ERROR", "message": str(e)}
        )

@router.get("/api/progress/achievements")
async def get_achievements(request: Request):
    """Get user achievements and badges"""
    try:
        user = get_current_user(request)
        db = get_db()
        user_id = user.get("userId") or user.get("sub")
        
        # Get achievements
        achievements = []
        cursor = db.achievements.find({"user_id": user_id})
        achs_list = await cursor.to_list(None)
        for ach in achs_list:
            achievements.append({
                "id": str(ach.get("_id")),
                "name": ach.get("name"),
                "description": ach.get("description"),
                "icon": ach.get("icon"),
                "unlocked": ach.get("unlocked", False),
                "earnedAt": ach.get("earned_at"),
            })
        
        unlocked_count = sum(1 for a in achievements if a["unlocked"])
        
        return {
            "success": True,
            "data": {
                "total": len(achievements),
                "unlocked": unlocked_count,
                "achievements": achievements
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": "ACHIEVEMENTS_ERROR", "message": str(e)}
        )

def get_streak_emoji(days: int) -> str:
    """Get emoji based on streak length"""
    if days == 0:
        return "🌱"
    elif days < 7:
        return "🔥"
    elif days < 30:
        return "🌟"
    elif days < 100:
        return "⭐"
    else:
        return "👑"

async def check_and_award_streak(db, user_id: str):
    """Check if user earned a streak achievement"""
    # Get current streak
    logs = []
    cursor = db.progress_logs.find({"user_id": user_id}).sort("date", -1).limit(8)
    logs_list = await cursor.to_list(None)
    logs = logs_list
    
    current_streak = 0
    if logs:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        if logs[0]["date"] == today or logs[0]["date"] == yesterday:
            current_streak = len(logs)
    
    # Award badges for milestones
    streak_badges = [7, 14, 30, 100]
    
    for badge_days in streak_badges:
        if current_streak == badge_days:
            badge_name = f"{badge_days}-Day Streak"
            
            # Check if already awarded
            existing = await db.achievements.find_one({
                "user_id": user_id,
                "name": badge_name
            })
            
            if not existing:
                # Award badge
                await db.achievements.update_one(
                    {
                        "user_id": user_id,
                        "name": badge_name
                    },
                    {
                        "$set": {
                            "unlocked": True,
                            "earned_at": datetime.utcnow().isoformat()
                        }
                    },
                    upsert=True
                )
